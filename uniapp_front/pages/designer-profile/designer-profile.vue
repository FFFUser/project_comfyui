<template>
	<view class="page">
		<view class="hero" :style="{ paddingTop: statusBarHeight + 'px' }">
			<image class="hero-bg-img" :src="profile.hero" mode="aspectFill" />
			<view class="hero-bg" />
			<view class="hero-gradient" />
			<view class="nav-bar" :style="{ height: barInnerHeight + 'px' }">
				<view class="back-btn" @click="onBack">
					<text class="back-icon">‹</text>
				</view>
			</view>
			<view class="hero-content">
				<view class="avatar-row">
					<image class="avatar" :src="profile.avatar" mode="aspectFill" />
					<view class="basic-info">
						<text class="studio-name">{{ profile.name }}</text>
						<text class="specialty">{{ profile.specialty }}</text>
					</view>
				</view>
				<view class="desc-block">
					<text class="desc-line">{{ profile.location }}</text>
					<text class="desc-line">{{ profile.cert }}</text>
					<text class="desc-line">{{ profile.awards }}</text>
					<view class="tag-row">
						<text v-for="tag in profile.tags" :key="tag" class="tag">{{ tag }}</text>
					</view>
				</view>
				<button class="btn-follow">关注设计师</button>
			</view>
		</view>
		<scroll-view scroll-y class="content" :style="{ height: scrollHeight + 'px' }">
			<view class="works-tab">
				<text class="works-tab-active">作品</text>
			</view>
			<view class="works-grid">
				<view
					v-for="(work, i) in profile.works"
					:key="i"
					class="work-card"
					@click="goWorkDetail"
				>
					<image v-if="work.cover" class="work-cover" :src="work.cover" mode="aspectFill" />
					<view v-else class="work-cover" :style="{ background: workColors[i % 4], height: workHeights[i % 4] }" />
					<view class="work-info">
						<text class="work-title">{{ work.title }}</text>
						<view class="work-meta">
							<text class="work-author">张馨予</text>
							<text class="work-likes">♥ {{ work.likes }}</text>
						</view>
					</view>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	import { DESIGNER_PROFILE } from '../../mock/qiju-data.js'

	export default {
		data() {
			return {
				profile: DESIGNER_PROFILE,
				statusBarHeight: 20,
				barInnerHeight: 56,
				scrollHeight: 500,
				workColors: ['#c8d4e0', '#d0d8c8', '#e0d0c8', '#d4cfc7'],
				workHeights: ['460rpx', '460rpx', '430rpx', '346rpx']
			}
		},
		onLoad() {
			const sys = uni.getSystemInfoSync()
			this.statusBarHeight = sys.statusBarHeight || 20
			this.barInnerHeight = Math.round(112 * sys.windowWidth / 750)

			// #ifdef MP-WEIXIN
			const menuButton = uni.getMenuButtonBoundingClientRect()
			if (menuButton && menuButton.height) {
				this.barInnerHeight = (menuButton.top - this.statusBarHeight) * 2 + menuButton.height
			}
			// #endif

			this.scrollHeight = sys.windowHeight - 460 + 48
		},
		methods: {
			onBack() {
				uni.navigateBack({ fail: () => uni.reLaunch({ url: '/pages/designers/designers' }) })
			},
			goWorkDetail() {
				uni.navigateTo({ url: '/pages/work-detail/work-detail' })
			}
		}
	}
</script>

<style scoped>
	.page { min-height: 100vh; background: #f5f3ef; }
	.hero { position: relative; height: 920rpx; overflow: hidden; }
	.hero-bg-img { position: absolute; inset: 0; width: 100%; height: 100%; }
	.hero-bg { position: absolute; inset: 0; background: rgba(0,0,0,0.25); }
	.hero-gradient {
		position: absolute; inset: 0;
		background: linear-gradient(180deg, transparent 30%, rgba(0,0,0,0.7));
	}
	.nav-bar {
		position: relative;
		z-index: 2;
		display: flex;
		align-items: center;
		box-sizing: border-box;
		padding: 0 48rpx;
	}
	.back-btn {
		width: 80rpx;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.back-icon {
		font-size: 56rpx;
		color: #fff;
		line-height: 1;
		font-weight: 300;
	}
	.hero-content { position: relative; z-index: 2; padding: 48rpx; margin-top: 80rpx; }
	.avatar-row { display: flex; gap: 32rpx; }
	.avatar {
		width: 192rpx; height: 192rpx; border-radius: 50%;
		border: 4rpx solid rgba(255,255,255,0.3); flex-shrink: 0;
		display: block;
	}
	.basic-info { flex: 1; padding-top: 16rpx; }
	.studio-name { display: block; font-size: 36rpx; font-weight: 700; color: #fff; line-height: 1.4; }
	.specialty { display: block; font-size: 26rpx; color: rgba(255,255,255,0.8); margin-top: 8rpx; }
	.desc-block { margin-top: 32rpx; }
	.desc-line { display: block; font-size: 26rpx; color: rgba(255,255,255,0.85); line-height: 1.6; }
	.tag-row { display: flex; flex-wrap: wrap; gap: 16rpx; margin-top: 16rpx; }
	.tag {
		padding: 8rpx 24rpx; background: rgba(255,255,255,0.15);
		border-radius: 8rpx; font-size: 24rpx; color: #fff;
	}
	.btn-follow {
		width: 100%; height: 88rpx; line-height: 88rpx; margin-top: 32rpx;
		background: #003da6; color: #fff; border-radius: 16rpx; font-size: 28rpx; border: none;
	}
	.content {
		margin-top: -48rpx; position: relative; z-index: 3;
		background: #f5f3ef; border-radius: 32rpx 32rpx 0 0; padding: 32rpx;
	}
	.works-tab { padding: 16rpx 0 32rpx; }
	.works-tab-active {
		font-size: 32rpx; font-weight: 700; color: #003da6;
		border-bottom: 4rpx solid #003da6; padding-bottom: 8rpx;
	}
	.works-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24rpx; }
	.work-card { background: #fff; border-radius: 24rpx; overflow: hidden; }
	.work-cover { width: 100%; height: 430rpx; display: block; }
	.work-info { padding: 24rpx; }
	.work-title { font-size: 26rpx; font-weight: 600; color: #1c1c18; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
	.work-meta { display: flex; justify-content: space-between; margin-top: 12rpx; font-size: 22rpx; color: #434654; }
</style>
