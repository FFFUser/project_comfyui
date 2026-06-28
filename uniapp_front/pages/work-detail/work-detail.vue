<template>
	<view class="page">
		<view class="content" :style="{ height: contentHeight + 'px' }">
			<view class="hero">
				<swiper
					class="hero-swiper"
					:current="currentImage"
					:duration="300"
					@change="onImageChange"
				>
					<swiper-item v-for="(src, i) in work.gallery" :key="i">
						<image class="hero-image" :src="src" mode="aspectFill" />
					</swiper-item>
				</swiper>
			</view>
			<view class="detail-panel">
				<view class="dots">
					<view
						v-for="(_, i) in work.gallery"
						:key="i"
						class="dot"
						:class="{ active: i === currentImage }"
					/>
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
		</view>
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
				contentHeight: 500,
				currentImage: 0
			}
		},
		onLoad() {
			const sys = uni.getSystemInfoSync()
			this.statusBarHeight = sys.statusBarHeight || 20
			const footerH = Math.round(168 * sys.windowWidth / 750) + (sys.safeAreaInsets?.bottom || 0)
			this.contentHeight = sys.windowHeight - footerH
		},
		methods: {
			onBack() {
				uni.navigateBack({ fail: () => uni.reLaunch({ url: '/pages/home/home' }) })
			},
			onImageChange(e) {
				this.currentImage = e.detail.current
			}
		}
	}
</script>

<style scoped>
	.page { height: 100vh; overflow: hidden; background: #fff; display: flex; flex-direction: column; }
	.content { display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0; }
	.hero { flex: 1; min-height: 0; width: 100%; }
	.hero-swiper { width: 100%; height: 100%; }
	.hero-image { width: 100%; height: 100%; display: block; }
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
