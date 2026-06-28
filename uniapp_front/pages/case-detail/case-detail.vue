<template>
	<view class="page">
		<TopAppBar variant="detail" :title="navTitle || detail.title" />
		<scroll-view scroll-y class="scroll" :style="{ height: scrollHeight + 'px' }">
			<view class="trust-bar">
				<text v-for="(t, i) in trustItems" :key="i" class="trust-item">{{ t }}</text>
			</view>
			<view class="card summary">
				<text class="project-title">{{ detail.title }}</text>
				<view class="tag-row">
					<text v-for="tag in detail.tags" :key="tag" class="tag">{{ tag }}</text>
				</view>
			</view>
			<view class="card cost">
				<view class="cost-header">
					<view>
						<text class="cost-label">总造价</text>
						<text class="cost-total">¥{{ detail.totalCost }}</text>
					</view>
					<button class="btn-outline">明细</button>
				</view>
				<view class="cost-grid">
					<view class="cost-item">
						<text class="cost-num">{{ detail.construction }}</text>
						<text class="cost-desc">施工费用</text>
					</view>
					<view class="cost-item">
						<text class="cost-num">{{ detail.material }}</text>
						<text class="cost-desc">辅材费用</text>
					</view>
					<view class="cost-item">
						<text class="cost-num small">{{ detail.ownerBuy }}</text>
						<text class="cost-desc">主材及设备</text>
					</view>
				</view>
			</view>
			<view class="section">
				<view class="section-head">
					<text class="section-title">完工图集</text>
					<text class="section-more">全部 ›</text>
				</view>
				<view class="photo-grid">
					<view v-for="(src, i) in detail.gallery" :key="i" class="photo-cell">
						<image class="photo" :src="src" mode="aspectFill" />
					</view>
				</view>
			</view>
			<view class="section">
				<view class="section-head">
					<text class="section-title">施工照片</text>
					<text class="section-more">全部 ›</text>
				</view>
				<view class="photo-grid">
					<view v-for="(src, i) in detail.constructionPhotos" :key="i" class="photo-cell">
						<image class="photo" :src="src" mode="aspectFill" />
					</view>
				</view>
			</view>
			<view class="card team">
				<view class="section-head">
					<text class="section-title">施工团队</text>
					<text class="section-more">★ 4.9分</text>
				</view>
				<view class="team-grid">
					<view v-for="m in detail.team" :key="m.role" class="team-member">
						<image class="team-avatar-img" :src="m.avatar" mode="aspectFill" />
						<view>
							<text class="team-role">{{ m.role }}</text>
							<text class="team-name">{{ m.name }}</text>
						</view>
					</view>
				</view>
				<view class="team-avatars">
					<image
						v-for="(src, i) in detail.teamPhotos"
						:key="i"
						class="team-avatar"
						:src="src"
						mode="aspectFill"
					/>
				</view>
			</view>
			<view class="section dynamics">
				<view class="section-head">
					<text class="section-title">施工动态</text>
					<text class="section-more">全部 ›</text>
				</view>
				<scroll-view scroll-x class="dyn-tabs" :show-scrollbar="false">
					<view class="dyn-inner">
						<text
							v-for="(d, i) in detail.dynamics"
							:key="d"
							class="dyn-tab"
							:class="{ active: dynTab === i }"
							@click="dynTab = i"
						>{{ d }}</text>
					</view>
				</scroll-view>
				<view v-for="(feed, i) in filteredFeeds" :key="i" class="feed-item">
					<view class="feed-header">
						<image class="feed-avatar" :src="feed.avatar" mode="aspectFill" />
						<view>
							<view class="feed-name-row">
								<text class="feed-name">{{ feed.name }}</text>
								<text class="feed-badge">{{ feed.badge }}</text>
							</view>
							<text class="feed-time">{{ feed.time }}</text>
						</view>
					</view>
					<view class="feed-body">
						<text class="feed-title">{{ feed.title }}</text>
						<image class="feed-image" :src="feed.image" mode="aspectFill" />
					</view>
				</view>
			</view>
			<view style="height: 160rpx" />
		</scroll-view>
		<view class="bottom-bar">
			<button class="btn-secondary">在线咨询</button>
			<button class="btn-primary">我要装修</button>
		</view>
	</view>
</template>

<script>
	import TopAppBar from '../../components/qiju/TopAppBar.vue'
	import { CASE_DETAIL } from '../../mock/qiju-data.js'

	export default {
		components: { TopAppBar },
		data() {
			return {
				detail: CASE_DETAIL,
				navTitle: '',
				trustItems: ['真实案例', '透明报价', '质保5年', '平台担保'],
				dynTab: 0,
				scrollHeight: 500
			}
		},
		onLoad(options) {
			if (options.title) {
				this.navTitle = decodeURIComponent(options.title)
			}
		},
		onReady() {
			const sys = uni.getSystemInfoSync()
			this.scrollHeight = sys.windowHeight - (sys.statusBarHeight || 20) - 56 - 80
		},
		computed: {
			filteredFeeds() {
				const feeds = this.detail.feeds || []
				const tab = this.detail.dynamics[this.dynTab]
				if (!tab || tab === '全部') return feeds
				return feeds.filter(f => f.category === tab)
			}
		}
	}
</script>

<style scoped>
	.page {
		min-height: 100vh;
		background: #fdf9f2;
		overflow-x: hidden;
		width: 100%;
		box-sizing: border-box;
	}
	.scroll {
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
		padding: 0 32rpx;
	}
	.trust-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		flex-wrap: wrap;
		gap: 8rpx 16rpx;
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
		padding: 16rpx 24rpx;
		background: #fff;
		border-radius: 16rpx;
		margin: 16rpx 0;
		font-size: 22rpx;
		color: #434654;
	}
	.trust-item::before { content: '✓ '; color: #003da6; }
	.card {
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
		background: #fff;
		border-radius: 24rpx;
		padding: 32rpx;
		margin-bottom: 24rpx;
		overflow: hidden;
	}
	.project-title { font-size: 36rpx; font-weight: 700; color: #1c1c18; }
	.tag-row { display: flex; flex-wrap: wrap; gap: 16rpx; margin-top: 16rpx; }
	.tag {
		padding: 4rpx 16rpx;
		background: #f1ede6;
		border-radius: 8rpx;
		font-size: 22rpx;
		color: #434654;
	}
	.cost-header { display: flex; justify-content: space-between; align-items: flex-start; min-width: 0; gap: 16rpx; }
	.cost-label { font-size: 24rpx; color: #434654; }
	.cost-total { display: block; font-size: 48rpx; font-weight: 700; color: #832700; margin-top: 8rpx; }
	.btn-outline {
		flex-shrink: 0;
		margin: 0;
		height: 58rpx; line-height: 58rpx; padding: 0 24rpx;
		background: transparent; border: 1rpx solid #ece8e1;
		border-radius: 12rpx; font-size: 24rpx; color: #434654;
		box-sizing: border-box;
	}
	.btn-outline::after { border: none; }
	.cost-grid {
		display: flex;
		width: 100%;
		min-width: 0;
		border-top: 1rpx solid #ece8e1;
		margin-top: 24rpx;
		padding-top: 24rpx;
	}
	.cost-item { flex: 1; min-width: 0; text-align: center; }
	.cost-item:first-child { text-align: left; }
	.cost-item:last-child { text-align: right; }
	.cost-num { display: block; font-size: 28rpx; font-weight: 600; color: #1c1c18; }
	.cost-num.small { font-size: 24rpx; }
	.cost-desc { display: block; font-size: 22rpx; color: #434654; margin-top: 4rpx; }
	.section {
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
		margin-bottom: 24rpx;
	}
	.section-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
	.section-title { font-size: 30rpx; font-weight: 600; color: #1c1c18; }
	.section-more { font-size: 24rpx; color: #434654; }
	.photo-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 12rpx;
		width: 100%;
		min-width: 0;
	}
	.photo-cell { position: relative; padding-bottom: 100%; }
	.photo { position: absolute; inset: 0; border-radius: 12rpx; width: 100%; height: 100%; }
	.team-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 24rpx;
		margin-top: 16rpx;
		width: 100%;
		min-width: 0;
	}
	.team-member { display: flex; gap: 16rpx; align-items: center; min-width: 0; }
	.team-avatar-img {
		width: 56rpx;
		height: 56rpx;
		border-radius: 50%;
		flex-shrink: 0;
		display: block;
		background: #f1ede6;
	}
	.team-role { display: block; font-size: 26rpx; font-weight: 600; color: #1c1c18; }
	.team-name { font-size: 22rpx; color: #434654; }
	.team-avatars { display: flex; gap: 24rpx; margin-top: 24rpx; }
	.team-avatar {
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
		flex-shrink: 0;
		display: block;
		background: #d4cfc7;
	}
	.dyn-tabs { white-space: nowrap; margin-bottom: 16rpx; }
	.dyn-inner { display: inline-flex; gap: 16rpx; }
	.dyn-tab {
		display: inline-block; padding: 8rpx 24rpx;
		background: #f1ede6; border-radius: 8rpx; font-size: 24rpx; color: #434654;
	}
	.dyn-tab.active { background: #003da6; color: #fff; }
	.feed-item {
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
		background: #fff;
		border-radius: 24rpx;
		padding: 24rpx;
		overflow: hidden;
		margin-bottom: 16rpx;
	}
	.feed-item:last-child { margin-bottom: 0; }
	.feed-header { display: flex; gap: 16rpx; }
	.feed-avatar {
		width: 64rpx;
		height: 64rpx;
		border-radius: 50%;
		flex-shrink: 0;
		display: block;
		background: #c8d4e0;
	}
	.feed-name-row { display: flex; align-items: center; gap: 12rpx; }
	.feed-name { font-size: 28rpx; font-weight: 600; color: #1c1c18; }
	.feed-badge { padding: 2rpx 12rpx; background: #f1ede6; border-radius: 4rpx; font-size: 20rpx; color: #434654; }
	.feed-time { font-size: 22rpx; color: #969799; }
	.feed-body { margin-top: 16rpx; }
	.feed-title { font-size: 28rpx; color: #1c1c18; }
	.feed-image {
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
		height: 360rpx;
		border-radius: 16rpx;
		margin-top: 16rpx;
		display: block;
		background: #d0d8c8;
	}
	.bottom-bar {
		position: fixed; left: 0; right: 0; bottom: 0;
		display: grid; grid-template-columns: 1fr 1fr; gap: 24rpx;
		width: 100%;
		box-sizing: border-box;
		padding: 18rpx 48rpx 48rpx 48rpx;
		background: rgba(253, 249, 242, 0.9);
		backdrop-filter: blur(24rpx);
		border-top: 1rpx solid rgba(230, 226, 219, 0.1);
		border-radius: 32rpx 32rpx 0 0;
		padding-bottom: calc(48rpx + env(safe-area-inset-bottom));
		box-shadow: 0 -50rpx 100rpx -24rpx rgba(0, 0, 0, 0.25);
	}
	.btn-secondary,
	.btn-primary {
		margin: 0;
		width: 100%;
		box-sizing: border-box;
		height: 88rpx;
		line-height: 88rpx;
		border-radius: 24rpx;
		font-size: 24rpx;
		font-weight: 600;
		border: 1rpx solid transparent;
	}
	.btn-secondary::after,
	.btn-primary::after { border: none; }
	.btn-secondary {
		background: #fff;
		color: #003da6;
		border-color: #003da6;
	}
	.btn-primary {
		background: #003da6;
		color: #fff;
		border-color: #003da6;
		box-shadow: 0 20rpx 30rpx -6rpx rgba(0, 0, 0, 0.1);
	}
</style>
