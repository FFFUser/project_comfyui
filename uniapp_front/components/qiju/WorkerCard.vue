<template>
	<view class="worker-card" :class="{ featured: worker.featured }">
		<view class="header">
			<image v-if="worker.avatar" class="avatar-img" :src="worker.avatar" mode="aspectFill" />
			<view v-else class="avatar" :style="{ background: avatarColor }" />
			<view class="info">
				<view class="name-row">
					<text class="name">{{ worker.name }}</text>
					<text class="badge">{{ worker.badge }}</text>
				</view>
				<text class="exp">{{ worker.exp }}</text>
			</view>
		</view>
		<text v-if="worker.desc" class="desc">{{ worker.desc }}</text>
		<view class="tags">
			<text v-for="(tag, i) in worker.tags" :key="i" class="tag">{{ tag }}</text>
		</view>
		<view class="actions">
			<button class="btn-primary" @click="$emit('contact')">立即联系</button>
			<view class="btn-icon" @click="$emit('favorite')">
				<text>♡</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'WorkerCard',
		props: {
			worker: { type: Object, required: true },
			index: { type: Number, default: 0 }
		},
		computed: {
			avatarColor() {
				const colors = ['#c8d4e0', '#d0d8c8', '#e0d0c8', '#d4cfc7']
				return colors[this.index % colors.length]
			}
		}
	}
</script>

<style scoped>
	.worker-card {
		background: #fff;
		border-radius: 24rpx;
		padding: 40rpx;
		margin-bottom: 32rpx;
		box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
	}

	.worker-card.featured {
		border: 2rpx solid rgba(0, 61, 166, 0.15);
	}

	.header {
		display: flex;
		gap: 32rpx;
	}

	.avatar,
	.avatar-img {
		width: 128rpx;
		height: 128rpx;
		border-radius: 50%;
		flex-shrink: 0;
	}

	.avatar-img {
		display: block;
	}

	.info {
		flex: 1;
		min-width: 0;
	}

	.name-row {
		display: flex;
		align-items: center;
		gap: 16rpx;
		flex-wrap: wrap;
	}

	.name {
		font-size: 36rpx;
		font-weight: 700;
		color: #1c1c18;
	}

	.badge {
		padding: 4rpx 16rpx;
		background: rgba(0, 61, 166, 0.08);
		border-radius: 8rpx;
		font-size: 22rpx;
		color: #003da6;
	}

	.exp {
		display: block;
		margin-top: 8rpx;
		font-size: 26rpx;
		color: #434654;
	}

	.desc {
		display: block;
		margin-top: 24rpx;
		font-size: 26rpx;
		color: #434654;
		line-height: 1.6;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 16rpx;
		margin-top: 24rpx;
	}

	.tag {
		padding: 8rpx 20rpx;
		background: #f1ede6;
		border-radius: 8rpx;
		font-size: 24rpx;
		color: #434654;
	}

	.actions {
		display: flex;
		gap: 24rpx;
		margin-top: 32rpx;
		align-items: center;
	}

	.btn-primary {
		flex: 1;
		height: 88rpx;
		line-height: 88rpx;
		background: #003da6;
		color: #fff;
		border-radius: 16rpx;
		font-size: 28rpx;
		border: none;
	}

	.btn-icon {
		width: 96rpx;
		height: 88rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 2rpx solid #ece8e1;
		border-radius: 16rpx;
		font-size: 36rpx;
		color: #434654;
	}
</style>
