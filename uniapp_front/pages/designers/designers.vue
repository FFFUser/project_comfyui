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
			<DesignerCard
				v-for="(d, i) in designers"
				:key="d.id"
				:designer="d"
				:index="i"
				@click="goProfile(d)"
				@book="onBook(d)"
			/>
		</scroll-view>
		<BottomNavBar current="designers" />
	</view>
</template>

<script>
	import TopAppBar from '../../components/qiju/TopAppBar.vue'
	import BottomNavBar from '../../components/qiju/BottomNavBar.vue'
	import DesignerCard from '../../components/qiju/DesignerCard.vue'
	import { getScrollHeightPx } from '../../utils/page-layout.js'
	import { DESIGNER_TABS, DESIGNERS } from '../../mock/qiju-data.js'

	export default {
		components: { TopAppBar, BottomNavBar, DesignerCard },
		data() {
			return {
				tabs: DESIGNER_TABS,
				designers: DESIGNERS,
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
			goProfile(d) {
				uni.navigateTo({ url: '/pages/designer-profile/designer-profile?id=' + d.id })
			},
			onBook(d) {
				uni.showToast({ title: '预约 ' + d.name, icon: 'none' })
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
	.sub-tab { font-size: 30rpx; color: #434654; position: relative; padding-bottom: 8rpx; white-space: nowrap; }
	.sub-tab.active { color: #003da6; font-weight: 700; }
	.sub-tab.active::after {
		content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
		width: 32rpx; height: 6rpx; background: #003da6; border-radius: 3rpx;
	}
	.list { padding: 16rpx 32rpx; }
</style>
