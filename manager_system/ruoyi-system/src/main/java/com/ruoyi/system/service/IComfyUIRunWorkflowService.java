package com.ruoyi.system.service;

/**
 * ComfyUI 工作流 服务层
 * <p>
 * 在 {@code comfyUI_python} 目录下执行 {@code run_workflow.py}，将入参映射为 {@code --image-41} / {@code --image-83}。
 *
 * @author ruoyi
 */
public interface IComfyUIRunWorkflowService
{
    /**
     * 执行 Python 工作流脚本；脚本输出的本地结果会复制到系统上传目录，并返回可访问的完整 URL。
     *
     * @param imagePath41 对应 {@code --image-41}（本地路径或脚本可识别的路径）
     * @param imagePath83 对应 {@code --image-83}
     * @return 与通用上传一致：服务根 URL + {@code /profile/upload/...}
     */
    public String run(String imagePath41, String imagePath83);
}
