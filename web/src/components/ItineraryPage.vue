<script setup lang="ts">
import { computed, ref } from 'vue'
import ItineraryMap from './ItineraryMap.vue'
import { resolvePlaceDetail, type PlaceDetail } from '../data/placeDetails'

const emit = defineEmits<{
  navigate: [screen: 'ai1' | 'discover' | 'itinerary' | 'navigation' | 'chat']
  viewDetail: [detail: PlaceDetail]
}>()

const levelsAsset = '/Levels.svg'

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

const itinerarySummaryStats = [
  { label: '总路程', value: '约1.8km' },
  { label: '预算估测', value: '¥230-350/人' },
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

const itineraryReminders = ['暴晒 25℃', 'RAC BAR 可能等位', '已预留缓冲']
const itineraryPackingList = ['遮阳伞', '一台傻瓜胶片相机', '充电宝']

const itineraryAdjustments = [
  { label: '更轻松一点', emphasized: false },
  { label: '减少步行', emphasized: false },
  { label: '避开排队', emphasized: false },
  { label: '重新生成', emphasized: true },
]

const itineraryPrompt = '今天突然下雨了，不去室外'
</script>

<template>
  <div class="itinerary-figma">
    <div class="itinerary-figma-background" aria-hidden="true"></div>

    <header class="itinerary-figma-status-bar">
      <div class="itinerary-figma-time">9:41</div>
      <div class="itinerary-figma-island"></div>
      <img :src="levelsAsset" alt="" class="itinerary-figma-levels" />
    </header>

    <div class="itinerary-figma-scroll" :class="{ 'itinerary-figma-scroll-locked': activeSwapStop !== null }">
      <section class="itinerary-figma-address-shell">
        <div class="itinerary-figma-address-card">
          <div class="itinerary-figma-address-line itinerary-figma-address-line-muted">
            <span class="itinerary-figma-address-pin" aria-hidden="true"></span>
            <span class="itinerary-figma-address-text">上海市徐汇区武康路 376 号附近</span>
          </div>
          <div class="itinerary-figma-address-divider"></div>
          <div class="itinerary-figma-address-line itinerary-figma-address-line-strong">
            <span class="itinerary-figma-address-pin itinerary-figma-address-pin-end" aria-hidden="true"></span>
            <span class="itinerary-figma-address-text">上海市徐汇区上海图书馆地铁站</span>
          </div>
        </div>

        <div class="itinerary-figma-address-actions">
          <button type="button" class="itinerary-figma-address-action" aria-label="更多选项">⋮</button>
          <button type="button" class="itinerary-figma-address-action" aria-label="交换">⇅</button>
        </div>
      </section>

      <section class="itinerary-figma-map-section">
        <div class="itinerary-figma-map-stage">
          <ItineraryMap />

          <button type="button" class="itinerary-figma-start-nav" @click="emit('navigate', 'navigation')">
            <span class="itinerary-figma-start-nav-icon" aria-hidden="true">▲</span>
            <span>开始导航</span>
          </button>
        </div>

        <div class="itinerary-figma-summary-card">
          <div
            v-for="(item, index) in itinerarySummaryStats"
            :key="item.label"
            class="itinerary-figma-summary-item"
            :class="{ 'itinerary-figma-summary-item-divider': index < itinerarySummaryStats.length - 1 }"
          >
            <p class="itinerary-figma-summary-label">{{ item.label }}</p>
            <p class="itinerary-figma-summary-value">{{ item.value }}</p>
          </div>
        </div>
      </section>

      <section class="itinerary-figma-timeline">
        <div v-for="stop in itineraryStops" :key="stop.id" class="itinerary-figma-step">
          <div class="itinerary-figma-step-walk">
            <span class="itinerary-figma-step-walk-icon" aria-hidden="true">⌄⌄</span>
            <span>{{ stop.walkFromPrevious }}</span>
          </div>

          <div class="itinerary-figma-step-row">
            <div class="itinerary-figma-step-rail" aria-hidden="true">
              <span class="itinerary-figma-step-marker">{{ stop.id }}</span>
              <span class="itinerary-figma-step-line"></span>
            </div>

            <article class="itinerary-figma-stop-card">
              <div class="itinerary-figma-stop-header">
                <p class="itinerary-figma-stop-time">{{ stop.time }}</p>
                <div class="itinerary-figma-stop-tools">
                  <button type="button" class="itinerary-figma-stop-tool-pill" aria-label="路线选项">
                    <span class="itinerary-figma-stop-tool-line"></span>
                    <span class="itinerary-figma-stop-tool-line itinerary-figma-stop-tool-line-short"></span>
                  </button>
                  <button type="button" class="itinerary-figma-stop-tool-dot" aria-label="收藏"></button>
                </div>
              </div>

              <h3 class="itinerary-figma-stop-title">{{ stop.title }}</h3>

              <div class="itinerary-figma-stop-tags">
                <span v-for="tag in stop.tags" :key="tag" class="itinerary-figma-stop-tag">{{ tag }}</span>
              </div>

              <div class="itinerary-figma-stop-actions">
                <button type="button" class="itinerary-figma-detail-btn" @click="openStopDetail(stop)">查看详情</button>
                <p class="itinerary-figma-stop-price">{{ stop.price }}</p>
                <button type="button" class="itinerary-figma-swap-btn" @click="openSwapOptions(stop.id)">换一个</button>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="itinerary-figma-section">
        <h3 class="itinerary-figma-section-title">出发前提醒</h3>

        <div class="itinerary-figma-reminder-grid">
          <article class="itinerary-figma-reminder-card">
            <h4 class="itinerary-figma-reminder-title">今日提醒</h4>
            <ul class="itinerary-figma-reminder-list">
              <li v-for="item in itineraryReminders" :key="item">{{ item }}</li>
            </ul>
          </article>

          <article class="itinerary-figma-reminder-card">
            <h4 class="itinerary-figma-reminder-title">建议携带</h4>
            <ul class="itinerary-figma-packing-list">
              <li v-for="item in itineraryPackingList" :key="item">
                <span class="itinerary-figma-checkbox" aria-hidden="true"></span>
                <span>{{ item }}</span>
              </li>
            </ul>
          </article>
        </div>
      </section>

      <section class="itinerary-figma-section itinerary-figma-section-tight">
        <h3 class="itinerary-figma-section-title">想调整一下？</h3>

        <div class="itinerary-figma-adjust-grid">
          <button
            v-for="item in itineraryAdjustments"
            :key="item.label"
            type="button"
            class="itinerary-figma-adjust-btn"
            :class="{ 'itinerary-figma-adjust-btn-emphasis': item.emphasized }"
          >
            {{ item.label }}
          </button>
        </div>
      </section>

      <div class="itinerary-figma-composer">
        <span class="itinerary-figma-composer-star" aria-hidden="true">✦</span>
        <span class="itinerary-figma-composer-text">{{ itineraryPrompt }}</span>
        <button type="button" class="itinerary-figma-composer-mic" aria-label="语音输入">●</button>
      </div>
    </div>

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

    <nav class="itinerary-figma-nav" aria-label="底部导航">
      <div class="itinerary-figma-nav-bg"></div>

      <button type="button" class="itinerary-figma-nav-btn itinerary-figma-nav-btn-muted" style="left:41px;top:768px;" aria-label="个人">
        <img src="/Icon-1.svg" alt="" class="itinerary-figma-nav-user-icon" />
      </button>

      <button
        type="button"
        class="itinerary-figma-nav-btn itinerary-figma-nav-btn-muted"
        style="left:113px;top:768px;"
        aria-label="发现"
        @click="emit('navigate', 'discover')"
      >
        <img src="/MagnifyingGlass.svg" alt="" class="itinerary-figma-nav-search-icon" />
      </button>

      <button
        type="button"
        class="itinerary-figma-nav-btn itinerary-figma-nav-btn-muted"
        style="left:177px;top:768px;"
        aria-label="AI"
        @click="emit('navigate', 'ai1')"
      >
        <img src="/Icon.svg" alt="" class="itinerary-figma-nav-ai-icon" />
      </button>

      <button
        type="button"
        class="itinerary-figma-nav-btn itinerary-figma-nav-btn-active"
        style="left:240px;top:768px;"
        aria-label="行程"
        aria-current="page"
        @click="emit('navigate', 'itinerary')"
      >
        <img src="/lucide_map.svg" alt="" class="itinerary-figma-nav-trip-icon" />
      </button>

      <button
        type="button"
        class="itinerary-figma-nav-btn itinerary-figma-nav-btn-muted"
        style="left:305px;top:768px;"
        aria-label="聊天"
        @click="emit('navigate', 'chat')"
      >
        <img src="/ChatTeardrop.svg" alt="" class="itinerary-figma-nav-chat-icon" />
      </button>
    </nav>

    <footer class="itinerary-figma-home-indicator">
      <div class="itinerary-figma-home-indicator-bar"></div>
    </footer>
  </div>
</template>

<style scoped>
.itinerary-figma {
  position: relative;
  height: 100%;
  overflow: hidden;
  background: #f9f9f9;
}

.itinerary-figma-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(46% 18% at 18% 72%, rgba(241, 196, 218, 0.78) 0%, rgba(241, 196, 218, 0) 72%),
    radial-gradient(44% 23% at 82% 92%, rgba(255, 249, 142, 0.8) 0%, rgba(255, 249, 142, 0) 69%),
    radial-gradient(52% 19% at 55% 100%, rgba(255, 255, 255, 0.92) 0%, rgba(255, 255, 255, 0) 78%),
    #f4eff3;
}

.itinerary-figma-status-bar {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  width: 100%;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.itinerary-figma-scroll {
  position: relative;
  z-index: 2;
  height: 100%;
  overflow-y: auto;
  padding: 60px 16px 132px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.itinerary-figma-scroll::-webkit-scrollbar {
  display: none;
}

.itinerary-figma-scroll-locked {
  overflow: hidden;
}

.itinerary-figma-address-shell {
  display: flex;
  gap: 8px;
  align-items: stretch;
}

.itinerary-figma-address-card {
  flex: 1;
  min-width: 0;
  padding: 16px;
  border-radius: 24px;
  border: 1px solid #f3f3f3;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.itinerary-figma-address-line {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 14px;
  line-height: 1.7;
  color: #2c2828;
}

.itinerary-figma-address-line-muted {
  opacity: 0.55;
}

.itinerary-figma-address-line-strong {
  font-weight: 500;
}

.itinerary-figma-address-pin {
  position: relative;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  border: 1.4px solid #000;
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  background: transparent;
}

.itinerary-figma-address-pin::after {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  top: 4px;
  left: 4px;
  border-radius: 50%;
  background: #000;
}

.itinerary-figma-address-pin-end {
  opacity: 1;
}

.itinerary-figma-address-divider {
  height: 1px;
  margin: 8px 0;
  background: #e8e3e7;
}

.itinerary-figma-address-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.itinerary-figma-address-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.itinerary-figma-address-action {
  width: 40px;
  height: 40px;
  border: 1px solid #f3f3f3;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
  color: #2a2a2a;
  font-size: 16px;
  cursor: pointer;
}

.itinerary-figma-map-section {
  margin-top: 10px;
}

.itinerary-figma-map-stage {
  position: relative;
  height: 312px;
  overflow: hidden;
  border-radius: 32px;
  background: #ece4e5;
  box-shadow: 0 10px 30px rgba(112, 86, 102, 0.12);
}

.itinerary-figma-start-nav {
  position: absolute;
  right: 10px;
  bottom: 12px;
  z-index: 4;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 40px;
  padding: 0 14px;
  border: 1px solid rgba(255, 255, 255, 0.92);
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.72);
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.itinerary-figma-start-nav-icon {
  font-size: 11px;
}

.itinerary-figma-summary-card {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin: -18px 2px 0;
  padding: 12px 8px;
  border: 1px solid #f3f3f3;
  border-radius: 24px 24px 18px 18px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.18);
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
  height: 34px;
  background: #e8e3e7;
}

.itinerary-figma-summary-label,
.itinerary-figma-summary-value {
  margin: 0;
}

.itinerary-figma-summary-label {
  font-size: 14px;
  color: #000;
}

.itinerary-figma-summary-value {
  margin-top: 5px;
  font-size: 10px;
  color: #000;
}

.itinerary-figma-timeline {
  margin-top: 14px;
}

.itinerary-figma-step + .itinerary-figma-step {
  margin-top: 4px;
}

.itinerary-figma-step-walk {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 8px 12px;
  font-size: 12px;
  line-height: 1.45;
  color: #1f1b1b;
}

.itinerary-figma-step-walk-icon {
  color: #6b5866;
  font-size: 11px;
}

.itinerary-figma-step-row {
  display: flex;
  align-items: stretch;
}

.itinerary-figma-step-rail {
  position: relative;
  width: 22px;
  flex-shrink: 0;
}

.itinerary-figma-step-marker {
  position: absolute;
  top: 10px;
  left: 0;
  z-index: 1;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid #fff;
  background: #5f3153;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.24);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  display: grid;
  place-items: center;
}

.itinerary-figma-step-line {
  position: absolute;
  top: 34px;
  bottom: -18px;
  left: 10px;
  width: 1.5px;
  background: linear-gradient(180deg, #d5c7d0 0%, #d5c7d0 78%, rgba(213, 199, 208, 0) 100%);
}

.itinerary-figma-step:last-child .itinerary-figma-step-line {
  display: none;
}

.itinerary-figma-stop-card {
  flex: 1;
  margin-left: 10px;
  padding: 12px 11px 11px;
  border: 0.65px solid #b4b4b4;
  border-radius: 13px;
  background: rgba(244, 239, 241, 0.96);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.itinerary-figma-stop-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.itinerary-figma-stop-time {
  margin: 0;
  font-size: 10px;
  line-height: 1.4;
  color: #000;
}

.itinerary-figma-stop-tools {
  display: flex;
  align-items: center;
  gap: 8px;
}

.itinerary-figma-stop-tool-pill {
  width: 57px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  border: 0.92px solid #e8e3e7;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
}

.itinerary-figma-stop-tool-line {
  display: block;
  width: 14px;
  height: 1.6px;
  border-radius: 999px;
  background: #6b5564;
}

.itinerary-figma-stop-tool-line-short {
  width: 8px;
}

.itinerary-figma-stop-tool-dot {
  width: 22px;
  height: 22px;
  border: 0;
  border-radius: 50%;
  background: #5f3153;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.16);
  cursor: pointer;
}

.itinerary-figma-stop-title {
  margin: 10px 0 8px;
  font-size: 16px;
  line-height: 1.35;
  font-weight: 400;
  color: #000;
}

.itinerary-figma-stop-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.itinerary-figma-stop-tag {
  min-width: 51px;
  padding: 0 10px;
  height: 19px;
  border: 0.5px solid #b8b8b8;
  border-radius: 28px;
  background: #fff;
  font-size: 10px;
  line-height: 18px;
  color: #000;
  text-align: center;
}

.itinerary-figma-stop-actions {
  display: grid;
  grid-template-columns: 81px 1fr 81px;
  align-items: center;
  gap: 8px;
  margin-top: 14px;
}

.itinerary-figma-detail-btn,
.itinerary-figma-swap-btn {
  height: 27px;
  border-radius: 5px;
  font-size: 13px;
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

.itinerary-figma-stop-price {
  margin: 0;
  justify-self: end;
  font-size: 12.57px;
  color: #000;
  white-space: nowrap;
}

.itinerary-figma-section {
  margin-top: 16px;
}

.itinerary-figma-section-tight {
  margin-top: 14px;
}

.itinerary-figma-section-title {
  margin: 0 0 12px;
  font-size: 17px;
  font-weight: 400;
  color: #000;
}

.itinerary-figma-reminder-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.itinerary-figma-reminder-card {
  min-height: 131px;
  padding: 10px 15px 12px;
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.47);
}

.itinerary-figma-reminder-title {
  margin: 0 0 10px;
  font-size: 14px;
  font-weight: 400;
  color: #000;
}

.itinerary-figma-reminder-list,
.itinerary-figma-packing-list {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 12px;
  color: #000;
}

.itinerary-figma-reminder-list li {
  position: relative;
  padding-left: 14px;
  line-height: 2.3;
}

.itinerary-figma-reminder-list li::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 2px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #5f3153;
}

.itinerary-figma-packing-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 2.5;
}

.itinerary-figma-checkbox {
  width: 11px;
  height: 11px;
  border: 0.8px solid #ababab;
  border-radius: 2px;
  background: transparent;
  flex-shrink: 0;
}

.itinerary-figma-adjust-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 4px;
}

.itinerary-figma-adjust-btn {
  height: 35px;
  border: 1px solid #c5c5c5;
  border-radius: 52px;
  background: #fff;
  color: #404040;
  font-size: 14px;
  cursor: pointer;
}

.itinerary-figma-adjust-btn-emphasis {
  border-color: #461c3a;
  background: #e8e3e7;
  color: #000;
}

.itinerary-figma-composer {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 47px;
  margin-top: 18px;
  padding: 0 13px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.74);
  border: 1px solid rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(10px);
}

.itinerary-figma-composer-star {
  font-size: 18px;
  color: #d59fc0;
}

.itinerary-figma-composer-text {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 15px;
  color: #a8a8a8;
}

.itinerary-figma-composer-mic {
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.02);
  color: #463341;
  font-size: 12px;
  cursor: pointer;
}

.itinerary-swap-backdrop {
  position: absolute;
  inset: 0;
  z-index: 18;
  background: rgba(24, 18, 23, 0.12);
  backdrop-filter: blur(4px);
}

.itinerary-swap-sheet {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 19;
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
  grid-template-columns: repeat(2, 163px);
  justify-content: center;
  gap: 8px;
}

.itinerary-swap-option-card {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 163px;
  height: 131px;
  padding: 10px 11px 0;
  border: 0;
  border-radius: 16px;
  background: #fff;
  overflow: visible;
  box-shadow: 0 0 0 1px rgba(25, 16, 24, 0.08);
  will-change: transform, opacity;
}

.itinerary-swap-option-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 6px;
  min-height: 29px;
  padding: 0;
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
  padding: 0;
  border-radius: 7px;
  background: rgba(214, 197, 249, 0.5);
  color: #51373f;
  font-size: 10px;
  line-height: 13px;
  font-weight: 400;
}

.itinerary-swap-option-travel {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 8px 0 0;
  padding: 0;
  font-size: 10px;
  line-height: 13px;
  font-weight: 400;
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
  font-weight: 400;
  overflow: hidden;
}

.itinerary-swap-option-action {
  margin-top: auto;
  width: 183px;
  height: 28px;
  margin-left: -10px;
  border: 0;
  background: #4a1e43;
  color: #fff;
  border-radius: 32px;
  font-size: 10px;
  line-height: 13px;
  font-weight: 400;
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

.itinerary-figma-nav {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
  pointer-events: none;
}

.itinerary-figma-nav-bg {
  position: absolute;
  width: 327px;
  height: 54px;
  left: 33px;
  top: 765px;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.66);
  border: 1px solid #ffffff;
  border-radius: 32px;
}

.itinerary-figma-nav-btn {
  position: absolute;
  width: 48px;
  height: 48px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 12px;
  gap: 8px;
  border: 0;
  border-radius: 1000px;
  cursor: pointer;
  pointer-events: auto;
}

.itinerary-figma-nav-btn-muted {
  background: rgba(0, 0, 0, 0.02);
}

.itinerary-figma-nav-btn-active {
  background: #000000;
}

.itinerary-figma-nav-user-icon {
  width: 14.4px;
  height: 14.4px;
  display: block;
}

.itinerary-figma-nav-search-icon,
.itinerary-figma-nav-chat-icon {
  width: 16px;
  height: 16px;
  display: block;
}

.itinerary-figma-nav-ai-icon {
  width: 22px;
  height: 22px;
  display: block;
  filter: brightness(0);
}

.itinerary-figma-nav-trip-icon {
  width: 12px;
  height: 11.83px;
  display: block;
  filter: brightness(0) invert(1);
}

.itinerary-figma-nav-btn:focus-visible {
  outline: 2px solid rgba(70, 28, 58, 0.45);
  outline-offset: 2px;
}

.itinerary-figma-home-indicator {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 8px;
  z-index: 10;
  display: flex;
  justify-content: center;
}

.itinerary-figma-home-indicator-bar {
  width: 144px;
  height: 5px;
  border-radius: 100px;
  background: #2a2a2a;
}
</style>