<template>
	<view class="material-card" @click="$emit('click')">
		<view class="card-inner">
			<view class="thumb-wrap">
				<image v-if="item.cover" class="thumb-img" :src="item.cover" mode="aspectFill" />
				<view v-else class="thumb" :style="{ background: thumbColor }" />
				<text v-if="item.hot" class="hot-tag">热销</text>
			</view>
			<view class="content">
				<view class="info-top">
					<view class="title-row">
						<text class="name">{{ item.name }}</text>
						<text
							class="bookmark"
							:class="{ active: bookmarked }"
							@click.stop="bookmarked = !bookmarked"
						>☆</text>
					</view>
					<text v-if="item.brand" class="brand">{{ item.brand }}</text>
					<view v-if="displayTags.length" class="tags">
						<text v-for="(tag, i) in displayTags" :key="i" class="tag">{{ tag }}</text>
					</view>
				</view>
				<view class="footer">
					<view class="price-wrap">
						<text class="price">{{ item.price }}</text>
						<text v-if="item.unit" class="unit">{{ item.unit }}</text>
					</view>
					<button class="btn-consult" @click.stop="$emit('cart')">立即咨询</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { MATERIAL_CATEGORIES } from '../../mock/qiju-data.js'

	const CATEGORY_TAGS = MATERIAL_CATEGORIES.filter(c => c !== '全部')

	export default {
		name: 'MaterialCard',
		props: {
			item: { type: Object, required: true },
			index: { type: Number, default: 0 }
		},
		data() {
			return {
				bookmarked: false
			}
		},
		computed: {
			thumbColor() {
				const colors = ['#2a2a2a', '#c8b896', '#d4cfc7']
				return colors[this.index % colors.length]
			},
			displayTags() {
				if (!this.item.tags) return []
				return this.item.tags.filter(tag => !CATEGORY_TAGS.includes(tag))
			}
		}
	}
</script>

<style scoped>
	.material-card {
		width: 100%;
		max-width: 100%;
		box-sizing: border-box;
		background: #ffffff;
		border-radius: 24rpx;
		overflow: hidden;
		margin-bottom: 48rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
	}

	.card-inner {
		display: flex;
		height: 320rpx;
	}

	.thumb-wrap {
		position: relative;
		width: 33.333%;
		flex-shrink: 0;
	}

	.thumb,
	.thumb-img {
		width: 100%;
		height: 100%;
		display: block;
	}

	.hot-tag {
		position: absolute;
		top: 16rpx;
		left: 16rpx;
		padding: 4rpx 16rpx;
		background: #003da6;
		border-radius: 8rpx;
		font-size: 20rpx;
		font-weight: 700;
		color: #ffffff;
		box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.08);
	}

	.content {
		flex: 1;
		width: 66.667%;
		padding: 32rpx;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		min-width: 0;
		box-sizing: border-box;
	}

	.info-top {
		flex: 1;
		min-width: 0;
	}

	.title-row {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 16rpx;
	}

	.name {
		flex: 1;
		font-size: 32rpx;
		font-weight: 700;
		color: #1c1c18;
		line-height: 1.4;
	}

	.bookmark {
		font-size: 36rpx;
		color: #737686;
		line-height: 1;
		flex-shrink: 0;
	}

	.bookmark.active {
		color: #003da6;
	}

	.brand {
		display: block;
		margin-top: 8rpx;
		font-size: 24rpx;
		color: #434654;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 16rpx;
		margin-top: 24rpx;
	}

	.tag {
		padding: 8rpx 16rpx;
		background: #f7f3ec;
		border: 1rpx solid rgba(195, 198, 215, 0.2);
		border-radius: 12rpx;
		font-size: 20rpx;
		color: #434654;
	}

	.footer {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 16rpx;
		gap: 16rpx;
	}

	.price-wrap {
		display: flex;
		align-items: baseline;
		flex: 1;
		min-width: 0;
	}

	.price {
		font-size: 36rpx;
		font-weight: 700;
		color: #003da6;
	}

	.unit {
		font-size: 20rpx;
		font-weight: 400;
		color: #737686;
		margin-left: 8rpx;
	}

	.btn-consult {
		flex-shrink: 0;
		height: 64rpx;
		line-height: 64rpx;
		padding: 0 24rpx;
		background: #003da6;
		color: #ffffff;
		border-radius: 16rpx;
		font-size: 22rpx;
		font-weight: 700;
		border: none;
		box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.08);
		box-sizing: border-box;
	}

	.btn-consult::after {
		border: none;
	}
</style>
