<template>
	<view class="page">
		<TopAppBar variant="home" />
		<view class="search-bar">
			<view class="search-inner">
				<view class="grid-btn">
					<image class="grid-icon" :src="icons.searchGrid" mode="aspectFit" />
				</view>
				<view class="case-tabs" :class="{ collapsed: searchOpen }">
					<view class="case-tab-track">
						<view class="case-tab-slider" :style="tabSliderStyle" />
						<view
							v-for="(tab, i) in homeTabs"
							:key="tab"
							class="case-tab"
							:class="{ active: activeTab === i }"
							@click="onTabTap(i)"
						>{{ tab }}</view>
					</view>
				</view>
				<view class="search-field" :class="{ open: searchOpen }">
					<input
						class="search-input"
						v-model="searchKeyword"
						:focus="searchFocus"
						placeholder="搜索案例、设计师..."
						confirm-type="search"
						@confirm="onSearchConfirm"
						@blur="onSearchBlur"
					/>
				</view>
				<view class="search-btn" @click="toggleSearch">
					<image class="search-icon" :src="icons.searchIcon" mode="aspectFit" />
				</view>
			</view>
		</view>
		<scroll-view scroll-x class="filter-bar" :show-scrollbar="false">
			<view class="filter-inner">
				<text
					v-for="(f, i) in filters"
					:key="f"
					class="filter-pill"
					:class="{ active: activeFilter === i }"
					@click="activeFilter = i"
				>{{ f }}</text>
			</view>
		</scroll-view>
		<swiper
			class="case-swiper"
			:current="activeTab"
			:duration="300"
			@change="onSwiperChange"
			:style="{ height: scrollHeight + 'px' }"
		>
			<swiper-item v-for="(list, tabIndex) in tabLists" :key="tabIndex">
				<scroll-view
					scroll-y
					class="main-scroll"
					:bounces="false"
					:lower-threshold="80"
					@scrolltolower="onScrollToLower(tabIndex)"
					:style="{ height: scrollHeight + 'px' }"
				>
					<view class="grid">
						<CaseCard
							v-for="(item, i) in list"
							:key="item.id"
							:item="item"
							:index="i"
							@click="goDetail(item, tabIndex)"
						/>
					</view>
					<view v-if="list.length && showNoMore[tabIndex]" class="list-footer">
						<text class="list-footer-text">没有更多案例了~</text>
					</view>
				</scroll-view>
			</swiper-item>
		</swiper>
		<BottomNavBar current="home" />
	</view>
</template>

<script>
	import TopAppBar from '../../components/qiju/TopAppBar.vue'
	import BottomNavBar from '../../components/qiju/BottomNavBar.vue'
	import CaseCard from '../../components/qiju/CaseCard.vue'
	import { ICONS } from '../../static/qiju/assets.js'
	import { getScrollHeightPx } from '../../utils/page-layout.js'
	import {
		HOME_TABS,
		HOME_FILTERS,
		DIRECT_CASES,
		WOOD_CASES,
		DESIGN_CASES
	} from '../../mock/qiju-data.js'

	export default {
		components: { TopAppBar, BottomNavBar, CaseCard },
		data() {
			return {
				icons: ICONS,
				homeTabs: HOME_TABS,
				filters: HOME_FILTERS,
				tabLists: [DIRECT_CASES, WOOD_CASES, DESIGN_CASES],
				activeTab: 0,
				activeFilter: 0,
				scrollHeight: 500,
				showNoMore: [false, false, false],
				searchOpen: false,
				searchFocus: false,
				searchKeyword: ''
			}
		},
		computed: {
			tabSliderStyle() {
				return {
					width: (100 / this.homeTabs.length) + '%',
					transform: `translateX(${this.activeTab * 100}%)`
				}
			}
		},
		watch: {
			activeFilter() {
				this.showNoMore = [false, false, false]
			}
		},
		onReady() {
			const sys = uni.getSystemInfoSync()
			const searchBarHeight = Math.round(112 * sys.windowWidth / 750)
			const filterBarHeight = Math.round(100 * sys.windowWidth / 750)
			this.scrollHeight = getScrollHeightPx(sys, searchBarHeight + filterBarHeight)
		},
		methods: {
			onTabTap(index) {
				if (this.activeTab === index) return
				this.activeTab = index
				this.showNoMore = [false, false, false]
			},
			onSwiperChange(e) {
				const index = e.detail.current
				if (this.activeTab === index) return
				this.activeTab = index
				this.showNoMore = [false, false, false]
			},
			onScrollToLower(tabIndex) {
				if (this.tabLists[tabIndex].length) {
					this.$set(this.showNoMore, tabIndex, true)
				}
			},
			goDetail(item, tabIndex) {
				if (tabIndex === 2) {
					uni.navigateTo({ url: '/pages/work-detail/work-detail?id=' + item.id })
					return
				}
				uni.navigateTo({
					url: '/pages/case-detail/case-detail?id=' + item.id + '&title=' + encodeURIComponent(item.title)
				})
			},
			toggleSearch() {
				if (this.searchOpen) {
					this.closeSearch()
					return
				}
				this.searchOpen = true
				this.$nextTick(() => {
					this.searchFocus = true
				})
			},
			closeSearch() {
				this.searchOpen = false
				this.searchFocus = false
				this.searchKeyword = ''
			},
			onSearchBlur() {
				this.searchFocus = false
				if (!this.searchKeyword.trim()) {
					this.searchOpen = false
				}
			},
			onSearchConfirm() {
				if (!this.searchKeyword.trim()) {
					this.closeSearch()
					return
				}
				uni.showToast({ title: '搜索：' + this.searchKeyword, icon: 'none' })
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

	.case-swiper,
	.main-scroll {
		width: 100%;
	}

	.search-bar {
		padding: 16rpx 32rpx;
		background: rgba(253, 249, 242, 0.8);
		backdrop-filter: blur(48rpx);
		-webkit-backdrop-filter: blur(48rpx);
		border-bottom: 1rpx solid rgba(195, 198, 215, 0.3);
	}

	.search-inner {
		display: flex;
		align-items: stretch;
		flex: 1;
		background: rgba(241, 237, 230, 0.5);
		border-radius: 24rpx;
		padding: 8rpx;
		gap: 8rpx;
	}

	.grid-btn {
		width: 80rpx;
		height: 64rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 16rpx;
		flex-shrink: 0;
	}

	.grid-icon {
		width: 40rpx;
		height: 40rpx;
	}

	.case-tabs {
		flex: 1;
		min-width: 0;
		max-width: 100%;
		opacity: 1;
		overflow: hidden;
		transition: max-width 0.32s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.24s ease, flex 0.32s ease;
	}

	.case-tabs.collapsed {
		flex: 0;
		max-width: 0;
		opacity: 0;
	}

	.search-field {
		flex: 0;
		max-width: 0;
		min-width: 0;
		height: 64rpx;
		opacity: 0;
		overflow: hidden;
		display: flex;
		align-items: center;
		transform-origin: right center;
		transition: max-width 0.32s cubic-bezier(0.4, 0, 0.2, 1), flex 0.32s ease, opacity 0.24s ease;
	}

	.search-field.open {
		flex: 1;
		max-width: 100%;
		opacity: 1;
	}

	.search-input {
		width: 100%;
		height: 64rpx;
		padding: 0 16rpx;
		font-size: 24rpx;
		color: #1c1c18;
		background: rgba(255, 255, 255, 0.65);
		border-radius: 16rpx;
		box-sizing: border-box;
	}

	.case-tab-track {
		position: relative;
		display: flex;
		align-items: stretch;
		height: 64rpx;
		border-radius: 16rpx;
	}

	.case-tab-slider {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		background: #003da6;
		border-radius: 16rpx;
		box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.05);
		transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		will-change: transform;
	}

	.case-tab {
		flex: 1;
		z-index: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 16rpx 0;
		font-size: 24rpx;
		font-weight: 700;
		color: #434654;
		border-radius: 16rpx;
		transition: color 0.25s ease;
	}

	.case-tab.active {
		color: #fff;
	}

	.search-btn {
		width: 64rpx;
		height: 64rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 16rpx;
		flex-shrink: 0;
	}

	.search-icon {
		width: 36rpx;
		height: 36rpx;
	}

	.filter-bar {
		white-space: nowrap;
		width: 100%;
		padding: 24rpx 0;
		margin-bottom: 4rpx;
		background: #fdf9f2;
		flex-shrink: 0;
	}

	.filter-inner {
		display: inline-flex;
		gap: 16rpx;
		padding: 0 32rpx;
	}

	.filter-pill {
		display: inline-block;
		flex-shrink: 0;
		padding: 12rpx 32rpx;
		background: #f1ede6;
		border-radius: 999rpx;
		font-size: 24rpx;
		font-weight: 500;
		color: #434654;
		border: 1rpx solid transparent;
		transition: background 0.2s, border-color 0.2s, color 0.2s;
	}

	.filter-pill.active {
		background: rgba(74, 92, 148, 0.1);
		border-color: rgba(74, 92, 148, 0.2);
		color: #4a5c94;
		font-weight: 700;
	}

	.grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 8rpx;
		padding: 0 8rpx 16rpx;
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
