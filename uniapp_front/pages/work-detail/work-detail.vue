<template>
	<view class="page">
		<scroll-view scroll-y class="scroll" :style="{ height: scrollHeight + 'px' }">
			<view class="hero">
				<image class="hero-image" :src="work.hero" mode="widthFix" />
			</view>
			<view class="detail-panel">
				<view class="dots">
					<view v-for="n in 5" :key="n" class="dot" :class="{ active: n === 2 }" />
				</view>
				<text class="title">{{ work.title }}</text>
				<text class="desc">{{ work.desc }}</text>
				<view class="location-row">
					<text class="loc-icon">📍</text>
					<text class="loc-text">{{ work.location }}</text>
				</view>
				<view class="hash-tags">
					<text v-for="tag in work.tags" :key="tag" class="hash-tag">{{ tag }}</text>
				</view>
				<text class="publish">{{ work.publishTime }}</text>
			</view>
		</scroll-view>
		<view class="top-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
			<view class="nav-inner">
				<view class="back-btn" @click="onBack"><text>‹</text></view>
				<view class="author-row">
					<image class="author-avatar" :src="work.authorAvatar" mode="aspectFill" />
					<text class="author-name">{{ work.author }}</text>
				</view>
			</view>
		</view>
		<view class="footer-cta">
			<button class="btn-detail">查看详情</button>
		</view>
	</view>
</template>

<script>
	import { WORK_DETAIL } from '../../mock/qiju-data.js'

	export default {
		data() {
			return {
				work: WORK_DETAIL,
				statusBarHeight: 20,
				scrollHeight: 500
			}
		},
		onLoad() {
			const sys = uni.getSystemInfoSync()
			this.statusBarHeight = sys.statusBarHeight || 20
			this.scrollHeight = sys.windowHeight - 85
		},
		methods: {
			onBack() {
				uni.navigateBack({ fail: () => uni.reLaunch({ url: '/pages/home/home' }) })
			}
		}
	}
</script>

<style scoped>
	.page { min-height: 100vh; background: #fff; }
	.scroll { padding-bottom: 170rpx; }
	.hero { width: 100%; }
	.hero-image { width: 100%; display: block; }
	.detail-panel { padding: 48rpx 40rpx; background: #fff; border-radius: 32rpx 32rpx 0 0; margin-top: -32rpx; position: relative; }
	.dots { display: flex; justify-content: center; gap: 8rpx; margin-bottom: 32rpx; }
	.dot { width: 12rpx; height: 12rpx; background: #ece8e1; border-radius: 50%; }
	.dot.active { width: 24rpx; border-radius: 6rpx; background: #003da6; }
	.title { display: block; font-size: 36rpx; font-weight: 700; color: #1c1c18; line-height: 1.5; }
	.desc { display: block; margin-top: 32rpx; font-size: 28rpx; color: #434654; line-height: 1.7; }
	.location-row { display: flex; align-items: center; gap: 8rpx; margin-top: 24rpx; }
	.loc-text { font-size: 28rpx; color: #434654; }
	.hash-tags { display: flex; flex-wrap: wrap; gap: 16rpx; margin-top: 24rpx; }
	.hash-tag { font-size: 26rpx; color: #003da6; }
	.publish { display: block; margin-top: 48rpx; font-size: 24rpx; color: #969799; }
	.top-nav {
		position: fixed; top: 0; left: 0; right: 0; z-index: 99;
		background: linear-gradient(180deg, rgba(0,0,0,0.4), transparent);
	}
	.nav-inner {
		display: flex; align-items: center; gap: 16rpx;
		padding: 16rpx 32rpx; height: 88rpx;
	}
	.back-btn {
		width: 64rpx; height: 64rpx; background: rgba(255,255,255,0.2);
		border-radius: 50%; display: flex; align-items: center; justify-content: center;
		font-size: 44rpx; color: #fff;
	}
	.author-row { display: flex; align-items: center; gap: 16rpx; }
	.author-avatar { width: 56rpx; height: 56rpx; border-radius: 50%; display: block; }
	.author-name { font-size: 28rpx; color: #fff; font-weight: 600; }
	.footer-cta {
		position: fixed; left: 0; right: 0; bottom: 0;
		padding: 32rpx; background: #fff;
		border-top: 1rpx solid #ece8e1;
		padding-bottom: calc(32rpx + env(safe-area-inset-bottom));
	}
	.btn-detail {
		width: 100%; height: 104rpx; line-height: 104rpx;
		background: #003da6; color: #fff; border-radius: 16rpx;
		font-size: 32rpx; font-weight: 600; border: none;
		box-shadow: 0 8rpx 24rpx rgba(0,61,166,0.25);
	}
</style>
