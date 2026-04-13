package com.ruoyi.web.controller.comfyui;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import java.nio.file.Path;
import java.nio.file.Paths;
import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.config.RuoYiConfig;
import com.ruoyi.common.config.ServerConfig;
import com.ruoyi.common.constant.Constants;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.domain.R;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.common.utils.file.FileUploadUtils;
import com.ruoyi.common.utils.file.FileUtils;
import com.ruoyi.system.service.IComfyUIRunWorkflowService;
import com.ruoyi.web.controller.comfyui.domain.ComfyUIGenerateRequest;
import com.ruoyi.web.controller.comfyui.domain.ComfyUIGenerateResponse;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;

/**
 * ComfyUI workflow HTTP API：调用 {@code comfyUI_python/run_workflow.py}。
 * <p>
 * 匿名访问（免登录）：由 {@code ShiroConfig} 中 {@code /comfyui/**} 与本类 {@link Anonymous} 共同保证。
 */
@Api(tags = "ComfyUI 生成接口")
@Anonymous
@RestController
@RequestMapping("/comfyui")
public class ComfyUIController extends BaseController
{
    @Autowired
    private IComfyUIRunWorkflowService comfyUIRunWorkflowService;

    @Autowired
    private ServerConfig serverConfig;

    @ApiOperation("匿名上传图片（供生成接口使用，表单字段名 file）")
    @PostMapping("/upload")
    public AjaxResult uploadFile(@RequestParam("file") MultipartFile file)
    {
        if (file == null || file.isEmpty())
        {
            return AjaxResult.error("文件不能为空");
        }
        try
        {
            String filePath = RuoYiConfig.getUploadPath();
            String fileName = FileUploadUtils.upload(filePath, file);
            String url = serverConfig.getUrl() + fileName;
            AjaxResult ajax = AjaxResult.success();
            ajax.put("url", url);
            ajax.put("fileName", fileName);
            ajax.put("newFileName", FileUtils.getName(fileName));
            ajax.put("originalFilename", file.getOriginalFilename());
            return ajax;
        }
        catch (Exception e)
        {
            logger.error("ComfyUI upload failed", e);
            return AjaxResult.error(e.getMessage());
        }
    }

    @ApiOperation("comfyUI 生成接口")
    @PostMapping(value = "/generate", produces = "application/json;charset=UTF-8")
    public R<ComfyUIGenerateResponse> generate(@RequestBody ComfyUIGenerateRequest request)
    {
        if (request == null || StringUtils.isEmpty(request.getImageUrl1()) || StringUtils.isEmpty(request.getImageUrl2()))
        {
            return R.fail("图片地址1、图片地址2不能为空");
        }

        try
        {
            String resultPath = comfyUIRunWorkflowService.run(request.getImageUrl1(), request.getImageUrl2());
            ComfyUIGenerateResponse resp = new ComfyUIGenerateResponse();
            resp.setResultUrl1(toAccessibleResultUrl(resultPath));
            return R.ok(resp);
        }
        catch (Exception e)
        {
            logger.error("ComfyUI run_workflow.py failed", e);
            return R.fail(e.getMessage() != null ? e.getMessage() : e.toString());
        }
    }

    /**
     * 将脚本输出的本地绝对路径（或已有 {@code /profile/...} 虚拟路径）转为前端可直接预览的完整 HTTP URL。
     * <ul>
     * <li>已是 {@code http(s)://} → 原样返回（如云端返回的地址）</li>
     * <li>以 {@code /profile} 开头 → 拼 {@link ServerConfig#getUrl()}</li>
     * <li>位于 {@code ruoyi.profile} 目录下 → {@code 站点根 + /profile/ + 相对 profile 的路径}</li>
     * <li>其它情况原样返回并打 warn（例如文件不在 profile 下）</li>
     * </ul>
     */
    private String toAccessibleResultUrl(String raw)
    {
        if (StringUtils.isEmpty(raw))
        {
            return raw;
        }
        String s = raw.trim();
        if (s.startsWith("http://") || s.startsWith("https://"))
        {
            return s;
        }
        if (s.startsWith(Constants.RESOURCE_PREFIX + "/") || s.equals(Constants.RESOURCE_PREFIX))
        {
            return serverConfig.getUrl() + s;
        }
        Path file;
        try
        {
            file = Paths.get(s).toAbsolutePath().normalize();
        }
        catch (Exception ex)
        {
            logger.warn("ComfyUI result path cannot be parsed as local path, return as-is: {}", s);
            return s;
        }
        Path profileRoot = Paths.get(RuoYiConfig.getProfile()).toAbsolutePath().normalize();
        if (!file.startsWith(profileRoot))
        {
            logger.warn("ComfyUI result is not under ruoyi.profile ({}), return as-is: {}", profileRoot, s);
            return s;
        }
        Path relative = profileRoot.relativize(file);
        String rel = relative.toString().replace('\\', '/');
        if (StringUtils.isEmpty(rel))
        {
            return s;
        }
        return serverConfig.getUrl() + Constants.RESOURCE_PREFIX + "/" + rel;
    }
}
