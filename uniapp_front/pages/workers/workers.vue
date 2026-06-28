<template>
	<view class="page">
		<TopAppBar variant="home" />
		<scroll-view scroll-x class="sub-tabs" :show-scrollbar="false">
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
		<scroll-view scroll-y class="list" :bounces="false" :style="{ height: scrollHeight + 'px' }">
			<WorkerCard
				v-for="(w, i) in workers"
				:key="w.id"
				:worker="w"
				:index="i"
				@contact="onContact(w)"
				@favorite="onFavorite(w)"
			/>
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
				workers: WORKERS,
				activeTab: 0,
				scrollHeight: 500
			}
		},
		onReady() {
			const sys = uni.getSystemInfoSync()
			const subTabsHeight = Math.round(80 * sys.windowWidth / 750)
			this.scrollHeight = getScrollHeightPx(sys, subTabsHeight)
		},
		methods: {
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
	.list { padding: 16rpx 48rpx; }
</style>
