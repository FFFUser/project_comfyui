/** 主 Tab 页滚动区域高度计算（与 BottomNavBar 固定底栏对齐） */

export const BOTTOM_NAV = {
	topPaddingRpx: 20,
	iconRpx: 36,
	gapRpx: 6,
	labelRpx: 33,
	basePaddingRpx: 12,
	horizontalPaddingRpx: 78
}

function rpxToPx(sys, rpx) {
	return Math.round(rpx * sys.windowWidth / 750)
}

export function getTopBarHeightPx(sys) {
	const statusBarHeight = sys.statusBarHeight || 20
	let barInnerHeight = Math.round(112 * sys.windowWidth / 750)

	// #ifdef MP-WEIXIN
	const menuButton = uni.getMenuButtonBoundingClientRect()
	if (menuButton && menuButton.height) {
		barInnerHeight = (menuButton.top - statusBarHeight) * 2 + menuButton.height
	}
	// #endif

	return statusBarHeight + barInnerHeight
}

export function getBottomNavHeightPx(sys) {
	const safeBottom = sys.safeAreaInsets?.bottom || 0
	const { topPaddingRpx, iconRpx, gapRpx, labelRpx, basePaddingRpx } = BOTTOM_NAV
	const contentRpx = topPaddingRpx + iconRpx + gapRpx + labelRpx + basePaddingRpx
	return rpxToPx(sys, contentRpx) + safeBottom
}

export function getBottomNavPaddingStyle(sys) {
	const safeBottom = sys.safeAreaInsets?.bottom || 0
	return {
		paddingTop: rpxToPx(sys, BOTTOM_NAV.topPaddingRpx) + 'px',
		paddingBottom: safeBottom + rpxToPx(sys, BOTTOM_NAV.basePaddingRpx) + 'px'
	}
}

export function getScrollHeightPx(sys, extraTopPx = 0) {
	return sys.windowHeight - getTopBarHeightPx(sys) - getBottomNavHeightPx(sys) - extraTopPx
}
