<template>
	<view class="page">
		<view class="hero" :style="heroStyle">
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
				<button class="btn-follow" @click="onBook">咨询预约</button>
			</view>
		</view>
		<view class="content-panel" :style="contentPanelStyle">
			<view class="works-tab">
				<text class="works-tab-active">作品</text>
			</view>
			<scroll-view scroll-y class="works-scroll" :bounces="false" :style="{ height: scrollHeight + 'px' }">
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
								<text class="work-author">{{ profile.name }}</text>
								<text class="work-likes">♥ {{ work.likes }}</text>
							</view>
						</view>
					</view>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script>
	import { DESIGNER_PROFILE, DESIGNERS } from '../../mock/qiju-data.js'

	export default {
		data() {
			return {
				profile: { ...DESIGNER_PROFILE },
				statusBarHeight: 20,
				barInnerHeight: 56,
				heroHeightPx: 460,
				contentTopPx: 280,
				panelHeightPx: 500,
				scrollHeight: 500,
				workColors: ['#c8d4e0', '#d0d8c8', '#e0d0c8', '#d4cfc7'],
				workHeights: ['300rpx', '300rpx', '280rpx', '240rpx']
			}
		},
		computed: {
			heroStyle() {
				return {
					paddingTop: this.statusBarHeight + 'px',
					height: this.heroHeightPx + 'px'
				}
			},
			contentPanelStyle() {
				return {
					top: this.contentTopPx + 'px',
					height: this.panelHeightPx + 'px'
				}
			}
		},
		onLoad(options) {
			const sys = uni.getSystemInfoSync()
			this.statusBarHeight = sys.statusBarHeight || 20
			this.barInnerHeight = Math.round(112 * sys.windowWidth / 750)

			// #ifdef MP-WEIXIN
			const menuButton = uni.getMenuButtonBoundingClientRect()
			if (menuButton && menuButton.height) {
				this.barInnerHeight = (menuButton.top - this.statusBarHeight) * 2 + menuButton.height
			}
			// #endif

			this.applyDesignerFromList(options)
			this.updateLayout(sys)
		},
		methods: {
			updateLayout(sys) {
				const heroHeightRpx = 920
				const overlapRpx = 180
				const extraOverlapPx = -20
				const worksTabHeightRpx = 72

				this.heroHeightPx = Math.round(heroHeightRpx * sys.windowWidth / 750)
				const overlapPx = Math.round(overlapRpx * sys.windowWidth / 750) + extraOverlapPx
				this.contentTopPx = this.heroHeightPx - overlapPx
				this.panelHeightPx = sys.windowHeight - this.contentTopPx
				const worksTabHeightPx = Math.round(worksTabHeightRpx * sys.windowWidth / 750)
				this.scrollHeight = this.panelHeightPx - worksTabHeightPx
			},
			applyDesignerFromList(options) {
				const id = Number(options.id)
				const designer = DESIGNERS.find(d => d.id === id)
				if (!designer) return

				this.profile = {
					...DESIGNER_PROFILE,
					name: designer.name,
					avatar: designer.avatar,
					hero: designer.cover,
					tags: designer.tags,
					location: `坐标${designer.location}`,
					specialty: `擅长：${designer.category}${designer.tags[0] ? ' / ' + designer.tags[0] : ''}`
				}
			},
			onBook() {
				uni.showToast({ title: '预约 ' + this.profile.name, icon: 'none' })
			},
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
	.page {
		height: 100vh;
		overflow: hidden;
		background: #f5f3ef;
		position: relative;
	}
	.hero {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 1;
		overflow: hidden;
		box-sizing: border-box;
	}
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
		position: relative;
		width: 64rpx;
		height: 64rpx;
		background: rgba(255, 255, 255, 0.2);
		border-radius: 50%;
		flex-shrink: 0;
	}
	.back-icon {
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-54%, -52%);
		font-size: 44rpx;
		color: #fff;
		line-height: 1;
		font-weight: 300;
	}
	.hero-content { position: relative; z-index: 2; padding: 24rpx 48rpx 24rpx; margin-top: 8rpx; }
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
		width: 100%; height: 88rpx; line-height: 88rpx; margin-top: 32rpx; margin-bottom: 0;
		background: #003da6; color: #fff; border-radius: 16rpx; font-size: 28rpx; border: none;
	}
	.content-panel {
		position: fixed;
		left: 0;
		right: 0;
		z-index: 3;
		background: #f5f3ef;
		border-radius: 32rpx 32rpx 0 0;
		padding: 8rpx 32rpx 0;
		box-sizing: border-box;
		overflow: hidden;
	}
	.works-scroll {
		width: 100%;
		box-sizing: border-box;
	}
	.works-tab { padding: 4rpx 0 16rpx; flex-shrink: 0; }
	.works-tab-active {
		font-size: 32rpx; font-weight: 700; color: #003da6;
		border-bottom: 4rpx solid #003da6; padding-bottom: 8rpx;
	}
	.works-grid {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: 20rpx 0;
		width: 100%;
		box-sizing: border-box;
		padding-bottom: 32rpx;
	}
	.work-card {
		width: 48%;
		background: #fff;
		border-radius: 20rpx;
		overflow: hidden;
		box-sizing: border-box;
	}
	.work-cover { width: 100%; height: 300rpx; display: block; }
	.work-info { padding: 16rpx; box-sizing: border-box; }
	.work-title {
		font-size: 24rpx; font-weight: 600; color: #1c1c18; line-height: 1.4;
		display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
		word-break: break-all;
	}
	.work-meta {
		display: flex; justify-content: space-between; align-items: center;
		margin-top: 8rpx; font-size: 20rpx; color: #434654; gap: 8rpx;
	}
	.work-author {
		flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
	}
	.work-likes { flex-shrink: 0; }
</style>
