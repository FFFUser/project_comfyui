/**
 * 后端接口配置（与 manager_system ruoyi-admin 等对接）
 * 微信小程序真机调试需使用本机局域网 IP 或已备案 HTTPS 域名，并在公众平台配置「服务器域名」
 */
const devHost = 'http://127.0.0.1:8088'
const prodHost = 'https://your-production-domain.com'

let baseURL = devHost

// #ifdef H5
// H5 开发可用代理避免跨域；若使用代理，将 baseURL 改为 '' 并在 devServer 配置 proxy
// baseURL = ''
// #endif

// #ifdef MP-WEIXIN
// 真机无法访问 127.0.0.1，请改为电脑局域网 IP，例如：http://192.168.1.100:8088
// baseURL = 'http://192.168.1.100:8088'
// #endif

// #ifdef APP-PLUS
// App 可直接访问局域网或公网地址
// #endif

// 生产构建时切换（HBuilderX 发行 / CLI NODE_ENV=production）
if (typeof process !== 'undefined' && process.env && process.env.NODE_ENV === 'production') {
	baseURL = prodHost
}

export default {
	baseURL,
	/** 请求超时（毫秒） */
	timeout: 60000,
	/** 若依等接口常用 JSON */
	contentType: 'application/json;charset=UTF-8'
}
