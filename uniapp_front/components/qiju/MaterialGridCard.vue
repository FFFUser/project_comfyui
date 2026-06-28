<template>
	<view class="grid-card" :class="'h' + (index % 4)" @click="$emit('click')">
		<view class="cover-wrap">
			<image v-if="item.cover" class="cover-img" :src="item.cover" mode="aspectFill" />
			<view v-else class="cover-placeholder" :style="{ background: thumbColor }" />
			<text v-if="badgeLabel" class="badge" :class="badgeType">{{ badgeLabel }}</text>
		</view>
		<view class="body">
			<text class="name">{{ item.name }}</text>
			<view class="price-row">
				<text class="price">{{ item.price }}</text>
				<text v-if="item.unit" class="unit">{{ item.unit }}</text>
				<text class="suffix">起</text>
			</view>
			<view v-if="displayTags.length" class="tags">
				<text v-for="(tag, i) in displayTags" :key="i" class="tag">#{{ tag }}</text>
			</view>
			<button class="btn-consult" @click.stop="$emit('cart')">立即咨询</button>
		</view>
	</view>
</template>

<script>
	import { MATERIAL_CATEGORIES } from '../../mock/qiju-data.js'

	const CATEGORY_TAGS = MATERIAL_CATEGORIES.filter(c => c !== '全部')

	export default {
		name: 'MaterialGridCard',
		props: {
			item: { type: Object, required: true },
			index: { type: Number, default: 0 }
		},
		computed: {
			thumbColor() {
				const colors = ['#d4cfc7', '#c8b896', '#2a2a2a', '#ece8e1']
				return colors[this.index % colors.length]
			},
			displayTags() {
				if (!this.item.tags) return []
				return this.item.tags.filter(tag => !CATEGORY_TAGS.includes(tag))
			},
			badgeLabel() {
				if (this.item.badge) return this.item.badge
				if (this.item.hot) return '热销'
				if (this.item.new) return '新品'
				if (this.item.eco) return '环保认证'
				return ''
			},
			badgeType() {
				if (this.item.badgeType) return this.item.badgeType
				if (this.item.hot) return 'hot'
				if (this.item.new) return 'new'
				if (this.item.eco) return 'eco'
				return 'hot'
			}
		}
	}
</script>

<style scoped>
	.grid-card {
		width: 100%;
		box-sizing: border-box;
		background: #ffffff;
		border-radius: 20rpx;
		overflow: hidden;
		box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
	}

	.cover-wrap {
		position: relative;
		width: 100%;
		overflow: hidden;
	}

	.h0 .cover-wrap { height: 240rpx; }
	.h1 .cover-wrap { height: 360rpx; }
	.h2 .cover-wrap { height: 200rpx; }
	.h3 .cover-wrap { height: 300rpx; }

	.cover-img,
	.cover-placeholder {
		width: 100%;
		height: 100%;
		display: block;
	}

	.badge {
		position: absolute;
		top: 12rpx;
		left: 12rpx;
		padding: 2rpx 10rpx;
		border-radius: 8rpx;
		font-size: 18rpx;
		font-weight: 700;
		line-height: 1.4;
		max-width: calc(100% - 24rpx);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.badge.hot {
		background: #ba1a1a;
		color: #ffffff;
	}

	.badge.new {
		background: #dbe1ff;
		color: #003da6;
	}

	.badge.eco {
		background: #ffccbc;
		color: #822600;
	}

	.body {
		padding: 16rpx;
		box-sizing: border-box;
	}

	.name {
		display: block;
		font-size: 26rpx;
		font-weight: 700;
		color: #1c1c18;
		line-height: 1.35;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.price-row {
		display: flex;
		align-items: baseline;
		margin-top: 8rpx;
		flex-wrap: wrap;
	}

	.price {
		font-size: 28rpx;
		font-weight: 700;
		color: #003da6;
	}

	.unit {
		font-size: 22rpx;
		color: #003da6;
		font-weight: 700;
	}

	.suffix {
		font-size: 20rpx;
		color: #737686;
		margin-left: 4rpx;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 8rpx;
		margin-top: 12rpx;
	}

	.tag {
		padding: 2rpx 10rpx;
		background: #f7f3ec;
		border-radius: 999rpx;
		font-size: 18rpx;
		color: #434654;
		max-width: 100%;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.btn-consult {
		width: 100%;
		height: 56rpx;
		line-height: 56rpx;
		margin-top: 12rpx;
		padding: 0;
		background: #003da6;
		color: #ffffff;
		border-radius: 12rpx;
		font-size: 22rpx;
		font-weight: 700;
		border: none;
		box-sizing: border-box;
	}

	.btn-consult::after {
		border: none;
	}
</style>
