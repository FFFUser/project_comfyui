<template>
	<view class="page">
		<TopAppBar variant="home" />
		<scroll-view scroll-x enhanced :show-scrollbar="false" class="sub-tabs">
			<view class="sub-inner">
				<text
					v-for="(tab, i) in tabs"
					:key="tab"
					class="sub-tab"
					:class="{ active: activeTab === i }"
					@click="activeTab = i"
				>{{ tab }}</text>
			</view>
		</scroll-view>
		<scroll-view
			scroll-y
			enhanced
			:show-scrollbar="false"
			:bounces="false"
			:lower-threshold="80"
			:scroll-top="scrollTop"
			class="list"
			:style="{ height: scrollHeight + 'px' }"
			@scroll="onListScroll"
			@scrolltolower="onScrollToLower"
		>
			<view class="list-inner">
				<WorkerCard
					v-for="(w, i) in displayWorkers"
					:key="w.id"
					:worker="w"
					:index="i"
					@contact="onContact(w)"
					@favorite="onFavorite(w)"
				/>
				<view v-if="showListFooter" class="list-footer">
					<text class="list-footer-text">没有更多工人了~</text>
				</view>
			</view>
		</scroll-view>
		<BottomNavBar current="workers" />
	</view>
</template>

<script>
	import TopAppBar from '../../components/qiju/TopAppBar.vue'
	import BottomNavBar from '../../components/qiju/BottomNavBar.vue'
	import WorkerCard from '../../components/qiju/WorkerCard.vue'
	import { getScrollHeightPx } from '../../utils/page-layout.js'
	import { WORKER_TABS, WORKERS } from '../../mock/qiju-data.js'

	export default {
		components: { TopAppBar, BottomNavBar, WorkerCard },
		data() {
			return {
				tabs: WORKER_TABS,
				allWorkers: WORKERS,
				activeTab: 0,
				scrollHeight: 500,
				showNoMore: false,
				scrollTop: 0,
				scrollTopCache: 0
			}
		},
		computed: {
			displayWorkers() {
				if (this.activeTab === 0) return this.allWorkers
				const category = this.tabs[this.activeTab]
				return this.allWorkers.filter(w => w.category === category)
			},
			showListFooter() {
				if (!this.displayWorkers.length) return true
				return this.showNoMore
			}
		},
		watch: {
			activeTab() {
				this.showNoMore = false
				this.scrollTop = this.scrollTopCache
				this.$nextTick(() => {
					this.scrollTop = 0
				})
			}
		},
		onReady() {
			const sys = uni.getSystemInfoSync()
			const subTabsHeight = Math.round(80 * sys.windowWidth / 750)
			this.scrollHeight = getScrollHeightPx(sys, subTabsHeight)
		},
		methods: {
			onListScroll(e) {
				this.scrollTopCache = e.detail.scrollTop
			},
			onScrollToLower() {
				if (this.displayWorkers.length) {
					this.showNoMore = true
				}
			},
			onContact(w) {
				uni.showToast({ title: '联系 ' + w.name, icon: 'none' })
			},
			onFavorite(w) {
				uni.showToast({ title: '已收藏 ' + w.name, icon: 'none' })
			}
		}
	}
</script>

<style scoped>
	.page {
		height: 100vh;
		overflow: hidden;
		background: #fdf9f2;
	}
	.sub-tabs { white-space: nowrap; padding: 16rpx 0; background: #fdf9f2; }
	.sub-inner { display: inline-flex; gap: 48rpx; padding: 0 48rpx; }
	.sub-tab {
		font-size: 30rpx; color: #434654; position: relative; padding-bottom: 8rpx;
	}
	.sub-tab.active { color: #003da6; font-weight: 700; }
	.sub-tab.active::after {
		content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
		width: 32rpx; height: 6rpx; background: #003da6; border-radius: 3rpx;
	}
	.list {
		box-sizing: border-box;
	}
	/* #ifdef H5 */
	.list {
		scrollbar-width: none;
		-ms-overflow-style: none;
	}
	.list::-webkit-scrollbar {
		display: none;
		width: 0;
		height: 0;
	}
	/* #endif */
	.list-inner {
		padding: 8rpx 32rpx 16rpx;
		box-sizing: border-box;
	}
	.list-footer {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 32rpx 0 48rpx;
	}
	.list-footer-text {
		font-size: 24rpx;
		color: #969799;
	}
</style>
