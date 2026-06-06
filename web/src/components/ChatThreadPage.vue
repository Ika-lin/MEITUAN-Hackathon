<script setup lang="ts">
const emit = defineEmits<{
  back: []
}>()

type ThreadMessage = {
  id: string
  sender: string
  time: string
  side: 'left' | 'right'
  text?: string
  image?: string
  imageCount?: number
  avatar?: string
  tone?: 'pink' | 'lavender'
}

const levelsAsset = '/Levels.svg'
const backAsset = '/chevron-left.svg'
const phoneAsset = '/Phone.svg'
const paperclipAsset = '/Paperclip.svg'
const microphoneAsset = '/Microphone.svg'
const paperPlaneAsset = '/PaperPlane.svg'
const groupCoverAsset = '/group-chat-cover.png'

const threadMessages: ThreadMessage[] = [
  {
    id: 'msg-1',
    sender: '小千',
    time: '1.55 PM',
    side: 'left',
    text: '终于凑齐啦，我提前做攻略了，武康大楼先打卡，梧桐遮阴特别出片，上午光线柔和最适合拍复古片。',
    avatar: '/Chat Image-1.png',
    tone: 'pink',
  },
  {
    id: 'msg-2',
    sender: '小优',
    time: '1.56 PM',
    side: 'left',
    text: '相机充电宝塞满了，还带了胶卷相机！',
    avatar: '/2149265200 1.png',
    tone: 'pink',
  },
  {
    id: 'msg-3',
    sender: '我',
    time: '2.12 PM',
    side: 'right',
    text: 'OK!',
    tone: 'lavender',
  },
  {
    id: 'msg-4',
    sender: '我',
    time: '2.12 PM',
    side: 'right',
    text: '顺路还能借街边复古自行车当道具，很多网红老洋房围栏边超好拍半身。',
    tone: 'lavender',
  },
  {
    id: 'msg-5',
    sender: '小优',
    time: '2.15 PM',
    side: 'left',
    text: '成片绝了，光影打在洋房窗沿，氛围感直接拉满。',
    avatar: '/2149265200 1.png',
    tone: 'pink',
  },
  {
    id: 'msg-6',
    sender: '小优',
    time: '2.15 PM',
    side: 'left',
    image: groupCoverAsset,
    imageCount: 3,
    avatar: '/2149265200 1.png',
    tone: 'pink',
  },
  {
    id: 'msg-7',
    sender: '我',
    time: '2.30 PM',
    side: 'right',
    text: '好漂亮！',
    tone: 'lavender',
  },
]
</script>

<template>
  <div class="chat-thread-page">
    <div class="chat-thread-bg" aria-hidden="true"></div>

    <header class="chat-thread-status-bar">
      <div class="chat-thread-time">9:41</div>
      <div class="chat-thread-island"></div>
      <img :src="levelsAsset" alt="" class="chat-thread-levels" />
    </header>

    <section class="chat-thread-header">
      <button type="button" class="chat-thread-header-btn" aria-label="返回聊天列表" @click="emit('back')">
        <img :src="backAsset" alt="" class="chat-thread-back-icon" />
      </button>

      <div class="chat-thread-header-main">
        <img :src="groupCoverAsset" alt="武康路老洋房摄影" class="chat-thread-group-avatar" />

        <div class="chat-thread-group-copy">
          <h1 class="chat-thread-group-title">武康路老洋房摄影</h1>
          <p class="chat-thread-group-meta">3 members</p>
        </div>
      </div>

      <button type="button" class="chat-thread-header-btn" aria-label="发起通话">
        <img :src="phoneAsset" alt="" class="chat-thread-phone-icon" />
      </button>
    </section>

    <section class="chat-thread-body">
      <article
        v-for="message in threadMessages"
        :key="message.id"
        class="chat-thread-message"
        :class="{
          'chat-thread-message-left': message.side === 'left',
          'chat-thread-message-right': message.side === 'right',
        }"
      >
        <template v-if="message.side === 'left'">
          <div class="chat-thread-left-shell">
            <div class="chat-thread-left-meta">
              <img v-if="message.avatar" :src="message.avatar" :alt="message.sender" class="chat-thread-avatar" />
              <span class="chat-thread-sender">{{ message.sender }}</span>
              <span class="chat-thread-stamp">{{ message.time }}</span>
            </div>

            <div v-if="message.text" class="chat-thread-bubble chat-thread-bubble-pink">
              {{ message.text }}
            </div>

            <div v-if="message.image" class="chat-thread-image-row">
              <img :src="message.image" :alt="message.sender + ' 分享的照片'" class="chat-thread-photo" />
              <span v-if="message.imageCount" class="chat-thread-photo-count">+{{ message.imageCount }}</span>
            </div>
          </div>
        </template>

        <template v-else>
          <div class="chat-thread-right-shell">
            <div class="chat-thread-right-meta">
              <span class="chat-thread-sender">{{ message.sender }}</span>
              <span class="chat-thread-stamp">{{ message.time }}</span>
            </div>

            <div v-if="message.text" class="chat-thread-bubble chat-thread-bubble-lavender">
              {{ message.text }}
            </div>
          </div>
        </template>
      </article>
    </section>

    <footer class="chat-thread-composer-wrap">
      <div class="chat-thread-composer">
        <button type="button" class="chat-thread-composer-side-btn" aria-label="添加附件">
          <img :src="paperclipAsset" alt="" class="chat-thread-composer-icon" />
        </button>

        <label class="chat-thread-input-shell">
          <img :src="microphoneAsset" alt="" class="chat-thread-input-mic" />
          <input type="text" class="chat-thread-input" aria-label="输入消息" />
        </label>

        <button type="button" class="chat-thread-send-btn" aria-label="发送消息">
          <img :src="paperPlaneAsset" alt="" class="chat-thread-send-icon" />
        </button>
      </div>

      <div class="chat-thread-home-indicator"></div>
    </footer>
  </div>
</template>

<style scoped>
.chat-thread-page {
  position: relative;
  height: 100%;
  overflow: hidden;
  background: linear-gradient(180deg, #f9f9f9 0%, #f8f4f4 62%, #f7f3ef 100%);
  font-family: 'SF Pro Rounded', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.chat-thread-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(44% 26% at 10% 82%, rgba(245, 195, 211, 0.86) 0%, rgba(245, 195, 211, 0) 72%),
    radial-gradient(34% 16% at 92% 98%, rgba(255, 236, 170, 0.84) 0%, rgba(255, 236, 170, 0) 72%),
    radial-gradient(46% 24% at 56% 64%, rgba(255, 255, 255, 0.92) 0%, rgba(255, 255, 255, 0) 80%);
}

.chat-thread-status-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 54px;
}

.chat-thread-time {
  width: 138px;
  color: #000;
  text-align: center;
  font-size: 17px;
  line-height: 22px;
  font-weight: 600;
  letter-spacing: -0.51px;
}

.chat-thread-island {
  width: 104px;
  height: 28px;
  border-radius: 999px;
  background: #2a2a2a;
}

.chat-thread-levels {
  width: 143px;
  height: 54px;
  object-fit: contain;
}

.chat-thread-header {
  position: absolute;
  top: 58px;
  left: 16px;
  right: 16px;
  z-index: 4;
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-thread-header-btn,
.chat-thread-composer-side-btn,
.chat-thread-send-btn {
  padding: 0;
  border: 0;
  cursor: pointer;
}

.chat-thread-header-btn {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 8px 20px rgba(35, 31, 32, 0.06);
  flex-shrink: 0;
}

.chat-thread-back-icon {
  width: 16px;
  height: 16px;
}

.chat-thread-phone-icon {
  width: 20px;
  height: 20px;
}

.chat-thread-header-main {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-thread-group-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.chat-thread-group-copy {
  min-width: 0;
}

.chat-thread-group-title,
.chat-thread-group-meta,
.chat-thread-sender,
.chat-thread-stamp {
  margin: 0;
}

.chat-thread-group-title {
  color: #2c2828;
  font-size: 16px;
  line-height: 22px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-thread-group-meta {
  color: #b0b0b0;
  font-size: 12px;
  line-height: 18px;
}

.chat-thread-body {
  position: absolute;
  top: 124px;
  left: 0;
  right: 0;
  bottom: 96px;
  z-index: 3;
  overflow-y: auto;
  padding: 8px 16px 24px;
  scrollbar-width: none;
}

.chat-thread-body::-webkit-scrollbar {
  display: none;
}

.chat-thread-message {
  display: flex;
  margin-bottom: 18px;
}

.chat-thread-message-left {
  justify-content: flex-start;
}

.chat-thread-message-right {
  justify-content: flex-end;
}

.chat-thread-left-shell,
.chat-thread-right-shell {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chat-thread-left-shell {
  max-width: 320px;
}

.chat-thread-right-shell {
  align-items: flex-end;
  max-width: 300px;
}

.chat-thread-left-meta,
.chat-thread-right-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-thread-right-meta {
  justify-content: flex-end;
}

.chat-thread-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.chat-thread-sender {
  color: #2c2828;
  font-size: 16px;
  line-height: 22px;
  font-weight: 600;
}

.chat-thread-stamp {
  color: #999;
  font-size: 12px;
  line-height: 18px;
}

.chat-thread-bubble {
  border-radius: 28px;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 24px;
  letter-spacing: 0.01em;
  box-shadow: 0 10px 24px rgba(53, 44, 54, 0.04);
}

.chat-thread-bubble-pink {
  background: #fa63a9;
  color: #fff;
}

.chat-thread-bubble-lavender {
  background: #d9c2ff;
  color: #2c2828;
}

.chat-thread-image-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  margin-left: 42px;
}

.chat-thread-photo {
  display: block;
  width: 204px;
  height: 254px;
  border-radius: 18px;
  object-fit: cover;
}

.chat-thread-photo-count {
  padding-bottom: 12px;
  color: #999;
  font-size: 14px;
  line-height: 20px;
}

.chat-thread-composer-wrap {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 4;
  padding: 8px 16px 8px;
}

.chat-thread-composer {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-thread-composer-side-btn {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.92);
}

.chat-thread-composer-icon {
  width: 24px;
  height: 24px;
}

.chat-thread-input-shell {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  height: 48px;
  padding: 0 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.96);
}

.chat-thread-input-mic {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.chat-thread-input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  color: #343330;
  font-size: 14px;
}

.chat-thread-send-btn {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #000;
}

.chat-thread-send-icon {
  width: 22px;
  height: 22px;
  filter: brightness(0) invert(1);
}

.chat-thread-home-indicator {
  width: 144px;
  height: 5px;
  margin: 10px auto 0;
  border-radius: 100px;
  background: #2a2a2a;
}
</style>