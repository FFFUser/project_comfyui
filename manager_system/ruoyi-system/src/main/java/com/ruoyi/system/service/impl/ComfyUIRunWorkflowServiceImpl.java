package com.ruoyi.system.service.impl;

import com.ruoyi.common.config.RuoYiConfig;
import com.ruoyi.common.config.ServerConfig;
import com.ruoyi.common.constant.Constants;
import com.ruoyi.common.exception.ServiceException;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.common.utils.file.FileUploadUtils;
import com.ruoyi.common.utils.uuid.IdUtils;
import com.ruoyi.system.service.IComfyUIRunWorkflowService;
import org.apache.commons.io.FilenameUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * ComfyUI ������ �����ʵ��
 *
 * @author ruoyi
 */
@Service
public class ComfyUIRunWorkflowServiceImpl implements IComfyUIRunWorkflowService
{
    private static final Logger log = LoggerFactory.getLogger(ComfyUIRunWorkflowServiceImpl.class);

    private static final Pattern SAVED_LINE = Pattern.compile("^Saved:\\s*(.+)$");

    @Autowired
    private ServerConfig serverConfig;

    @Value("${comfyui.python-executable:python}")
    private String pythonExecutable;

    /** {@code comfyUI_python} ����·���������� {@code user.dir/../comfyUI_python} */
    @Value("${comfyui.python-script-dir:}")
    private String pythonScriptDir;

    @Value("${comfyui.cloud-enabled:true}")
    private boolean cloudEnabled;

    @Value("${comfyui.process-timeout-seconds:900}")
    private long processTimeoutSeconds;

    @Value("${comfyui.cloud-api-key:}")
    private String cloudApiKey;

    /**
     * ִ�� Python �������ű���
     *
     * @param imagePath41 ��Ӧ {@code --image-41}
     * @param imagePath83 ��Ӧ {@code --image-83}
     * @return �ű�����е�һ�� {@code Saved: ...} ��·��
     */
    @Override
    public String run(String imagePath41, String imagePath83)
    {
        try
        {
            return runPythonWorkflow(imagePath41, imagePath83);
        }
        catch (IOException e)
        {
            throw new ServiceException(e.getMessage()).setDetailMessage(e.toString());
        }
        catch (InterruptedException e)
        {
            Thread.currentThread().interrupt();
            throw new ServiceException("ComfyUI �����ж�").setDetailMessage(e.toString());
        }
    }

    private String runPythonWorkflow(String imagePath41, String imagePath83) throws IOException, InterruptedException
    {
        Path scriptDir = resolveScriptDir();
        Path script = scriptDir.resolve("run_workflow.py");
        if (!Files.isRegularFile(script))
        {
            throw new IOException("run_workflow.py not found: " + script);
        }

        String local41 = toLocalPathForPython(imagePath41);
        String local83 = toLocalPathForPython(imagePath83);
        log.debug("ComfyUI image paths for python: [{}] -> [{}], [{}] -> [{}]", imagePath41, local41, imagePath83, local83);

        List<String> command = new ArrayList<>();
        command.add(pythonExecutable);
        command.add("run_workflow.py");
        if (cloudEnabled)
        {
            command.add("--cloud");
            if (StringUtils.isNotEmpty(cloudApiKey))
            {
                command.add("--cloud-api-key");
                command.add(cloudApiKey);
            }
        }
        command.add("--image-41");
        command.add(local41);
        command.add("--image-83");
        command.add(local83);

        ProcessBuilder pb = new ProcessBuilder(command);
        pb.directory(scriptDir.toFile());
        pb.redirectErrorStream(true);
        if (StringUtils.isNotEmpty(cloudApiKey))
        {
            pb.environment().put("COMFY_CLOUD_API_KEY", cloudApiKey);
        }

        List<String> cmdForLog = maskCloudApiKeyForLog(command);
        log.info("ComfyUI Python 工作目录: {}", scriptDir.toAbsolutePath().normalize());
        log.info("ComfyUI Python 命令行: {}", formatCommandLine(cmdForLog));

        Process process = pb.start();
        StringBuilder output = new StringBuilder();
        Thread drain = new Thread(() -> drainStream(process.getInputStream(), output), "comfyui-python-stdout");
        drain.setDaemon(true);
        drain.start();

        boolean finished = process.waitFor(processTimeoutSeconds, TimeUnit.SECONDS);
        if (!finished)
        {
            process.destroyForcibly();
            drain.join(5000);
            throw new IOException("Python process timeout after " + processTimeoutSeconds + "s");
        }
        drain.join(60000);
        int exit = process.exitValue();
        String text = output.toString();
        if (exit != 0)
        {
            throw new IOException("Python exited with code " + exit + ". Output tail:\n" + tail(text, 4000));
        }
        List<String> saved = parseSavedPaths(text);
        if (saved.isEmpty())
        {
            throw new IOException("No 'Saved:' line in Python output. Output tail:\n" + tail(text, 4000));
        }
        return copyPythonResultToUploadUrl(saved.get(0));
    }

    /**
     * 将 Python 输出的本地文件复制到 {@link RuoYiConfig#getUploadPath()}（与通用上传一致），返回 {@link ServerConfig#getUrl()} + {@code /profile/upload/...}。
     */
    private String copyPythonResultToUploadUrl(String pythonSavedPath) throws IOException
    {
        String trimmed = pythonSavedPath == null ? "" : pythonSavedPath.trim();
        if (StringUtils.isEmpty(trimmed))
        {
            throw new IOException("Empty path from Python Saved: line");
        }
        Path src = Paths.get(trimmed).toAbsolutePath().normalize();
        if (!Files.isRegularFile(src))
        {
            throw new IOException("Python result is not a regular file: " + src);
        }
        String ext = FilenameUtils.getExtension(src.getFileName().toString());
        if (StringUtils.isEmpty(ext))
        {
            ext = "png";
        }
        String relativeName = DateUtils.datePath() + "/" + IdUtils.fastSimpleUUID() + "." + ext;
        String uploadBase = RuoYiConfig.getUploadPath();
        java.io.File destFile = FileUploadUtils.getAbsoluteFile(uploadBase, relativeName);
        Files.copy(src, destFile.toPath(), StandardCopyOption.REPLACE_EXISTING);
        String profileRelative = FileUploadUtils.getPathFileName(uploadBase, relativeName);
        String url = serverConfig.getUrl() + profileRelative;
        log.info("ComfyUI python output copied to upload: {} -> {} ({})", src, destFile.getAbsolutePath(), url);
        return url;
    }

    /**
     * 将前端传入的 {@code http(s)://.../profile/...} 或 {@code /profile/...} 转为 {@link RuoYiConfig#getProfile()} 下绝对路径，供本机 Python 读盘；
     * 其它字符串按本地路径规范化。
     */
    private static String toLocalPathForPython(String raw)
    {
        if (StringUtils.isEmpty(raw))
        {
            return raw;
        }
        String s = raw.trim();
        if (s.startsWith("http://") || s.startsWith("https://"))
        {
            int p = s.indexOf(Constants.RESOURCE_PREFIX);
            if (p >= 0
                && (p + Constants.RESOURCE_PREFIX.length() == s.length()
                    || s.charAt(p + Constants.RESOURCE_PREFIX.length()) == '/'))
            {
                return resolveProfileUriToAbsolutePath(s.substring(p));
            }
            return s;
        }
        if (s.startsWith(Constants.RESOURCE_PREFIX))
        {
            return resolveProfileUriToAbsolutePath(s);
        }
        return Paths.get(s).toAbsolutePath().normalize().toString();
    }

    private static String resolveProfileUriToAbsolutePath(String profileUriPath)
    {
        String suffix = StringUtils.substringAfter(profileUriPath, Constants.RESOURCE_PREFIX);
        while (suffix.startsWith("/") || suffix.startsWith("\\"))
        {
            suffix = suffix.substring(1);
        }
        if (StringUtils.isEmpty(suffix))
        {
            return Paths.get(RuoYiConfig.getProfile()).toAbsolutePath().normalize().toString();
        }
        return Paths.get(RuoYiConfig.getProfile(), suffix).toAbsolutePath().normalize().toString();
    }

    private void drainStream(InputStream in, StringBuilder sink)
    {
        Charset cs = Charset.defaultCharset();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(in, cs)))
        {
            String line;
            while ((line = br.readLine()) != null)
            {
                synchronized (sink)
                {
                    sink.append(line).append('\n');
                }
                log.debug("[python] {}", line);
            }
        }
        catch (IOException e)
        {
            log.warn("read python stdout: {}", e.getMessage());
        }
    }

    private static List<String> parseSavedPaths(String output)
    {
        List<String> list = new ArrayList<>();
        for (String line : output.split("\\R"))
        {
            Matcher m = SAVED_LINE.matcher(line.trim());
            if (m.matches())
            {
                list.add(m.group(1).trim());
            }
        }
        return list;
    }

    private static String tail(String s, int maxLen)
    {
        if (s == null || s.length() <= maxLen)
        {
            return s == null ? "" : s;
        }
        return s.substring(s.length() - maxLen);
    }

    private Path resolveScriptDir() throws IOException
    {
        if (StringUtils.isNotEmpty(pythonScriptDir))
        {
            Path p = Paths.get(pythonScriptDir).toAbsolutePath().normalize();
            if (!Files.isDirectory(p))
            {
                throw new IOException("comfyui.python-script-dir is not a directory: " + p);
            }
            return p;
        }
        Path found = resolveComfyPythonDirFallback();
        if (found != null)
        {
            return found;
        }
        Path base = Paths.get(System.getProperty("user.dir")).toAbsolutePath().normalize();
        throw new IOException(
            "comfyUI_python not found (tried sibling paths under user.dir=" + base
                + "). Set comfyui.python-script-dir in application.yml to the absolute path of comfyUI_python.");
    }

    /**
     * 未配置 {@code comfyui.python-script-dir} 时，按常见启动工作目录探测 {@code comfyUI_python}：
     * <ul>
     *   <li>{@code user.dir/comfyUI_python} — 从 {@code manager_system} 启动</li>
     *   <li>{@code user.dir/../comfyUI_python} — 从 {@code ruoyi-admin} 启动</li>
     *   <li>{@code user.dir/manager_system/comfyUI_python} — 从仓库根 {@code project_comfyui} 启动</li>
     * </ul>
     */
    private Path resolveComfyPythonDirFallback()
    {
        Path base = Paths.get(System.getProperty("user.dir")).toAbsolutePath().normalize();
        List<Path> candidates = Arrays.asList(
            base.resolve("comfyUI_python"),
            base.resolve("../comfyUI_python").normalize(),
            base.resolve("manager_system/comfyUI_python").normalize());
        for (Path dir : candidates)
        {
            if (Files.isDirectory(dir) && Files.isRegularFile(dir.resolve("run_workflow.py")))
            {
                return dir.normalize();
            }
        }
        return null;
    }

    /** 拼成可读的 shell 风格命令行（仅用于日志展示）。 */
    private static String formatCommandLine(List<String> parts)
    {
        if (parts == null || parts.isEmpty())
        {
            return "";
        }
        StringBuilder sb = new StringBuilder(shellQuoteForLog(parts.get(0)));
        for (int i = 1; i < parts.size(); i++)
        {
            sb.append(' ').append(shellQuoteForLog(parts.get(i)));
        }
        return sb.toString();
    }

    private static String shellQuoteForLog(String arg)
    {
        if (arg == null)
        {
            return "";
        }
        if (arg.indexOf(' ') < 0 && arg.indexOf('\t') < 0 && arg.indexOf('"') < 0)
        {
            return arg;
        }
        return '"' + arg.replace("\\", "\\\\").replace("\"", "\\\"") + '"';
    }

    /** 日志中隐藏 {@code --cloud-api-key} 后的密钥，避免写入日志文件。 */
    private static List<String> maskCloudApiKeyForLog(List<String> command)
    {
        List<String> out = new ArrayList<>(command.size());
        for (int i = 0; i < command.size(); i++)
        {
            String part = command.get(i);
            out.add(part);
            if ("--cloud-api-key".equals(part) && i + 1 < command.size())
            {
                i++;
                out.add("****");
            }
        }
        return out;
    }
}
