/** 主 Tab 页滚动区域高度计算（与 BottomNavBar 固定底栏对齐） */

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
	const basePadding = Math.round(20 * sys.windowWidth / 750)
	const navBar = Math.round(128 * sys.windowWidth / 750)
	return navBar + safeBottom + basePadding
}

export function getScrollHeightPx(sys, extraTopPx = 0) {
	return sys.windowHeight - getTopBarHeightPx(sys) - getBottomNavHeightPx(sys) - extraTopPx
}
