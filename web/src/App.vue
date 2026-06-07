<script setup lang="ts">
import { ref } from 'vue'
import ItineraryPage from './components/ItineraryPage.vue'
import DiscoverPage from './components/DiscoverPage.vue'
import CreatePostPage from './components/CreatePostPage.vue'
import PlaceDetailPage from './components/PlaceDetailPage.vue'
import NavigationPage from './components/NavigationPage.vue'
import ChatPage from './components/ChatPage.vue'
import ChatThreadPage from './components/ChatThreadPage.vue'
import ProfilePage from './components/ProfilePage.vue'
import SettingsPage from './components/SettingsPage.vue'
import type { PlaceDetail } from './data/placeDetails'

type Screen = 'home1' | 'home2' | 'discover' | 'createPost' | 'ai1' | 'ai5' | 'itinerary' | 'placeDetail' | 'navigation' | 'chat' | 'chatDetail' | 'profile' | 'settings'

const activeScreen = ref<Screen>('home1')
const selectedPlaceDetail = ref<PlaceDetail | null>(null)
const profileReturnScreen = ref<Screen>('ai1')

interface CardData {
  title: string
  tags: string[]
  tagColor: string
  tagTextColor: string
  time: string
  photo: string
  cardBg: string
}

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

const currentCardIndex = ref(0)
let touchStartX = 0
let touchEndX = 0
let isMouseDragging = false
let mouseStartX = 0
let mouseEndX = 0

function handleTouchStart(e: TouchEvent) {
  touchStartX = e.touches[0].clientX
}

function handleTouchEnd(e: TouchEvent) {
  touchEndX = e.changedTouches[0].clientX
  const diff = touchStartX - touchEndX
  if (Math.abs(diff) > 50) {
    if (diff > 0) {
      currentCardIndex.value = (currentCardIndex.value + 1) % cardList.length
    } else {
      currentCardIndex.value = (currentCardIndex.value - 1 + cardList.length) % cardList.length
    }
  }
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
  
  // Final position from mouseup event
  const finalX = (e as any).pageX || e.clientX
  mouseEndX = finalX
  
  const diff = mouseStartX - mouseEndX
  if (Math.abs(diff) > 50) {
    if (diff > 0) {
      currentCardIndex.value = (currentCardIndex.value + 1) % cardList.length
    } else {
      currentCardIndex.value = (currentCardIndex.value - 1 + cardList.length) % cardList.length
    }
  }
}

const logoAsset = '/Frame 12.svg'
const levelsAsset = '/Levels.svg'
const wechatAsset = '/微信 1.svg'
const meituanAsset = '/美团 1.svg'
const appleAsset = '/苹果.svg'

// AI生成页1 Figma 资产
const ai1LevelsAsset = 'https://www.figma.com/api/mcp/asset/35bb016e-759a-449f-b9af-7ef15e90c5f3'
const ai1SparkIconAsset = 'https://www.figma.com/api/mcp/asset/6dd54065-b1b9-4654-8362-9e0c1ff8543e'
const ai1VectorAsset = 'https://www.figma.com/api/mcp/asset/491a50d0-2331-4679-9b9a-14a8c39322dd'
const ai1MicGroupAsset = 'https://www.figma.com/api/mcp/asset/a2768da7-ad02-4777-9a79-ecf393d548e3'

// 底部导航图标使用 public 下的本地正式资源
const ai1MicAsset = '/ChatTeardrop.svg'
const ai1SearchAsset = '/MagnifyingGlass.svg'
const ai1NavCenterAsset = '/Icon-3.svg'
const ai1NavLeftAsset = '/user.svg'
const ai1NavRightAsset = '/lucide_map.svg'

function goToHome2() {
  activeScreen.value = 'home2'
}

function goToAi1() {
  activeScreen.value = 'ai1'
}

function goToAi5() {
  activeScreen.value = 'ai5'
}

function setActiveScreen(screen: Screen) {
  if (screen === 'profile' && activeScreen.value !== 'profile') {
    profileReturnScreen.value = activeScreen.value
  }

  activeScreen.value = screen
}

function openPlaceDetail(detail: PlaceDetail) {
  selectedPlaceDetail.value = detail
  activeScreen.value = 'placeDetail'
}

function goBackToItinerary() {
  activeScreen.value = 'itinerary'
}

function goBackToChat() {
  activeScreen.value = 'chat'
}

function goBackFromProfile() {
  activeScreen.value = profileReturnScreen.value === 'profile' ? 'ai1' : profileReturnScreen.value
}

function goBackFromSettings() {
  activeScreen.value = 'profile'
}

// AI5 偏好页状态
const ai5TimeType = ref('')
const ai5Activities = ref<string[]>([])
const ai5Range = ref('')
const ai5Budget = ref('')
const ai5Stay = ref('')
const ai5TimelineValue = ref(3) // 时间轴默认值，范围 1-6 小时

function selectAi5TimeType(type: string) {
  ai5TimeType.value = type

  if (type !== '周末两天') {
    ai5Stay.value = ''
  }
}

function toggleAi5Activity(tag: string) {
  const idx = ai5Activities.value.indexOf(tag)
  if (idx === -1) ai5Activities.value.push(tag)
  else ai5Activities.value.splice(idx, 1)
}

// Phone simulator enhancements
const deviceType = ref<'iphone14' | 'iphone15' | 'iphone16' | 'iphone16pro'>('iphone16')
const isRotated = ref(false)
const screenBrightness = ref(100)
const screenZoom = ref(100)

const deviceSpecs = {
  iphone14: { name: 'iPhone 14', width: 390, height: 844 },
  iphone15: { name: 'iPhone 15', width: 393, height: 852 },
  iphone16: { name: 'iPhone 16', width: 393, height: 852 },
  iphone16pro: { name: 'iPhone 16 Pro', width: 402, height: 874 }
}

function toggleRotate() {
  isRotated.value = !isRotated.value
}

function resetSimulator() {
  screenBrightness.value = 100
  screenZoom.value = 100
  isRotated.value = false
}

function changeDevice(device: typeof deviceType.value) {
  deviceType.value = device
}

function takeScreenshot() {
  const shell = document.querySelector('.iphone-shell') as HTMLElement
  if (!shell) return
  
  // Simple approach: use html2canvas or built-in screenshot
  alert('Screenshot功能可通过集成html2canvas库实现 📸')
}
</script>

<template>
  <div class="preview-page">
    <!-- 控制面板 -->
    <div class="device-controls">
      <div class="control-section">
        <label class="control-label">设备选择</label>
        <div class="device-buttons">
          <button
            v-for="(spec, device) in deviceSpecs"
            :key="device"
            :class="['device-btn', { active: deviceType === device }]"
            @click="changeDevice(device as any)"
          >
            {{ spec.name }}
          </button>
        </div>
      </div>

      <div class="control-section">
        <label class="control-label">屏幕亮度: {{ screenBrightness }}%</label>
        <input
          v-model.number="screenBrightness"
          type="range"
          min="30"
          max="100"
          class="slider"
        />
      </div>

      <div class="control-section">
        <label class="control-label">缩放: {{ screenZoom }}%</label>
        <input
          v-model.number="screenZoom"
          type="range"
          min="50"
          max="150"
          step="10"
          class="slider"
        />
      </div>

      <div class="control-section">
        <div class="control-buttons">
          <button
            :class="['control-btn', { active: isRotated }]"
            @click="toggleRotate"
            title="旋转设备"
          >
            🔄 旋转
          </button>
          <button class="control-btn" @click="resetSimulator" title="重置模拟器">
            ↺ 重置
          </button>
          <button class="control-btn" @click="takeScreenshot" title="截图">
            📸 截图
          </button>
        </div>
      </div>

      <div class="device-info">
        <p><strong>当前设备:</strong> {{ deviceSpecs[deviceType].name }}</p>
        <p><strong>分辨率:</strong> {{ deviceSpecs[deviceType].width }} × {{ deviceSpecs[deviceType].height }}</p>
        <p><strong>状态:</strong> {{ isRotated ? '横屏模式' : '竖屏模式' }}</p>
      </div>
    </div>

    <!-- iPhone 外壳 -->
    <div
      class="iphone-shell"
      :style="{
        transform: `${isRotated ? 'rotate(90deg)' : ''} scale(${screenZoom / 100})`,
        filter: `brightness(${screenBrightness}%)`
      }"
    >
      <div class="iphone-body">
        <div class="dynamic-island"></div>

        <!-- 屏幕区域，严格 393×852 -->
        <div class="app-container">
          <main
            v-if="activeScreen === 'home1'"
            class="screen home1-screen"
            data-node-id="147:12"
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

            <header class="status-bar" data-node-id="147:13">
              <div class="status-time" data-node-id="147:15">9:41</div>
              <div class="status-island" data-node-id="147:17"></div>
              <img :src="levelsAsset" alt="" class="status-levels" data-node-id="147:18" />
            </header>

            <section class="brand-block" data-node-id="147:786">
              <img :src="logoAsset" alt="Weekendgo Logo" class="brand-logo" data-node-id="147:801" />
              <h1 class="brand-title" data-node-id="147:35">Weekendgo</h1>
            </section>

            <p class="tagline" data-node-id="147:36">你的闲时逛逛搭子</p>

            <footer class="home-indicator-wrap" data-node-id="147:26">
              <div class="home-indicator" data-node-id="147:27"></div>
            </footer>
          </main>

          <main v-else-if="activeScreen === 'home2'" class="screen home2-screen" data-node-id="224:1574">
            <div class="screen-bg" aria-hidden="true">
              <div class="bg-blob bg-blob-rose home2-blob-rose"></div>
              <div class="bg-blob bg-blob-gold home2-blob-gold"></div>
              <div class="bg-blob bg-blob-ivory home2-blob-ivory"></div>
              <div class="bg-blob bg-blob-mist home2-blob-mist"></div>
            </div>

            <header class="status-bar" data-node-id="147:13">
              <div class="status-time" data-node-id="147:15">9:41</div>
              <div class="status-island" data-node-id="147:17"></div>
              <img :src="levelsAsset" alt="" class="status-levels" data-node-id="147:18" />
            </header>

            <section class="login-brand-block">
              <img :src="logoAsset" alt="Weekendgo Logo" class="login-brand-logo" />
              <h2 class="login-brand-title">Weekendgo</h2>
            </section>

            <section class="login-copy-block">
              <h1 class="login-title">轻松规划你的周末闲时活动 让每一刻都不浪费</h1>
            </section>

            <section class="login-form">
              <label class="login-field">
                <span class="login-field-label">昵称</span>
              </label>
              <label class="login-field">
                <span class="login-field-label">手机号</span>
              </label>
              <label class="login-field login-field-password">
                <span class="login-field-label">密码</span>
              </label>
            </section>

            <button type="button" class="login-button" @click="goToAi1">登录</button>

            <section class="login-divider-row">
              <div class="login-divider-line"></div>
              <p class="login-divider-text">或者使用以下方式登录</p>
              <div class="login-divider-line"></div>
            </section>

            <section class="social-login-row">
              <button type="button" class="social-login-button" aria-label="苹果登录">
                <img :src="appleAsset" alt="" class="social-login-icon social-login-icon-apple" />
              </button>
              <button type="button" class="social-login-button" aria-label="微信登录">
                <img :src="wechatAsset" alt="" class="social-login-icon" />
              </button>
              <button type="button" class="social-login-button" aria-label="美团登录">
                <img :src="meituanAsset" alt="" class="social-login-icon" />
              </button>
            </section>

            <p class="signup-hint">
              还没有账户？
              <a href="#" class="signup-link">注册账号</a>
            </p>

            <footer class="home-indicator-wrap" data-node-id="147:26">
              <div class="home-indicator" data-node-id="147:27"></div>
            </footer>
          </main>

          <main v-else-if="activeScreen === 'ai1'" class="screen ai1-screen" data-node-id="210:628" @mousemove="handleMouseMove" @mouseup="handleMouseUp" @mouseleave="handleMouseUp">
            <!-- 背景光斑：纯 CSS 渐变，避免位图边缘伪影 -->
            <div class="ai1-bg" aria-hidden="true"></div>

            <!-- 状态栏 -->
            <header class="ai1-status-bar" data-node-id="210:638">
              <div class="ai1-status-time">9:41</div>
              <div class="ai1-status-island"></div>
              <img :src="ai1LevelsAsset" alt="" class="ai1-status-levels" />
            </header>

            <!-- 主标题 -->
            <h1 class="ai1-title" data-node-id="210:653">今天想怎么过？</h1>

            <!-- 活动推荐卡：轮播容器 -->
            <div
              class="ai1-card"
              data-node-id="188:591"
              @touchstart="handleTouchStart"
              @touchend="handleTouchEnd"
              @mousedown="handleMouseDown"
            >
              <!-- 每张卡片独立背景色 -->
              <div class="ai1-card-bg" :style="{ background: cardList[currentCardIndex].cardBg }"></div>
              <!-- 图片区域 -->
              <div class="ai1-card-photo-wrap">
                <img :src="cardList[currentCardIndex].photo" :alt="cardList[currentCardIndex].title" class="ai1-card-photo" />
              </div>
              <!-- 标签（居中，top:122px） -->
              <div class="ai1-tags">
                <span
                  v-for="tag in cardList[currentCardIndex].tags"
                  :key="tag"
                  class="ai1-tag"
                  :style="{ background: cardList[currentCardIndex].tagColor, color: cardList[currentCardIndex].tagTextColor }"
                >{{ tag }}</span>
              </div>
              <!-- 卡片标题 -->
              <p class="ai1-card-title">{{ cardList[currentCardIndex].title }}</p>
              <!-- Go 按钞 -->
              <button type="button" class="ai1-card-go" aria-label="Go">Go</button>
              <!-- 时间胶囊 -->
              <div class="ai1-card-time-pill">
                <span class="ai1-card-time-text">{{ cardList[currentCardIndex].time }}</span>
              </div>
            </div>

            <!-- 说明文字 -->
            <p class="ai1-hint" data-node-id="210:654">选一个状态，我来为你生成一条刚刚好的出行路线</p>

            <!-- 翻页指示点 -->
            <div class="ai1-dots" data-node-id="210:675">
              <span
                v-for="(_, index) in cardList"
                :key="index"
                class="ai1-dot"
                :class="{ 'ai1-dot-active': index === currentCardIndex }"
              ></span>
            </div>

            <!-- 输入搜索栏 (left:19 top:537 w:357 h:47) -->
            <label class="ai1-input-bar" data-node-id="233:1064">
              <img :src="ai1SparkIconAsset" alt="" class="ai1-input-spark" />
              <input
                type="text"
                class="ai1-input-field"
                aria-label="输入出行想法"
                enterkeyhint="done"
              />
              <img :src="ai1MicGroupAsset" alt="" class="ai1-input-mic" />
            </label>

            <!-- 补充想法 (left:122 top:606 w:149 h:32) -->
            <div class="ai1-supplement" data-node-id="210:679"
                 role="button" tabindex="0"
                 @click="goToAi5"
                 @keyup.enter="goToAi5">
              <span class="ai1-supplement-text">补充我的想法</span>
              <img :src="ai1VectorAsset" alt="" class="ai1-supplement-arrow" />
            </div>

            <!-- 底部导航背景胶囊 (left:33 top:765 w:327 h:54) -->
            <div class="ai1-nav-bg" data-node-id="233:997"></div>
            <!-- 个人 (left:41 top:768 size:48) -->
            <button
              type="button"
              class="ai1-nav-btn ai1-nav-btn-muted"
              style="left:41px;top:768px;"
              aria-label="个人"
              @click="setActiveScreen('profile')"
            >
              <img :src="ai1NavLeftAsset" alt="" class="ai1-nav-btn-user-icon" />
            </button>
            <!-- 发现 (left:113 top:768 size:48) -->
            <button
              type="button"
              class="ai1-nav-btn ai1-nav-btn-muted"
              style="left:113px;top:768px;"
              aria-label="发现"
              @click="setActiveScreen('discover')"
            >
              <img :src="ai1SearchAsset" alt="" class="ai1-nav-btn-search-icon" />
            </button>
            <!-- AI (left:177 top:768 size:48) -->
            <button
              type="button"
              class="ai1-nav-btn ai1-nav-btn-active"
              style="left:177px;top:768px;"
              aria-label="AI"
              aria-current="page"
              @click="setActiveScreen('ai1')"
            >
              <img :src="ai1NavCenterAsset" alt="" class="ai1-nav-btn-ai-icon" />
            </button>
            <!-- 行程 (left:240 top:768 size:48) -->
            <button
              type="button"
              class="ai1-nav-btn ai1-nav-btn-muted"
              style="left:240px;top:768px;"
              aria-label="行程"
              @click="setActiveScreen('itinerary')"
            >
              <img :src="ai1NavRightAsset" alt="" class="ai1-nav-btn-trip-icon" />
            </button>
            <!-- 聊天 (left:305 top:768 size:48) -->
            <button
              type="button"
              class="ai1-nav-btn ai1-nav-btn-muted"
              style="left:305px;top:768px;"
              aria-label="聊天"
              @click="setActiveScreen('chat')"
            >
              <img :src="ai1MicAsset" alt="" class="ai1-nav-btn-chat-icon" />
            </button>

            <!-- Home Indicator -->
            <footer class="home-indicator-wrap" data-node-id="210:651">
              <div class="home-indicator"></div>
            </footer>
          </main>

          <!-- AI偏好设置页 (node 224:1026) -->
          <main v-else-if="activeScreen === 'ai5'" class="screen ai5-screen" data-node-id="224:1026">
            <div class="screen-bg" aria-hidden="true">
              <div class="bg-blob bg-blob-rose"></div>
              <div class="bg-blob bg-blob-gold"></div>
              <div class="bg-blob bg-blob-ivory"></div>
              <div class="bg-blob bg-blob-mist"></div>
            </div>

            <!-- 状态栏 -->
            <header class="ai1-status-bar">
              <div class="ai1-status-time">9:41</div>
              <div class="ai1-status-island"></div>
              <img :src="levelsAsset" alt="" class="ai1-status-levels" />
            </header>

            <!-- 返回按鈕 -->
            <button type="button" class="ai5-back-btn" @click="activeScreen = 'ai1'" aria-label="返回">
              <span class="ai5-back-chevron"></span>
            </button>

            <!-- 页面标题 -->
            <h1 class="ai5-page-title">告诉我你的偏好</h1>

            <!-- 跳过 -->
            <button type="button" class="ai5-skip-btn" @click="activeScreen = 'itinerary'">跳过</button>

            <div class="ai5-scroll">
              <section class="ai5-section ai5-section-first">
                <p class="ai5-label">游玩时间类型</p>
                <div class="ai5-row ai5-row-pill">
                  <button class="ai5-pill" :class="{active: ai5TimeType==='短时闲逛'}" @click="selectAi5TimeType('短时闲逛')">短时闲逛</button>
                  <button class="ai5-pill" :class="{active: ai5TimeType==='城市一日'}" @click="selectAi5TimeType('城市一日')">城市一日</button>
                  <button class="ai5-pill" :class="{active: ai5TimeType==='周末两天'}" @click="selectAi5TimeType('周末两天')">周末两天</button>
                </div>
              </section>

              <section v-if="ai5TimeType === '短时闲逛'" class="ai5-section ai5-section-timeline">
                <div class="ai5-timeline-container">
                  <p class="ai5-timeline-label">预计可用时间</p>
                  <div class="ai5-timeline-track">
                    <span class="ai5-timeline-min">1小时</span>
                    <input
                      v-model.number="ai5TimelineValue"
                      type="range"
                      min="1"
                      max="6"
                      class="ai5-timeline-slider"
                    />
                    <span class="ai5-timeline-max">6小时</span>
                  </div>
                  <p class="ai5-timeline-current">{{ ai5TimelineValue }}小时</p>
                </div>
              </section>

              <section v-if="ai5TimeType === '周末两天'" class="ai5-section">
                <p class="ai5-label">是否在沪留宿</p>
                <div class="ai5-row ai5-row-stay">
                  <button class="ai5-pill ai5-pill--stay" :class="{active: ai5Stay==='是'}" @click="ai5Stay='是'">是</button>
                  <button class="ai5-pill ai5-pill--stay" :class="{active: ai5Stay==='否'}" @click="ai5Stay='否'">否</button>
                </div>
              </section>

              <section class="ai5-section">
                <p class="ai5-label">活动偏好 (多选)</p>
                <div class="ai5-chip-grid">
                  <button class="ai5-chip" :class="{active: ai5Activities.includes('寻味美食')}" @click="toggleAi5Activity('寻味美食')">寻味美食</button>
                  <button class="ai5-chip" :class="{active: ai5Activities.includes('喝咖啡')}" @click="toggleAi5Activity('喝咖啡')">喝咖啡</button>
                  <button class="ai5-chip" :class="{active: ai5Activities.includes('逛街区')}" @click="toggleAi5Activity('逛街区')">逛街区</button>
                  <button class="ai5-chip" :class="{active: ai5Activities.includes('手作体验')}" @click="toggleAi5Activity('手作体验')">手作体验</button>
                  <button class="ai5-chip" :class="{active: ai5Activities.includes('城市散步')}" @click="toggleAi5Activity('城市散步')">城市散步</button>
                  <button class="ai5-chip" :class="{active: ai5Activities.includes('拍照打卡')}" @click="toggleAi5Activity('拍照打卡')">拍照打卡</button>
                  <button class="ai5-chip" :class="{active: ai5Activities.includes('书店阅读')}" @click="toggleAi5Activity('书店阅读')">书店阅读</button>
                  <button class="ai5-chip" :class="{active: ai5Activities.includes('看展览')}" @click="toggleAi5Activity('看展览')">看展览</button>
                </div>
              </section>

              <section class="ai5-section">
                <p class="ai5-label">出行范围</p>
                <div class="ai5-row ai5-row-pill">
                  <button class="ai5-pill" :class="{active: ai5Range==='就近玩玩'}" @click="ai5Range='就近玩玩'">就近玩玩</button>
                  <button class="ai5-pill" :class="{active: ai5Range==='地铁30分钟'}" @click="ai5Range='地铁30分钟'">地铁30分钟</button>
                  <button class="ai5-pill" :class="{active: ai5Range==='可以跨区'}" @click="ai5Range='可以跨区'">可以跨区</button>
                </div>
              </section>

              <section class="ai5-section">
                <p class="ai5-label">人均预算</p>
                <div class="ai5-budget-grid">
                  <button class="ai5-budget" :class="{active: ai5Budget==='100元内'}" @click="ai5Budget='100元内'">100元内</button>
                  <button class="ai5-budget" :class="{active: ai5Budget==='100-200元'}" @click="ai5Budget='100-200元'">100-200元</button>
                  <button class="ai5-budget" :class="{active: ai5Budget==='200-300元'}" @click="ai5Budget='200-300元'">200-300元</button>
                  <button class="ai5-budget" :class="{active: ai5Budget==='不限'}" @click="ai5Budget='不限'">不限</button>
                </div>
              </section>

              <button type="button" class="ai5-cta-btn" @click="activeScreen = 'itinerary'">
                生成我的闲时计划<span class="ai5-cta-lightning">⚡</span>
              </button>
            </div>

            <!-- Home Indicator -->
            <footer class="home-indicator-wrap">
              <div class="home-indicator"></div>
            </footer>
          </main>

          <!-- 行程页 (node 156:994) -->
          <main v-else-if="activeScreen === 'itinerary'" class="screen" data-node-id="156:994">
            <ItineraryPage @navigate="setActiveScreen" @view-detail="openPlaceDetail" />
          </main>

          <main v-else-if="activeScreen === 'discover'" class="screen" data-node-id="156:553">
            <DiscoverPage @navigate="setActiveScreen" />
          </main>

          <main v-else-if="activeScreen === 'profile'" class="screen" data-node-id="156:729">
            <ProfilePage @navigate="setActiveScreen" @back="goBackFromProfile" />
          </main>

          <main v-else-if="activeScreen === 'settings'" class="screen" data-node-id="187:265">
            <SettingsPage @back="goBackFromSettings" />
          </main>

          <main v-else-if="activeScreen === 'createPost'" class="screen" data-node-id="181:320">
            <CreatePostPage @navigate="setActiveScreen" />
          </main>

          <main v-else-if="activeScreen === 'chat'" class="screen" data-node-id="155:61">
            <ChatPage @navigate="setActiveScreen" />
          </main>

          <main v-else-if="activeScreen === 'chatDetail'" class="screen" data-node-id="155:314">
            <ChatThreadPage @back="goBackToChat" />
          </main>

          <main v-else-if="activeScreen === 'navigation'" class="screen" data-node-id="174:375">
            <NavigationPage @back="goBackToItinerary" />
          </main>

          <main v-else-if="activeScreen === 'placeDetail'" class="screen" data-node-id="233:1138">
            <PlaceDetailPage v-if="selectedPlaceDetail" :detail="selectedPlaceDetail" @back="goBackToItinerary" />
          </main>
        </div>
      </div>

      <!-- 侧边按钮 -->
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
