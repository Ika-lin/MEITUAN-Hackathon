<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import ItineraryMap from './ItineraryMap.vue'
import { resolvePlaceDetail, type PlaceDetail } from '../data/placeDetails'

const emit = defineEmits<{
  navigate: [screen: 'ai1' | 'discover' | 'itinerary' | 'navigation' | 'chat' | 'profile']
  viewDetail: [detail: PlaceDetail]
}>()

const levelsAsset = '/Levels.svg'
const addressStartAsset = '/Location Icon.svg'
const addressEndAsset = '/map-pin.svg'
const moreVerticalAsset = '/more-vertical.svg'
const swapAsset = '/iconamoon_swap.svg'
const startAsset = '/Start Icon.svg'
const walkAsset = '/CaretDoubleDown.svg'
const clockAsset = '/clock.svg'
const composerMicAsset = '/Group 3.svg'
const navProfileAsset = '/user.svg'
const navSearchAsset = '/MagnifyingGlass.svg'
const navAiAsset = '/Icon-3.svg'
const navTripAsset = '/lucide_map.svg'
const navChatAsset = '/ChatTeardrop-dark.svg'

type ItineraryStop = {
  id: number
  time: string
  title: string
  tags: string[]
  price: string
  walkFromPrevious: string
}

type ReplacementOption = {
  id: string
  title: string
  price: string
  travel: string
  summary: string
  tags: string[]
  walkFromPrevious: string
}

type StopLayout = {
  walkTop: number
  cardTop: number
  cardHeight: number
  markerTop: number
  connectorTop: number
  connectorHeight: number
}

type ReminderItem = {
  id: string
  text: string
  done: boolean
}

type PackingItem = {
  id: string
  text: string
  checked: boolean
}

type AdjustmentItem = {
  id: string
  label: string
  emphasized: boolean
}

const defaultStartLocation = '上海市徐汇区武康路 376 号附近'
const defaultEndLocation = '上海市徐汇区上海图书馆地铁站'

const startLocation = ref(defaultStartLocation)
const endLocation = ref(defaultEndLocation)

let dynamicItemSeed = 0

function createDynamicId(prefix: string) {
  dynamicItemSeed += 1
  return `${prefix}-${dynamicItemSeed}`
}

const routeOriginLabel = computed(() => startLocation.value.trim() || defaultStartLocation)

function restoreLocationDefaults() {
  startLocation.value = defaultStartLocation
  endLocation.value = defaultEndLocation
}

function swapLocations() {
  const previousStart = startLocation.value
  startLocation.value = endLocation.value
  endLocation.value = previousStart
}

const itinerarySummaryStats = [
  { label: '总路程', value: '约1.8km' },
  { label: '预算估测', value: '¥230–350/人' },
  { label: '交通方式', value: '全程步行' },
  { label: '步行时间', value: '约25分钟' },
]

const initialItineraryStops: ItineraryStop[] = [
  {
    id: 1,
    time: '14:08 - 14:55（50分钟）',
    title: 'FILM电影时光书店',
    tags: ['电影主题', '安静翻阅', '胶片气质'],
    price: '人均 ¥43',
    walkFromPrevious: '步行约 5-8 分钟',
  },
  {
    id: 2,
    time: '15:00 - 16:00（60分钟）',
    title: 'RAC BAR（安福路店）',
    tags: ['街角咖啡', '露台小坐', '法式风情'],
    price: '人均 ¥120-150',
    walkFromPrevious: '步行约 5 分钟',
  },
  {
    id: 3,
    time: '16:10 - 16:50（40分钟）',
    title: '一面春风（吴兴路总店/武康周边）',
    tags: ['烟火小馆', '本帮风味', '匠心汤底'],
    price: '人均 ¥55-70',
    walkFromPrevious: '步行约 8-10 分钟',
  },
]

const stopLayouts: StopLayout[] = [
  { walkTop: 711, cardTop: 742, cardHeight: 140, markerTop: 742, connectorTop: 767, connectorHeight: 169 },
  { walkTop: 905, cardTop: 942, cardHeight: 144, markerTop: 942, connectorTop: 964, connectorHeight: 169 },
  { walkTop: 1110, cardTop: 1146, cardHeight: 141, markerTop: 1146, connectorTop: 1171, connectorHeight: 169 },
]

const itineraryStops = ref(initialItineraryStops.map((stop) => ({ ...stop, tags: [...stop.tags] })))

const replacementOptionsByStop: Record<number, ReplacementOption[]> = {
  1: [
    {
      id: 'duozhuayu',
      title: '多抓鱼循环商店',
      price: '约￥60-70',
      travel: '步行约 3-5 分钟',
      summary: '二手书和服饰都能逛',
      tags: ['循环商店', '旧书淘选', '服饰闲逛'],
      walkFromPrevious: '步行约 3-5 分钟',
    },
    {
      id: 'hengshanheji',
      title: '衡山和集',
      price: '约￥35-45',
      travel: '骑行约 8-12 分钟',
      summary: '空间更完整，适合慢慢停留',
      tags: ['复合空间', '慢逛停留', '书店展陈'],
      walkFromPrevious: '骑行约 8-12 分钟',
    },
  ],
  2: [
    {
      id: 'manner-anfu',
      title: 'MANNER COFFEE（安福路店）',
      price: '约￥28-40',
      travel: '步行约 4-6 分钟',
      summary: '出杯更快，适合轻量停留',
      tags: ['精品咖啡', '出杯很快', '街边停留'],
      walkFromPrevious: '步行约 4-6 分钟',
    },
    {
      id: 'cafe-del-volcan',
      title: 'Café del Volcán',
      price: '约￥36-52',
      travel: '步行约 7-9 分钟',
      summary: '空间更松弛，适合慢聊久坐',
      tags: ['空间更松弛', '慢坐聊天', '风味咖啡'],
      walkFromPrevious: '步行约 7-9 分钟',
    },
  ],
  3: [
    {
      id: 'lanxin',
      title: '兰心餐厅（进贤路店）',
      price: '约￥70-90',
      travel: '步行约 6-9 分钟',
      summary: '本帮味更稳，适合经典收尾',
      tags: ['本帮经典', '收尾更稳', '口味扎实'],
      walkFromPrevious: '步行约 6-9 分钟',
    },
    {
      id: 'wuyuan',
      title: '福和面馆（武康路附近）',
      price: '约￥32-48',
      travel: '步行约 3-5 分钟',
      summary: '热汤面食更轻松，适合快速收尾',
      tags: ['轻量晚餐', '热汤面食', '快速结束'],
      walkFromPrevious: '步行约 3-5 分钟',
    },
  ],
}

const activeSwapStopId = ref<number | null>(null)
const scrollRoot = ref<HTMLElement | null>(null)

const positionedStops = computed(() =>
  itineraryStops.value.map((stop, index) => ({
    ...stop,
    ...stopLayouts[index],
    titleWide: stop.id === 3,
  })),
)

const activeSwapStop = computed(() => {
  if (activeSwapStopId.value === null) return null
  return itineraryStops.value.find((stop) => stop.id === activeSwapStopId.value) ?? null
})

const activeSwapOptions = computed(() => {
  if (activeSwapStopId.value === null) return []
  return replacementOptionsByStop[activeSwapStopId.value] ?? []
})

function openSwapOptions(stopId: number) {
  activeSwapStopId.value = stopId
}

function closeSwapOptions() {
  activeSwapStopId.value = null
}

function applySwapOption(option: ReplacementOption) {
  const index = itineraryStops.value.findIndex((stop) => stop.id === activeSwapStopId.value)
  if (index === -1) return

  itineraryStops.value[index] = {
    ...itineraryStops.value[index],
    title: option.title,
    price: option.price,
    tags: [...option.tags],
    walkFromPrevious: option.walkFromPrevious,
  }

  closeSwapOptions()
}

function openStopDetail(stop: ItineraryStop) {
  emit(
    'viewDetail',
    resolvePlaceDetail({
      title: stop.title,
      tags: stop.tags,
      price: stop.price,
    }),
  )
}

const itineraryReminders = ref<ReminderItem[]>([
  { id: 'reminder-1', text: '暴晒 25℃', done: false },
  { id: 'reminder-2', text: 'RAC BAR 可能等位', done: false },
  { id: 'reminder-3', text: '已预留缓冲', done: false },
])

const itineraryPackingList = ref<PackingItem[]>([
  { id: 'packing-1', text: '遮阳伞', checked: false },
  { id: 'packing-2', text: '一台傻瓜胶片相机', checked: false },
  { id: 'packing-3', text: '充电宝', checked: false },
])

const itineraryAdjustments = ref<AdjustmentItem[]>([
  { id: 'adjustment-1', label: '更轻松一点', emphasized: false },
  { id: 'adjustment-2', label: '减少步行', emphasized: false },
  { id: 'adjustment-3', label: '避开排队', emphasized: false },
  { id: 'adjustment-4', label: '重新生成', emphasized: true },
])

const reminderDraft = ref('')
const packingDraft = ref('')
const adjustmentDraft = ref('')
const selectedAdjustmentId = ref<string | null>(null)
const itineraryPrompt = ref('今天突然下雨了，不去室外')
const itineraryFinalWalk = '步行约 8-10 分钟'

function addReminder() {
  const text = reminderDraft.value.trim()
  if (!text) return

  itineraryReminders.value.push({
    id: createDynamicId('reminder'),
    text,
    done: false,
  })
  reminderDraft.value = ''
}

function toggleReminder(id: string) {
  const reminder = itineraryReminders.value.find((item) => item.id === id)
  if (!reminder) return

  reminder.done = !reminder.done
}

function removeReminder(id: string) {
  itineraryReminders.value = itineraryReminders.value.filter((item) => item.id !== id)
}

function addPackingItem() {
  const text = packingDraft.value.trim()
  if (!text) return

  itineraryPackingList.value.push({
    id: createDynamicId('packing'),
    text,
    checked: false,
  })
  packingDraft.value = ''
}

function togglePackingItem(id: string) {
  const packingItem = itineraryPackingList.value.find((item) => item.id === id)
  if (!packingItem) return

  packingItem.checked = !packingItem.checked
}

function removePackingItem(id: string) {
  itineraryPackingList.value = itineraryPackingList.value.filter((item) => item.id !== id)
}

function selectAdjustment(item: AdjustmentItem) {
  selectedAdjustmentId.value = selectedAdjustmentId.value === item.id ? null : item.id
  itineraryPrompt.value = item.label
}

function addAdjustment() {
  const label = adjustmentDraft.value.trim()
  if (!label) return

  const nextItem = {
    id: createDynamicId('adjustment'),
    label,
    emphasized: false,
  }

  itineraryAdjustments.value.push(nextItem)
  adjustmentDraft.value = ''
  selectAdjustment(nextItem)
}

function removeAdjustment(id: string) {
  itineraryAdjustments.value = itineraryAdjustments.value.filter((item) => item.id !== id)

  if (selectedAdjustmentId.value === id) {
    selectedAdjustmentId.value = null
  }
}

onMounted(() => {
  scrollRoot.value?.scrollTo({ top: 0 })
})
</script>

<template>
  <div class="itinerary-figma">
    <header class="itinerary-figma-status-bar">
      <div class="itinerary-figma-time">9:41</div>
      <div class="itinerary-figma-island"></div>
      <img :src="levelsAsset" alt="" class="itinerary-figma-levels" />
    </header>

    <div ref="scrollRoot" class="itinerary-figma-scroll" :class="{ 'itinerary-figma-scroll-locked': activeSwapStop !== null }">
      <div class="itinerary-figma-canvas">
        <div class="itinerary-figma-background" aria-hidden="true">
          <div class="itinerary-figma-glow itinerary-figma-glow-white"></div>
          <div class="itinerary-figma-glow itinerary-figma-glow-rose"></div>
          <div class="itinerary-figma-glow itinerary-figma-glow-ellipse"></div>
          <div class="itinerary-figma-glow itinerary-figma-glow-gold"></div>
        </div>

        <div class="itinerary-figma-map-stage">
          <ItineraryMap />
        </div>

        <section class="itinerary-figma-address-shell">
          <div class="itinerary-figma-address-card">
            <div class="itinerary-figma-address-details">
              <label class="itinerary-figma-address-line itinerary-figma-address-line-muted">
                <img :src="addressStartAsset" alt="" class="itinerary-figma-address-icon itinerary-figma-address-icon-muted" />
                <input
                  v-model="startLocation"
                  type="text"
                  class="itinerary-figma-address-input"
                  aria-label="起始点位置"
                  :placeholder="defaultStartLocation"
                />
              </label>
              <div class="itinerary-figma-address-divider"></div>
              <label class="itinerary-figma-address-line itinerary-figma-address-line-strong">
                <img :src="addressEndAsset" alt="" class="itinerary-figma-address-icon" />
                <input
                  v-model="endLocation"
                  type="text"
                  class="itinerary-figma-address-input"
                  aria-label="终点位置"
                  :placeholder="defaultEndLocation"
                />
              </label>
            </div>
          </div>

          <div class="itinerary-figma-address-actions">
            <button type="button" class="itinerary-figma-address-action" aria-label="恢复默认地点" @click="restoreLocationDefaults">
              <img :src="moreVerticalAsset" alt="" class="itinerary-figma-address-action-icon" />
            </button>
            <button type="button" class="itinerary-figma-address-action" aria-label="交换起终点" @click="swapLocations">
              <img :src="swapAsset" alt="" class="itinerary-figma-address-action-icon" />
            </button>
          </div>
        </section>

        <button type="button" class="itinerary-figma-start-nav" @click="emit('navigate', 'navigation')">
          <img :src="startAsset" alt="" class="itinerary-figma-start-nav-icon" />
          <span>开始导航</span>
        </button>

        <section class="itinerary-figma-summary-card">
          <div
            v-for="(item, index) in itinerarySummaryStats"
            :key="item.label"
            class="itinerary-figma-summary-item"
            :class="{ 'itinerary-figma-summary-item-divider': index < itinerarySummaryStats.length - 1 }"
          >
            <p class="itinerary-figma-summary-label">{{ item.label }}</p>
            <p class="itinerary-figma-summary-value">{{ item.value }}</p>
          </div>
        </section>

        <div class="itinerary-figma-route-origin">
          <img :src="addressStartAsset" alt="" class="itinerary-figma-route-origin-icon" />
          <span class="itinerary-figma-route-origin-text">{{ routeOriginLabel }}</span>
        </div>

        <template v-for="stop in positionedStops" :key="stop.id">
          <div class="itinerary-figma-step-walk" :style="{ top: `${stop.walkTop}px` }">
            <img :src="walkAsset" alt="" class="itinerary-figma-step-walk-icon" />
            <span>{{ stop.walkFromPrevious }}</span>
          </div>

          <div class="itinerary-figma-step-connector" :style="{ top: `${stop.connectorTop}px`, height: `${stop.connectorHeight}px` }"></div>

          <div class="itinerary-figma-step-marker" :style="{ top: `${stop.markerTop}px` }">{{ stop.id }}</div>

          <article class="itinerary-figma-stop-card" :style="{ top: `${stop.cardTop}px`, height: `${stop.cardHeight}px` }">
            <div class="itinerary-figma-stop-card-inner">
              <div class="itinerary-figma-stop-header">
                <p class="itinerary-figma-stop-time">
                  <img :src="clockAsset" alt="" class="itinerary-figma-stop-time-icon" />
                  <span>{{ stop.time }}</span>
                </p>

                <div class="itinerary-figma-stop-tools">
                  <button type="button" class="itinerary-figma-stop-tool-pill" aria-label="路线选项">
                    <span class="itinerary-figma-stop-tool-line"></span>
                    <span class="itinerary-figma-stop-tool-line itinerary-figma-stop-tool-line-short"></span>
                  </button>
                  <button type="button" class="itinerary-figma-stop-tool-dot" aria-label="收起站点操作">
                    <span class="itinerary-figma-stop-tool-minus"></span>
                  </button>
                </div>
              </div>

              <h3 class="itinerary-figma-stop-title" :class="{ 'itinerary-figma-stop-title-wide': stop.titleWide }">{{ stop.title }}</h3>

              <div class="itinerary-figma-stop-meta">
                <div class="itinerary-figma-stop-tags">
                  <span v-for="tag in stop.tags" :key="tag" class="itinerary-figma-stop-tag">{{ tag }}</span>
                </div>
                <p class="itinerary-figma-stop-price">{{ stop.price }}</p>
              </div>

              <div class="itinerary-figma-stop-actions">
                <button type="button" class="itinerary-figma-detail-btn" @click="openStopDetail(stop)">查看详情</button>
                <button type="button" class="itinerary-figma-swap-btn" @click="openSwapOptions(stop.id)">换一个</button>
              </div>
            </div>
          </article>
        </template>

        <div class="itinerary-figma-step-walk itinerary-figma-step-walk-final" style="top: 1304px;">
          <img :src="walkAsset" alt="" class="itinerary-figma-step-walk-icon" />
          <span>{{ itineraryFinalWalk }}</span>
        </div>

        <section class="itinerary-figma-reminder-section">
          <h3 class="itinerary-figma-section-title">出发前提醒</h3>

          <div class="itinerary-figma-reminder-grid">
            <article class="itinerary-figma-reminder-card">
              <h4 class="itinerary-figma-reminder-title">今日提醒</h4>
              <ul class="itinerary-figma-reminder-list">
                <li
                  v-for="item in itineraryReminders"
                  :key="item.id"
                  :class="{ 'itinerary-figma-reminder-item-done': item.done }"
                >
                  <button type="button" class="itinerary-figma-reminder-row" @click="toggleReminder(item.id)">
                    <span class="itinerary-figma-reminder-bullet" aria-hidden="true"></span>
                    <span>{{ item.text }}</span>
                  </button>
                  <button type="button" class="itinerary-figma-item-remove" aria-label="删除提醒" @click="removeReminder(item.id)">×</button>
                </li>
              </ul>

              <form class="itinerary-figma-inline-form" @submit.prevent="addReminder">
                <input
                  v-model="reminderDraft"
                  type="text"
                  class="itinerary-figma-inline-input"
                  aria-label="新增提醒"
                  placeholder="添加提醒"
                />
                <button type="submit" class="itinerary-figma-inline-btn">添加</button>
              </form>
            </article>

            <article class="itinerary-figma-reminder-card">
              <h4 class="itinerary-figma-reminder-title">建议携带</h4>
              <ul class="itinerary-figma-packing-list">
                <li
                  v-for="item in itineraryPackingList"
                  :key="item.id"
                  :class="{ 'itinerary-figma-packing-item-checked': item.checked }"
                >
                  <button type="button" class="itinerary-figma-packing-row" @click="togglePackingItem(item.id)">
                    <span class="itinerary-figma-checkbox" :class="{ 'itinerary-figma-checkbox-checked': item.checked }" aria-hidden="true"></span>
                    <span>{{ item.text }}</span>
                  </button>
                  <button type="button" class="itinerary-figma-item-remove" aria-label="删除携带物品" @click="removePackingItem(item.id)">×</button>
                </li>
              </ul>

              <form class="itinerary-figma-inline-form" @submit.prevent="addPackingItem">
                <input
                  v-model="packingDraft"
                  type="text"
                  class="itinerary-figma-inline-input"
                  aria-label="新增携带物品"
                  placeholder="添加物品"
                />
                <button type="submit" class="itinerary-figma-inline-btn">添加</button>
              </form>
            </article>
          </div>
        </section>

        <section class="itinerary-figma-adjust-section">
          <h3 class="itinerary-figma-section-title">想调整一下？</h3>

          <div class="itinerary-figma-adjust-grid">
            <div v-for="item in itineraryAdjustments" :key="item.id" class="itinerary-figma-adjust-item">
              <button
                type="button"
                class="itinerary-figma-adjust-btn"
                :class="{
                  'itinerary-figma-adjust-btn-emphasis': item.emphasized,
                  'itinerary-figma-adjust-btn-selected': item.id === selectedAdjustmentId,
                }"
                @click="selectAdjustment(item)"
              >
                {{ item.label }}
              </button>
              <button type="button" class="itinerary-figma-adjust-remove" aria-label="删除调整项" @click="removeAdjustment(item.id)">×</button>
            </div>
          </div>

          <form class="itinerary-figma-inline-form itinerary-figma-inline-form-adjust" @submit.prevent="addAdjustment">
            <input
              v-model="adjustmentDraft"
              type="text"
              class="itinerary-figma-inline-input"
              aria-label="新增调整项"
              placeholder="添加新的调整方向"
            />
            <button type="submit" class="itinerary-figma-inline-btn">添加</button>
          </form>
        </section>

        <div class="itinerary-figma-composer">
          <span class="itinerary-figma-composer-star" aria-hidden="true">✦</span>
          <input
            v-model="itineraryPrompt"
            type="text"
            class="itinerary-figma-composer-input"
            aria-label="输入行程要求"
            placeholder="今天突然下雨了，不去室外"
          />
          <button type="button" class="itinerary-figma-composer-mic" aria-label="语音输入">
            <img :src="composerMicAsset" alt="" class="itinerary-figma-composer-mic-icon" />
          </button>
        </div>

        <footer class="itinerary-figma-home-indicator">
          <div class="itinerary-figma-home-indicator-bar"></div>
        </footer>
      </div>
    </div>

    <nav class="itinerary-figma-nav" aria-label="底部导航">
      <button type="button" class="itinerary-figma-nav-btn" aria-label="个人" @click="emit('navigate', 'profile')">
        <img :src="navProfileAsset" alt="" class="itinerary-figma-nav-icon itinerary-figma-nav-icon-profile" />
      </button>
      <button type="button" class="itinerary-figma-nav-btn" aria-label="发现" @click="emit('navigate', 'discover')">
        <img :src="navSearchAsset" alt="" class="itinerary-figma-nav-icon itinerary-figma-nav-icon-search" />
      </button>
      <button type="button" class="itinerary-figma-nav-btn" aria-label="AI" @click="emit('navigate', 'ai1')">
        <img :src="navAiAsset" alt="" class="itinerary-figma-nav-icon itinerary-figma-nav-icon-ai" />
      </button>
      <button type="button" class="itinerary-figma-nav-btn itinerary-figma-nav-btn-active" aria-label="行程" aria-current="page" @click="emit('navigate', 'itinerary')">
        <img :src="navTripAsset" alt="" class="itinerary-figma-nav-icon itinerary-figma-nav-icon-trip" />
      </button>
      <button type="button" class="itinerary-figma-nav-btn itinerary-figma-nav-btn-chat" aria-label="聊天" @click="emit('navigate', 'chat')">
        <img :src="navChatAsset" alt="" class="itinerary-figma-nav-icon itinerary-figma-nav-icon-chat" />
      </button>
    </nav>

    <Transition name="swap-fade">
      <div v-if="activeSwapStop" class="itinerary-swap-backdrop" @click="closeSwapOptions"></div>
    </Transition>

    <Transition name="swap-sheet">
      <section v-if="activeSwapStop" class="itinerary-swap-sheet" @click.stop>
        <div class="itinerary-swap-sheet-handle"></div>

        <div class="itinerary-swap-sheet-header">
          <div class="itinerary-swap-sheet-title-wrap">
            <span class="itinerary-swap-sheet-title-icon" aria-hidden="true">✦</span>
            <h3 class="itinerary-swap-sheet-title">精选备选 | 替换第 {{ activeSwapStop.id }} 站</h3>
          </div>

          <button type="button" class="itinerary-swap-sheet-close" aria-label="关闭备选方案" @click="closeSwapOptions">
            ×
          </button>
        </div>

        <div class="itinerary-swap-sheet-grid">
          <article v-for="option in activeSwapOptions" :key="option.id" class="itinerary-swap-option-card">
            <div class="itinerary-swap-option-head">
              <h4 class="itinerary-swap-option-title">{{ option.title }}</h4>
              <span class="itinerary-swap-option-price">{{ option.price }}</span>
            </div>

            <p class="itinerary-swap-option-travel">
              <span class="itinerary-swap-option-travel-icon" aria-hidden="true">📍</span>
              <span>{{ option.travel }}</span>
            </p>

            <p class="itinerary-swap-option-summary">{{ option.summary }}</p>

            <button type="button" class="itinerary-swap-option-action" @click="applySwapOption(option)">
              选用此站
            </button>
          </article>
        </div>
      </section>
    </Transition>
  </div>
</template>

<style scoped>
.itinerary-figma {
  position: relative;
  height: 100%;
  overflow: hidden;
  background: #f9f9f9;
}

.itinerary-figma-scroll {
  position: relative;
  z-index: 2;
  height: 100%;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.itinerary-figma-scroll::-webkit-scrollbar {
  display: none;
}

.itinerary-figma-scroll-locked {
  overflow: hidden;
}

.itinerary-figma-canvas {
  position: relative;
  width: 393px;
  min-height: 2031px;
  background: #f4eff3;
  overflow: hidden;
}

.itinerary-figma-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: #f4eff3;
}

.itinerary-figma-glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(100px);
  pointer-events: none;
}

.itinerary-figma-glow-white {
  top: 1360px;
  left: 44px;
  width: 220px;
  height: 360px;
  background: rgba(255, 255, 255, 0.9);
  transform: rotate(-67deg) skewX(-45deg) scaleY(0.7);
}

.itinerary-figma-glow-rose {
  top: 744px;
  left: -98px;
  width: 160px;
  height: 520px;
  background: rgba(215, 164, 224, 0.45);
  transform: rotate(-67deg) skewX(-45deg) scaleY(0.7);
}

.itinerary-figma-glow-ellipse {
  top: 812px;
  left: -132px;
  width: 340px;
  height: 860px;
  background: rgba(255, 255, 255, 0.36);
  transform: rotate(74deg) skewX(44deg) scaleY(0.72);
}

.itinerary-figma-glow-gold {
  top: 1710px;
  right: -34px;
  width: 210px;
  height: 360px;
  background: rgba(255, 249, 142, 0.82);
  transform: rotate(114deg) skewX(-45deg) scaleY(0.7);
}

.itinerary-figma-status-bar {
  position: absolute;
  top: -4px;
  left: 0;
  z-index: 20;
  width: 100%;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.96);
}

.itinerary-figma-time {
  width: 138px;
  text-align: center;
  font-family: 'SF Pro Text', sans-serif;
  font-size: 17px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: -0.51px;
  color: #000;
}

.itinerary-figma-island {
  width: 104px;
  height: 28px;
  border-radius: 999px;
  background: #2a2a2a;
}

.itinerary-figma-levels {
  width: 143px;
  height: 54px;
  object-fit: contain;
}

.itinerary-figma-map-stage {
  position: absolute;
  top: 55px;
  left: 50%;
  width: 417px;
  height: 551px;
  overflow: hidden;
  background: #ece4e5;
  transform: translateX(-50%);
}

.itinerary-figma-address-shell {
  position: absolute;
  top: 60px;
  left: 16px;
  z-index: 8;
  display: flex;
  gap: 8px;
  width: 361px;
}

.itinerary-figma-address-card {
  width: 297px;
  height: 92px;
  padding: 16px;
  border: 1px solid #f3f3f3;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.itinerary-figma-address-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.itinerary-figma-address-line {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  font-family: 'SF Pro Rounded', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  line-height: 1.7;
  color: #2c2828;
}

.itinerary-figma-address-line-muted {
  opacity: 0.5;
}

.itinerary-figma-address-line-strong {
  font-weight: 500;
}

.itinerary-figma-address-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.itinerary-figma-address-icon-muted {
  opacity: 0.8;
}

.itinerary-figma-address-divider {
  width: 100%;
  height: 1px;
  background: #e8e3e7;
}

.itinerary-figma-address-text {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.itinerary-figma-address-input {
  min-width: 0;
  width: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  font: inherit;
  color: inherit;
}

.itinerary-figma-address-input::placeholder {
  color: rgba(44, 40, 40, 0.48);
}

.itinerary-figma-address-input:focus {
  outline: none;
}

.itinerary-figma-address-actions {
  display: flex;
  flex-direction: column;
  width: 56px;
  padding: 2px 8px;
  border: 1px solid #f3f3f3;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.itinerary-figma-address-action {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 0;
  border-radius: 999px;
  background: #fff;
  cursor: pointer;
}

.itinerary-figma-address-action-icon {
  width: 16px;
  height: 16px;
}

.itinerary-figma-start-nav {
  position: absolute;
  top: 523px;
  left: 278px;
  z-index: 7;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  width: 90px;
  height: 44px;
  padding: 10px 8px;
  border: 1px solid rgba(255, 255, 255, 0.95);
  border-radius: 166px;
  background: rgba(0, 0, 0, 0.72);
  color: #fff;
  font-family: 'SF Pro Rounded', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 13px;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
}

.itinerary-figma-start-nav-icon {
  width: 14px;
  height: 14px;
}

.itinerary-figma-summary-card {
  position: absolute;
  top: 586px;
  left: 18px;
  z-index: 8;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  width: 358px;
  height: 61px;
  padding: 11px 13px 12px 21px;
  border: 1px solid #f3f3f3;
  border-radius: 24px 24px 18px 18px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.36);
}

.itinerary-figma-summary-item {
  position: relative;
  text-align: center;
}

.itinerary-figma-summary-item-divider::after {
  content: '';
  position: absolute;
  top: 6px;
  right: 0;
  width: 1px;
  height: 38px;
  background: #e8e3e7;
}

.itinerary-figma-summary-label,
.itinerary-figma-summary-value {
  margin: 0;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #000;
}

.itinerary-figma-summary-label {
  font-size: 14px;
  line-height: 1.15;
}

.itinerary-figma-summary-value {
  margin-top: 8px;
  font-size: 10px;
  line-height: 1.2;
}

.itinerary-figma-route-origin {
  position: absolute;
  top: 666px;
  left: 7px;
  z-index: 6;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 380px;
  height: 30px;
  border: 0.5px solid #000;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.94);
}

.itinerary-figma-route-origin-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.itinerary-figma-route-origin-text {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 13px;
  line-height: 1;
  color: #000;
}

.itinerary-figma-step-walk {
  position: absolute;
  left: 30px;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 12px;
  line-height: 17.5px;
  color: #000;
}

.itinerary-figma-step-walk-final {
  left: 28px;
}

.itinerary-figma-step-walk-icon {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

.itinerary-figma-step-connector {
  position: absolute;
  left: 16px;
  z-index: 1;
  width: 1.5px;
  background: linear-gradient(180deg, #9e6c90 0%, #d7bccf 100%);
}

.itinerary-figma-step-marker {
  position: absolute;
  left: 5px;
  z-index: 3;
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1.5px solid rgba(255, 255, 255, 0.9);
  background: #5f3153;
  color: #fff;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 15px;
  line-height: 1;
  box-shadow: 0 0 0 3px rgba(230, 217, 227, 0.6) inset;
}

.itinerary-figma-stop-card {
  position: absolute;
  left: 29px;
  z-index: 4;
  width: 355px;
  border: 0.646px solid #b4b4b4;
  border-radius: 12.929px;
  background: rgba(244, 239, 241, 0.96);
}

.itinerary-figma-stop-card-inner {
  position: relative;
  height: 100%;
  padding: 14px 11px 11px;
}

.itinerary-figma-stop-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.itinerary-figma-stop-time {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin: 0;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 10px;
  line-height: 1.2;
  color: #000;
}

.itinerary-figma-stop-time-icon {
  width: 10px;
  height: 10px;
  flex-shrink: 0;
}

.itinerary-figma-stop-tools {
  display: flex;
  align-items: center;
  gap: 11px;
}

.itinerary-figma-stop-tool-pill {
  width: 56.833px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 0;
  border: 0.917px solid #e8e3e7;
  border-radius: 8.041px;
  background: #fff;
  cursor: pointer;
}

.itinerary-figma-stop-tool-line {
  width: 14px;
  height: 1.6px;
  border-radius: 999px;
  background: #6a5765;
}

.itinerary-figma-stop-tool-line-short {
  width: 8px;
}

.itinerary-figma-stop-tool-dot {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #5f3153;
  cursor: pointer;
}

.itinerary-figma-stop-tool-minus {
  width: 9px;
  height: 1.6px;
  border-radius: 999px;
  background: #fff;
}

.itinerary-figma-stop-title {
  margin: 12px 0 0;
  max-width: 252px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 16px;
  line-height: 1.2;
  color: #000;
}

.itinerary-figma-stop-title-wide {
  max-width: 268px;
}

.itinerary-figma-stop-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 11px;
}

.itinerary-figma-stop-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  max-width: 228px;
}

.itinerary-figma-stop-tag {
  min-width: 51px;
  height: 19px;
  padding: 0 10px;
  border: 0.5px solid #b8b8b8;
  border-radius: 28.348px;
  background: #fff;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 10px;
  line-height: 18px;
  color: #000;
  text-align: center;
}

.itinerary-figma-stop-price {
  flex-shrink: 0;
  margin: 0;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 12.57px;
  line-height: 1.2;
  color: #000;
  white-space: nowrap;
}

.itinerary-figma-stop-actions {
  position: absolute;
  left: 11px;
  right: 11px;
  bottom: 11px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.itinerary-figma-detail-btn,
.itinerary-figma-swap-btn {
  width: 81px;
  height: 27px;
  padding: 0;
  border-radius: 4.654px;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 12.96px;
  line-height: 1;
  cursor: pointer;
}

.itinerary-figma-detail-btn {
  border: 0;
  background: #461c3a;
  color: #fff;
}

.itinerary-figma-swap-btn {
  border: 0.54px solid #461c3a;
  background: #e8e3e7;
  color: #000;
}

.itinerary-figma-nav {
  position: absolute;
  box-sizing: border-box;
  top: 765px;
  left: calc(50% - 327px / 2);
  z-index: 18;
  display: flex;
  align-items: flex-start;
  gap: 18px;
  width: 327px;
  height: 54px;
  padding: 3px 7px 3px 8px;
  border: 1px solid rgba(255, 255, 255, 0.92);
  border-radius: 32px;
  background: rgba(255, 255, 255, 0.66);
  backdrop-filter: blur(18px);
}

.itinerary-figma-nav-btn {
  position: relative;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  border: 0;
  border-radius: 1000px;
  background: rgba(0, 0, 0, 0.02);
  cursor: pointer;
}

.itinerary-figma-nav-btn-active {
  background: #000;
}

.itinerary-figma-nav-icon {
  display: block;
  object-fit: contain;
}

.itinerary-figma-nav-icon-profile {
  width: 14.4px;
  height: 14.4px;
}

.itinerary-figma-nav-icon-search,
.itinerary-figma-nav-icon-chat {
  width: 16px;
  height: 16px;
}

.itinerary-figma-nav-icon-ai {
  width: 22px;
  height: 22px;
}

.itinerary-figma-nav-icon-trip {
  width: 12px;
  height: 11.83px;
  filter: brightness(0) invert(1);
}

.itinerary-figma-reminder-section {
  position: absolute;
  top: 1442px;
  left: 19px;
  width: 354px;
}

.itinerary-figma-section-title {
  margin: 0 0 10px;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 17px;
  line-height: 20px;
  color: #000;
}

.itinerary-figma-reminder-grid {
  display: grid;
  grid-template-columns: 170px 170px;
  gap: 14px;
}

.itinerary-figma-reminder-card {
  min-height: 158px;
  display: flex;
  flex-direction: column;
  padding: 10px 15px 12px;
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.47);
}

.itinerary-figma-reminder-title {
  margin: 0 0 10px;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  line-height: 1.15;
  color: #000;
}

.itinerary-figma-reminder-list,
.itinerary-figma-packing-list {
  list-style: none;
  margin: 0;
  padding: 0;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 12px;
  line-height: 17px;
  color: #000;
}

.itinerary-figma-reminder-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 31px;
}

.itinerary-figma-packing-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  min-height: 31px;
}

.itinerary-figma-reminder-row,
.itinerary-figma-packing-row {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  font: inherit;
  text-align: left;
  cursor: pointer;
}

.itinerary-figma-reminder-bullet {
  width: 7px;
  height: 7px;
  flex-shrink: 0;
  border-radius: 50%;
  background: #5f3153;
}

.itinerary-figma-checkbox {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 11px;
  height: 11px;
  border: 0.8px solid #ababab;
  border-radius: 2px;
  background: transparent;
  flex-shrink: 0;
}

.itinerary-figma-checkbox-checked {
  border-color: #5f3153;
  background: #5f3153;
}

.itinerary-figma-checkbox-checked::after {
  content: '';
  width: 5px;
  height: 3px;
  border-left: 1.5px solid #fff;
  border-bottom: 1.5px solid #fff;
  transform: rotate(-45deg) translateY(-1px);
}

.itinerary-figma-reminder-item-done .itinerary-figma-reminder-row span:last-child,
.itinerary-figma-packing-item-checked .itinerary-figma-packing-row span:last-child {
  color: #7f7f7f;
  text-decoration: line-through;
}

.itinerary-figma-item-remove {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: rgba(95, 49, 83, 0.12);
  color: #5f3153;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
}

.itinerary-figma-inline-form {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: auto;
  padding-top: 10px;
}

.itinerary-figma-inline-input {
  flex: 1;
  min-width: 0;
  height: 32px;
  padding: 0 12px;
  border: 1px solid rgba(95, 49, 83, 0.14);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.78);
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 12px;
  color: #2c2828;
}

.itinerary-figma-inline-input::placeholder {
  color: #9b9499;
}

.itinerary-figma-inline-input:focus {
  outline: none;
  border-color: rgba(95, 49, 83, 0.4);
}

.itinerary-figma-inline-btn {
  height: 32px;
  flex-shrink: 0;
  padding: 0 12px;
  border: 0;
  border-radius: 16px;
  background: #5f3153;
  color: #fff;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 12px;
  cursor: pointer;
}

.itinerary-figma-adjust-section {
  position: absolute;
  top: 1624px;
  left: 19px;
  width: 354px;
}

.itinerary-figma-adjust-grid {
  display: grid;
  grid-template-columns: repeat(2, 175px);
  gap: 4px 4px;
}

.itinerary-figma-adjust-item {
  position: relative;
}

.itinerary-figma-adjust-btn {
  width: 100%;
  height: 35px;
  padding: 0 28px 0 14px;
  border: 1px solid #c5c5c5;
  border-radius: 52px;
  background: #fff;
  color: #404040;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  line-height: 16px;
  cursor: pointer;
}

.itinerary-figma-adjust-btn-emphasis {
  border-color: #461c3a;
  background: #e8e3e7;
  color: #000;
}

.itinerary-figma-adjust-btn-selected {
  border-color: #461c3a;
  box-shadow: inset 0 0 0 1px rgba(70, 28, 58, 0.14);
}

.itinerary-figma-adjust-remove {
  position: absolute;
  top: 50%;
  right: 8px;
  width: 18px;
  height: 18px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: transparent;
  color: #7b5471;
  font-size: 13px;
  line-height: 1;
  transform: translateY(-50%);
  cursor: pointer;
}

.itinerary-figma-inline-form-adjust {
  margin-top: 10px;
}

.itinerary-figma-composer {
  position: absolute;
  top: 1751px;
  left: 19px;
  z-index: 4;
  display: flex;
  align-items: center;
  gap: 12px;
  width: 357px;
  height: 47px;
  padding: 0 13px;
  border: 1px solid rgba(255, 255, 255, 0.88);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.74);
  backdrop-filter: blur(10px);
}

.itinerary-figma-composer-star {
  font-size: 18px;
  line-height: 1;
  color: #dbb6de;
}

.itinerary-figma-composer-input {
  flex: 1;
  min-width: 0;
  padding: 0;
  border: 0;
  background: transparent;
  font-family: 'FZLanTingHeiS-DB-GB', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 15px;
  line-height: 1;
  color: #6d6d6d;
}

.itinerary-figma-composer-input::placeholder {
  color: #a8a8a8;
}

.itinerary-figma-composer-input:focus {
  outline: none;
}

.itinerary-figma-composer-mic {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.itinerary-figma-composer-mic-icon {
  width: 16px;
  height: 22px;
  display: block;
}

.itinerary-figma-home-indicator {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 8px;
  display: flex;
  justify-content: center;
}

.itinerary-figma-home-indicator-bar {
  width: 144px;
  height: 5px;
  border-radius: 100px;
  background: #2a2a2a;
}

.itinerary-swap-backdrop {
  position: absolute;
  inset: 0;
  z-index: 28;
  background: rgba(24, 18, 23, 0.12);
  backdrop-filter: blur(4px);
}

.itinerary-swap-sheet {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 29;
  padding: 8px 11px 16px;
  border-top-left-radius: 24px;
  border-top-right-radius: 24px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.08);
  transform-origin: bottom center;
  will-change: transform, opacity;
}

.itinerary-swap-sheet-handle {
  width: 40px;
  height: 5px;
  margin: 0 auto 14px;
  border-radius: 100px;
  background: #dedede;
}

.itinerary-swap-sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.itinerary-swap-sheet-title-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.itinerary-swap-sheet-title-icon {
  color: #8f8f8f;
  font-size: 16px;
  line-height: 1;
}

.itinerary-swap-sheet-title {
  margin: 0;
  font-size: 16px;
  line-height: 1.4;
  font-weight: 600;
  color: #6f6f6f;
}

.itinerary-swap-sheet-close {
  width: 32px;
  height: 32px;
  border: 1px solid #ececec;
  border-radius: 50%;
  background: #fff;
  color: #7a7a7a;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
}

.itinerary-swap-sheet-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.itinerary-swap-option-card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 131px;
  padding: 10px 11px 0;
  border: 0;
  border-radius: 16px;
  background: #fff;
  overflow: hidden;
  box-shadow: 0 0 0 1px rgba(25, 16, 24, 0.08);
  will-change: transform, opacity;
}

.itinerary-swap-option-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 6px;
  min-height: 29px;
}

.itinerary-swap-option-title {
  margin: 0;
  flex: 1;
  min-width: 0;
  max-width: calc(100% - 66px);
  overflow: hidden;
  color: #000;
  font-size: 13px;
  line-height: 17px;
  font-weight: 400;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.itinerary-swap-option-price {
  flex: none;
  width: 60px;
  height: 23px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;
  background: rgba(214, 197, 249, 0.5);
  color: #51373f;
  font-size: 10px;
  line-height: 13px;
}

.itinerary-swap-option-travel {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 8px 0 0;
  font-size: 10px;
  line-height: 13px;
  color: #000;
}

.itinerary-swap-option-travel-icon {
  flex: none;
  font-size: 9px;
  line-height: 17px;
}

.itinerary-swap-option-summary {
  display: flex;
  align-items: center;
  min-height: 21px;
  margin: 8px 0 0;
  padding: 4px 5px;
  border-radius: 5px;
  background: #efefef;
  color: #000;
  font-size: 9px;
  line-height: 13px;
  overflow: hidden;
}

.itinerary-swap-option-action {
  margin-top: auto;
  width: calc(100% + 22px);
  height: 28px;
  margin-left: -11px;
  border: 0;
  background: #4a1e43;
  color: #fff;
  border-radius: 0 0 16px 16px;
  font-size: 10px;
  line-height: 13px;
  cursor: pointer;
}

.swap-fade-enter-active,
.swap-fade-leave-active {
  transition: opacity 220ms ease;
}

.swap-fade-enter-from,
.swap-fade-leave-to {
  opacity: 0;
}

.swap-sheet-enter-active {
  transition: transform 320ms cubic-bezier(0.22, 1, 0.36, 1), opacity 240ms ease;
}

.swap-sheet-leave-active {
  transition: transform 220ms ease, opacity 180ms ease;
}

.swap-sheet-enter-from,
.swap-sheet-leave-to {
  transform: translateY(32px) scale(0.98);
  opacity: 0;
}

.swap-sheet-enter-active .itinerary-swap-option-card,
.swap-sheet-leave-active .itinerary-swap-option-card {
  transition: transform 260ms cubic-bezier(0.22, 1, 0.36, 1), opacity 180ms ease;
}

.swap-sheet-enter-from .itinerary-swap-option-card,
.swap-sheet-leave-to .itinerary-swap-option-card {
  transform: translateY(18px);
  opacity: 0;
}

.swap-sheet-enter-active .itinerary-swap-option-card:nth-child(2),
.swap-sheet-leave-active .itinerary-swap-option-card:nth-child(2) {
  transition-delay: 50ms;
}
</style>