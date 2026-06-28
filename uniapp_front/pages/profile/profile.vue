<template>
	<view class="page">
		<TopAppBar variant="profile" />
		<scroll-view scroll-y class="main" :bounces="false" :style="{ height: scrollHeight + 'px' }">
			<view class="profile-header">
				<view class="avatar-wrap">
					<image class="avatar" :src="profileAvatar" mode="aspectFill" />
					<view class="edit-btn">
						<image class="edit-icon" :src="icons.profileEdit" mode="aspectFit" />
					</view>
				</view>
				<view class="profile-info">
					<text class="nickname">林 栖居</text>
					<view class="level-badge">
						<image class="crown-icon" :src="icons.profileCrown" mode="aspectFit" />
						<text class="level-text">尊享会员</text>
					</view>
					<text class="bio">寻找生活中的建筑美学</text>
				</view>
				<image class="arrow" :src="icons.chevronRight" mode="aspectFit" />
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
					<image class="menu-arrow" :src="icons.chevronRight" mode="aspectFit" />
				</view>
			</view>
			<view class="cta-banner">
				<view class="cta-content">
					<text class="cta-title">发现更多家居灵感</text>
					<text class="cta-sub">定制您的专属生活空间</text>
					<button class="cta-btn">立即探索</button>
				</view>
				<image class="cta-deco" :src="icons.ctaDeco" mode="aspectFit" />
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
		padding: 32rpx 48rpx 0;
	}

	.profile-header {
		display: flex;
		align-items: center;
		gap: 48rpx;
		padding: 32rpx 0;
	}

	.avatar-wrap {
		position: relative;
		flex-shrink: 0;
	}

	.avatar {
		width: 192rpx;
		height: 192rpx;
		border-radius: 50%;
		border: 4rpx solid #fff;
		box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.05);
		display: block;
	}

	.edit-btn {
		position: absolute;
		right: -8rpx;
		bottom: -8rpx;
		width: 56rpx;
		height: 56rpx;
		background: #003da6;
		border-radius: 50%;
		border: 4rpx solid #fdf9f2;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.edit-icon {
		width: 29rpx;
		height: 28rpx;
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

	.level-badge {
		display: inline-flex;
		align-items: center;
		gap: 12rpx;
		margin-top: 8rpx;
		padding: 4rpx 24rpx;
		background: #ffdbd0;
		border-radius: 999rpx;
	}

	.crown-icon {
		width: 19rpx;
		height: 25rpx;
	}

	.level-text {
		font-size: 24rpx;
		color: #832700;
		letter-spacing: 1.2rpx;
		text-transform: uppercase;
	}

	.bio {
		display: block;
		margin-top: 14rpx;
		font-size: 28rpx;
		color: #434654;
		line-height: 40rpx;
	}

	.arrow {
		width: 15rpx;
		height: 24rpx;
		flex-shrink: 0;
		padding: 16rpx;
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
		background: #fff;
		border-radius: 24rpx;
		overflow: hidden;
		margin-bottom: 64rpx;
	}

	.menu-item {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 40rpx;
	}

	.menu-left {
		display: flex;
		align-items: center;
		gap: 32rpx;
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
	}

	.menu-label {
		font-size: 32rpx;
		color: #1c1c18;
	}

	.menu-arrow {
		width: 15rpx;
		height: 24rpx;
	}

	.cta-banner {
		position: relative;
		background: #ece8e1;
		border-radius: 24rpx;
		padding: 48rpx;
		overflow: hidden;
		margin-bottom: 32rpx;
	}

	.cta-title {
		display: block;
		font-size: 36rpx;
		font-weight: 500;
		color: #1c1c18;
		line-height: 56rpx;
	}

	.cta-sub {
		display: block;
		font-size: 28rpx;
		color: #434654;
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

	.cta-deco {
		position: absolute;
		right: -32rpx;
		top: 50%;
		transform: translateY(-50%);
		width: 160rpx;
		height: 160rpx;
		opacity: 0.2;
	}
</style>
