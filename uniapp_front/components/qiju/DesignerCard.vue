<template>
	<view class="designer-card" @click="$emit('click')">
		<view class="cover-wrap">
			<image v-if="designer.cover" class="cover-img" :src="designer.cover" mode="aspectFill" />
			<view v-else class="cover" :style="{ background: coverColor }" />
			<text v-if="designer.badge" class="cover-badge">{{ designer.badge }}</text>
		</view>
		<view class="body">
			<view class="profile">
				<image v-if="designer.avatar" class="avatar-img" :src="designer.avatar" mode="aspectFill" />
				<view v-else class="avatar" :style="{ background: avatarColor }" />
				<view class="profile-info">
					<text class="name">{{ designer.name }}</text>
					<view class="rating-row">
						<text class="star">★</text>
						<text class="rating">{{ designer.rating }}</text>
						<text class="location">{{ designer.location || designer.projects }}</text>
					</view>
				</view>
			</view>
			<view class="tags">
				<text v-for="(tag, i) in designer.tags" :key="i" class="tag">{{ tag }}</text>
			</view>
			<view class="action-row">
				<view class="price-info">
					<text class="price-label">咨询费</text>
					<view class="price-value">
						<text class="price">{{ designer.price }}{{ designer.unit }}</text>
						<text class="price-suffix">起</text>
					</view>
				</view>
				<button class="btn-book" @click.stop="$emit('book')">立即咨询</button>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'DesignerCard',
		props: {
			designer: { type: Object, required: true },
			index: { type: Number, default: 0 }
		},
		computed: {
			coverColor() {
				const colors = ['#c8d4e0', '#d0d8c8', '#e0d0c8']
				return colors[this.index % colors.length]
			},
			avatarColor() {
				const colors = ['#d4cfc7', '#c0c8d8', '#d8d0c0']
				return colors[this.index % colors.length]
			}
		}
	}
</script>

<style scoped>
	.designer-card {
		background: #fff;
		border-radius: 24rpx;
		overflow: hidden;
		margin-bottom: 32rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.cover-wrap {
		position: relative;
		height: 320rpx;
	}

	.cover,
	.cover-img {
		width: 100%;
		height: 100%;
		display: block;
	}

	.cover-badge {
		position: absolute;
		top: 24rpx;
		left: 24rpx;
		padding: 6rpx 20rpx;
		background: rgba(0, 0, 0, 0.45);
		backdrop-filter: blur(8px);
		border-radius: 8rpx;
		font-size: 22rpx;
		color: #fff;
	}

	.body {
		padding: 24rpx 28rpx 28rpx;
	}

	.profile {
		display: flex;
		align-items: center;
		gap: 16rpx;
	}

	.avatar,
	.avatar-img {
		width: 72rpx;
		height: 72rpx;
		border-radius: 50%;
		flex-shrink: 0;
	}

	.avatar-img {
		display: block;
	}

	.profile-info {
		flex: 1;
		min-width: 0;
	}

	.name {
		font-size: 30rpx;
		font-weight: 700;
		color: #1c1c18;
		line-height: 1.3;
	}

	.rating-row {
		display: flex;
		align-items: center;
		gap: 6rpx;
		margin-top: 6rpx;
	}

	.star {
		font-size: 20rpx;
		color: #f5a623;
		line-height: 1;
	}

	.rating {
		font-size: 24rpx;
		font-weight: 600;
		color: #1c1c18;
	}

	.location {
		font-size: 24rpx;
		color: #8a8a8a;
		margin-left: 4rpx;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 14rpx;
		margin-top: 20rpx;
	}

	.tag {
		padding: 10rpx 22rpx;
		background: #fdf9f2;
		border-radius: 8rpx;
		font-size: 26rpx;
		color: #666;
		line-height: 1.4;
	}

	.action-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 24rpx;
	}

	.price-info {
		display: flex;
		flex-direction: column;
		gap: 4rpx;
	}

	.price-label {
		font-size: 22rpx;
		color: #434654;
		line-height: 1.3;
	}

	.price-value {
		display: flex;
		align-items: baseline;
	}

	.price {
		font-size: 32rpx;
		font-weight: 700;
		color: #003da6;
		line-height: 1.2;
	}

	.price-suffix {
		font-size: 24rpx;
		font-weight: 600;
		color: #003da6;
		margin-left: 2rpx;
	}

	.btn-book {
		height: 72rpx;
		line-height: 72rpx;
		padding: 0 40rpx;
		background: linear-gradient(0deg, #002878 0%, #003da6 55%, #0056d6 100%);
		color: #fff;
		border-radius: 12rpx;
		font-size: 26rpx;
		font-weight: 500;
		border: none;
		flex-shrink: 0;
		margin-right: -10rpx;
	}

	.btn-book::after {
		border: none;
	}
</style>
