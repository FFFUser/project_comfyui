# -*- coding: utf-8 -*-
"""
Load workflow JSON from ../comfyUI_json, submit to ComfyUI, save output image(s) under ../output/ by default.

Requires: pip install comfy_api_client

Default: does not call GET / before submitting (use --verify-server to enable that probe).

On Windows, use 127.0.0.1 in --host if localhost gives 502 while the browser works on 127.0.0.1.

Comfy Cloud (remote): https://docs.comfy.org/development/cloud/overview
  Set COMFY_CLOUD_API_KEY and run with --cloud (never commit API keys).
  API key mode requires a paid Cloud plan; Free tier only supports the web UI, not API key auth.

Examples:
  python run_workflow.py
  python run_workflow.py --workflow comfy_job_1_replace.json --host 127.0.0.1:8188
  python run_workflow.py --image-41 D:\\photos\\a.jpg --image-83 D:\\photos\\b.png
  python run_workflow.py --verify-server
  python run_workflow.py -v
  set COMFY_CLOUD_API_KEY=... & python run_workflow.py --cloud --image-41 a.jpg --image-83 b.jpg
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import mimetypes
import os
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

import httpx
from comfy_api_client.client import (
    ComfyAPIClient,
    ComfyExecutionError,
    PromptResult,
    create_comfy_state_tracker,
)

log = logging.getLogger(__name__)

# Comfy Cloud API (experimental): https://docs.comfy.org/development/cloud/overview
CLOUD_BASE_URL = "https://cloud.comfy.org"


def _cloud_client_headers(api_key: str) -> dict[str, str]:
    """Match official docs: only X-API-Key (same as curl -H for Comfy Cloud)."""
    return {"X-API-Key": api_key}


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        force=True,
    )
    # Avoid httpx "HTTP Request: ..." at INFO (use -v / DEBUG to see)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _json_dir() -> Path:
    return _repo_root() / "comfyUI_json"


def _default_output_dir() -> Path:
    """Default folder for saved images: manager_system/output/."""
    return _repo_root() / "output"


def load_workflow(name: str) -> dict:
    path = _json_dir() / name
    if not path.is_file():
        raise FileNotFoundError(f"Workflow file not found: {path}")
    log.debug("Reading JSON: %s", path)
    # UTF-8: avoid Windows default (e.g. GBK) used by comfy_api_client.utils.read_json
    text = path.read_text(encoding="utf-8-sig")
    return json.loads(text)


def _load_image_input_value(path_or_name: str) -> str:
    """LoadImage API expects the filename under ComfyUI input/; accept paths and use basename."""
    return Path(path_or_name.strip()).name


def _local_httpx_timeout(total_seconds: float) -> httpx.Timeout:
    """Generous read/write for /upload/image (library re-encodes images) and /prompt."""
    return httpx.Timeout(
        connect=min(60.0, total_seconds),
        read=total_seconds,
        write=total_seconds,
        pool=60.0,
    )


@asynccontextmanager
async def _comfy_client(
    comfy_url: str,
    *,
    skip_health_check: bool,
    http_timeout: float = 300.0,
    start_state_tracker: Literal["websocket", "http"] | None = "websocket",
):
    """Same as comfy_api_client.create_client, optional skip of GET / (used for some proxies)."""
    log.info("Connecting to ComfyUI: %s", comfy_url)
    async with httpx.AsyncClient(timeout=_local_httpx_timeout(http_timeout)) as http_client:
        client = ComfyAPIClient(comfy_url, http_client)
        log.debug("httpx per-request read/write timeout=%ss (connect capped)", http_timeout)
        if not skip_health_check:
            log.info("Probe: GET / (verify-server)")
            await client.get_index()
            log.info("Probe OK: root responded")
        else:
            log.info("Probe: skipped GET / (default)")
        if start_state_tracker is not None:
            log.info("Starting state tracker: %s", start_state_tracker)
            # websockets defaults: ping_interval=20, ping_timeout=20. Sync work on the event loop
            # (e.g. comfy_api_client.upload_image re-encoding to PNG) blocks pings ?? ~20s disconnect.
            ws_kwargs: dict = {}
            if start_state_tracker == "websocket":
                ws_kwargs = {"ping_interval": None, "ping_timeout": None}
            await create_comfy_state_tracker(client, start_state_tracker, **ws_kwargs)
            log.info("State tracker running; ready to submit workflow")
        try:
            yield client
        finally:
            log.info("Closing ComfyUI client (stopping state trackers)")
            for tracker in client.state_trackers:
                await tracker.stop()
            log.info("Client closed")


def _format_comfy_connect_help(host: str, status_code: int | None) -> str:
    base = f"http://{host}" if "://" not in host else host
    return (
        f"HTTP {status_code} from ComfyUI ({base}) during GET /. "
        "502 usually means no healthy upstream (ComfyUI down, wrong port, or bad reverse proxy).\n"
        "Check the URL in a browser. Omit --verify-server to skip this probe (default)."
    )


def _log_http_error_response(e: httpx.HTTPStatusError) -> None:
    try:
        text = e.response.text
    except Exception as err:  # noqa: BLE001
        log.error("Could not read error response body: %s", err)
        return
    max_len = 6000
    if len(text) > max_len:
        text = text[:max_len] + f"... ({len(e.response.text)} chars total)"
    log.error("Server response body:\n%s", text)


_CLOUD_FREE_TIER_API = "API key authentication is not available for free tier"


def _raise_if_cloud_free_tier_error(e: httpx.HTTPStatusError) -> None:
    """Comfy Cloud returns this JSON message when the account is on Free tier."""
    try:
        text = e.response.text
    except Exception:
        return
    if _CLOUD_FREE_TIER_API in text:
        raise RuntimeError(
            "Comfy Cloud: Free tier does not support API key / programmatic API. "
            "Upgrade: https://www.comfy.org/cloud/pricing - or use local ComfyUI (run without --cloud)."
        ) from e


def _cloud_raise_for_status(response: httpx.Response) -> None:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        _raise_if_cloud_free_tier_error(e)
        raise


def _format_prompt_gateway_help(host: str, status_code: int) -> str:
    base = f"http://{host}" if "://" not in host else host
    return (
        f"HTTP {status_code} on POST {base}/prompt - the request did not reach a working ComfyUI backend.\n"
        "This is not a workflow JSON bug. Fix the server side:\n"
        "  - Start ComfyUI and confirm the UI works in a browser at the same host:port as --host.\n"
        "  - If you use nginx / frp / Cloudflare Tunnel, fix upstream so /prompt is proxied to ComfyUI.\n"
        "  - Try connecting directly to ComfyUI's port (no proxy) to verify."
    )


def strip_workflow_meta_for_api(workflow: dict) -> dict:
    """Remove per-node _meta (UI labels). ComfyUI /prompt often rejects or mishandles them."""
    cleaned: dict = {}
    for nid, node in workflow.items():
        if isinstance(node, dict):
            cleaned[nid] = {k: v for k, v in node.items() if k != "_meta"}
        else:
            cleaned[nid] = node
    return cleaned


async def _upload_local_image_multipart(client: ComfyAPIClient, path: Path) -> None:
    """POST /upload/image with raw file bytes (no PIL re-encode), read in a thread for large files."""
    fname = path.name
    mime = mimetypes.guess_type(fname)[0]
    body = await asyncio.to_thread(path.read_bytes)
    file_field: tuple[str, bytes] | tuple[str, bytes, str]
    if mime:
        file_field = (fname, body, mime)
    else:
        file_field = (fname, body)
    response = await client.client.post(
        client.get_endpoint_url("/upload/image"),
        data={"overwrite": True, "type": "input"},
        files={"image": file_field},
    )
    response.raise_for_status()


async def upload_local_input_images_if_needed(
    client: ComfyAPIClient,
    image_41: str | None,
    image_83: str | None,
) -> None:
    """If --image-41 / --image-83 point to existing files, upload via /upload/image (LoadImage needs them in input/)."""
    for label, raw in (("41", image_41), ("83", image_83)):
        if not raw:
            continue
        path = Path(raw.strip())
        if path.is_file():
            log.info("Uploading to ComfyUI input for node %s: %s", label, path.resolve())
            try:
                await _upload_local_image_multipart(client, path)
            except httpx.TimeoutException as e:
                raise RuntimeError(
                    f"Upload timed out for {path.name}. Try --http-timeout 600 or copy the file into "
                    f"ComfyUI input/ manually; very large uploads need a higher timeout."
                ) from e
            log.info("Upload finished for node %s: %s", label, path.name)
        else:
            log.warning(
                "No local file at %r - LoadImage must resolve %r under the ComfyUI input folder "
                "(copy files there or pass a full path to an existing image).",
                raw,
                path.name,
            )


async def _cloud_request_with_retries(
    op_name: str,
    do_request,
    *,
    attempts: int = 4,
) -> httpx.Response:
    """Retry transient network errors (common behind misconfigured HTTP proxies)."""
    last: BaseException | None = None
    for attempt in range(1, attempts + 1):
        try:
            r = await do_request()
            r.raise_for_status()
            return r
        except (
            httpx.ReadError,
            httpx.ConnectError,
            httpx.RemoteProtocolError,
            httpx.WriteError,
            httpx.PoolTimeout,
        ) as e:
            last = e
            if attempt >= attempts:
                break
            delay = min(2 ** (attempt - 1), 30.0)
            log.warning(
                "%s failed (%s: %s), retry %s/%s in %.1fs",
                op_name,
                type(e).__name__,
                e,
                attempt,
                attempts,
                delay,
            )
            await asyncio.sleep(delay)
    assert last is not None
    raise last


async def cloud_upload_local_images_if_needed(
    client: httpx.AsyncClient,
    workflow: dict,
    image_41: str | None,
    image_83: str | None,
) -> None:
    """Upload local files to Comfy Cloud (POST /api/upload/image).

    Equivalent to:
      curl -X POST \"$BASE_URL/api/upload/image\" \\
        -H \"X-API-Key: ...\" \\
        -F \"image=@file.png\" -F \"type=input\" -F \"overwrite=true\"
    """
    for label, raw in (("41", image_41), ("83", image_83)):
        if not raw:
            continue
        path = Path(raw.strip())
        if path.is_file():
            log.info("Cloud upload for node %s: %s", label, path.resolve())
            data_bytes = path.read_bytes()
            fname = path.name
            mime_val = mimetypes.guess_type(fname)[0]

            async def _post_upload(
                _fname: str = fname,
                _body: bytes = data_bytes,
                _mime: str | None = mime_val,
            ) -> httpx.Response:
                # Same multipart as: -F "image=@..." -F "type=input" -F "overwrite=true"
                if _mime:
                    image_field: tuple[str | bytes, ...] = (_fname, _body, _mime)
                else:
                    image_field = (_fname, _body)
                return await client.post(
                    f"{CLOUD_BASE_URL}/api/upload/image",
                    files={"image": image_field},
                    data={"type": "input", "overwrite": "true"},
                )

            try:
                r = await _cloud_request_with_retries(f"Cloud upload ({fname})", _post_upload)
            except httpx.HTTPStatusError as e:
                log.error("Cloud upload failed: HTTP %s", e.response.status_code)
                _raise_if_cloud_free_tier_error(e)
                _log_http_error_response(e)
                raise RuntimeError(
                    "Comfy Cloud rejected image upload (HTTP %s). Common causes: subscription/API "
                    "does not allow uploads, or WAF blocked the request. Try: upload images in the "
                    "Comfy Cloud web UI first, then run with --cloud-skip-upload and matching "
                    "filenames in the workflow."
                    % (e.response.status_code,)
                ) from e

            try:
                info = r.json()
            except json.JSONDecodeError:
                info = {}
            name = info.get("name")
            node_id = label
            if name and node_id in workflow and isinstance(workflow[node_id], dict):
                workflow[node_id].setdefault("inputs", {})["image"] = name
                log.info("LoadImage node %s will use cloud input name: %s", node_id, name)
        else:
            log.warning(
                "No local file at %r - ensure %r exists in cloud input or pass a real file path.",
                raw,
                path.name,
            )


def _cloud_httpx_timeout(job_timeout: float) -> httpx.Timeout:
    """Per-request timeouts; uploads and long polls need generous read/write."""
    return httpx.Timeout(
        connect=60.0,
        read=max(300.0, min(job_timeout, 3600.0)),
        write=600.0,
        pool=60.0,
    )


def _cloud_extract_history_outputs(hist: object, prompt_id: str) -> dict | None:
    """GET /api/history_v2/{id} may return top-level outputs or {prompt_id: {outputs: {...}}}."""
    if not isinstance(hist, dict):
        return None
    top = hist.get("outputs")
    if isinstance(top, dict) and top:
        return top
    entry = hist.get(prompt_id)
    if isinstance(entry, dict):
        inner = entry.get("outputs")
        if isinstance(inner, dict) and inner:
            return inner
    if len(hist) == 1:
        only = next(iter(hist.values()))
        if isinstance(only, dict):
            inner = only.get("outputs")
            if isinstance(inner, dict) and inner:
                return inner
    return None


async def run_comfy_cloud(
    workflow: dict,
    output_path: Path,
    api_key: str,
    image_41: str | None,
    image_83: str | None,
    *,
    poll_interval: float,
    job_timeout: float,
    trust_env: bool,
    skip_local_upload: bool,
) -> None:
    """Run workflow on Comfy Cloud (https://docs.comfy.org/development/cloud/overview)."""
    headers = _cloud_client_headers(api_key)
    if trust_env:
        log.info("Comfy Cloud HTTP client: using system proxy (HTTP_PROXY / HTTPS_PROXY)")
    else:
        log.info(
            "Comfy Cloud HTTP client: trust_env=False (ignoring HTTP_PROXY/HTTPS_PROXY; "
            "avoids broken proxies on multipart upload). Use --cloud-use-system-proxy if you need a proxy."
        )
    async with httpx.AsyncClient(
        headers=headers,
        timeout=_cloud_httpx_timeout(job_timeout),
        follow_redirects=True,
        trust_env=trust_env,
    ) as client:
        if skip_local_upload:
            log.info("Skipping cloud local upload (--cloud-skip-upload); ensure LoadImage names exist in cloud.")
        else:
            await cloud_upload_local_images_if_needed(client, workflow, image_41, image_83)

        log.info("Step 4/5: POST %s/api/prompt (Comfy Cloud)", CLOUD_BASE_URL)
        try:
            r = await client.post(
                f"{CLOUD_BASE_URL}/api/prompt",
                json={"prompt": workflow},
            )
            _cloud_raise_for_status(r)
        except httpx.HTTPStatusError as e:
            log.error("Cloud POST /api/prompt: HTTP %s", e.response.status_code)
            _raise_if_cloud_free_tier_error(e)
            _log_http_error_response(e)
            raise RuntimeError(
                "Comfy Cloud rejected the workflow. See Server response body above."
            ) from e

        body = r.json()
        prompt_id = body.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"Unexpected /api/prompt response: {body}")

        log.info("Cloud job queued: prompt_id=%s (polling status)", prompt_id)

        deadline = time.monotonic() + job_timeout
        while time.monotonic() < deadline:
            sr = await client.get(f"{CLOUD_BASE_URL}/api/job/{prompt_id}/status")
            _cloud_raise_for_status(sr)
            payload = sr.json() or {}
            status = payload.get("status")
            log.info("Cloud job status: %s", status)
            # Cloud API returns "success" when done; older/alternate docs use "completed"
            if status in ("completed", "success"):
                break
            # "error" is a terminal state (same as failed); do not keep polling until timeout
            if status in ("failed", "cancelled", "error"):
                extra = {k: v for k, v in payload.items() if k != "status"}
                detail = (
                    payload.get("message")
                    or payload.get("error")
                    or payload.get("detail")
                    or (extra if extra else None)
                )
                raise RuntimeError(
                    f"Comfy Cloud job {prompt_id} status={status!r}"
                    + (f": {detail!r}" if detail is not None else "")
                )
            await asyncio.sleep(poll_interval)
        else:
            raise TimeoutError(
                f"Comfy Cloud job {prompt_id} did not complete within {job_timeout}s"
            )

        hr = await client.get(f"{CLOUD_BASE_URL}/api/history_v2/{prompt_id}")
        _cloud_raise_for_status(hr)
        hist = hr.json()
        outputs = _cloud_extract_history_outputs(hist, prompt_id)
        if not outputs:
            raise RuntimeError(f"No outputs in history for {prompt_id}: {hist!r}")

        first_meta: dict | None = None
        for _node_id, node_out in outputs.items():
            if not isinstance(node_out, dict):
                continue
            for img in node_out.get("images") or []:
                if isinstance(img, dict) and img.get("filename"):
                    first_meta = img
                    break
            if first_meta:
                break

        if not first_meta:
            raise RuntimeError(f"No image entries in cloud outputs: {outputs!r}")

        params = {
            "filename": first_meta["filename"],
            "subfolder": first_meta.get("subfolder") or "",
            "type": first_meta.get("type") or "output",
        }
        log.info("Step 5/5: Download first output via /api/view")
        vr = await client.get(f"{CLOUD_BASE_URL}/api/view", params=params)
        _cloud_raise_for_status(vr)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(vr.content)
        log.info("Saved file: %s", output_path.resolve())


def _save_local_output_images(output_path: Path, result: PromptResult) -> list[Path]:
    """Write all returned PIL images under output_path.parent; first uses output_path name."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    items = result.output_images
    for i, item in enumerate(items):
        dest = output_path if i == 0 else output_path.parent / f"{output_path.stem}_{i + 1}{output_path.suffix}"
        item.image.save(str(dest))
        resolved = dest.resolve()
        saved.append(resolved)
        log.info("Saved file (%s/%s): %s", i + 1, len(items), resolved)
    return saved


def apply_comfy_job_1_replace_overrides(
    workflow: dict,
    *,
    image_41: str | None,
    image_83: str | None,
    prompt_negative: str | None,
    prompt_positive: str | None,
    seed: int | None,
) -> None:
    """Patch nodes for comfy_job_1_replace.json (same node ids if you copy the graph)."""
    applied: list[str] = []
    if image_41 is not None and "41" in workflow:
        workflow["41"]["inputs"]["image"] = _load_image_input_value(image_41)
        applied.append(f"node 41 image={workflow['41']['inputs']['image']}")
    if image_83 is not None and "83" in workflow:
        workflow["83"]["inputs"]["image"] = _load_image_input_value(image_83)
        applied.append(f"node 83 image={workflow['83']['inputs']['image']}")
    if prompt_negative is not None and "170:149" in workflow:
        workflow["170:149"]["inputs"]["prompt"] = prompt_negative
        applied.append("node 170:149 prompt (negative)")
    if prompt_positive is not None and "170:151" in workflow:
        workflow["170:151"]["inputs"]["prompt"] = prompt_positive
        applied.append("node 170:151 prompt (positive)")
    if seed is not None and "170:169" in workflow:
        workflow["170:169"]["inputs"]["seed"] = seed
        applied.append(f"node 170:169 seed={seed}")
    if applied:
        log.info("Overrides applied: %s", "; ".join(applied))
    else:
        log.info("No CLI overrides (using JSON as-is)")


async def run(
    workflow_name: str,
    host: str,
    output_path: Path,
    *,
    image_41: str | None,
    image_83: str | None,
    prompt_negative: str | None,
    prompt_positive: str | None,
    seed: int | None,
    skip_health_check: bool,
    state_tracker: Literal["websocket", "http"] = "websocket",
    keep_meta: bool = False,
    cloud: bool = False,
    cloud_api_key: str | None = None,
    cloud_poll_interval: float = 2.0,
    cloud_job_timeout: float = 600.0,
    cloud_trust_env: bool = False,
    cloud_skip_upload: bool = False,
    http_timeout: float = 300.0,
) -> list[Path]:
    log.info("Step 1/5: Load workflow JSON: %s", workflow_name)
    workflow = load_workflow(workflow_name)
    log.info("Loaded workflow: %s node(s)", len(workflow))

    log.info("Step 2/5: Apply parameter overrides")
    apply_comfy_job_1_replace_overrides(
        workflow,
        image_41=image_41,
        image_83=image_83,
        prompt_negative=prompt_negative,
        prompt_positive=prompt_positive,
        seed=seed,
    )
    if not keep_meta:
        workflow = strip_workflow_meta_for_api(workflow)
        log.info("Stripped _meta from nodes for /prompt API (use --keep-meta if your build requires it)")

    if cloud:
        if not cloud_api_key:
            raise RuntimeError(
                "Comfy Cloud requires an API key: set env COMFY_CLOUD_API_KEY or use --cloud-api-key"
            )
        log.info("Mode: Comfy Cloud (%s)", CLOUD_BASE_URL)
        await run_comfy_cloud(
            workflow,
            output_path,
            cloud_api_key,
            image_41,
            image_83,
            poll_interval=cloud_poll_interval,
            job_timeout=cloud_job_timeout,
            trust_env=cloud_trust_env,
            skip_local_upload=cloud_skip_upload,
        )
        return [output_path.resolve()]

    log.info("Mode: local ComfyUI")
    try:
        log.info("Step 3/5: Connect to ComfyUI and open session (tracker=%s)", state_tracker)
        async with _comfy_client(
            host,
            skip_health_check=skip_health_check,
            start_state_tracker=state_tracker,
            http_timeout=http_timeout,
        ) as client:
            await upload_local_input_images_if_needed(client, image_41, image_83)
            log.info("Step 4/5: POST /prompt (submit workflow, %s nodes)", len(workflow))
            log.info("Calling ComfyUI API: POST /prompt ...")
            try:
                prompt = await client.submit_workflow(workflow)
                log.info(
                    "Queued: prompt_id=%s - waiting for execution",
                    prompt.prompt_id,
                )
                result = await prompt.future
                log.info("Execution finished for prompt_id=%s", prompt.prompt_id)
            except asyncio.CancelledError:
                log.warning("Cancelled during submit_workflow or wait", exc_info=True)
                raise
            except httpx.HTTPStatusError as e:
                log.error("ComfyUI POST /prompt: HTTP %s", e.response.status_code)
                _log_http_error_response(e)
                path = (getattr(e.request.url, "path", "") or "").replace("\\", "/").rstrip("/") or "/"
                if e.request.method == "POST" and path.endswith("/prompt"):
                    raise RuntimeError(
                        "ComfyUI rejected the workflow. Read 'Server response body' above for "
                        "node_errors. For LoadImage 'Invalid image file', copy files into ComfyUI input/ "
                        "or pass full paths so the script can upload via /upload/image."
                    ) from e
                raise RuntimeError(
                    f"HTTP {e.response.status_code} {e.request.method} {e.request.url}"
                ) from e
            except Exception:
                log.exception(
                    "Failure during submit_workflow or await result (before session cleanup)"
                )
                raise
    except httpx.HTTPStatusError as e:
        log.error(
            "HTTP error: %s %s -> %s",
            e.request.method,
            e.request.url,
            e.response.status_code,
        )
        print(
            f"[run_workflow] HTTP {e.response.status_code} {e.request.method} {e.request.url}",
            file=sys.stderr,
            flush=True,
        )
        _log_http_error_response(e)
        req = e.request
        path = (getattr(req.url, "path", "") or "").replace("\\", "/").rstrip("/") or "/"
        code = e.response.status_code
        if req.method == "GET" and path in ("/", ""):
            raise RuntimeError(_format_comfy_connect_help(host, code)) from e
        if req.method == "POST" and path.endswith("/prompt") and code in (502, 503, 504):
            raise RuntimeError(_format_prompt_gateway_help(host, code)) from e
        raise RuntimeError(
            f"ComfyUI HTTP {code} {req.method} {req.url}"
        ) from e
    except httpx.RequestError as e:
        # ConnectError, timeouts, etc. (HTTPStatusError is handled above)
        log.error("Network error reaching ComfyUI: %s", e)
        print(f"[run_workflow] {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        raise RuntimeError(
            f"Cannot reach ComfyUI at http://{host}/ - is it running? ({e})"
        ) from e
    except ComfyExecutionError as e:
        log.error("ComfyUI reported execution failure: %s", e)
        print(f"[run_workflow] ComfyExecutionError: {e}", file=sys.stderr, flush=True)
        raise RuntimeError(
            "Workflow run failed on the server; see ComfyUI console and log line above."
        ) from e
    except asyncio.CancelledError:
        # Python 3.11+: CancelledError is BaseException, not Exception
        log.warning("Cancelled during ComfyUI submit/wait (task cancelled)")
        print("[run_workflow] CancelledError: async task was cancelled", file=sys.stderr, flush=True)
        raise
    except RuntimeError:
        raise
    except Exception as e:
        log.exception("Failed during submit or wait (see traceback below)")
        print(f"[run_workflow] {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        raise

    if not result.output_images:
        log.error("No images in result for prompt_id=%s", getattr(prompt, "prompt_id", "?"))
        raise RuntimeError("No output images; check workflow and ComfyUI logs.")

    log.info(
        "Step 5/5: Save output to %s (%s image(s))",
        output_path.parent.resolve(),
        len(result.output_images),
    )
    return _save_local_output_images(output_path, result)


def main() -> None:
    default_json = "comfy_job_1_replace.json"
    parser = argparse.ArgumentParser(description="Run ComfyUI API workflow JSON from comfyUI_json/")
    parser.add_argument(
        "--workflow",
        "-w",
        default=default_json,
        help=f"JSON filename under comfyUI_json/ (default: {default_json})",
    )
    parser.add_argument(
        "--host",
        "-H",
        default="127.0.0.1:8188",
        help=(
            "ComfyUI host:port (default: 127.0.0.1:8188). "
            "Prefer 127.0.0.1 over localhost on Windows: localhost may resolve to IPv6 ::1 "
            "while ComfyUI listens only on IPv4, causing 502 or connection errors."
        ),
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help=(
            "Path for primary output image (default: manager_system/output/output.png). "
            "Extra images become output_2.png, output_3.png, etc. in the same folder."
        ),
    )
    parser.add_argument(
        "--prompt-positive",
        "-p",
        default=None,
        help="Override positive prompt (node 170:151 if present)",
    )
    parser.add_argument(
        "--prompt-negative",
        "-n",
        default=None,
        help="Override negative / empty slot prompt (node 170:149 if present)",
    )
    parser.add_argument(
        "--seed",
        "-s",
        type=int,
        default=None,
        help="Override KSampler seed (node 170:169)",
    )
    parser.add_argument(
        "--image-41",
        default=None,
        metavar="NAME_OR_PATH",
        help="Node 41: basename used in workflow; if this path exists locally, upload to ComfyUI input first",
    )
    parser.add_argument(
        "--image-83",
        default=None,
        metavar="NAME_OR_PATH",
        help="Node 83: basename used in workflow; if this path exists locally, upload to ComfyUI input first",
    )
    parser.add_argument(
        "--verify-server",
        action="store_true",
        help="Run GET / before workflow (default: skip; avoids 502 on some proxies when only / is broken)",
    )
    parser.add_argument(
        "--http-tracker",
        action="store_true",
        help="Use HTTP polling instead of WebSocket to track progress (slower; use if shutdown logs confuse debugging)",
    )
    parser.add_argument(
        "--http-timeout",
        type=float,
        default=300.0,
        metavar="SEC",
        help="Local ComfyUI: httpx read/write timeout per request in seconds (default: 300; uploads need time)",
    )
    parser.add_argument(
        "--keep-meta",
        action="store_true",
        help="Keep per-node _meta in JSON (default: strip for /prompt; stripping fixes many HTTP 400 errors)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="DEBUG-level logs (more detail)",
    )
    parser.add_argument(
        "--cloud",
        action="store_true",
        help=(
            f"Use Comfy Cloud API ({CLOUD_BASE_URL}); requires API key and a paid plan (Free tier has no API key auth)"
        ),
    )
    parser.add_argument(
        "--cloud-api-key",
        default=None,
        metavar="KEY",
        help="Comfy Cloud API key (prefer env COMFY_CLOUD_API_KEY; do not commit keys)",
    )
    parser.add_argument(
        "--cloud-poll-interval",
        type=float,
        default=2.0,
        metavar="SEC",
        help="Seconds between GET /api/job/.../status polls (default: 2)",
    )
    parser.add_argument(
        "--cloud-job-timeout",
        type=float,
        default=600.0,
        metavar="SEC",
        help="Max seconds to wait for cloud job (default: 600)",
    )
    parser.add_argument(
        "--cloud-use-system-proxy",
        action="store_true",
        help=(
            "Use HTTP_PROXY/HTTPS_PROXY for Comfy Cloud (default: off; misconfigured proxies often cause ReadError on upload)"
        ),
    )
    parser.add_argument(
        "--cloud-skip-upload",
        action="store_true",
        help=(
            "Do not call POST /api/upload/image; use filenames already present in Comfy Cloud (e.g. uploaded via web UI)"
        ),
    )

    args = parser.parse_args()
    _configure_logging(args.verbose)
    if args.output is not None:
        out = Path(args.output)
    else:
        _default_output_dir().mkdir(parents=True, exist_ok=True)
        out = _default_output_dir() / "output.png"

    cloud_key = args.cloud_api_key or os.environ.get("COMFY_CLOUD_API_KEY")
    if args.cloud and not cloud_key:
        parser.error("Comfy Cloud requires COMFY_CLOUD_API_KEY or --cloud-api-key")

    tracker: Literal["websocket", "http"] = "http" if args.http_tracker else "websocket"
    if args.cloud:
        log.info(
            "Starting run (cloud): workflow=%s output=%s base=%s",
            args.workflow,
            out,
            CLOUD_BASE_URL,
        )
    else:
        log.info(
            "Starting run: host=%s workflow=%s output=%s verify_server=%s tracker=%s http_timeout=%ss",
            args.host,
            args.workflow,
            out,
            args.verify_server,
            tracker,
            args.http_timeout,
        )

    saved = asyncio.run(
        run(
            args.workflow,
            args.host,
            out,
            image_41=args.image_41,
            image_83=args.image_83,
            prompt_negative=args.prompt_negative,
            prompt_positive=args.prompt_positive,
            seed=args.seed,
            skip_health_check=not args.verify_server,
            state_tracker=tracker,
            keep_meta=args.keep_meta,
            cloud=args.cloud,
            cloud_api_key=cloud_key,
            cloud_poll_interval=args.cloud_poll_interval,
            cloud_job_timeout=args.cloud_job_timeout,
            cloud_trust_env=args.cloud_use_system_proxy,
            cloud_skip_upload=args.cloud_skip_upload,
            http_timeout=args.http_timeout,
        )
    )
    log.info("Done.")
    for p in saved:
        print(f"Saved: {p}")


if __name__ == "__main__":
    main()
