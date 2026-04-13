import config from '../config/config.js'

/**
 * 发起 HTTP 请求，自动拼接 config.baseURL
 * @param {Object} options 与 uni.request 一致，其中 url 可写相对路径如 '/login'
 */
export function request(options = {}) {
	const { url, header = {}, ...rest } = options
	const fullUrl = url.startsWith('http://') || url.startsWith('https://')
		? url
		: `${config.baseURL.replace(/\/$/, '')}/${String(url).replace(/^\//, '')}`

	return new Promise((resolve, reject) => {
		uni.request({
			url: fullUrl,
			timeout: rest.timeout ?? config.timeout,
			header: {
				'Content-Type': config.contentType,
				...header
			},
			...rest,
			success: (res) => {
				if (res.statusCode >= 200 && res.statusCode < 300) {
					resolve(res.data)
				} else {
					reject(res)
				}
			},
			fail: (err) => reject(err)
		})
	})
}

export function get(url, data, options = {}) {
	return request({ ...options, url, data, method: 'GET' })
}

export function post(url, data, options = {}) {
	return request({ ...options, url, data, method: 'POST' })
}
