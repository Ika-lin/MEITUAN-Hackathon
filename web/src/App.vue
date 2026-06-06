<script setup lang="ts">
import { ref } from 'vue'

const activeScreen = ref<'home1' | 'home2' | 'ai1'>('home1')

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

          <main v-else class="screen ai1-screen" data-node-id="210:628" @mousemove="handleMouseMove" @mouseup="handleMouseUp" @mouseleave="handleMouseUp">
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
            <div class="ai1-supplement" data-node-id="210:679">
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
