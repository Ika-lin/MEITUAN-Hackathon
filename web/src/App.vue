<script setup lang="ts">
import { computed, defineComponent, h, onMounted, ref, type PropType } from 'vue'
import {
  chatAgent,
  createTrip,
  getDiscoverCategories,
  getDiscoverEvents,
  getDiscoverPlaces,
  getTripDetail,
  getTripReminders,
  getTripRouteMap,
  getTrips,
  getTripWeather,
  getUserFootprints,
  getUserProfile,
  groupChat,
  groupPlan,
  type ChatPayload,
} from './api'

type Screen = 'home1' | 'home2' | 'onboarding' | 'ai1' | 'discover' | 'itinerary' | 'profile' | 'groups' | 'groupRoom' | 'groupSettings' | 'addMembers'
type UserId = 'u_demo_001' | 'u_demo_002' | 'u_demo_003'

interface CardData {
  title: string
  tags: string[]
  tagColor: string
  tagTextColor: string
  time: string
  photo: string
  cardBg: string
}

interface DemoUser {
  id: UserId
  name: string
  role: string
  icon: string
}

interface Friend {
  id: UserId
  name: string
  note: string
  avatar: string
}

interface GroupItem {
  id: string
  name: string
  desc: string
  unread: number
  members: UserId[]
}

interface ChatMessage {
  from: string
  text: string
  mine?: boolean
}

interface MiniCardView {
  title: string
  time: string
  photo: string
}

const activeScreen = ref<Screen>('home1')
const currentUserId = ref<UserId>('u_demo_001')
const userProfile = ref<any>(null)
const footprints = ref<any[]>([])
const discoverCategories = ref<string[]>(['全部'])
const discoverItems = ref<any[]>([])
const agentSuggestions = ref<any[]>([])
const discoverEvents = ref<any[]>([])
const selectedCategory = ref('全部')
const isLoadingDiscover = ref(false)
const isOnboarding = ref(false)
const onboardingStep = ref(0)
const onboardingReply = ref('')
const aiInput = ref('')
const aiReply = ref('')
const isChatting = ref(false)
const currentTrip = ref<any | null>(null)
const tripList = ref<any[]>([])
const selectedTripId = ref('')
const tripWeather = ref<any | null>(null)
const tripRouteMap = ref<any | null>(null)
const tripReminders = ref<any | null>(null)
const isLoadingTrips = ref(false)
const tripViewMode = ref<'list' | 'detail'>('list')
const itinerarySourceScreen = ref<Screen>('ai1')
const itineraryBusy = ref(false)
const itineraryNotice = ref('')
const aiMessages = ref<ChatMessage[]>([
  {
    from: '小薇',
    text: '我已经准备好结合你的画像、记忆和当前想法来规划。你可以直接说时间、地点、心情，或者问我“今天怎么安排”。',
  },
])
const selectedGroupId = ref('g_001')
const groupDraft = ref('')
const groupMessages = ref<ChatMessage[]>([
  { from: '你', text: '周末想找一个大家都舒服的安排。', mine: true },
  { from: '小周', text: '我想要轻松一点，别太赶路。' },
  { from: '阿琳', text: '可以有咖啡和展览，拍照也要好看。' },
])

const logoAsset = '/Frame 12.svg'
const levelsAsset = '/Levels.svg'
const wechatAsset = '/微信 1.svg'
const meituanAsset = '/美团 1.svg'
const appleAsset = '/苹果.svg'

const cardList: CardData[] = [
  {
    title: '约会夜晚计划',
    tags: ['夜景', '微醺', '约会'],
    tagColor: '#ffffff',
    tagTextColor: '#000000',
    time: '约3h · 氛围感',
    photo: '/cards/card-1.png',
    cardBg: 'rgba(197, 209, 249, 0.36)',
  },
  {
    title: '轻松恢复半日',
    tags: ['治愈', '展览', '休闲'],
    tagColor: '#6d7167',
    tagTextColor: '#ffffff',
    time: '半日 · 不赶路',
    photo: '/cards/card-2.png',
    cardBg: 'rgba(216, 204, 212, 0.64)',
  },
  {
    title: '一个人的慢下午',
    tags: ['咖啡', '独处', '放空'],
    tagColor: '#f4758c',
    tagTextColor: '#ffffff',
    time: '约2h · 少走路',
    photo: '/cards/card-3.png',
    cardBg: 'rgba(255, 226, 243, 0.47)',
  },
  {
    title: '城市漫游时刻',
    tags: ['City Walk', '探店', '出片'],
    tagColor: '#ffffff',
    tagTextColor: '#000000',
    time: '约2.5h · 好拍照',
    photo: '/cards/card-4.png',
    cardBg: 'rgba(211, 204, 245, 0.37)',
  },
]

const demoUsers: DemoUser[] = [
  { id: 'u_demo_001', name: '周末散步家', role: '咖啡 / 展览 / 城市散步', icon: appleAssetPath() },
  { id: 'u_demo_002', name: '轻松探店派', role: '美食 / 朋友局 / 不赶路', icon: wechatAssetPath() },
  { id: 'u_demo_003', name: '灵感收集者', role: '书店 / 拍照 / 小众地点', icon: meituanAssetPath() },
]

const friendList: Friend[] = [
  { id: 'u_demo_001', name: '周末散步家', note: '偏好咖啡和安静空间', avatar: '周' },
  { id: 'u_demo_002', name: '轻松探店派', note: '喜欢饭点后轻松集合', avatar: '探' },
  { id: 'u_demo_003', name: '灵感收集者', note: '适合展览和拍照路线', avatar: '灵' },
]

const groups = ref<GroupItem[]>([
  { id: 'g_001', name: '周末去哪儿', desc: '3 人 · AI 正在协调大家偏好', unread: 2, members: ['u_demo_001', 'u_demo_002', 'u_demo_003'] },
  { id: 'g_002', name: '安福路饭搭子', desc: '2 人 · 咖啡、简餐、散步', unread: 0, members: ['u_demo_001', 'u_demo_002'] },
])

const currentCardIndex = ref(0)
let touchStartX = 0
let touchEndX = 0
let isMouseDragging = false
let mouseStartX = 0
let mouseEndX = 0

function appleAssetPath() {
  return appleAsset
}

function wechatAssetPath() {
  return wechatAsset
}

function meituanAssetPath() {
  return meituanAsset
}

const ai1LevelsAsset = 'https://www.figma.com/api/mcp/asset/35bb016e-759a-449f-b9af-7ef15e90c5f3'
const ai1SparkIconAsset = 'https://www.figma.com/api/mcp/asset/6dd54065-b1b9-4654-8362-9e0c1ff8543e'
const ai1MicAsset = 'https://www.figma.com/api/mcp/asset/4e819871-83a0-4659-aeb8-09d6741f852b'
const ai1SearchAsset = 'https://www.figma.com/api/mcp/asset/a2d32556-ed0d-45f1-b69d-e8fefe4c4c15'
const ai1NavCenterAsset = 'https://www.figma.com/api/mcp/asset/2d7f8b06-66d4-41ff-9503-73c02a38afe8'
const ai1NavLeftAsset = 'https://www.figma.com/api/mcp/asset/1b02c613-4c53-4f59-be0b-3831acae10bc'
const ai1NavRightAsset = 'https://www.figma.com/api/mcp/asset/bbdb994e-672d-4cb1-816a-d8fcd62348c7'
const ai1MicGroupAsset = 'https://www.figma.com/api/mcp/asset/a2768da7-ad02-4777-9a79-ecf393d548e3'

const ProductHeader = defineComponent({
  props: {
    title: { type: String, required: true },
    levelsAsset: { type: String, required: true },
    back: { type: Boolean, default: false },
  },
  emits: ['back'],
  setup(props, { emit }) {
    return () => h('header', { class: 'product-header' }, [
      h('div', { class: 'ai1-status-time' }, '9:41'),
      h('div', { class: 'ai1-status-island' }),
      h('img', { src: props.levelsAsset, alt: '', class: 'ai1-status-levels' }),
      props.back
        ? h('button', { type: 'button', class: 'product-back-btn', 'aria-label': '返回', onClick: () => emit('back') }, '‹')
        : null,
      h('h1', props.title),
    ])
  },
})

const BottomNav = defineComponent({
  props: {
    activeScreen: { type: String as PropType<Screen>, required: true },
    assets: {
      type: Object as PropType<{ left: string; search: string; center: string; map: string; group: string }>,
      required: true,
    },
  },
  emits: ['navigate'],
  setup(props, { emit }) {
    const nav = (screen: Screen) => emit('navigate', screen)
    return () => h('div', { class: 'ai1-nav-layer' }, [
      h('div', { class: 'ai1-nav-bg' }),
      h('button', { type: 'button', class: ['nav-hit', props.activeScreen === 'profile' && 'active'], style: 'left:41px;top:768px;', 'aria-label': '我的', onClick: () => nav('profile') }, [
        h('img', { src: props.assets.left, alt: '', class: 'ai1-nav-icon-img' }),
      ]),
      h('button', { type: 'button', class: ['nav-hit', 'ai1-nav-circle', 'ai1-nav-dim', props.activeScreen === 'discover' && 'active'], style: 'left:113px;top:768px;', 'aria-label': '发现', onClick: () => nav('discover') }, [
        h('img', { src: props.assets.search, alt: '', class: 'ai1-nav-inner' }),
      ]),
      h('button', { type: 'button', class: ['nav-hit', 'ai1-nav-circle', 'ai1-nav-black', props.activeScreen === 'ai1' && 'active'], style: 'left:177px;top:768px;', 'aria-label': 'AI 首页', onClick: () => nav('ai1') }, [
        h('img', { src: props.assets.center, alt: '', class: 'ai1-nav-center-icon' }),
      ]),
      h('button', { type: 'button', class: ['nav-hit', props.activeScreen === 'itinerary' && 'active'], style: 'left:240px;top:768px;', 'aria-label': '行程', onClick: () => nav('itinerary') }, [
        h('img', { src: props.assets.map, alt: '', class: 'ai1-nav-icon-img' }),
      ]),
      h('button', { type: 'button', class: ['nav-hit', 'ai1-nav-circle', 'ai1-nav-dim', props.activeScreen === 'groups' && 'active'], style: 'left:305px;top:768px;', 'aria-label': '群聊', onClick: () => nav('groups') }, [
        h('img', { src: props.assets.group, alt: '', class: 'ai1-nav-inner' }),
      ]),
    ])
  },
})

const selectedGroup = computed(() => groups.value.find((group) => group.id === selectedGroupId.value) || groups.value[0])
const groupMembers = computed(() => selectedGroup.value.members.map((id) => friendList.find((friend) => friend.id === id)).filter(Boolean) as Friend[])
const profileTags = computed(() => {
  const tags = userProfile.value?.personaTags || userProfile.value?.favoriteTags || []
  return tags.length ? tags.slice(0, 4) : ['新用户', '正在学习']
})
const currentMiniCard = computed<MiniCardView>(() => {
  const source = agentSuggestions.value.length ? agentSuggestions.value : discoverItems.value
  const item = source[currentCardIndex.value % Math.max(source.length, 1)]
  if (item) {
    return {
      title: item.name || item.title || item.category || '附近推荐',
      time: `${item.category || item.badge || '推荐'} · ${item.subtitle || item.neighborhood || item.district || 'agent 推荐'}`,
      photo: item.heroImage || cardList[currentCardIndex.value % cardList.length].photo,
    }
  }

  return cardList[currentCardIndex.value]
})
const aiQuickPrompts = computed(() => [
  '我今天只有 2 小时',
  '想轻松一点少走路',
  '帮我根据画像推荐',
  currentMiniCard.value.title,
])
const itineraryStops = computed(() => currentTrip.value?.stops || [])
const itineraryTitle = computed(() => currentTrip.value?.title || '还没有生成行程')
const itineraryStartAddress = computed(() => itineraryStops.value[0]?.address || '告诉小薇你的出发区域')
const itineraryEndAddress = computed(() => {
  const last = itineraryStops.value[itineraryStops.value.length - 1]
  return last?.address || '生成后会显示终点'
})
const itineraryStats = computed(() => {
  const overview = currentTrip.value?.overview || {}
  const totalDuration = currentTrip.value?.totalDuration || overview.duration || '待规划'
  const transportMode = currentTrip.value?.transportMode || overview.transportMode || 'AI 规划中'
  const totalBudget = currentTrip.value?.totalBudget || currentTrip.value?.totalBudget || '待估算'
  const walkMinutes = currentTrip.value?.totalWalkMinutes ?? overview.totalWalkMinutes ?? overview.walkDurationMinutes
  return [
    { label: '总时长', value: totalDuration },
    { label: '交通方式', value: transportMode },
    { label: '预算估测', value: totalBudget },
    { label: '步行时间', value: typeof walkMinutes === 'number' ? `约${walkMinutes}分钟` : '待计算' },
  ]
})
const groupedTrips = computed(() => {
  const groupsByDate = new Map<string, any[]>()
  for (const trip of tripList.value) {
    const key = trip.date || '未定日期'
    groupsByDate.set(key, [...(groupsByDate.get(key) || []), trip])
  }
  return Array.from(groupsByDate.entries()).map(([date, items]) => ({ date, items }))
})
const routeMarkers = computed(() => tripRouteMap.value?.markers || currentTrip.value?.routeMap?.markers || [])
const reminderToday = computed(() => tripReminders.value?.today || [])
const reminderChecklist = computed(() => tripReminders.value?.packingChecklist || [])
const miniCardCount = computed(() => agentSuggestions.value.length || discoverItems.value.length || cardList.length)

onMounted(() => {
  void loadDiscover()
  const savedUser = window.localStorage.getItem('weekendgo-user') as UserId | null
  const onboarded = window.localStorage.getItem(`weekendgo-onboarded-${savedUser || 'u_demo_001'}`)
  if (savedUser) {
    currentUserId.value = savedUser
    activeScreen.value = onboarded ? 'ai1' : 'home2'
    void loadUserData(savedUser)
  }
})

function handleTouchStart(e: TouchEvent) {
  touchStartX = e.touches[0].clientX
}

function handleTouchEnd(e: TouchEvent) {
  touchEndX = e.changedTouches[0].clientX
  moveCard(touchStartX - touchEndX)
}

function handleMouseDown(e: MouseEvent) {
  isMouseDragging = true
  mouseStartX = (e as any).pageX || e.clientX
  mouseEndX = (e as any).pageX || e.clientX
}

function handleMouseMove(e: MouseEvent) {
  if (!isMouseDragging) return
  mouseEndX = (e as any).pageX || e.clientX
}

function handleMouseUp(e: MouseEvent) {
  if (!isMouseDragging) return
  isMouseDragging = false
  mouseEndX = (e as any).pageX || e.clientX
  moveCard(mouseStartX - mouseEndX)
}

function moveCard(diff: number) {
  if (Math.abs(diff) <= 50) return
  const total = miniCardCount.value
  currentCardIndex.value = diff > 0
    ? (currentCardIndex.value + 1) % total
    : (currentCardIndex.value - 1 + total) % total
}

function goToHome2() {
  activeScreen.value = 'home2'
}

function goToAi1() {
  activeScreen.value = 'ai1'
}

function navigate(screen: Screen) {
  activeScreen.value = screen
  if (screen === 'discover') void loadDiscover()
  if (screen === 'itinerary') {
    tripViewMode.value = 'list'
    void loadTrips()
  }
}

async function loginAs(userId: UserId) {
  currentUserId.value = userId
  window.localStorage.setItem('weekendgo-user', userId)
  await loadUserData(userId)
  const onboarded = window.localStorage.getItem(`weekendgo-onboarded-${userId}`)
  if (onboarded) {
    activeScreen.value = 'ai1'
  } else {
    await startOnboarding()
  }
}

async function startOnboarding() {
  activeScreen.value = 'onboarding'
  isOnboarding.value = true
  onboardingStep.value = 0
  onboardingReply.value = ''
  const ticker = window.setInterval(() => {
    onboardingStep.value = Math.min(onboardingStep.value + 1, 3)
  }, 700)

  try {
    const result = await chatAgent({
      userId: currentUserId.value,
      sessionId: `onboarding-${currentUserId.value}`,
      action: 'onboarding_profile',
      message: '第一次登录，请基于我的历史记录生成简短用户画像，不要直接生成行程。',
    })
    onboardingReply.value = normalizeReply(result)
  } catch {
    onboardingReply.value = '我已经读取到你的偏好线索：会结合真实到店、消费、搜索和出行动作来理解你，而不是把一次搜索当成到店。'
  } finally {
    window.clearInterval(ticker)
    onboardingStep.value = 3
    isOnboarding.value = false
    window.localStorage.setItem(`weekendgo-onboarded-${currentUserId.value}`, '1')
  }
}

async function loadUserData(userId = currentUserId.value) {
  try {
    userProfile.value = await getUserProfile(userId)
  } catch {
    userProfile.value = null
  }
  try {
    const data = await getUserFootprints(userId)
    footprints.value = data.footprints || []
  } catch {
    footprints.value = []
  }
}

async function loadDiscover(category = selectedCategory.value) {
  isLoadingDiscover.value = true
  try {
    const [categories, places, events] = await Promise.all([
      getDiscoverCategories(),
      getDiscoverPlaces(category),
      getDiscoverEvents(),
    ])
    discoverCategories.value = categories.categories || ['全部']
    discoverItems.value = places.items || []
    discoverEvents.value = events.events || []
    if (currentCardIndex.value >= miniCardCount.value) currentCardIndex.value = 0
  } finally {
    isLoadingDiscover.value = false
  }
}

async function chooseCategory(category: string) {
  selectedCategory.value = category
  await loadDiscover(category)
}

async function sendAiMessage() {
  const message = aiInput.value.trim()
  if (!message || isChatting.value) return
  isChatting.value = true
  aiInput.value = ''
  aiMessages.value.push({ from: '你', text: message, mine: true })
  try {
    const result = await chatAgent({
      userId: currentUserId.value,
      sessionId: `main-${currentUserId.value}`,
      message,
    })
    aiReply.value = normalizeReply(result)
    aiMessages.value.push({ from: '小薇', text: aiReply.value })
    if (result.suggestions?.length) {
      agentSuggestions.value = result.suggestions
      currentCardIndex.value = 0
    }
    if (result.trip) {
      await showTrip(result.trip, 'ai1')
    }
  } catch {
    aiReply.value = '后端暂时没有响应，我先保留你的想法，稍后可以继续让 AI 规划。'
    aiMessages.value.push({ from: '小薇', text: aiReply.value })
  } finally {
    isChatting.value = false
  }
}

async function generateByCard() {
  aiInput.value = `我想要${currentMiniCard.value.title}，帮我规划一条路线`
  await sendAiMessage()
}

async function askQuickPrompt(prompt: string) {
  aiInput.value = prompt
  await sendAiMessage()
}

async function sendGroupMessage() {
  const text = groupDraft.value.trim()
  if (!text) return
  groupMessages.value.push({ from: '你', text, mine: true })
  groupDraft.value = ''
  try {
    const result = await groupChat({ sessionId: selectedGroup.value.id, message: text })
    for (const item of result.messages || []) {
      groupMessages.value.push({ from: item.persona, text: item.text })
    }
  } catch {
    groupMessages.value.push({ from: 'Weekendgo AI', text: '我先记录大家的想法，等服务恢复后继续协商。' })
  }
}

async function synthesizeGroupPlan() {
  const ids = selectedGroup.value.members
  try {
    const result = await groupPlan({
      sessionId: selectedGroup.value.id,
      user_ids: ids,
      message: '请综合群成员画像，生成适合大家的周末路线。',
    })
    groupMessages.value.push({ from: 'Weekendgo AI', text: result.reply || '已综合大家偏好，生成一条折中路线。' })
    if (result.trip) {
      await showTrip(result.trip, 'groupRoom')
    } else {
      activeScreen.value = 'itinerary'
    }
  } catch {
    groupMessages.value.push({ from: 'Weekendgo AI', text: '我会优先平衡预算、步行距离和每个人的兴趣。' })
  }
}

function toggleMember(id: UserId) {
  const group = selectedGroup.value
  if (group.members.includes(id)) {
    group.members = group.members.filter((member) => member !== id)
  } else {
    group.members = [...group.members, id]
  }
}

function logout() {
  window.localStorage.removeItem('weekendgo-user')
  activeScreen.value = 'home2'
}

function clearCurrentFirstLogin() {
  window.localStorage.removeItem(`weekendgo-onboarded-${currentUserId.value}`)
  activeScreen.value = 'home2'
}

function normalizeReply(result: ChatPayload) {
  return result.reply || result.actions?.map((action) => action.label).join('，') || '我已经理解你的偏好，可以开始使用了。'
}

function stopOrder(stop: any, index: number | string) {
  return stop.order || stop.index || Number(index) + 1
}

async function loadTrips() {
  isLoadingTrips.value = true
  try {
    const data = await getTrips(currentUserId.value)
    tripList.value = data.items || []
  } catch {
    tripList.value = currentTrip.value
      ? [tripToListItem(currentTrip.value)]
      : []
  } finally {
    isLoadingTrips.value = false
  }
}

function tripToListItem(trip: any) {
  const stops = trip.stops || []
  const overview = trip.overview || {}
  return {
    tripId: trip.tripId || trip.planId || 'draft',
    planId: trip.planId,
    title: trip.title || 'AI 生成路线',
    date: trip.date || new Date().toISOString().slice(0, 10),
    status: trip.status || 'draft',
    type: trip.type || overview.type || 'AI 路线',
    duration: trip.totalDuration || overview.duration || '',
    totalBudget: trip.totalBudget || '',
    transportMode: trip.transportMode || overview.transportMode || '',
    totalWalkMinutes: trip.totalWalkMinutes ?? overview.totalWalkMinutes,
    stopCount: stops.length,
    firstStop: stops[0]?.name || '',
    lastStop: stops[stops.length - 1]?.name || '',
    source: trip.source || overview.source || 'agent',
  }
}

async function showTrip(trip: any, source: Screen = 'ai1') {
  itinerarySourceScreen.value = source
  itineraryNotice.value = ''
  activeScreen.value = 'itinerary'
  tripViewMode.value = 'detail'

  try {
    const saved = trip.tripId
      ? { tripId: trip.tripId, trip }
      : await createTrip({
          userId: currentUserId.value,
          planId: trip.planId || '',
          plan: trip,
          date: new Date().toISOString().slice(0, 10),
          city: trip.city || '上海',
        })
    selectedTripId.value = saved.tripId
    await loadTripDetail(saved.tripId, saved.trip || trip)
    await loadTrips()
  } catch {
    currentTrip.value = trip
    selectedTripId.value = trip.planId || 'draft'
    tripWeather.value = mockWeatherForTrip(trip)
    tripRouteMap.value = mockRouteForTrip(trip)
    tripReminders.value = mockRemindersForTrip(trip)
  }
  initItineraryMap()
}

async function openTripDetail(tripId: string) {
  selectedTripId.value = tripId
  itineraryNotice.value = ''
  tripViewMode.value = 'detail'
  await loadTripDetail(tripId)
}

async function loadTripDetail(tripId: string, fallbackTrip?: any) {
  try {
    const [detail, routeMap, weather, reminders] = await Promise.all([
      getTripDetail(tripId),
      getTripRouteMap(tripId),
      getTripWeather(tripId),
      getTripReminders(tripId),
    ])
    currentTrip.value = detail
    tripRouteMap.value = routeMap
    tripWeather.value = weather
    tripReminders.value = reminders
  } catch {
    currentTrip.value = fallbackTrip || currentTrip.value
    tripWeather.value = mockWeatherForTrip(currentTrip.value)
    tripRouteMap.value = mockRouteForTrip(currentTrip.value)
    tripReminders.value = mockRemindersForTrip(currentTrip.value)
  }
  initItineraryMap()
}

let itineraryMap: any = null
function initItineraryMap() {
  const stops = currentTrip.value?.stops || []
  if (stops.length === 0) return
  setTimeout(() => {
    const el = document.getElementById('itinerary-map')
    if (!el) return
    if (itineraryMap) { itineraryMap.remove(); itineraryMap = null }
    const L = (window as any).L
    if (!L) return
    const map = L.map(el, { zoomControl: false, attributionControl: false }).setView([31.215, 121.45], 14)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map)
    const markers: any[] = []
    stops.forEach((s: any, i: number) => {
      // 用 POI 的真实坐标或默认偏移
      const lat = s.lat || (31.212 + i * 0.002)
      const lng = s.lng || (121.44 + i * 0.003)
      const m = L.circleMarker([lat, lng], {
        radius: 8, color: '#461c3a', fillColor: '#fff', fillOpacity: 1, weight: 2
      }).addTo(map).bindPopup(`<b>${s.name || s.poiName}</b>`)
      markers.push(m)
      L.marker([lat, lng], {
        icon: L.divIcon({ html: `<div style="background:#461c3a;color:#fff;width:20px;height:20px;border-radius:50%;text-align:center;line-height:20px;font-size:11px;font-weight:700">${s.order || i+1}</div>`, className: '' })
      }).addTo(map)
    })
    if (markers.length >= 2) {
      const group = L.featureGroup(markers)
      map.fitBounds(group.getBounds().pad(0.2))
    }
    itineraryMap = map
  }, 300)
}

function backToTripList() {
  tripViewMode.value = 'list'
  void loadTrips()
}

function mockWeatherForTrip(_trip: any) {
  return {
    provider: 'frontend_mock_weather_fallback',
    condition: '多云转晴',
    temperatureText: '24-29°C',
    comfortLevel: '适合步行',
    rainProbability: 12,
    agentTips: ['天气适合步行，下午注意防晒。', '路线可保留 10-15 分钟缓冲。'],
  }
}

function mockRouteForTrip(trip: any) {
  return {
    provider: 'frontend_mock_route_fallback',
    markers: (trip?.stops || []).map((stop: any, index: number) => ({
      order: stop.order || stop.index || index + 1,
      name: stop.name,
      lat: stop.lat,
      lng: stop.lng,
      category: stop.category,
    })),
    agentPath: 'generate_structured_trip -> route_map',
  }
}

function mockRemindersForTrip(_trip: any) {
  return {
    today: ['已检查天气和步行强度', '建议保留 15 分钟机动时间'],
    packingChecklist: ['充电宝', '遮阳伞'],
  }
}

async function requestItineraryChange(message: string) {
  if (itineraryBusy.value) return
  itineraryBusy.value = true
  itineraryNotice.value = '小薇正在重新评估路线...'
  try {
    const result = await chatAgent({
      userId: currentUserId.value,
      sessionId: `main-${currentUserId.value}`,
      message: currentTrip.value
        ? `${message}。这是当前路线：${currentTrip.value.title || ''}，请基于现有路线重新给出完整结构化 trip。`
        : message,
    })
    const reply = normalizeReply(result)
    aiMessages.value.push({ from: '你', text: message, mine: true })
    aiMessages.value.push({ from: '小薇', text: reply })
    if (result.trip) {
      await showTrip(result.trip, 'itinerary')
      itineraryNotice.value = '已根据你的要求更新路线。'
    } else {
      itineraryNotice.value = reply
    }
  } catch {
    itineraryNotice.value = '后端暂时没有响应，稍后可以回到 AI 聊天继续调整。'
  } finally {
    itineraryBusy.value = false
  }
}
</script>

<template>
  <div class="preview-page">
    <div class="iphone-shell">
      <div class="iphone-body">
        <div class="dynamic-island"></div>

        <div class="app-container">
          <main
            v-if="activeScreen === 'home1'"
            class="screen home1-screen"
            role="button"
            tabindex="0"
            @click="goToHome2"
            @keyup.enter="goToHome2"
            @keyup.space.prevent="goToHome2"
          >
            <div class="screen-bg" aria-hidden="true">
              <div class="bg-blob bg-blob-rose"></div>
              <div class="bg-blob bg-blob-gold"></div>
              <div class="bg-blob bg-blob-ivory"></div>
              <div class="bg-blob bg-blob-mist"></div>
            </div>
            <header class="status-bar">
              <div class="status-time">9:41</div>
              <div class="status-island"></div>
              <img :src="levelsAsset" alt="" class="status-levels" />
            </header>
            <section class="brand-block">
              <img :src="logoAsset" alt="Weekendgo Logo" class="brand-logo" />
              <h1 class="brand-title">Weekendgo</h1>
            </section>
            <p class="tagline">你的闲时逛逛搭子</p>
            <footer class="home-indicator-wrap">
              <div class="home-indicator"></div>
            </footer>
          </main>

          <main v-else-if="activeScreen === 'home2'" class="screen home2-screen">
            <div class="screen-bg" aria-hidden="true">
              <div class="bg-blob bg-blob-rose home2-blob-rose"></div>
              <div class="bg-blob bg-blob-gold home2-blob-gold"></div>
              <div class="bg-blob bg-blob-ivory home2-blob-ivory"></div>
              <div class="bg-blob bg-blob-mist home2-blob-mist"></div>
            </div>
            <header class="status-bar">
              <div class="status-time">9:41</div>
              <div class="status-island"></div>
              <img :src="levelsAsset" alt="" class="status-levels" />
            </header>
            <section class="login-brand-block">
              <img :src="logoAsset" alt="Weekendgo Logo" class="login-brand-logo" />
              <h2 class="login-brand-title">Weekendgo</h2>
            </section>
            <section class="login-copy-block">
              <h1 class="login-title">轻松规划你的周末闲时活动 让每一刻都不浪费</h1>
            </section>
            <section class="login-form">
              <label class="login-field"><span class="login-field-label">昵称</span></label>
              <label class="login-field"><span class="login-field-label">手机号</span></label>
              <label class="login-field login-field-password"><span class="login-field-label">密码</span></label>
            </section>
            <button type="button" class="login-button" @click="loginAs(currentUserId)">登录</button>
            <section class="login-divider-row">
              <div class="login-divider-line"></div>
              <p class="login-divider-text">选择 Demo 用户登录</p>
              <div class="login-divider-line"></div>
            </section>
            <section class="social-login-row">
              <button
                v-for="user in demoUsers"
                :key="user.id"
                type="button"
                class="social-login-button demo-login-button"
                :aria-label="`${user.name} 登录`"
                @click="loginAs(user.id)"
              >
                <img :src="user.icon" alt="" class="social-login-icon" :class="{ 'social-login-icon-apple': user.id === 'u_demo_001' }" />
                <span class="demo-login-tip">{{ user.name }}</span>
              </button>
            </section>
            <p class="signup-hint">
              当前：{{ demoUsers.find((user) => user.id === currentUserId)?.name }}
            </p>
            <footer class="home-indicator-wrap">
              <div class="home-indicator"></div>
            </footer>
          </main>

          <main v-else-if="activeScreen === 'onboarding'" class="screen product-screen">
            <div class="ai1-bg" aria-hidden="true"></div>
            <header class="ai1-status-bar">
              <div class="ai1-status-time">9:41</div>
              <div class="ai1-status-island"></div>
              <img :src="ai1LevelsAsset" alt="" class="ai1-status-levels" />
            </header>
            <section class="onboarding-panel">
              <p class="product-kicker">Weekendgo AI</p>
              <h1>正在理解你</h1>
              <div class="analysis-orbit" :class="{ done: !isOnboarding }">
                <span></span><span></span><span></span>
              </div>
              <div class="analysis-steps">
                <p :class="{ active: onboardingStep >= 0 }">读取真实到店与消费记录</p>
                <p :class="{ active: onboardingStep >= 1 }">区分搜索兴趣、出行信号和实际偏好</p>
                <p :class="{ active: onboardingStep >= 2 }">整理预算、时间、社交风格</p>
                <p :class="{ active: onboardingStep >= 3 }">生成可用于 Agent 的长期画像</p>
              </div>
              <p class="analysis-reply">{{ onboardingReply || 'AI 会先学习你的行为数据，不会第一次登录就直接替你生成行程。' }}</p>
              <button type="button" class="product-primary" :disabled="isOnboarding" @click="goToAi1">
                {{ isOnboarding ? '分析中...' : '开始使用' }}
              </button>
            </section>
            <footer class="home-indicator-wrap">
              <div class="home-indicator"></div>
            </footer>
          </main>

          <main v-else-if="activeScreen === 'ai1'" class="screen ai1-screen" @mousemove="handleMouseMove" @mouseup="handleMouseUp" @mouseleave="handleMouseUp">
            <div class="ai1-bg" aria-hidden="true"></div>
            <header class="ai1-status-bar">
              <div class="ai1-status-time">9:41</div>
              <div class="ai1-status-island"></div>
              <img :src="ai1LevelsAsset" alt="" class="ai1-status-levels" />
            </header>
            <section class="ai-chat-title">
              <p>小薇</p>
              <h1>和我说说今天怎么过</h1>
            </section>
            <section class="ai-chat-thread" aria-label="AI 对话记录">
              <div v-for="(message, index) in aiMessages" :key="index" class="ai-message" :class="{ mine: message.mine }">
                <span>{{ message.from }}</span>
                <p>{{ message.text }}</p>
              </div>
              <div v-if="isChatting" class="ai-message typing">
                <span>小薇</span>
                <p>正在结合你的画像、记忆和可用工具思考...</p>
              </div>
            </section>
            <section class="ai-suggestion-row" aria-label="快捷提问">
              <button v-for="prompt in aiQuickPrompts" :key="prompt" type="button" @click="askQuickPrompt(prompt)">
                {{ prompt }}
              </button>
            </section>
            <div class="ai-mini-card" @touchstart="handleTouchStart" @touchend="handleTouchEnd" @mousedown="handleMouseDown">
              <img :src="currentMiniCard.photo" :alt="currentMiniCard.title" />
              <div>
                <span>{{ currentMiniCard.time }}</span>
                <strong>{{ currentMiniCard.title }}</strong>
              </div>
              <button type="button" @click="generateByCard">Go</button>
            </div>
            <form class="ai1-input-bar ai-chat-input" @submit.prevent="sendAiMessage">
              <img :src="ai1SparkIconAsset" alt="" class="ai1-input-spark" />
              <input
                v-model="aiInput"
                type="text"
                class="ai1-input-field"
                aria-label="输入出行想法"
                placeholder="告诉我今天的时间、地点或心情"
                enterkeyhint="send"
              />
              <button type="submit" class="ai-input-submit" aria-label="发送">
                <img :src="ai1MicGroupAsset" alt="" class="ai1-input-mic" />
              </button>
            </form>
            <BottomNav :active-screen="activeScreen" :assets="{ left: ai1NavLeftAsset, search: ai1SearchAsset, center: ai1NavCenterAsset, map: ai1NavRightAsset, group: ai1MicAsset }" @navigate="navigate" />
            <footer class="home-indicator-wrap">
              <div class="home-indicator"></div>
            </footer>
          </main>

          <main v-else-if="activeScreen === 'discover'" class="screen product-screen">
            <ProductHeader title="发现" :levels-asset="levelsAsset" />
            <section class="product-scroll">
              <div class="category-row">
                <button v-for="category in discoverCategories" :key="category" class="product-chip" :class="{ active: selectedCategory === category }" @click="chooseCategory(category)">
                  {{ category }}
                </button>
              </div>
              <p v-if="isLoadingDiscover" class="product-muted">正在连接后端发现数据...</p>
              <article v-for="event in discoverEvents.slice(0, 2)" :key="event.eventId || event.name" class="wide-tile">
                <span>活动</span>
                <h2>{{ event.title || event.name }}</h2>
                <p>{{ event.city || '上海' }} · {{ event.dateText || event.time || '周末可约' }}</p>
              </article>
              <div class="discover-grid">
                <article v-for="item in discoverItems.slice(0, 8)" :key="item.itemId" class="discover-card">
                  <span>{{ item.badge }}</span>
                  <h3>{{ item.name }}</h3>
                  <p>{{ item.subtitle || item.category }}</p>
                </article>
              </div>
            </section>
            <BottomNav :active-screen="activeScreen" :assets="{ left: ai1NavLeftAsset, search: ai1SearchAsset, center: ai1NavCenterAsset, map: ai1NavRightAsset, group: ai1MicAsset }" @navigate="navigate" />
          </main>

          <main v-else-if="activeScreen === 'profile'" class="screen product-screen">
            <ProductHeader title="我的" :levels-asset="levelsAsset" />
            <section class="product-scroll profile-scroll">
              <div class="profile-hero">
                <div class="profile-avatar">{{ userProfile?.nickname?.slice(0, 1) || '我' }}</div>
                <div>
                  <h1>{{ userProfile?.nickname || demoUsers.find((user) => user.id === currentUserId)?.name }}</h1>
                  <p>{{ userProfile?.personaSummary || '画像还在完善中' }}</p>
                </div>
              </div>
              <div class="profile-tags">
                <span v-for="tag in profileTags" :key="tag">{{ tag }}</span>
              </div>
              <section class="profile-section">
                <h2>好友列表</h2>
                <button v-for="friend in friendList" :key="friend.id" class="friend-row" @click="currentUserId = friend.id">
                  <span>{{ friend.avatar }}</span>
                  <strong>{{ friend.name }}</strong>
                  <em>{{ friend.note }}</em>
                </button>
              </section>
              <section class="profile-section">
                <h2>最近足迹</h2>
                <p v-for="item in footprints.slice(0, 4)" :key="`${item.date}-${item.poiName}`" class="footprint-row">
                  {{ item.date }} · {{ item.poiName }} · {{ item.category }}
                </p>
              </section>
              <button type="button" class="product-primary" @click="clearCurrentFirstLogin">清理当前用户首次登录</button>
              <button type="button" class="product-secondary" @click="logout">退出登录</button>
            </section>
            <BottomNav :active-screen="activeScreen" :assets="{ left: ai1NavLeftAsset, search: ai1SearchAsset, center: ai1NavCenterAsset, map: ai1NavRightAsset, group: ai1MicAsset }" @navigate="navigate" />
          </main>

          <main v-else-if="activeScreen === 'groups'" class="screen product-screen">
            <ProductHeader title="群聊" :levels-asset="levelsAsset" />
            <section class="product-scroll group-list">
              <button v-for="group in groups" :key="group.id" class="group-row" @click="selectedGroupId = group.id; activeScreen = 'groupRoom'">
                <span class="group-avatar">{{ group.name.slice(0, 1) }}</span>
                <span>
                  <strong>{{ group.name }}</strong>
                  <em>{{ group.desc }}</em>
                </span>
                <b v-if="group.unread">{{ group.unread }}</b>
              </button>
            </section>
            <BottomNav :active-screen="activeScreen" :assets="{ left: ai1NavLeftAsset, search: ai1SearchAsset, center: ai1NavCenterAsset, map: ai1NavRightAsset, group: ai1MicAsset }" @navigate="navigate" />
          </main>

          <main v-else-if="activeScreen === 'groupRoom'" class="screen product-screen">
            <ProductHeader :title="selectedGroup.name" :levels-asset="levelsAsset" back @back="activeScreen = 'groups'" />
            <button type="button" class="group-setting-btn" @click="activeScreen = 'groupSettings'">设置</button>
            <section class="chat-scroll">
              <div v-for="(message, index) in groupMessages" :key="index" class="chat-bubble" :class="{ mine: message.mine }">
                <span>{{ message.from }}</span>
                <p>{{ message.text }}</p>
              </div>
            </section>
            <form class="group-input" @submit.prevent="sendGroupMessage">
              <input v-model="groupDraft" placeholder="和大家商量一下..." />
              <button type="submit">发送</button>
            </form>
          </main>

          <main v-else-if="activeScreen === 'groupSettings'" class="screen product-screen">
            <ProductHeader title="群聊设置" :levels-asset="levelsAsset" back @back="activeScreen = 'groupRoom'" />
            <section class="product-scroll profile-scroll">
              <div class="setting-members">
                <button v-for="friend in groupMembers" :key="friend.id" class="member-dot">
                  <span>{{ friend.avatar }}</span>
                  <em>{{ friend.name }}</em>
                </button>
                <button class="member-dot add" @click="activeScreen = 'addMembers'">
                  <span>+</span>
                  <em>添加</em>
                </button>
              </div>
              <button type="button" class="product-primary" @click="synthesizeGroupPlan">让 AI 综合大家偏好</button>
              <button type="button" class="product-secondary" @click="activeScreen = 'groups'">退出当前群聊</button>
            </section>
          </main>

          <main v-else-if="activeScreen === 'addMembers'" class="screen product-screen">
            <ProductHeader title="添加成员" :levels-asset="levelsAsset" back @back="activeScreen = 'groupSettings'" />
            <section class="product-scroll group-list">
              <button v-for="friend in friendList" :key="friend.id" class="friend-row" @click="toggleMember(friend.id)">
                <span>{{ friend.avatar }}</span>
                <strong>{{ friend.name }}</strong>
                <em>{{ selectedGroup.members.includes(friend.id) ? '已在群聊' : '点击添加' }}</em>
              </button>
            </section>
          </main>

          <main v-else-if="activeScreen === 'itinerary'" class="screen itinerary-screen">
            <div class="itinerary-bg-decoration"></div>
            <header class="ai1-status-bar">
              <div class="ai1-status-time">9:41</div>
              <div class="ai1-status-island"></div>
              <img :src="levelsAsset" alt="" class="ai1-status-levels" />
            </header>
            <button type="button" class="itinerary-back-btn" @click="tripViewMode === 'detail' ? backToTripList() : activeScreen = itinerarySourceScreen">返回</button>

            <section v-if="tripViewMode === 'list'" class="trip-list-page">
              <div class="trip-list-header">
                <p>Weekendgo Trips</p>
                <h1>我的行程计划</h1>
                <button type="button" @click="activeScreen = 'ai1'">找小薇生成</button>
              </div>

              <p v-if="isLoadingTrips" class="product-muted">正在从行程 API 读取计划...</p>
              <section v-for="group in groupedTrips" :key="group.date" class="trip-day-group">
                <h2>{{ group.date }}</h2>
                <button v-for="trip in group.items" :key="trip.tripId" type="button" class="trip-list-row" @click="openTripDetail(trip.tripId)">
                  <span class="trip-row-avatar">{{ trip.type?.slice(0, 1) || '行' }}</span>
                  <span class="trip-row-main">
                    <strong>{{ trip.title }}</strong>
                    <em>{{ trip.type }} · {{ trip.stopCount }} 站 · {{ trip.duration || trip.transportMode || 'AI 已生成' }}</em>
                    <small>{{ trip.firstStop }}{{ trip.lastStop ? ` → ${trip.lastStop}` : '' }}</small>
                  </span>
                  <b>{{ trip.status === 'planned' ? '计划' : trip.status }}</b>
                </button>
              </section>

              <section v-if="!isLoadingTrips && !tripList.length" class="itinerary-empty trip-empty">
                <h3>还没有行程计划</h3>
                <p>从中间的小薇聊天生成路线后，会先保存为计划，再出现在这里。一天生成多条也会按日期归档。</p>
                <button type="button" class="product-primary" @click="activeScreen = 'ai1'">去找小薇</button>
              </section>
            </section>

            <template v-else>
              <div class="itinerary-address-bar">
                <div class="itinerary-address-info">
                  <div class="itinerary-address-item"><span class="itinerary-icon">📍</span><span class="itinerary-address-text">{{ itineraryStartAddress }}</span></div>
                  <div class="itinerary-address-divider"></div>
                  <div class="itinerary-address-item"><span class="itinerary-icon">📍</span><span class="itinerary-address-text">{{ itineraryEndAddress }}</span></div>
                </div>
                <div class="itinerary-action-buttons">
                  <button class="itinerary-icon-btn" aria-label="更多选项">⋮</button>
                  <button class="itinerary-icon-btn" aria-label="重新生成" @click="requestItineraryChange('重新生成一条更适合我的路线')">↻</button>
                </div>
              </div>
              <div class="itinerary-map-card">
                <p class="itinerary-map-title">{{ itineraryTitle }}</p>
                <div class="itinerary-stats">
                  <div v-for="stat in itineraryStats" :key="stat.label" class="itinerary-stat"><span class="itinerary-stat-label">{{ stat.label }}</span><span class="itinerary-stat-value">{{ stat.value }}</span></div>
                </div>
              </div>

              <!-- 小地图 -->
              <div id="itinerary-map" style="width:100%;height:180px;margin:0 16px;border-radius:12px;overflow:hidden;z-index:10;position:relative"></div>

              <section class="agent-context-grid">
                <article class="agent-context-card weather">
                  <span>天气 API</span>
                  <strong>{{ tripWeather?.condition || '待获取' }} · {{ tripWeather?.temperatureText || '--' }}</strong>
                  <p>{{ tripWeather?.comfortLevel || '小薇会根据天气调整路线节奏' }} · 降雨 {{ tripWeather?.rainProbability ?? '--' }}%</p>
                </article>
                <article class="agent-context-card route">
                  <span>路线 API</span>
                  <strong>{{ routeMarkers.length }} 个路线点</strong>
                  <p>{{ tripRouteMap?.agentPath || 'agent 规划路径会显示在这里' }}</p>
                </article>
              </section>

              <p v-if="itineraryNotice" class="itinerary-notice">{{ itineraryNotice }}</p>
              <div v-if="itineraryStops.length" class="itinerary-cards-container">
                <div v-for="(stop, index) in itineraryStops" :key="stop.poiId || stop.stopId || stop.name" class="itinerary-card">
                  <div class="itinerary-card-time">{{ stop.time }} - {{ stop.endTime }}</div>
                  <div class="itinerary-card-number">{{ stopOrder(stop, index) }}</div>
                  <h3 class="itinerary-card-name">{{ stop.name }}</h3>
                  <div class="itinerary-card-tags">
                    <span v-for="tag in (stop.tags || [stop.category]).slice(0, 3)" :key="tag" class="itinerary-tag">{{ tag }}</span>
                    <span v-if="stop.walkFromPrevious" class="itinerary-tag">步行 {{ stop.walkFromPrevious }} 分钟</span>
                  </div>
                  <p class="itinerary-card-price">人均 ¥{{ stop.pricePerCapita || '待估' }} · {{ stop.category || '地点' }}</p>
                  <p v-if="stop.reason || stop.desc" class="itinerary-card-reason">{{ stop.reason || stop.desc }}</p>
                  <div class="itinerary-card-actions">
                    <button class="itinerary-btn-detail" @click="itineraryNotice = stop.reason || stop.desc || '这个点位来自小薇的画像匹配结果。'">查看理由</button>
                    <button class="itinerary-btn-swap" @click="requestItineraryChange(`把第 ${stopOrder(stop, index)} 站「${stop.name}」换一个更合适的地点`)">换一个</button>
                  </div>
                </div>
              </div>
              <section v-else class="itinerary-empty">
                <h3>还没有路线</h3>
                <p>从中间的 AI 聊天告诉小薇你的时间、地点和心情，她会调用后端 agent 生成完整行程。</p>
                <button type="button" class="product-primary" @click="activeScreen = 'ai1'">去找小薇</button>
              </section>

              <section v-if="reminderToday.length || reminderChecklist.length || tripWeather?.agentTips?.length" class="itinerary-reminders">
                <h3 class="itinerary-section-title">小薇出发前检查</h3>
                <div class="itinerary-reminder-box">
                  <div v-if="tripWeather?.agentTips?.length" class="itinerary-reminder-item">
                    <strong>天气影响</strong>
                    <ul class="itinerary-reminder-list">
                      <li v-for="tip in tripWeather.agentTips" :key="tip">{{ tip }}</li>
                    </ul>
                  </div>
                  <div v-if="reminderToday.length" class="itinerary-reminder-item">
                    <strong>路线提醒</strong>
                    <ul class="itinerary-reminder-list">
                      <li v-for="item in reminderToday" :key="item">{{ item }}</li>
                    </ul>
                  </div>
                  <div v-if="reminderChecklist.length" class="itinerary-reminder-item">
                    <strong>带上这些</strong>
                    <ul class="itinerary-reminder-checklist">
                      <li v-for="item in reminderChecklist" :key="item"><input type="checkbox" />{{ item }}</li>
                    </ul>
                  </div>
                </div>
              </section>

              <div class="itinerary-adjustments">
                <h3 class="itinerary-section-title">想调整一下？</h3>
                <div class="itinerary-adjustment-buttons">
                  <button class="itinerary-adjustment-btn" :disabled="itineraryBusy" @click="requestItineraryChange('把路线改得更轻松一点')">更轻松一点</button>
                  <button class="itinerary-adjustment-btn" :disabled="itineraryBusy" @click="requestItineraryChange('尽量避开排队和高峰')">避开排队</button>
                  <button class="itinerary-adjustment-btn itinerary-adjustment-btn-primary" :disabled="itineraryBusy" @click="requestItineraryChange('减少步行距离')">减少步行</button>
                  <button class="itinerary-adjustment-btn itinerary-adjustment-btn-primary" :disabled="itineraryBusy" @click="requestItineraryChange('重新生成一条路线')">重新生成</button>
                </div>
              </div>
            </template>
            <BottomNav :active-screen="activeScreen" :assets="{ left: ai1NavLeftAsset, search: ai1SearchAsset, center: ai1NavCenterAsset, map: ai1NavRightAsset, group: ai1MicAsset }" @navigate="navigate" />
            <footer class="home-indicator-wrap">
              <div class="home-indicator"></div>
            </footer>
          </main>
        </div>
      </div>

      <div class="side-buttons left">
        <div class="btn-mute"></div>
        <div class="btn-vol-up"></div>
        <div class="btn-vol-down"></div>
      </div>
      <div class="side-buttons right">
        <div class="btn-power"></div>
      </div>
    </div>
  </div>
</template>
