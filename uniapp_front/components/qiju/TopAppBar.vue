<template>
	<view class="top-bar" :class="variant" :style="{ paddingTop: statusBarHeight + 'px' }">
		<view
			class="bar-inner"
			:class="{ 'detail-inner': variant === 'detail' }"
			:style="barInnerStyle"
		>
			<template v-if="variant === 'detail'">
				<view class="back-btn" :style="backBtnStyle" @click="onBack">
					<text class="back-icon" :style="backIconStyle">‹</text>
				</view>
				<text class="title detail-title">{{ title }}</text>
				<view class="nav-spacer" :style="backBtnStyle" />
			</template>
			<template v-else>
				<view class="brand">
					<image v-if="variant === 'profile'" class="brand-icon" :src="icons.headerCompass" mode="aspectFit" />
					<text class="logo" :class="{ profile: variant === 'profile' }">栖居 QĪJŪ</text>
				</view>
			</template>
		</view>
	</view>
</template>

<script>
	import { ICONS } from '../../static/qiju/assets.js'

	export default {
		name: 'TopAppBar',
		props: {
			title: { type: String, default: '' },
			variant: { type: String, default: 'home' }
		},
		data() {
			return {
				statusBarHeight: 20,
				barInnerHeight: 56,
				navPaddingLeft: 24,
				navPaddingRight: 24,
				menuButtonSize: 32,
				icons: ICONS
			}
		},
		computed: {
			barInnerStyle() {
				const style = { height: this.barInnerHeight + 'px' }
				if (this.variant === 'detail') {
					style.paddingLeft = this.navPaddingLeft + 'px'
					style.paddingRight = this.navPaddingRight + 'px'
				}
				return style
			},
			backBtnStyle() {
				return {
					width: this.menuButtonSize + 'px',
					height: this.menuButtonSize + 'px'
				}
			},
			backIconStyle() {
				return {
					fontSize: Math.round(this.menuButtonSize * 0.72) + 'px'
				}
			}
		},
		created() {
			this.initNavMetrics()
		},
		methods: {
			initNavMetrics() {
				const sys = uni.getSystemInfoSync()
				this.statusBarHeight = sys.statusBarHeight || 20
				const defaultHeight = Math.round(112 * sys.windowWidth / 750)
				const defaultSize = Math.round(64 * sys.windowWidth / 750)
				this.menuButtonSize = defaultSize
				this.navPaddingLeft = Math.round(24 * sys.windowWidth / 750)
				this.navPaddingRight = Math.round(48 * sys.windowWidth / 750)

				// #ifdef MP-WEIXIN
				const menuButton = uni.getMenuButtonBoundingClientRect()
				if (menuButton && menuButton.height) {
					this.barInnerHeight = (menuButton.top - this.statusBarHeight) * 2 + menuButton.height
					this.menuButtonSize = menuButton.height
					this.navPaddingLeft = 10
					this.navPaddingRight = sys.windowWidth - menuButton.right
					return
				}
				// #endif

				this.barInnerHeight = defaultHeight
			},
			onBack() {
				uni.navigateBack({ fail: () => uni.reLaunch({ url: '/pages/home/home' }) })
			}
		}
	}
</script>

<style scoped>
	.top-bar {
		position: sticky;
		top: 0;
		z-index: 99;
		background: rgba(253, 249, 242, 0.8);
		backdrop-filter: blur(24rpx);
	}

	.bar-inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		box-sizing: border-box;
		padding: 0 48rpx;
	}

	.top-bar.profile .bar-inner {
		padding-left: 48rpx;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 16rpx;
	}

	.brand-icon {
		width: 22rpx;
		height: 36rpx;
	}

	.logo {
		font-size: 36rpx;
		font-weight: 800;
		color: #003da6;
		letter-spacing: -0.9rpx;
		line-height: 1;
	}

	.logo.profile {
		font-size: 40rpx;
		letter-spacing: 4rpx;
	}

	.title {
		flex: 1;
		text-align: center;
		font-size: 28rpx;
		font-weight: 700;
		color: #1c1c18;
		letter-spacing: -0.7rpx;
	}

	.detail-inner {
		position: relative;
		justify-content: flex-start;
		padding: 0;
	}

	.detail-title {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		flex: none;
		max-width: 42%;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.nav-spacer {
		flex-shrink: 0;
		margin-left: auto;
	}

	.back-btn {
		flex-shrink: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.back-icon {
		color: #1c1c18;
		line-height: 1;
		font-weight: 300;
	}
</style>
