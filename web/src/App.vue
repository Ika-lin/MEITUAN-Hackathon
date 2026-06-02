<script setup lang="ts">
import { computed, ref } from 'vue'

const heroIcon = 'https://www.figma.com/api/mcp/asset/256bc662-d72a-4fc0-b1f6-fecbc9a2242c'
const micIcon = 'https://www.figma.com/api/mcp/asset/46bd6e81-842e-4ae9-9767-3493d9e244db'
const locationCurrentIcon = 'https://www.figma.com/api/mcp/asset/16f3806f-4e82-4a07-b0ea-ea0a6f6404ed'
const locationTargetIcon = 'https://www.figma.com/api/mcp/asset/a293b465-f7c2-49bc-81a6-c3124e6b87d6'
const swapIcon = 'https://www.figma.com/api/mcp/asset/b86fae0f-4ac8-433f-aa73-9545f4932c95'
const sparkIcon = 'https://www.figma.com/api/mcp/asset/ad36f983-e95d-4a1c-b87b-87885cc3e32d'
const topLogo = 'https://www.figma.com/api/mcp/asset/d356a9c0-4979-4c33-a360-8915666a8740'
const searchIcon = 'https://www.figma.com/api/mcp/asset/8436b146-4d20-4b74-88a9-55b8dcb6eacc'
const navDiscover = 'https://www.figma.com/api/mcp/asset/410f36cf-bfcd-45ae-883a-7966eb4a8950'
const navPlan = 'https://www.figma.com/api/mcp/asset/fe941997-cae3-478d-9ab5-ff8542dcbcde'
const navTrip = 'https://www.figma.com/api/mcp/asset/c99a7f0f-ed52-407f-8d52-2ce5272b0082'
const navMe = 'https://www.figma.com/api/mcp/asset/c6ea31f5-0b89-46c5-a4b5-c690c0a705a8'

const blockLeftImage =
  'https://www.figma.com/api/mcp/asset/fce40aea-5162-4540-bdcd-b5ab2f93158b'
const blockRightImage =
  'https://www.figma.com/api/mcp/asset/b4317017-fca3-4026-aff4-e0d476890b85'

const timeTags = ['短时闲逛', '城市一日', '周末两天'] as const
const activityTags = ['寻味美食', '喝咖啡', '逛街区', '看展览'] as const
const budgetTags = ['100元内', '100-300', '不限'] as const

const selectedTime = ref<(typeof timeTags)[number]>('短时闲逛')
const selectedActivities = ref<(typeof activityTags)[number][]>(['喝咖啡'])
const selectedBudget = ref<(typeof budgetTags)[number]>('100-300')
const activeTab = ref<'discover' | 'plan' | 'trip' | 'me'>('plan')

const startLocation = ref('我的位置')
const endLocation = ref('想去哪儿？')
const promptText = ref('例如：想去武康路附近逛逛，喝杯手冲咖啡，最好能看个小众艺术展...')
const aiStatusText = ref('AI 将结合当地最新动态为您量身定制')
const isGenerating = ref(false)
const toastText = ref('')
const frameRef = ref<HTMLElement | null>(null)
const activeSideKey = ref<'volume-up' | 'volume-down' | 'action' | 'power' | null>(null)
const activeMaterial = ref<'titanium' | 'silver' | 'black'>('titanium')

const canGenerate = computed(() => promptText.value.trim().length > 0)

const materialLabelMap: Record<'titanium' | 'silver' | 'black', string> = {
  titanium: '钛金灰',
  silver: '银色',
  black: '深空黑',
}

function toggleActivity(tag: (typeof activityTags)[number]) {
  if (selectedActivities.value.includes(tag)) {
    selectedActivities.value = selectedActivities.value.filter((item) => item !== tag)
    return
  }
  selectedActivities.value = [...selectedActivities.value, tag]
}

function swapLocations() {
  const temp = startLocation.value
  startLocation.value = endLocation.value
  endLocation.value = temp
  toastText.value = '已交换位置'
  window.setTimeout(() => {
    toastText.value = ''
  }, 1300)
}

function fillPromptByVoice() {
  promptText.value = '想在安福路周边轻松逛 3 小时，先喝咖啡再看展，预算 100-300 元。'
  toastText.value = '已填入语音草稿'
  window.setTimeout(() => {
    toastText.value = ''
  }, 1300)
}

function generatePlan() {
  if (!canGenerate.value || isGenerating.value) {
    return
  }
  isGenerating.value = true
  aiStatusText.value = '正在结合你的位置和偏好生成中...'
  window.setTimeout(() => {
    isGenerating.value = false
    aiStatusText.value = '已为你生成 2 条可执行方案，可继续微调偏好'
    toastText.value = '生成成功'
    window.setTimeout(() => {
      toastText.value = ''
    }, 1300)
  }, 1100)
}

function updateGlarePosition(clientX: number, clientY: number) {
  if (!frameRef.value) {
    return
  }
  const rect = frameRef.value.getBoundingClientRect()
  const x = ((clientX - rect.left) / rect.width) * 100
  const y = ((clientY - rect.top) / rect.height) * 100
  frameRef.value.style.setProperty('--glare-x', `${Math.min(100, Math.max(0, x))}%`)
  frameRef.value.style.setProperty('--glare-y', `${Math.min(100, Math.max(0, y))}%`)
}

function handlePointerMove(event: PointerEvent) {
  updateGlarePosition(event.clientX, event.clientY)
}

function handleTouchMove(event: TouchEvent) {
  const touch = event.touches[0]
  if (!touch) {
    return
  }
  updateGlarePosition(touch.clientX, touch.clientY)
}

function resetGlarePosition() {
  if (!frameRef.value) {
    return
  }
  frameRef.value.style.setProperty('--glare-x', '22%')
  frameRef.value.style.setProperty('--glare-y', '14%')
}

function pressSideKey(key: 'volume-up' | 'volume-down' | 'action' | 'power') {
  activeSideKey.value = key
  if (!frameRef.value) {
    return
  }

  const glareMap: Record<'volume-up' | 'volume-down' | 'action' | 'power', [string, string]> = {
    'volume-up': ['14%', '18%'],
    'volume-down': ['14%', '34%'],
    action: ['14%', '10%'],
    power: ['84%', '24%'],
  }

  const [x, y] = glareMap[key]
  frameRef.value.style.setProperty('--glare-x', x)
  frameRef.value.style.setProperty('--glare-y', y)
}

function releaseSideKey() {
  activeSideKey.value = null
  resetGlarePosition()
}
</script>

<template>
  <div class="app-shell" :class="`material-${activeMaterial}`">
    <div class="material-switcher">
      <p>边框材质</p>
      <div class="material-options">
        <button
          v-for="material in ['titanium', 'silver', 'black'] as const"
          :key="material"
          class="material-btn"
          :class="{ 'material-btn-active': activeMaterial === material }"
          @click="activeMaterial = material"
        >
          {{ materialLabelMap[material] }}
        </button>
      </div>
    </div>

    <div class="phone-body-shadow" aria-hidden="true">
      <div class="side-controls">
        <button
          class="side-btn volume-up"
          :class="{ 'side-btn-active': activeSideKey === 'volume-up' }"
          aria-label="音量加"
          @pointerdown="pressSideKey('volume-up')"
          @pointerup="releaseSideKey"
          @pointerleave="releaseSideKey"
        />
        <button
          class="side-btn volume-down"
          :class="{ 'side-btn-active': activeSideKey === 'volume-down' }"
          aria-label="音量减"
          @pointerdown="pressSideKey('volume-down')"
          @pointerup="releaseSideKey"
          @pointerleave="releaseSideKey"
        />
        <button
          class="side-btn action"
          :class="{ 'side-btn-active': activeSideKey === 'action' }"
          aria-label="功能键"
          @pointerdown="pressSideKey('action')"
          @pointerup="releaseSideKey"
          @pointerleave="releaseSideKey"
        />
        <button
          class="side-btn power"
          :class="{ 'side-btn-active': activeSideKey === 'power' }"
          aria-label="电源键"
          @pointerdown="pressSideKey('power')"
          @pointerup="releaseSideKey"
          @pointerleave="releaseSideKey"
        />
      </div>
      <div class="antenna-cuts" aria-hidden="true">
        <span class="antenna-cut top-left" />
        <span class="antenna-cut top-right" />
        <span class="antenna-cut bottom-left" />
        <span class="antenna-cut bottom-right" />
      </div>
    </div>
    <div
      ref="frameRef"
      class="phone-frame"
      @pointermove="handlePointerMove"
      @pointerleave="resetGlarePosition"
      @touchmove.passive="handleTouchMove"
      @touchend="resetGlarePosition"
    >
      <div class="phone-notch" aria-hidden="true">
        <span class="island-speaker" />
        <span class="island-camera" />
      </div>
      <div class="screen-glare" aria-hidden="true" />

      <header class="top-bar">
        <div class="top-brand">
          <img :src="topLogo" alt="" />
          <span>智能规划</span>
        </div>
        <button class="icon-button" aria-label="搜索">
          <img :src="searchIcon" alt="" />
        </button>
      </header>

      <main class="phone-scroll">
        <section class="content">
        <section class="inspire-card">
          <div class="inspire-head">
            <h1>说吧，你想怎么过今天？</h1>
            <img :src="heroIcon" alt="" />
          </div>
          <div class="textarea-wrap">
            <textarea
              v-model="promptText"
              class="prompt-input"
              aria-label="输入你的想法"
              placeholder="例如：想去武康路附近逛逛，喝杯手冲咖啡，最好能看个小众艺术展..."
            />
            <button class="mic-btn" aria-label="语音输入" @click="fillPromptByVoice">
              <img :src="micIcon" alt="" />
            </button>
          </div>
        </section>

        <section class="filters">
          <div class="filter-group">
            <h2>时间安排</h2>
            <div class="chips-row">
              <button
                v-for="tag in timeTags"
                :key="tag"
                class="chip"
                :class="{ 'chip-active': selectedTime === tag }"
                @click="selectedTime = tag"
              >
                {{ tag }}
              </button>
            </div>
          </div>

          <div class="filter-group">
            <h2>偏好活动 (可多选)</h2>
            <div class="chips-row">
              <button
                v-for="tag in activityTags"
                :key="tag"
                class="chip"
                :class="{ 'chip-active': selectedActivities.includes(tag) }"
                @click="toggleActivity(tag)"
              >
                {{ tag }}
              </button>
            </div>
          </div>

          <div class="filter-group">
            <h2>消费预算</h2>
            <div class="chips-row">
              <button
                v-for="budget in budgetTags"
                :key="budget"
                class="chip"
                :class="{ 'chip-active chip-strong': selectedBudget === budget }"
                @click="selectedBudget = budget"
              >
                {{ budget }}
              </button>
            </div>
          </div>
        </section>

        <section class="location-card">
          <div class="location-row">
            <img :src="locationCurrentIcon" alt="" />
            <span>{{ startLocation }}</span>
          </div>
          <div class="line" />
          <div class="location-row muted">
            <img :src="locationTargetIcon" alt="" />
            <span>{{ endLocation }}</span>
          </div>
          <button class="swap-btn" aria-label="交换位置" @click="swapLocations">
            <img :src="swapIcon" alt="" />
          </button>
        </section>

        <section class="primary-cta">
          <button
            class="generate-btn"
            :class="{ 'generate-btn-disabled': !canGenerate || isGenerating }"
            :aria-label="isGenerating ? '生成中' : '生成计划'"
            :disabled="!canGenerate || isGenerating"
            @click="generatePlan"
          >
            <span>{{ isGenerating ? '正在生成计划...' : '生成我的闲时计划' }}</span>
            <img :src="sparkIcon" alt="" />
          </button>
          <p>{{ aiStatusText }}</p>
        </section>

        <section class="bento-strip" aria-label="可横向滑动推荐">
          <article class="bento-card warm">
            <p class="card-tag">热门街区</p>
            <h3>安福路</h3>
            <img :src="blockLeftImage" alt="安福路" />
          </article>
          <article class="bento-card cool">
            <p class="card-tag">正在开展</p>
            <h3>莫奈印象展</h3>
            <img :src="blockRightImage" alt="莫奈印象展" />
          </article>
          <article class="bento-card warm">
            <p class="card-tag">周末限定</p>
            <h3>梧桐树市集</h3>
            <img :src="blockLeftImage" alt="梧桐树市集" />
          </article>
        </section>
        </section>
      </main>

      <nav class="bottom-nav" aria-label="主导航">
        <button class="nav-item" :class="{ 'nav-item-active': activeTab === 'discover' }" @click="activeTab = 'discover'">
          <img :src="navDiscover" alt="" />
          <span>发现</span>
        </button>
        <button class="nav-item" :class="{ 'nav-item-active': activeTab === 'plan' }" @click="activeTab = 'plan'">
          <img :src="navPlan" alt="" />
          <span>规划</span>
        </button>
        <button class="nav-item" :class="{ 'nav-item-active': activeTab === 'trip' }" @click="activeTab = 'trip'">
          <img :src="navTrip" alt="" />
          <span>行程</span>
        </button>
        <button class="nav-item" :class="{ 'nav-item-active': activeTab === 'me' }" @click="activeTab = 'me'">
          <img :src="navMe" alt="" />
          <span>我的</span>
        </button>
      </nav>

      <transition name="toast">
        <div v-if="toastText" class="toast">{{ toastText }}</div>
      </transition>
    </div>
  </div>
</template>
