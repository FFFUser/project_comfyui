package com.ruoyi.web.controller.comfyui.domain;

import java.io.Serializable;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

/**
 * ComfyUI /generate 入参
 */
@ApiModel("ComfyUI 生成请求")
public class ComfyUIGenerateRequest implements Serializable
{
    private static final long serialVersionUID = 1L;

    @ApiModelProperty(value = "图片地址1", required = true)
    private String imageUrl1;

    @ApiModelProperty(value = "图片地址2", required = true)
    private String imageUrl2;

    public String getImageUrl1()
    {
        return imageUrl1;
    }

    public void setImageUrl1(String imageUrl1)
    {
        this.imageUrl1 = imageUrl1;
    }

    public String getImageUrl2()
    {
        return imageUrl2;
    }

    public void setImageUrl2(String imageUrl2)
    {
        this.imageUrl2 = imageUrl2;
    }
}
