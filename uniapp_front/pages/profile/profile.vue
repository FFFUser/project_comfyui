<template>
	<view class="page">
		<TopAppBar variant="profile" />
		<scroll-view scroll-y class="main" :bounces="false" :style="{ height: scrollHeight + 'px', width: '100%' }">
			<view class="main-inner">
			<view class="profile-header">
				<view class="avatar-wrap">
					<image class="avatar" :src="profileAvatar" mode="aspectFill" />
					<view class="edit-btn">
						<image class="edit-icon" :src="icons.profileEdit" mode="aspectFit" />
					</view>
				</view>
				<view class="profile-info">
					<text class="nickname">林 栖居</text>
					<text class="bio">寻找生活中的建筑美学</text>
				</view>
				<view class="list-arrow" />
			</view>
			<view class="quick-links">
				<view v-for="link in quickLinks" :key="link.label" class="quick-item">
					<view class="quick-icon-wrap" :class="link.bgClass">
						<image class="quick-icon" :src="link.icon" mode="aspectFit" />
					</view>
					<text class="quick-label">{{ link.label }}</text>
				</view>
			</view>
			<view class="menu-list">
				<view v-for="menu in menus" :key="menu.label" class="menu-item">
					<view class="menu-left">
						<view class="menu-icon-wrap">
							<image class="menu-icon" :src="menu.icon" mode="aspectFit" />
						</view>
						<text class="menu-label">{{ menu.label }}</text>
					</view>
					<view class="list-arrow" />
				</view>
			</view>
			<view class="cta-banner">
				<image class="cta-bg" :src="ctaBannerBg" mode="aspectFill" />
				<view class="cta-overlay" />
				<view class="cta-content">
					<text class="cta-title">发现更多家居灵感</text>
					<text class="cta-sub">定制您的专属生活空间</text>
					<button class="cta-btn">立即探索</button>
				</view>
			</view>
			<view class="scroll-spacer" />
			</view>
		</scroll-view>
		<BottomNavBar current="profile" />
	</view>
</template>

<script>
	import TopAppBar from '../../components/qiju/TopAppBar.vue'
	import BottomNavBar from '../../components/qiju/BottomNavBar.vue'
	import { getScrollHeightPx } from '../../utils/page-layout.js'
	import { PROFILE_QUICK_LINKS, PROFILE_MENUS, ASSETS, ICONS } from '../../mock/qiju-data.js'

	export default {
		components: { TopAppBar, BottomNavBar },
		data() {
			return {
				quickLinks: PROFILE_QUICK_LINKS,
				menus: PROFILE_MENUS,
				profileAvatar: ASSETS.profile.avatar,
				ctaBannerBg: ASSETS.profile.ctaBanner,
				icons: ICONS,
				scrollHeight: 500
			}
		},
		onReady() {
			const sys = uni.getSystemInfoSync()
			this.scrollHeight = getScrollHeightPx(sys)
		}
	}
</script>

<style scoped>
	.page {
		height: 100vh;
		overflow: hidden;
		background: #fdf9f2;
	}

	.main {
		box-sizing: border-box;
		width: 100%;
	}

	.main-inner {
		box-sizing: border-box;
		padding: 32rpx 48rpx 0;
	}

	.scroll-spacer {
		height: 64rpx;
	}

	.profile-header {
		display: flex;
		align-items: center;
		gap: 32rpx;
		padding: 32rpx 32rpx 32rpx 0;
	}

	.avatar-wrap {
		position: relative;
		flex-shrink: 0;
	}

	.avatar {
		width: 160rpx;
		height: 160rpx;
		border-radius: 50%;
		border: 4rpx solid #fff;
		box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.05);
		display: block;
	}

	.edit-btn {
		position: absolute;
		right: -6rpx;
		bottom: -6rpx;
		width: 48rpx;
		height: 48rpx;
		background: #003da6;
		border-radius: 50%;
		border: 4rpx solid #fdf9f2;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.edit-icon {
		width: 24rpx;
		height: 24rpx;
	}

	.profile-info {
		flex: 1;
		min-width: 0;
	}

	.nickname {
		font-size: 48rpx;
		font-weight: 500;
		color: #1c1c18;
		letter-spacing: -1.2rpx;
		line-height: 64rpx;
	}

	.bio {
		display: block;
		margin-top: 20rpx;
		font-size: 28rpx;
		color: #434654;
		line-height: 40rpx;
	}

	.list-arrow {
		width: 14rpx;
		height: 14rpx;
		flex-shrink: 0;
		margin-left: 16rpx;
		border-top: 3rpx solid #737686;
		border-right: 3rpx solid #737686;
		transform: rotate(45deg);
		box-sizing: border-box;
	}

	.quick-links {
		display: flex;
		gap: 32rpx;
		margin-bottom: 64rpx;
	}

	.quick-item {
		flex: 1;
		background: #fff;
		border-radius: 24rpx;
		padding: 40rpx 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 16rpx;
	}

	.quick-icon-wrap {
		width: 96rpx;
		height: 96rpx;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.quick-icon-wrap.blue {
		background: #dbe1ff;
	}

	.quick-icon-wrap.orange {
		background: #ffdbd0;
	}

	.quick-icon {
		width: 40rpx;
		height: 40rpx;
	}

	.quick-label {
		font-size: 28rpx;
		color: #1c1c18;
	}

	.menu-list {
		box-sizing: border-box;
		width: 100%;
		background: #fff;
		border-radius: 24rpx;
		overflow: hidden;
		margin-bottom: 64rpx;
	}

	.menu-item {
		box-sizing: border-box;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 32rpx;
	}

	.menu-left {
		flex: 1;
		min-width: 0;
		display: flex;
		align-items: center;
		gap: 24rpx;
	}

	.menu-icon-wrap {
		width: 80rpx;
		height: 80rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.menu-icon {
		width: 40rpx;
		height: 40rpx;
		display: block;
		flex-shrink: 0;
	}

	.menu-label {
		font-size: 32rpx;
		color: #1c1c18;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.cta-banner {
		position: relative;
		border-radius: 24rpx;
		overflow: hidden;
		min-height: 280rpx;
	}

	.cta-bg {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
	}

	.cta-overlay {
		position: absolute;
		inset: 0;
		background: linear-gradient(
			90deg,
			rgba(28, 28, 24, 0.82) 0%,
			rgba(28, 28, 24, 0.68) 40%,
			rgba(28, 28, 24, 0.35) 70%,
			rgba(28, 28, 24, 0.12) 100%
		);
	}

	.cta-content {
		position: relative;
		z-index: 1;
		padding: 48rpx;
	}

	.cta-title {
		display: block;
		font-size: 36rpx;
		font-weight: 500;
		color: #fff;
		line-height: 56rpx;
	}

	.cta-sub {
		display: block;
		font-size: 28rpx;
		color: rgba(255, 255, 255, 0.78);
		margin-top: 8rpx;
		padding-bottom: 24rpx;
		line-height: 40rpx;
	}

	.cta-btn {
		height: 80rpx;
		line-height: 80rpx;
		padding: 0 48rpx;
		background: #003da6;
		color: #fff;
		border-radius: 16rpx;
		font-size: 28rpx;
		border: none;
		display: inline-block;
		width: auto;
		box-shadow: 0 8rpx 12rpx -2rpx rgba(0, 0, 0, 0.1);
	}
</style>
