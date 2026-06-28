<template>
	<view class="worker-card">
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
		<view v-if="worker.tags && worker.tags.length" class="tags">
			<text v-for="tag in visibleTags" :key="tag" class="tag">{{ tag }}</text>
			<text v-if="showMoreTag" class="tag tag-more" @click="expandTags">+{{ extraTagCount }}</text>
		</view>
		<text v-if="worker.desc" class="desc">{{ worker.desc }}</text>
		<view class="actions">
			<button class="btn-primary" @click="$emit('contact')">立即咨询</button>
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
		data() {
			return {
				tagsExpanded: false
			}
		},
		computed: {
			avatarColor() {
				const colors = ['#c8d4e0', '#d0d8c8', '#e0d0c8', '#d4cfc7']
				return colors[this.index % colors.length]
			},
			allTags() {
				return this.worker.tags || []
			},
			visibleTags() {
				if (this.tagsExpanded || this.allTags.length <= 3) return this.allTags
				return this.allTags.slice(0, 3)
			},
			extraTagCount() {
				return this.allTags.length > 3 ? this.allTags.length - 3 : 0
			},
			showMoreTag() {
				return !this.tagsExpanded && this.extraTagCount > 0
			}
		},
		methods: {
			expandTags() {
				this.tagsExpanded = true
			}
		}
	}
</script>

<style src="./worker-card.css"></style>
