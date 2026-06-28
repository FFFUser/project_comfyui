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
						<text class="projects">{{ designer.projects }}</text>
					</view>
				</view>
			</view>
			<view class="tags">
				<text v-for="(tag, i) in designer.tags" :key="i" class="tag">{{ tag }}</text>
			</view>
			<view class="action-row">
				<view class="price-info">
					<text class="price">{{ designer.price }}</text>
					<text class="unit">{{ designer.unit }}起</text>
				</view>
				<button class="btn-book" @click.stop="$emit('book')">预约咨询</button>
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
		margin-bottom: 48rpx;
		box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
	}

	.cover-wrap {
		position: relative;
		height: 400rpx;
	}

	.cover,
	.cover-img {
		width: 100%;
		height: 100%;
		display: block;
	}

	.cover-badge {
		position: absolute;
		top: 32rpx;
		left: 32rpx;
		padding: 8rpx 24rpx;
		background: rgba(0, 0, 0, 0.45);
		backdrop-filter: blur(8px);
		border-radius: 8rpx;
		font-size: 24rpx;
		color: #fff;
	}

	.body {
		padding: 40rpx;
	}

	.profile {
		display: flex;
		gap: 24rpx;
	}

	.avatar,
	.avatar-img {
		width: 96rpx;
		height: 96rpx;
		border-radius: 50%;
		border: 4rpx solid #fff;
		margin-top: -72rpx;
		flex-shrink: 0;
	}

	.avatar-img {
		display: block;
		background: #fff;
	}

	.profile-info {
		flex: 1;
		padding-top: 8rpx;
	}

	.name {
		font-size: 32rpx;
		font-weight: 700;
		color: #1c1c18;
	}

	.rating-row {
		display: flex;
		align-items: center;
		gap: 8rpx;
		margin-top: 8rpx;
	}

	.star {
		font-size: 22rpx;
		color: #f5a623;
	}

	.rating {
		font-size: 26rpx;
		font-weight: 600;
		color: #1c1c18;
	}

	.projects {
		font-size: 24rpx;
		color: #434654;
		margin-left: 8rpx;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 16rpx;
		margin-top: 24rpx;
	}

	.tag {
		padding: 8rpx 24rpx;
		background: #f1ede6;
		border-radius: 8rpx;
		font-size: 24rpx;
		color: #434654;
	}

	.action-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 32rpx;
	}

	.price-info {
		display: flex;
		align-items: baseline;
	}

	.price {
		font-size: 36rpx;
		font-weight: 700;
		color: #003da6;
	}

	.unit {
		font-size: 24rpx;
		color: #434654;
		margin-left: 4rpx;
	}

	.btn-book {
		height: 96rpx;
		line-height: 96rpx;
		padding: 0 64rpx;
		background: #003da6;
		color: #fff;
		border-radius: 16rpx;
		font-size: 28rpx;
		border: none;
	}
</style>
