<template>
	<view class="page">
		<view class="section">
			<text class="label">图片 1</text>
			<view class="upload-box" @click="chooseImage(1)">
				<view v-if="uploading1" class="upload-mask">上传中…</view>
				<image v-if="preview1" class="preview" :src="preview1" mode="aspectFit" />
				<text v-else class="placeholder">点击选择或拍摄</text>
			</view>
			<text v-if="imageUrl1" class="url-hint">已上传</text>
		</view>
		<view class="section">
			<text class="label">图片 2</text>
			<view class="upload-box" @click="chooseImage(2)">
				<view v-if="uploading2" class="upload-mask">上传中…</view>
				<image v-if="preview2" class="preview" :src="preview2" mode="aspectFit" />
				<text v-else class="placeholder">点击选择或拍摄</text>
			</view>
			<text v-if="imageUrl2" class="url-hint">已上传</text>
		</view>
		<button
			class="btn-produce"
			type="primary"
			:disabled="loading || !imageUrl1 || !imageUrl2 || uploading1 || uploading2"
			:loading="loading"
			@click="onProduce"
		>
			{{ loading ? '生成中…' : '生产' }}
		</button>
		<view v-if="resultPathHint || resultPreviewSrc" class="section result-wrap">
			<text class="label">生成结果</text>
			<view v-if="resultPathHint" class="result-hint">
				<text selectable="true">{{ resultPathHint }}</text>
			</view>
			<image
				v-if="resultPreviewSrc"
				class="result-img"
				:src="resultPreviewSrc"
				mode="widthFix"
				@error="onResultImageError"
			/>
		</view>
	</view>
</template>

<script>
	import config from '../../config/config.js'
	import { post } from '../../utils/request.js'
	import { uploadComfyUIImage } from '../../utils/upload.js'

	/** ComfyUI 生成可能较久，与后端 process-timeout 对齐（毫秒） */
	const GENERATE_TIMEOUT_MS = 900000

	/**
	 * @param {string} path 后端 resultUrl1：可能是 https URL、/profile/...、或本机绝对路径
	 * @param {string} baseURL config.baseURL
	 */
	function normalizeResultForPreview(path, baseURL) {
		const base = String(baseURL || '').replace(/\/$/, '')
		const s = String(path || '').trim()
		if (!s) return { kind: 'empty' }
		if (s.startsWith('http://') || s.startsWith('https://')) {
			return { kind: 'http', url: s }
		}
		// Windows 盘符路径或明显本地路径：无法在端内作为网络图预览
		if (/^[A-Za-z]:[\\/]/.test(s) || /^\\\\[^\\]/.test(s)) {
			return { kind: 'localPath', display: s }
		}
		// Unix 绝对路径（若依对外文件为 /profile/...，其余按本地路径处理）
		if (s.startsWith('/') && !s.startsWith('/profile')) {
			return { kind: 'localPath', display: s }
		}
		const join = s.startsWith('/') ? base + s : `${base}/${s.replace(/^\//, '')}`
		return { kind: 'http', url: join }
	}

	export default {
		data() {
			return {
				/** 服务端返回的可访问地址，用于 /comfyui/generate */
				imageUrl1: '',
				imageUrl2: '',
				preview1: '',
				preview2: '',
				uploading1: false,
				uploading2: false,
				loading: false,
				/** 用于 <image>：本地临时路径或网络图缓存路径 */
				resultPreviewSrc: '',
				/** 本地磁盘路径等无法预览时的说明 */
				resultPathHint: ''
			}
		},
		methods: {
			chooseImage(slot) {
				if (slot === 1 && this.uploading1) return
				if (slot === 2 && this.uploading2) return
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					sourceType: ['album', 'camera'],
					success: async (res) => {
						const path = res.tempFilePaths[0]
						this.resultPreviewSrc = ''
						this.resultPathHint = ''
						if (slot === 1) {
							this.preview1 = path
							this.imageUrl1 = ''
							this.uploading1 = true
						} else {
							this.preview2 = path
							this.imageUrl2 = ''
							this.uploading2 = true
						}
						try {
							const url = await uploadComfyUIImage(path)
							// 预览始终用本地临时路径：服务端 URL 在小程序中常因合法域名/127.0.0.1 无法作为 <image> 的 src 回显
							if (slot === 1) {
								this.imageUrl1 = url
							} else {
								this.imageUrl2 = url
							}
						} catch (e) {
							const msg = e && e.message ? e.message : String(e)
							uni.showToast({
								title: msg.length > 18 ? msg.slice(0, 18) + '…' : msg,
								icon: 'none'
							})
							if (slot === 1) {
								this.preview1 = ''
								this.imageUrl1 = ''
							} else {
								this.preview2 = ''
								this.imageUrl2 = ''
							}
						} finally {
							if (slot === 1) this.uploading1 = false
							else this.uploading2 = false
						}
					}
				})
			},
			async onProduce() {
				if (!this.imageUrl1 || !this.imageUrl2) {
					uni.showToast({ title: '请先完成两张图片上传', icon: 'none' })
					return
				}
				this.loading = true
				this.resultPreviewSrc = ''
				this.resultPathHint = ''
				try {
					// 后端：POST /comfyui/generate，Body JSON { imageUrl1, imageUrl2 }
					const res = await post(
						'/comfyui/generate',
						{ imageUrl1: this.imageUrl1, imageUrl2: this.imageUrl2 },
						{ timeout: GENERATE_TIMEOUT_MS }
					)
					if (res.code !== 0) {
						throw new Error(res.msg || '生成失败')
					}
					const path = res.data && res.data.resultUrl1
					if (!path) {
						throw new Error('未返回结果地址')
					}
					const norm = normalizeResultForPreview(path, config.baseURL)
					if (norm.kind === 'localPath') {
						this.resultPathHint =
							'结果为服务器本地路径，无法在小程序内直接预览，请将后端返回改为可访问 URL 或把文件放到 /profile 可访问路径：\n' +
							norm.display
						uni.showToast({ title: '完成（见文字说明）', icon: 'none' })
						return
					}
					if (norm.kind !== 'http' || !norm.url) {
						throw new Error('无法解析结果地址')
					}
					await this.loadResultImagePreview(norm.url)
					uni.showToast({ title: '完成', icon: 'success' })
				} catch (e) {
					const msg = e && e.message ? e.message : String(e)
					uni.showToast({ title: msg.length > 20 ? msg.slice(0, 20) + '…' : msg, icon: 'none' })
				} finally {
					this.loading = false
				}
			},
			/** 将可访问的 http(s) 图转为本地临时路径，提升小程序 / 各端预览成功率 */
			loadResultImagePreview(httpUrl) {
				return new Promise((resolve) => {
					uni.downloadFile({
						url: httpUrl,
						success: (res) => {
							if (res.statusCode === 200 && res.tempFilePath) {
								this.resultPreviewSrc = res.tempFilePath
							} else {
								this.resultPreviewSrc = httpUrl
							}
							resolve()
						},
						fail: () => {
							this.resultPreviewSrc = httpUrl
							resolve()
						}
					})
				})
			},
			onResultImageError() {
				uni.showToast({ title: '图片预览失败，请检查域名白名单或改用 HTTPS', icon: 'none' })
			}
		}
	}
</script>

<style scoped>
	.page {
		min-height: 100vh;
		padding: 32rpx;
		padding-bottom: 64rpx;
		box-sizing: border-box;
		background: #f5f6f8;
	}

	.section {
		margin-bottom: 40rpx;
	}

	.label {
		display: block;
		font-size: 28rpx;
		color: #333;
		margin-bottom: 16rpx;
		font-weight: 500;
	}

	.upload-box {
		position: relative;
		height: 320rpx;
		border-radius: 16rpx;
		background: #fff;
		border: 2rpx dashed #c8c9cc;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}

	.placeholder {
		font-size: 28rpx;
		color: #969799;
	}

	.preview {
		width: 100%;
		height: 100%;
	}

	.upload-mask {
		position: absolute;
		inset: 0;
		z-index: 2;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.85);
		font-size: 28rpx;
		color: #646566;
	}

	.url-hint {
		display: block;
		margin-top: 12rpx;
		font-size: 24rpx;
		color: #07c160;
	}

	.btn-produce {
		margin-top: 16rpx;
		height: 88rpx;
		line-height: 88rpx;
		border-radius: 12rpx;
		font-size: 32rpx;
	}

	.result-wrap {
		margin-top: 48rpx;
	}

	.result-hint {
		padding: 20rpx;
		margin-bottom: 20rpx;
		background: #fff7e6;
		border-radius: 12rpx;
		border: 1rpx solid #ffe7ba;
		font-size: 24rpx;
		color: #666;
		line-height: 1.5;
		word-break: break-all;
	}

	.result-img {
		width: 100%;
		border-radius: 16rpx;
		background: #fff;
	}
</style>
