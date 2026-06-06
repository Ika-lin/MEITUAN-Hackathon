<script setup lang="ts">
import { ref } from 'vue'
import { computed } from 'vue'

const activeScreen = ref<'home1' | 'home2' | 'ai1' | 'ai5' | 'itinerary'>('home1')

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
const ai1MicAsset = 'https://www.figma.com/api/mcp/asset/4e819871-83a0-4659-aeb8-09d6741f852b'
const ai1VectorAsset = 'https://www.figma.com/api/mcp/asset/491a50d0-2331-4679-9b9a-14a8c39322dd'
const ai1SearchAsset = 'https://www.figma.com/api/mcp/asset/a2d32556-ed0d-45f1-b69d-e8fefe4c4c15'
const ai1NavCenterAsset = 'https://www.figma.com/api/mcp/asset/2d7f8b06-66d4-41ff-9503-73c02a38afe8'
const ai1NavLeftAsset = 'https://www.figma.com/api/mcp/asset/1b02c613-4c53-4f59-be0b-3831acae10bc'
const ai1NavRightAsset = 'https://www.figma.com/api/mcp/asset/bbdb994e-672d-4cb1-816a-d8fcd62348c7'
const ai1MicGroupAsset = 'https://www.figma.com/api/mcp/asset/a2768da7-ad02-4777-9a79-ecf393d548e3'

function goToHome2() {
  activeScreen.value = 'home2'
}

function goToAi1() {
  activeScreen.value = 'ai1'
}

function goToAi5() {
  activeScreen.value = 'ai5'
}

// AI5 偏好页状态
const ai5TimeType = ref('')
const ai5Activities = ref<string[]>([])
const ai5Range = ref('')
const ai5Budget = ref('')
const ai5Stay = ref('')
const ai5TimelineValue = ref(3) // 时间轴默认值，范围 1-6 小时

// 选周末两天时，活动偏好及以下区块整体下移 75px
// 短时闲逛时，活动偏好区块下移以容纳时间轴选择器
const ai5Offset = computed(() => {
  if (ai5TimeType.value === '周末两天') return 75
  if (ai5TimeType.value === '短时闲逛') return 100
  return 0
})

function toggleAi5Activity(tag: string) {
  const idx = ai5Activities.value.indexOf(tag)
  if (idx === -1) ai5Activities.value.push(tag)
  else ai5Activities.value.splice(idx, 1)
}
</script>

<template>
  <div class="preview-page">
    <!-- iPhone 16 外壳 -->
    <div class="iphone-shell">
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
            <!-- 头像/我的 (left:41 top:768 size:48) -->
            <img :src="ai1NavLeftAsset" alt="我的" class="ai1-nav-icon-abs" style="left:41px;top:768px;" />
            <!-- 搜索 (left:113 top:768 size:48) -->
            <div class="ai1-nav-circle ai1-nav-dim" style="left:113px;top:768px;">
              <img :src="ai1SearchAsset" alt="搜索" class="ai1-nav-inner" />
            </div>
            <!-- 主按钮黑圆 (left:177 top:768 size:48) -->
            <div class="ai1-nav-circle ai1-nav-black" style="left:177px;top:768px;">
              <img :src="ai1NavCenterAsset" alt="" class="ai1-nav-center-icon" />
            </div>
            <!-- 地图 (left:240 top:768 size:48) -->
            <img :src="ai1NavRightAsset" alt="地图" class="ai1-nav-icon-abs" style="left:240px;top:768px;" />
            <!-- 消息 (left:305 top:768 size:48) -->
            <div class="ai1-nav-circle ai1-nav-dim" style="left:305px;top:768px;">
              <img :src="ai1MicAsset" alt="消息" class="ai1-nav-inner" />
            </div>

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

            <!-- 游玩时间类型 -->
            <p class="ai5-label" style="top:159px">游玩时间类型</p>
            <div class="ai5-row" style="top:196px">
              <button class="ai5-pill" :class="{active: ai5TimeType==='短时闲逛'}" @click="ai5TimeType='短时闲逛'">短时闲逛</button>
              <button class="ai5-pill" :class="{active: ai5TimeType==='城市一日'}" @click="ai5TimeType='城市一日'">城市一日</button>
              <button class="ai5-pill" :class="{active: ai5TimeType==='周末两天'}" @click="ai5TimeType='周末两天'">周末两天</button>
            </div>

            <!-- 预计可用时间（仅短时闲逛显示） -->
            <template v-if="ai5TimeType === '短时闲逛'">
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
            </template>

            <!-- 是否在沪留宿（仅周末两天显示） -->
            <template v-if="ai5TimeType === '周末两天'">
              <p class="ai5-label" style="top:275px">是否在沪留宿</p>
              <div class="ai5-row" style="top:310px">
                <button class="ai5-pill ai5-pill--stay" :class="{active: ai5Stay==='是'}" @click="ai5Stay='是'">是</button>
                <button class="ai5-pill ai5-pill--stay" :class="{active: ai5Stay==='否'}" @click="ai5Stay='否'">否</button>
              </div>
            </template>

            <!-- 活动偏好 (多选) -->
            <p class="ai5-label" :style="{top: (275 + ai5Offset) + 'px'}">活动偏好 (多选)</p>
            <div class="ai5-row" :style="{top: (316 + ai5Offset) + 'px'}">
              <button class="ai5-chip" :class="{active: ai5Activities.includes('寻味美食')}" @click="toggleAi5Activity('寻味美食')">寻味美食</button>
              <button class="ai5-chip" :class="{active: ai5Activities.includes('喝咖啡')}" @click="toggleAi5Activity('喝咖啡')">喝咖啡</button>
              <button class="ai5-chip" :class="{active: ai5Activities.includes('逛街区')}" @click="toggleAi5Activity('逛街区')">逛街区</button>
              <button class="ai5-chip" :class="{active: ai5Activities.includes('手作体验')}" @click="toggleAi5Activity('手作体验')">手作体验</button>
            </div>
            <div class="ai5-row" :style="{top: (370 + ai5Offset) + 'px'}">
              <button class="ai5-chip" :class="{active: ai5Activities.includes('城市散步')}" @click="toggleAi5Activity('城市散步')">城市散步</button>
              <button class="ai5-chip" :class="{active: ai5Activities.includes('拍照打卡')}" @click="toggleAi5Activity('拍照打卡')">拍照打卡</button>
              <button class="ai5-chip" :class="{active: ai5Activities.includes('书店阅读')}" @click="toggleAi5Activity('书店阅读')">书店阅读</button>
              <button class="ai5-chip" :class="{active: ai5Activities.includes('看展览')}" @click="toggleAi5Activity('看展览')">看展览</button>
            </div>

            <!-- 出行范围 -->
            <p class="ai5-label" :style="{top: (444 + ai5Offset) + 'px'}">出行范围</p>
            <div class="ai5-row" :style="{top: (479 + ai5Offset) + 'px'}">
              <button class="ai5-pill" :class="{active: ai5Range==='就近玩玩'}" @click="ai5Range='就近玩玩'">就近玩玩</button>
              <button class="ai5-pill" :class="{active: ai5Range==='地铁30分钟'}" @click="ai5Range='地铁30分钟'">地铁30分钟</button>
              <button class="ai5-pill" :class="{active: ai5Range==='可以跨区'}" @click="ai5Range='可以跨区'">可以跨区</button>
            </div>

            <!-- 人均预算 -->
            <p class="ai5-label" :style="{top: (552 + ai5Offset) + 'px'}">人均预算</p>
            <div class="ai5-row" :style="{top: (586 + ai5Offset) + 'px'}">
              <button class="ai5-budget" :class="{active: ai5Budget==='100元内'}" @click="ai5Budget='100元内'">100元内</button>
              <button class="ai5-budget" :class="{active: ai5Budget==='100-200元'}" @click="ai5Budget='100-200元'">100-200元</button>
              <button class="ai5-budget" :class="{active: ai5Budget==='200-300元'}" @click="ai5Budget='200-300元'">200-300元</button>
              <button class="ai5-budget" :class="{active: ai5Budget==='不限'}" @click="ai5Budget='不限'">不限</button>
            </div>

            <!-- 生成按鈕 -->
            <button type="button" class="ai5-cta-btn" @click="activeScreen = 'itinerary'">
              生成我的闲时计划<span class="ai5-cta-lightning">⚡</span>
            </button>

            <!-- Home Indicator -->
            <footer class="home-indicator-wrap">
              <div class="home-indicator"></div>
            </footer>
          </main>

          <!-- 行程页 (node 156:994) -->
          <main v-else-if="activeScreen === 'itinerary'" class="screen itinerary-screen" data-node-id="156:994">
            <!-- 背景装饰 -->
            <div class="itinerary-bg-decoration"></div>

            <!-- 状态栏 -->
            <header class="ai1-status-bar">
              <div class="ai1-status-time">9:41</div>
              <div class="ai1-status-island"></div>
              <img :src="levelsAsset" alt="" class="ai1-status-levels" />
            </header>

            <!-- 地址导航栏 -->
            <div class="itinerary-address-bar">
              <div class="itinerary-address-info">
                <div class="itinerary-address-item">
                  <span class="itinerary-icon">📍</span>
                  <span class="itinerary-address-text">上海市徐汇区武康路 376 号附近</span>
                </div>
                <div class="itinerary-address-divider"></div>
                <div class="itinerary-address-item">
                  <span class="itinerary-icon">📍</span>
                  <span class="itinerary-address-text">上海市徐汇区上海图书馆地铁站</span>
                </div>
              </div>
              <div class="itinerary-action-buttons">
                <button class="itinerary-icon-btn" aria-label="更多选项">⋮</button>
                <button class="itinerary-icon-btn" aria-label="交换">🔄</button>
              </div>
            </div>

            <!-- 地图信息卡 -->
            <div class="itinerary-map-card">
              <p class="itinerary-map-title">步行时间</p>
              <div class="itinerary-stats">
                <div class="itinerary-stat">
                  <span class="itinerary-stat-label">总路程</span>
                  <span class="itinerary-stat-value">约1.8km</span>
                </div>
                <div class="itinerary-stat">
                  <span class="itinerary-stat-label">交通方式</span>
                  <span class="itinerary-stat-value">全程步行</span>
                </div>
                <div class="itinerary-stat">
                  <span class="itinerary-stat-label">预算估测</span>
                  <span class="itinerary-stat-value">¥230–350/人</span>
                </div>
                <div class="itinerary-stat">
                  <span class="itinerary-stat-label">预计时间</span>
                  <span class="itinerary-stat-value">约25分钟</span>
                </div>
              </div>
            </div>

            <!-- 行程卡片 -->
            <div class="itinerary-cards-container">
              <!-- 第1个卡片 -->
              <div class="itinerary-card">
                <div class="itinerary-card-time">14:08 - 14:55（50分钟）</div>
                <div class="itinerary-card-number">1</div>
                <h3 class="itinerary-card-name">FILM电影时光书店</h3>
                <div class="itinerary-card-tags">
                  <span class="itinerary-tag">电影主题</span>
                  <span class="itinerary-tag">安静翻阅</span>
                  <span class="itinerary-tag">胶片气质</span>
                </div>
                <p class="itinerary-card-price">人均 ¥43</p>
                <div class="itinerary-card-actions">
                  <button class="itinerary-btn-detail">查看详情</button>
                  <button class="itinerary-btn-swap">换一个</button>
                </div>
              </div>

              <!-- 中间步行时间 -->
              <div class="itinerary-walking">
                <span>⬇️</span>
                <span class="itinerary-walking-text">步行约 5 分钟</span>
              </div>

              <!-- 第2个卡片 -->
              <div class="itinerary-card">
                <div class="itinerary-card-time">15:00 - 16:00（60分钟）</div>
                <div class="itinerary-card-number">2</div>
                <h3 class="itinerary-card-name">RAC BAR（安福路店）</h3>
                <div class="itinerary-card-tags">
                  <span class="itinerary-tag">街角咖啡</span>
                  <span class="itinerary-tag">露台小坐</span>
                  <span class="itinerary-tag">法式风情</span>
                </div>
                <p class="itinerary-card-price">人均 ¥120-150</p>
                <div class="itinerary-card-actions">
                  <button class="itinerary-btn-detail">查看详情</button>
                  <button class="itinerary-btn-swap">换一个</button>
                </div>
              </div>

              <!-- 中间步行时间 -->
              <div class="itinerary-walking">
                <span>⬇️</span>
                <span class="itinerary-walking-text">步行约 8–10 分钟</span>
              </div>

              <!-- 第3个卡片 -->
              <div class="itinerary-card">
                <div class="itinerary-card-time">16:10 - 16:50（40分钟）</div>
                <div class="itinerary-card-number">3</div>
                <h3 class="itinerary-card-name">一面春风 （吴兴路总店/武康周边）</h3>
                <div class="itinerary-card-tags">
                  <span class="itinerary-tag">烟火小馆</span>
                  <span class="itinerary-tag">本帮风味</span>
                  <span class="itinerary-tag">匠心汤底</span>
                </div>
                <p class="itinerary-card-price">人均 ¥55-70</p>
                <div class="itinerary-card-actions">
                  <button class="itinerary-btn-detail">查看详情</button>
                  <button class="itinerary-btn-swap">换一个</button>
                </div>
              </div>
            </div>

            <!-- 出发前提醒 -->
            <div class="itinerary-reminders">
              <h3 class="itinerary-section-title">出发前提醒</h3>
              <div class="itinerary-reminder-box">
                <div class="itinerary-reminder-item">
                  <strong>今日提醒</strong>
                  <ul class="itinerary-reminder-list">
                    <li>暴晒 25℃</li>
                    <li>RAC BAR 可能等位</li>
                    <li>已预留缓冲</li>
                  </ul>
                </div>
                <div class="itinerary-reminder-item">
                  <strong>建议携带</strong>
                  <ul class="itinerary-reminder-checklist">
                    <li><input type="checkbox"> 遮阳伞</li>
                    <li><input type="checkbox"> 一台傻瓜胶片相机</li>
                    <li><input type="checkbox"> 充电宝</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- 调整选项 -->
            <div class="itinerary-adjustments">
              <h3 class="itinerary-section-title">想调整一下？</h3>
              <div class="itinerary-adjustment-buttons">
                <button class="itinerary-adjustment-btn">更轻松一点</button>
                <button class="itinerary-adjustment-btn">避开排队</button>
                <button class="itinerary-adjustment-btn itinerary-adjustment-btn-primary">减少步行</button>
                <button class="itinerary-adjustment-btn itinerary-adjustment-btn-primary">重新生成</button>
              </div>
            </div>

            <!-- 底部导航 -->
            <div class="itinerary-bottom-nav">
              <button class="itinerary-nav-btn" aria-label="我的">👤</button>
              <button class="itinerary-nav-btn" aria-label="搜索">🔍</button>
              <button class="itinerary-nav-btn itinerary-nav-primary" aria-label="开始导航">🧭</button>
              <button class="itinerary-nav-btn" aria-label="消息">💬</button>
              <button class="itinerary-nav-btn" aria-label="返回AI1" @click="activeScreen = 'ai1'">×</button>
            </div>

            <!-- Home Indicator -->
            <footer class="home-indicator-wrap">
              <div class="home-indicator"></div>
            </footer>
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
