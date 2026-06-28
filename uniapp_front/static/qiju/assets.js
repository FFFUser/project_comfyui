/** Figma 资源路径（static/qiju/） */

export const ICONS = {
	navHome: '/static/qiju/icons/nav-home.png',
	navHomeActive: '/static/qiju/icons/nav-home-active.png',
	navWorkers: '/static/qiju/icons/nav-workers.png',
	navWorkersActive: '/static/qiju/icons/nav-workers-active.png',
	navDesigners: '/static/qiju/icons/nav-designers.png',
	navDesignersActive: '/static/qiju/icons/nav-designers-active.png',
	navMaterials: '/static/qiju/icons/nav-materials.png',
	navMaterialsActive: '/static/qiju/icons/nav-materials-active.png',
	navProfile: '/static/qiju/icons/nav-profile.png',
	navProfileActive: '/static/qiju/icons/nav-profile-active.png',
	headerMore: '/static/qiju/icons/header-more.png',
	headerClose: '/static/qiju/icons/header-close.png',
	headerCompass: '/static/qiju/icons/header-compass.png',
	searchGrid: '/static/qiju/icons/search-grid.png',
	searchIcon: '/static/qiju/icons/search-icon.png',
	profileEdit: '/static/qiju/icons/profile-edit.png',
	profileCrown: '/static/qiju/icons/profile-crown.png',
	chevronRight: '/static/qiju/icons/chevron-right.png',
	quickOrder: '/static/qiju/icons/quick-order.png',
	quickDesign: '/static/qiju/icons/quick-design.png',
	quickCoupon: '/static/qiju/icons/quick-coupon.png',
	menuAddress: '/static/qiju/icons/menu-address.png',
	menuService: '/static/qiju/icons/menu-service.png',
	menuFeedback: '/static/qiju/icons/menu-feedback.png',
	menuSetting: '/static/qiju/icons/menu-setting.png',
	ctaDeco: '/static/qiju/icons/cta-deco.png'
}

export const ASSETS = {
	home: {
		cases: Array.from({ length: 8 }, (_, i) => `/static/qiju/home/case-${i + 1}.jpg`)
	},
	wood: {
		cases: ['/static/qiju/wood/case-1.jpg', '/static/qiju/wood/case-2.jpg']
	},
	design: {
		cases: Array.from({ length: 4 }, (_, i) => `/static/qiju/design/case-${i + 1}.jpg`)
	},
	caseDetail: {
		gallery: Array.from({ length: 5 }, (_, i) => `/static/qiju/case-detail/gallery-${i + 1}.jpg`),
		construction: Array.from({ length: 4 }, (_, i) => `/static/qiju/case-detail/construction-${i + 1}.jpg`)
	},
	workers: {
		avatars: Array.from({ length: 4 }, (_, i) => `/static/qiju/workers/avatar-${i + 1}.jpg`)
	},
	materials: {
		thumbs: Array.from({ length: 3 }, (_, i) => `/static/qiju/materials/thumb-${i + 1}.jpg`),
		bentoMain: '/static/qiju/materials/bento-main.jpg',
		bentoOak: '/static/qiju/materials/bento-oak.jpg'
	},
	stones: [
		'/static/qiju/stones/stone-1.jpg',
		'/static/qiju/stones/stone-2.jpg',
		'/static/qiju/stones/stone-3.jpg',
		'/static/qiju/stones/stone-4.png'
	],
	designers: {
		// 卡片封面：装修成果图
		covers: Array.from({ length: 3 }, (_, i) => `/static/qiju/designers/cover-${i + 1}.png`),
		avatars: Array.from({ length: 3 }, (_, i) => `/static/qiju/designers/avatar-${i + 1}.png`)
	},
	profile: {
		avatar: '/static/qiju/profile/avatar.jpg'
	},
	designerProfile: {
		hero: '/static/qiju/designer-profile/hero.jpg',
		avatar: '/static/qiju/designer-profile/avatar.png',
		works: Array.from({ length: 4 }, (_, i) => `/static/qiju/designer-profile/work-${i + 1}.jpg`)
	},
	workDetail: {
		hero: '/static/qiju/work-detail/hero.png'
	}
}
