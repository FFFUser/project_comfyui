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
		<scroll-view
			scroll-y
			class="list"
			:bounces="false"
			:lower-threshold="80"
			:scroll-top="scrollTop"
			:style="{ height: scrollHeight + 'px' }"
			@scroll="onListScroll"
			@scrolltolower="onScrollToLower"
		>
			<view class="list-inner">
				<DesignerCard
					v-for="(d, i) in displayDesigners"
					:key="d.id"
					:designer="d"
					:index="i"
					@click="goProfile(d)"
					@book="onBook(d)"
				/>
				<view v-if="showListFooter" class="list-footer">
					<text class="list-footer-text">没有更多设计师了~</text>
				</view>
			</view>
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
				allDesigners: DESIGNERS,
				activeTab: 0,
				scrollHeight: 500,
				showNoMore: false,
				scrollTop: 0,
				scrollTopCache: 0
			}
		},
		computed: {
			displayDesigners() {
				if (this.activeTab === 0) return this.allDesigners
				const category = this.tabs[this.activeTab]
				return this.allDesigners.filter(d => d.category === category)
			},
			showListFooter() {
				if (!this.displayDesigners.length) return true
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
				if (this.displayDesigners.length) {
					this.showNoMore = true
				}
			},
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
	.list {
		box-sizing: border-box;
	}
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
