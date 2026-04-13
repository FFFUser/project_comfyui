package com.ruoyi.web.controller.comfyui.domain;

import java.io.Serializable;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

/**
 * ComfyUI /generate response body.
 */
@ApiModel("ComfyUI 生成结果")
public class ComfyUIGenerateResponse implements Serializable
{
    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "结果图访问 URL（已写入系统上传目录，与通用上传返回格式一致）")
    private String resultUrl1;

    public String getResultUrl1()
    {
        return resultUrl1;
    }

    public void setResultUrl1(String resultUrl1)
    {
        this.resultUrl1 = resultUrl1;
    }
}
