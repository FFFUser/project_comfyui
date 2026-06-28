<template>
	<view class="case-card" @click="$emit('click')">
		<view class="cover-wrap">
			<image v-if="item.cover" class="cover-img" :src="item.cover" mode="aspectFill" />
			<view v-else class="cover" :style="{ background: coverColor }" />
			<text v-if="item.badge" class="badge">{{ item.badge }}</text>
		</view>
		<view class="info">
			<text class="title">{{ item.title }}</text>
			<text class="meta">{{ item.meta }}</text>
			<view class="row">
				<view class="team">
					<view class="avatar" :style="avatarStyle">
						<text v-if="item.initials" class="initials">{{ item.initials }}</text>
					</view>
					<text class="team-name">{{ item.team }}</text>
				</view>
				<view class="likes">
					<text class="heart">♡</text>
					<text class="like-num">{{ item.likes }}</text>
				</view>
			</view>
			<text v-if="item.price" class="price">{{ item.price }}</text>
		</view>
	</view>
</template>

<script>
	const COLORS = ['#d4cfc7', '#c8d4e0', '#d0d8c8', '#e0d0c8', '#c0c8d8', '#d8d0c0']

	export default {
		name: 'CaseCard',
		props: {
			item: { type: Object, required: true },
			index: { type: Number, default: 0 }
		},
		computed: {
			coverColor() {
				return COLORS[this.index % COLORS.length]
			},
			avatarStyle() {
				if (this.item.color) return { background: this.item.color }
				if (this.item.initials) return { background: '#0052d9' }
				return { background: '#ece8e1' }
			}
		}
	}
</script>

<style scoped>
	.case-card {
		background: #fff;
		border-radius: 24rpx;
		overflow: hidden;
		box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.05);
	}

	.cover-wrap {
		position: relative;
		width: 100%;
		padding-bottom: 100%;
	}

	.cover,
	.cover-img {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
	}

	.cover-img {
		display: block;
	}

	.badge {
		position: absolute;
		top: 16rpx;
		left: 16rpx;
		padding: 4rpx 12rpx;
		background: rgba(0, 0, 0, 0.4);
		backdrop-filter: blur(12rpx);
		border-radius: 4rpx;
		font-size: 20rpx;
		color: #fff;
		line-height: 30rpx;
	}

	.info {
		padding: 16rpx;
		display: flex;
		flex-direction: column;
		gap: 8rpx;
	}

	.title {
		display: block;
		font-size: 28rpx;
		font-weight: 700;
		color: #1c1c18;
		line-height: 40rpx;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.meta {
		display: block;
		font-size: 20rpx;
		font-weight: 500;
		color: #434654;
		line-height: 30rpx;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 8rpx;
	}

	.team {
		display: flex;
		align-items: center;
		gap: 8rpx;
		min-width: 0;
	}

	.avatar {
		width: 32rpx;
		height: 32rpx;
		border-radius: 50%;
		flex-shrink: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.initials {
		font-size: 14rpx;
		color: #fff;
		font-weight: 700;
	}

	.team-name {
		max-width: 100rpx;
		font-size: 20rpx;
		color: #434654;
		line-height: 30rpx;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.likes {
		display: flex;
		align-items: center;
		gap: 4rpx;
		flex-shrink: 0;
	}

	.heart {
		font-size: 18rpx;
		color: #434654;
	}

	.like-num {
		font-size: 18rpx;
		color: #434654;
		line-height: 27rpx;
	}

	.price {
		display: block;
		margin-top: 8rpx;
		font-size: 28rpx;
		font-weight: 700;
		color: #003da6;
		line-height: 40rpx;
	}
</style>
