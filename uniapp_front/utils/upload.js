import config from '../config/config.js'

/**
 * 上传单张图片到后端（若依 AjaxResult：code===0 且根级 url）
 * @param {string} filePath 本地临时路径（chooseImage 返回的 tempFilePaths）
 */
export function uploadComfyUIImage(filePath) {
	const url = `${config.baseURL.replace(/\/$/, '')}/comfyui/upload`
	return new Promise((resolve, reject) => {
		uni.uploadFile({
			url,
			filePath,
			name: 'file',
			success: (res) => {
				if (res.statusCode < 200 || res.statusCode >= 300) {
					reject(new Error(`HTTP ${res.statusCode}`))
					return
				}
				try {
					const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data
					if (data.code === 0 && data.url) {
						resolve(data.url)
					} else {
						reject(new Error(data.msg || '上传失败'))
					}
				} catch (e) {
					reject(e)
				}
			},
			fail: (err) => reject(err.errMsg ? new Error(err.errMsg) : err)
		})
	})
}
