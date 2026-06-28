<template>
	<view class="bottom-nav" :style="navPaddingStyle">
		<view class="nav-row">
			<view
				v-for="item in tabs"
				:key="item.key"
				class="nav-item"
				:class="{ active: current === item.key }"
				@click="onTap(item)"
			>
				<image
					class="nav-icon"
					:src="current === item.key ? item.iconActive : item.icon"
					mode="aspectFit"
				/>
				<text class="nav-label">{{ item.label }}</text>
			</view>
		</view>
	</view>
</template>

<script>
	import { ICONS } from '../../static/qiju/assets.js'

	const TAB_ROUTES = {
		home: '/pages/home/home',
		workers: '/pages/workers/workers',
		designers: '/pages/designers/designers',
		materials: '/pages/materials/materials',
		profile: '/pages/profile/profile'
	}

	export default {
		name: 'BottomNavBar',
		props: {
			current: { type: String, default: 'home' }
		},
		data() {
			return {
				safeBottom: 0,
				basePaddingPx: 10,
				tabs: [
					{ key: 'home', label: '首页', icon: ICONS.navHome, iconActive: ICONS.navHomeActive },
					{ key: 'workers', label: '工人', icon: ICONS.navWorkers, iconActive: ICONS.navWorkersActive },
					{ key: 'designers', label: '设计师', icon: ICONS.navDesigners, iconActive: ICONS.navDesignersActive },
					{ key: 'materials', label: '材料', icon: ICONS.navMaterials, iconActive: ICONS.navMaterialsActive },
					{ key: 'profile', label: '我的', icon: ICONS.navProfile, iconActive: ICONS.navProfileActive }
				]
			}
		},
		computed: {
			navPaddingStyle() {
				return {
					paddingBottom: this.safeBottom + this.basePaddingPx + 'px'
				}
			}
		},
		created() {
			const sys = uni.getSystemInfoSync()
			this.safeBottom = sys.safeAreaInsets ? sys.safeAreaInsets.bottom : 0
			this.basePaddingPx = Math.round(20 * sys.windowWidth / 750)
		},
		methods: {
			onTap(item) {
				if (item.key === this.current) return
				uni.reLaunch({ url: TAB_ROUTES[item.key] })
			}
		}
	}
</script>

<style scoped>
	.bottom-nav {
		position: fixed;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 100;
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		height: 128rpx;
		padding: 0 78rpx;
		background: #fdf9f2;
		border-top: 1rpx solid rgba(195, 198, 215, 0.3);
		box-sizing: content-box;
	}

	.nav-row {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		width: 100%;
	}

	.nav-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 8rpx;
	}

	.nav-icon {
		width: 32rpx;
		height: 36rpx;
	}

	.nav-item.active .nav-icon {
		opacity: 1;
	}

	.nav-item:not(.active) .nav-icon {
		opacity: 0.85;
	}

	.nav-label {
		font-size: 22rpx;
		color: #737686;
		letter-spacing: 0.55rpx;
		line-height: 33rpx;
	}

	.nav-item.active .nav-label {
		color: #003da6;
	}
</style>
