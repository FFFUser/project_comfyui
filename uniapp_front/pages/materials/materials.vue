<template>

	<view class="page">

		<TopAppBar variant="home" />

		<view class="search-wrap">

			<text class="search-icon">🔍</text>

			<input class="search-input" :placeholder="searchPlaceholder" />

		</view>

		<scroll-view scroll-x class="cat-tabs" :show-scrollbar="false">

			<view class="cat-inner">

				<text

					v-for="(c, i) in categories"

					:key="c"

					class="cat-tab"

					:class="{ active: activeCat === i }"

					@click="onCatTap(i)"

				>{{ c }}</text>

			</view>

		</scroll-view>

		<scroll-view scroll-y class="main" :bounces="false" :style="{ height: scrollHeight + 'px', width: '100%' }">
			<view class="main-inner">
			<!-- 全部 -->

			<template v-if="activeCat === 0">

				<view class="bento">

					<view class="bento-left">

						<image class="bento-bg" :src="bentoMain" mode="aspectFill" />

						<view class="bento-cover" />

						<view class="bento-info">

							<text class="bento-tag">本月推荐</text>

							<text class="bento-title">极地雪岩 Premium Marble</text>

						</view>

						<view class="bento-footer" @click="activeCat = 1">

							<text class="bento-badge">绿碳石材</text>

							<text class="bento-arrow">→</text>

						</view>

					</view>

					<view class="bento-right">

						<view class="bento-sm bento-sm-img">

							<image class="bento-sm-bg" :src="bentoOak" mode="aspectFill" />

							<text class="sm-title">北欧橡木</text>

							<text class="sm-sub">三层实木</text>

						</view>

						<view class="bento-sm" style="background: #4a5c94">

							<text class="sm-title">艺术涂料</text>

							<text class="sm-sub">零VOC系列</text>

						</view>

					</view>

				</view>

				<MaterialCard

					v-for="(m, i) in materials"

					:key="m.id"

					:item="m"

					:index="i"

					@click="onMaterialTap(m)"

					@cart="onCart(m)"

				/>

			</template>



			<!-- 分类列表（双列瀑布流） -->

			<template v-else>

				<view class="waterfall">

					<view class="waterfall-col">

						<MaterialGridCard

							v-for="({ item, index }) in waterfallLeft"

							:key="item.id"

							:item="item"

							:index="index"

							@cart="onCategoryCart(item)"

						/>

					</view>

					<view class="waterfall-col">

						<MaterialGridCard

							v-for="({ item, index }) in waterfallRight"

							:key="item.id"

							:item="item"

							:index="index"

							@cart="onCategoryCart(item)"

						/>

					</view>

				</view>

				<view v-if="!categoryItems.length" class="empty-hint">

					<text class="empty-text">暂无{{ categories[activeCat] }}材料，敬请期待</text>

				</view>

				<view v-if="activeCat === 1 && categoryItems.length" class="loading-hint">

					<view class="dot" />

					<text>正在加载更多材料...</text>

				</view>

			</template>

			<view class="scroll-spacer" />
			</view>
		</scroll-view>

		<BottomNavBar current="materials" />

	</view>

</template>



<script>

	import TopAppBar from '../../components/qiju/TopAppBar.vue'

	import BottomNavBar from '../../components/qiju/BottomNavBar.vue'

	import MaterialCard from '../../components/qiju/MaterialCard.vue'

	import MaterialGridCard from '../../components/qiju/MaterialGridCard.vue'

	import { getScrollHeightPx } from '../../utils/page-layout.js'

	import { MATERIAL_CATEGORIES, MATERIALS, STONE_MATERIALS, ASSETS } from '../../mock/qiju-data.js'



	export default {

		components: { TopAppBar, BottomNavBar, MaterialCard, MaterialGridCard },

		data() {

			return {

				categories: MATERIAL_CATEGORIES,

				materials: MATERIALS,

				stones: STONE_MATERIALS,

				bentoMain: ASSETS.materials.bentoMain,

				bentoOak: ASSETS.materials.bentoOak,

				activeCat: 0,

				scrollHeight: 500

			}

		},

		computed: {

			searchPlaceholder() {
				if (this.activeCat === 0) return '搜索环保木材、极简石材...'
				return '搜索' + this.categories[this.activeCat] + '系列...'
			},

			filteredMaterials() {

				const cat = this.categories[this.activeCat]

				return this.materials.filter(m => m.tags && m.tags.includes(cat))

			},

			categoryItems() {

				if (this.activeCat === 1) return this.stones

				return this.filteredMaterials

			},

			waterfallLeft() {

				return this.categoryItems

					.filter((_, i) => i % 2 === 0)

					.map((item, colIndex) => ({ item, index: colIndex * 2 }))

			},

			waterfallRight() {

				return this.categoryItems

					.filter((_, i) => i % 2 === 1)

					.map((item, colIndex) => ({ item, index: colIndex * 2 + 1 }))

			}

		},

		onReady() {

			const sys = uni.getSystemInfoSync()

			const searchHeight = Math.round(96 * sys.windowWidth / 750)

			const catTabsHeight = Math.round(58 * sys.windowWidth / 750)

			this.scrollHeight = getScrollHeightPx(sys, searchHeight + catTabsHeight)

		},

		methods: {

			onCatTap(i) {

				this.activeCat = i

			},

			onMaterialTap(m) {

				if (m.tags && m.tags.includes('绿碳石材')) {

					this.activeCat = 1

				}

			},

			onCart(m) {

				uni.showToast({ title: '已加入 ' + m.name, icon: 'none' })

			},

			onCategoryCart(item) {

				uni.showToast({ title: '已加入 ' + item.name, icon: 'none' })

			}

		}

	}

</script>



<style scoped>

	.page {
		height: 100vh;
		overflow: hidden;
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
		background: #fdf9f2;
	}

	.search-wrap {

		display: flex; align-items: center;

		margin: 16rpx 24rpx; padding: 0 24rpx;

		height: 80rpx; background: #fff; border-radius: 16rpx;
		box-sizing: border-box;

	}

	.search-icon { font-size: 28rpx; margin-right: 16rpx; }

	.search-input { flex: 1; font-size: 28rpx; color: #434654; }

	.cat-tabs { white-space: nowrap; padding-bottom: 8rpx; width: 100%; }

	.cat-inner { display: inline-flex; gap: 40rpx; padding: 0 24rpx; }

	.cat-tab { font-size: 28rpx; color: #434654; padding: 12rpx 0; position: relative; }

	.cat-tab.active { color: #003da6; font-weight: 700; }

	.cat-tab.active::after {

		content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);

		width: 48rpx; height: 4rpx; background: #003da6; border-radius: 2rpx;

	}

	.main {
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
	}

	.main-inner {
		padding: 0 24rpx;
		box-sizing: border-box;
	}

	.scroll-spacer {
		height: 64rpx;
	}

	.bento {
		display: flex;
		gap: 16rpx;
		margin-bottom: 32rpx;
		width: 100%;
		min-width: 0;
	}

	.bento-left {

		flex: 1;
		min-width: 0;
		height: 512rpx;
		border-radius: 24rpx;
		overflow: hidden;

		position: relative; background: #d4cfc7;

	}

	.bento-bg {

		position: absolute; inset: 0; width: 100%; height: 100%; border-radius: 24rpx;

	}

	.bento-cover { position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(0,0,0,0.5)); border-radius: 24rpx; }

	.bento-info { position: absolute; top: 32rpx; left: 32rpx; z-index: 1; }

	.bento-tag { display: block; font-size: 22rpx; color: rgba(255,255,255,0.8); }

	.bento-title { display: block; font-size: 32rpx; font-weight: 700; color: #fff; margin-top: 8rpx; line-height: 1.4; }

	.bento-footer { position: absolute; bottom: 32rpx; left: 32rpx; display: flex; align-items: center; gap: 16rpx; z-index: 1; }

	.bento-badge { padding: 4rpx 16rpx; background: rgba(255,255,255,0.2); border-radius: 8rpx; font-size: 22rpx; color: #fff; }

	.bento-arrow { color: #fff; font-size: 28rpx; }

	.bento-right {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
		gap: 16rpx;
	}

	.bento-sm {

		flex: 1; border-radius: 24rpx; padding: 32rpx;

		display: flex; flex-direction: column; justify-content: center;

		position: relative; overflow: hidden;

	}

	.bento-sm-img { color: #fff; }

	.bento-sm-bg { position: absolute; inset: 0; width: 100%; height: 100%; }

	.bento-sm .sm-title, .bento-sm .sm-sub { position: relative; z-index: 1; }

	.sm-title { font-size: 28rpx; font-weight: 600; color: #fff; }

	.sm-sub { font-size: 22rpx; color: rgba(255,255,255,0.7); margin-top: 8rpx; }

	.waterfall {
		display: flex;
		align-items: flex-start;
		gap: 20rpx;
		width: 100%;
		padding-top: 8rpx;
		box-sizing: border-box;
	}

	.waterfall-col {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}

	.loading-hint { display: flex; flex-direction: column; align-items: center; padding: 48rpx 0; }

	.dot { width: 12rpx; height: 12rpx; background: #003da6; border-radius: 50%; margin-bottom: 16rpx; }

	.loading-hint text { font-size: 24rpx; color: #969799; }

	.empty-hint { padding: 48rpx 0; text-align: center; }

	.empty-text { font-size: 28rpx; color: #969799; }

</style>

