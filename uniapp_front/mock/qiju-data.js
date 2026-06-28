/** QIJU 齐居 - 页面 mock 数据（来自 Figma 设计稿） */
import { ASSETS, ICONS } from '../static/qiju/assets.js'

export { ASSETS, ICONS }

export const HOME_TABS = ['直连案例', '木作案例', '设计案例']
export const HOME_FILTERS = ['全部', '水电', '泥木', '油漆', '安装']

export const DIRECT_CASES = [
	{ id: 1, title: '静安现代简装项目', meta: '现代简约 | 143平米 | 上海市', team: '张师傅团队', likes: '1.2w', price: '¥4.2w', badge: '顾家', cover: ASSETS.home.cases[0] },
	{ id: 2, title: '天山路老房改造', meta: '老房改造 | 62平米 | 上海市', team: '李师傅', likes: '8.9k', price: '¥2.8w', badge: '顾家', cover: ASSETS.home.cases[1], initials: 'LS' },
	{ id: 3, title: '徐汇区旧屋翻新', meta: '意式轻奢 | 210平米 | 杭州市', team: '王工', likes: '5.6k', price: '¥3.5w', badge: '顾家', cover: ASSETS.home.cases[2] },
	{ id: 4, title: '滨江壹号院软装', meta: '法式浪漫 | 158平米 | 南京市', team: '陈工', likes: '3.2k', price: '¥5.8w', badge: '顾家', cover: ASSETS.home.cases[4], initials: 'CG' },
	{ id: 5, title: '虹桥路二手房翻新', meta: '现代简约 | 89平米 | 北京市', team: '赵工', likes: '2.1k', price: '¥1.9w', badge: '顾家', cover: ASSETS.home.cases[4], initials: 'ZG' },
	{ id: 6, title: '静安府大平层设计', meta: '现代简约 | 512平米 | 上海市', team: '刘工', likes: '9.8k', price: '¥12.5w', badge: '顾家', cover: ASSETS.home.cases[5] },
	{ id: 7, title: '老弄堂精致改造', meta: '全18集 | 复古 | 120万播放', team: '李师傅', likes: '6.5k', price: '¥4.8w', badge: '顾家', cover: ASSETS.home.cases[6], initials: 'LS' },
	{ id: 8, title: '浦东联排别墅装修', meta: '全45集 | 简欧 | 340万播放', team: '张师傅团队', likes: '1.8w', price: '¥8.2w', badge: '顾家', cover: ASSETS.home.cases[7] }
]

export const WOOD_CASES = [
	{ id: 101, title: '极简无拉手橱柜', meta: '木作定制 | 脆米灰 | 上海市', team: '木作工坊', likes: '3.4k', price: '¥1.2w', badge: '顾家', cover: ASSETS.wood.cases[0], initials: 'MZ' },
	{ id: 102, title: '北美白橡木书柜', meta: '实木定制 | 象牙白 | 杭州市', team: '匠心木作', likes: '2.1k', price: '¥2.5w', badge: '顾家', cover: ASSETS.wood.cases[1], initials: 'JX' }
]

export const DESIGN_CASES = [
	{ id: 201, title: '极简美学空间', meta: '现代简约 | 180平米 | 上海市', team: '林设计师', likes: '4.5k', price: '', badge: '', cover: ASSETS.design.cases[0] },
	{ id: 202, title: '意式轻奢卧室', meta: '意式轻奢 | 45平米 | 北京市', team: '周设计', likes: '1.8k', price: '', badge: '', cover: ASSETS.design.cases[1], initials: 'ZS' },
	{ id: 203, title: '法式浪漫餐厅', meta: '法式浪漫 | 35平米 | 南京市', team: '吴设计', likes: '2.3k', price: '', badge: '', cover: ASSETS.design.cases[2], initials: 'WS' },
	{ id: 204, title: '侘寂之境：别院', meta: '侘寂风 | 210平米 | 杭州市', team: '张设计', likes: '6.7k', price: '', badge: '', cover: ASSETS.design.cases[3] }
]

export const WORKER_TABS = ['全部', '水电', '泥木', '油漆', '安装', '保洁', '其他']

export const WORKERS = [
	{ id: 1, name: '张建国', badge: '金牌师傅', exp: '15年经验 · 上海', tags: ['水电改造', '全屋布线', '强弱电'], featured: false, avatar: ASSETS.workers.avatars[0] },
	{ id: 2, name: '李明亮', badge: '资深师傅', exp: '12年经验 · 上海', tags: ['泥木工程', '贴砖铺地', '防水'], featured: false, avatar: ASSETS.workers.avatars[1] },
	{ id: 3, name: '王大海', badge: '明星师傅', exp: '18年经验 · 杭州', tags: ['微水泥', '岩板密缝', '高难度施工'], desc: '擅长高难度微水泥铺设与岩板密缝施工，曾参与多个样板房设计落地。', featured: true, avatar: ASSETS.workers.avatars[2] },
	{ id: 4, name: '赵铁柱', badge: '优质师傅', exp: '10年经验 · 北京', tags: ['油漆', '艺术涂料', '墙面翻新'], featured: false, avatar: ASSETS.workers.avatars[3] }
]

export const MATERIAL_CATEGORIES = ['全部', '绿碳石材', '瓷砖', '地板', '涂料', '五金', '灯具', '软装', '其他']

export const MATERIALS = [
	{ id: 1, name: '深海玄武·哑光大板', brand: '品牌: 简一大理石瓷砖', tags: ['绿碳石材', '进口'], price: '¥268', unit: '/㎡', hot: true, cover: ASSETS.materials.thumbs[0] },
	{ id: 2, name: '北欧橡木·三层实木', brand: '品牌: 圣象地板 PowerDekor', tags: ['环保E0', '三层实木'], price: '¥198', unit: '/㎡', hot: false, cover: ASSETS.materials.thumbs[1] },
	{ id: 3, name: '大地系列·艺术涂料', brand: '品牌: Farrow & Ball', tags: ['零VOC', '进口品牌'], price: '¥128', unit: '/㎡', hot: false, cover: ASSETS.materials.thumbs[2] }
]

export const STONE_MATERIALS = [
	{ id: 11, name: '极地雪岩石材', price: '¥299', unit: '/㎡', tags: ['环保', 'A级耐磨'], hot: true, cover: ASSETS.stones[0] },
	{ id: 12, name: '森影绿碳板', price: '¥268', unit: '/㎡', tags: ['绿碳', '进口'], new: true, cover: ASSETS.stones[1] },
	{ id: 13, name: '暖沙漫流大理石', price: '¥450', unit: '/㎡', tags: ['天然大理石'], eco: true, cover: ASSETS.stones[2] },
	{ id: 14, name: '曜黑碳精石', price: '¥380', unit: '/㎡', tags: ['哑光', '防滑'], hot: true, cover: ASSETS.stones[3] },
	{ id: 15, name: '云纹白岩板', price: '¥320', unit: '/㎡', tags: ['岩板', '大板'], new: true, cover: ASSETS.stones[0] },
	{ id: 16, name: '墨玉碳晶石', price: '¥410', unit: '/㎡', tags: ['碳晶', '耐磨'], eco: true, cover: ASSETS.stones[1] }
]

export const DESIGNER_TABS = ['全部', '现代简约', '意式轻奢', '法式浪漫', '侘寂风', '新中式']

export const DESIGNERS = [
	{ id: 1, name: '林语堂', rating: '4.9', projects: '128套', tags: ['现代简约', '全案设计', '别墅专精'], price: '¥280', unit: '/㎡', featured: true, badge: 'TOP设计师', cover: ASSETS.designers.covers[0], avatar: ASSETS.designers.avatars[0] },
	{ id: 2, name: '周雅文', rating: '4.8', projects: '86套', tags: ['意式轻奢', '软装搭配', '空间规划'], price: '¥220', unit: '/㎡', featured: false, cover: ASSETS.designers.covers[1], avatar: ASSETS.designers.avatars[1] },
	{ id: 3, name: '吴思远', rating: '4.7', projects: '64套', tags: ['侘寂风', '自然材质', '禅意空间'], price: '¥260', unit: '/㎡', featured: false, cover: ASSETS.designers.covers[2], avatar: ASSETS.designers.avatars[2] }
]

export const PROFILE_QUICK_LINKS = [
	{ icon: ICONS.quickOrder, label: '我的订单', bgClass: 'blue' },
	{ icon: ICONS.quickDesign, label: '设计方案', bgClass: 'blue' },
	{ icon: ICONS.quickCoupon, label: '优惠券', bgClass: 'orange' }
]

export const PROFILE_MENUS = [
	{ icon: ICONS.menuAddress, label: '地址管理' },
	{ icon: ICONS.menuService, label: '客服服务' },
	{ icon: ICONS.menuFeedback, label: '反馈建议' },
	{ icon: ICONS.menuSetting, label: '系统设置' }
]

export const CASE_DETAIL = {
	title: '嘉诚花园(南区)*号楼*单元*',
	tags: ['现代简约', '143㎡', '全包'],
	totalCost: '79935.42',
	construction: '61428',
	material: '18507.42',
	ownerBuy: '业主自购',
	gallery: ASSETS.caseDetail.gallery,
	constructionPhotos: ASSETS.caseDetail.construction,
	team: [
		{ role: '项目经理', name: '张经理' },
		{ role: '水电工', name: '李师傅' },
		{ role: '泥木工', name: '王师傅' },
		{ role: '油漆工', name: '赵师傅' }
	],
	dynamics: ['全部', '水电', '泥木', '油漆']
}

export const DESIGNER_PROFILE = {
	name: '张馨予私宅设计工作室',
	specialty: '擅长：意式极简 / 侘寂风',
	location: '坐标杭州，上百套别墅设计落地',
	cert: '国际 (香港) 建筑装饰协会室内设计',
	awards: '金奖室内设计师 | 全案设计 | 施工落地',
	tags: ['全案设计', '别墅专精', '在线中'],
	hero: ASSETS.designerProfile.hero,
	avatar: ASSETS.designerProfile.avatar,
	works: [
		{ title: '寻浙江 20 位别墅业主 | 免费户型规划', likes: '2.3w', cover: ASSETS.designerProfile.works[0] },
		{ title: '坐标杭州 / 一个别墅设计师的自述', likes: '1.8w', cover: ASSETS.designerProfile.works[1] },
		{ title: '现代简约风格 | 极简之美', likes: '9.6k', cover: ASSETS.designerProfile.works[2] },
		{ title: '全案交付 | 从毛坯到拎包入住', likes: '1.2w', cover: ASSETS.designerProfile.works[3] }
	]
}

export const WORK_DETAIL = {
	title: '杭州 500㎡ 雅居 | 东方极简·现代中式豪宅 ✨',
	desc: '本案汲取东方美学精髓，融合现代简约设计语言。通过天然木材、原石与光影的交错，重塑宁静、雅致且富有禅意的生活边界，让归家成为一场温润的精神洗礼 🥰。',
	location: '浙江 · 杭州',
	tags: ['#现代中式', '#东方极简', '#豪宅设计'],
	author: '张馨予私宅设计',
	publishTime: '发布于 昨天 12:57 杭州',
	hero: ASSETS.workDetail.hero,
	authorAvatar: ASSETS.designerProfile.avatar
}
