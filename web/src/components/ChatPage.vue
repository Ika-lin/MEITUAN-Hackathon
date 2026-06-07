<script setup lang="ts">
type Screen = 'discover' | 'ai1' | 'itinerary' | 'chat' | 'chatDetail' | 'profile'

const emit = defineEmits<{
  navigate: [screen: Screen]
}>()

type Story = {
  id: string
  label: string
  image: string
  highlighted?: boolean
  isSelf?: boolean
}

type Conversation = {
  id: string
  title: string
  preview: string
  time: string
  image: string
  unread?: number
  isGroup?: boolean
}

const levelsAsset = '/Levels.svg'
const searchAsset = '/uil_search.svg'
const caretAsset = '/CaretRight.svg'
const userAsset = '/user.svg'
const aiAsset = '/Icon.svg'
const tripAsset = '/lucide_map.svg'
const chatAsset = '/ChatTeardrop-light.svg'
const groupChatCoverAsset = '/group-chat-cover.png'

const stories: Story[] = [
  {
    id: 'self',
    label: '我',
    image: '/3b7a548733ee2a58982b32aae111822d65320db9.jpg',
    isSelf: true,
  },
  {
    id: 'xiaoyou',
    label: '小优',
    image: '/2149265200 1.png',
    highlighted: true,
  },
  {
    id: 'xiaoai',
    label: '小艾',
    image: '/Chat Image.png',
    highlighted: true,
  },
  {
    id: 'jack',
    label: '杰克',
    image: '/Chat Image-2.png',
  },
  {
    id: 'xiaogai',
    label: '小盖',
    image: '/Profile Image.png',
  },
  {
    id: 'xiaoqian',
    label: '小千',
    image: '/Chat Image-1.png',
  },
]

const conversations: Conversation[] = [
  {
    id: 'group',
    title: '武康路老洋房摄影',
    preview: 'OK!',
    time: '2.12PM',
    image: groupChatCoverAsset,
    isGroup: true,
  },
  {
    id: 'xiaoai',
    title: '小艾',
    preview: '你们拍的照片好漂亮，可以分享一下技巧吗？',
    time: '2.35 PM',
    image: '/Chat Image.png',
    unread: 1,
  },
  {
    id: 'xiaogai',
    title: '小盖',
    preview: '你们拍的下午阳光很好！',
    time: '2.25 PM',
    image: '/Profile Image.png',
    unread: 1,
  },
  {
    id: 'xiaoyou',
    title: '小优',
    preview: '回头我把照片传给你。',
    time: '2.16PM',
    image: '/2149265200 1.png',
  },
  {
    id: 'xiaoqian',
    title: '小千',
    preview: '你带相机了吗？',
    time: '1.56 PM',
    image: '/Chat Image-1.png',
    unread: 1,
  },
  {
    id: 'jack',
    title: '杰克',
    preview: '我们约在校外Manner咖啡店吧。',
    time: '11月1日',
    image: '/Chat Image-2.png',
  },
]

function openConversation(conversation: Conversation) {
  if (conversation.id !== 'group') return
  emit('navigate', 'chatDetail')
}
</script>

<template>
  <div class="chat-page">
    <div class="chat-page-bg" aria-hidden="true"></div>

    <header class="chat-status-bar">
      <div class="chat-status-time">9:41</div>
      <div class="chat-status-island"></div>
      <img :src="levelsAsset" alt="" class="chat-status-levels" />
    </header>

    <section class="chat-content">
      <button type="button" class="chat-search">
        <span class="chat-search-main">
          <img :src="searchAsset" alt="" class="chat-search-icon" />
          <span class="chat-search-placeholder">Search</span>
        </span>

        <span class="chat-search-action" aria-hidden="true">
          <img :src="caretAsset" alt="" class="chat-search-caret" />
        </span>
      </button>

      <div class="chat-stories" role="list" aria-label="聊天动态">
        <div v-for="story in stories" :key="story.id" class="chat-story" role="listitem">
          <div
            class="chat-story-avatar"
            :class="{
              'chat-story-avatar-highlight': story.highlighted,
              'chat-story-avatar-self': story.isSelf,
            }"
          >
            <img :src="story.image" :alt="story.label" />
            <span v-if="story.isSelf" class="chat-story-add" aria-hidden="true">+</span>
          </div>

          <p class="chat-story-label">{{ story.label }}</p>
        </div>
      </div>

      <div class="chat-divider"></div>

      <div class="chat-list">
        <button
          v-for="conversation in conversations"
          :key="conversation.id"
          type="button"
          class="chat-row"
          @click="openConversation(conversation)"
        >
          <div class="chat-row-main">
            <div class="chat-avatar" :class="{ 'chat-avatar-group': conversation.isGroup }">
              <img :src="conversation.image" :alt="conversation.title" />
            </div>

            <div class="chat-copy">
              <h2 class="chat-title">{{ conversation.title }}</h2>
              <p class="chat-preview">{{ conversation.preview }}</p>
            </div>
          </div>

          <div class="chat-meta">
            <span class="chat-time">{{ conversation.time }}</span>
            <span v-if="conversation.unread" class="chat-badge">{{ conversation.unread }}</span>
          </div>
        </button>
      </div>
    </section>

    <nav class="chat-nav" aria-label="底部导航">
      <div class="chat-nav-bg"></div>

      <button
        type="button"
        class="chat-nav-btn chat-nav-btn-muted chat-nav-btn-user"
        aria-label="个人"
        @click="emit('navigate', 'profile')"
      >
        <img :src="userAsset" alt="" class="chat-nav-user-icon" />
      </button>

      <button
        type="button"
        class="chat-nav-btn chat-nav-btn-muted chat-nav-btn-search"
        aria-label="发现"
        @click="emit('navigate', 'discover')"
      >
        <img src="/MagnifyingGlass.svg" alt="" class="chat-nav-search-icon" />
      </button>

      <button
        type="button"
        class="chat-nav-btn chat-nav-btn-muted chat-nav-btn-ai"
        aria-label="AI"
        @click="emit('navigate', 'ai1')"
      >
        <img :src="aiAsset" alt="" class="chat-nav-ai-icon" />
      </button>

      <button
        type="button"
        class="chat-nav-btn chat-nav-btn-muted chat-nav-btn-trip"
        aria-label="行程"
        @click="emit('navigate', 'itinerary')"
      >
        <img :src="tripAsset" alt="" class="chat-nav-trip-icon" />
      </button>

      <button
        type="button"
        class="chat-nav-btn chat-nav-btn-active chat-nav-btn-chat"
        aria-label="聊天"
        aria-current="page"
      >
        <img :src="chatAsset" alt="" class="chat-nav-chat-icon" />
      </button>
    </nav>

    <footer class="chat-home-indicator-wrap">
      <div class="chat-home-indicator"></div>
    </footer>
  </div>
</template>

<style scoped>
.chat-page {
  position: relative;
  height: 100%;
  overflow: hidden;
  background: linear-gradient(180deg, #f9f9f9 0%, #f8f5f4 56%, #f6f0ee 100%);
  font-family: 'SF Pro Rounded', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.chat-page-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(42% 22% at 10% 84%, rgba(243, 194, 210, 0.84) 0%, rgba(243, 194, 210, 0) 70%),
    radial-gradient(36% 18% at 92% 96%, rgba(255, 236, 177, 0.82) 0%, rgba(255, 236, 177, 0) 72%),
    radial-gradient(44% 25% at 50% 86%, rgba(255, 255, 255, 0.86) 0%, rgba(255, 255, 255, 0) 76%);
}

.chat-status-bar {
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

.chat-status-time {
  width: 138px;
  color: #000;
  text-align: center;
  font-size: 17px;
  line-height: 22px;
  font-weight: 600;
  letter-spacing: -0.51px;
}

.chat-status-island {
  width: 104px;
  height: 28px;
  border-radius: 999px;
  background: #2a2a2a;
}

.chat-status-levels {
  width: 143px;
  height: 54px;
  object-fit: contain;
}

.chat-content {
  position: absolute;
  top: 58px;
  left: 16px;
  right: 16px;
  bottom: 84px;
  z-index: 3;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.chat-search,
.chat-row,
.chat-nav-btn {
  padding: 0;
  border: 0;
  cursor: pointer;
}

.chat-search {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 48px;
  padding: 4px 4px 4px 16px;
  border: 1px solid #f3f3f3;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.94);
}

.chat-search-main {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-search-icon {
  width: 14px;
  height: 14px;
}

.chat-search-placeholder {
  color: #b0b0b0;
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
}

.chat-search-action {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border: 1.275px solid #f3f3f3;
  border-radius: 999px;
  background: #f9f9f9;
  flex-shrink: 0;
}

.chat-search-caret {
  width: 18px;
  height: 18px;
}

.chat-stories {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-right: 20px;
  padding-bottom: 2px;
  scrollbar-width: none;
}

.chat-stories::-webkit-scrollbar,
.chat-list::-webkit-scrollbar {
  display: none;
}

.chat-story {
  flex: 0 0 auto;
  width: 56px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.chat-story-avatar {
  position: relative;
  width: 56px;
  height: 56px;
  padding: 2px;
  border-radius: 50%;
  border: 2px solid #eee;
  background: #f7f7f7;
}

.chat-story-avatar img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.chat-story-avatar-highlight {
  border-color: transparent;
  background: linear-gradient(135deg, #57d4ff 0%, #7d60ff 100%);
}

.chat-story-avatar-self {
  padding: 0;
  border: 0;
  overflow: hidden;
  background: #000;
}

.chat-story-avatar-self img {
  opacity: 0.5;
}

.chat-story-add {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  color: #fff;
  font-size: 28px;
  line-height: 1;
  font-weight: 300;
}

.chat-story-label {
  margin: 0;
  color: #000;
  font-size: 12px;
  line-height: 18px;
  white-space: nowrap;
}

.chat-divider {
  height: 1px;
  background: rgba(224, 224, 224, 0.92);
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-right: 4px;
  padding-bottom: 110px;
}

.chat-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  background: transparent;
  text-align: left;
}

.chat-row-main {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-avatar {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  overflow: hidden;
  background: #f7f7f7;
}

.chat-avatar img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.chat-avatar-group {
  display: grid;
  place-items: center;
  background: transparent;
}

.chat-avatar-group img {
  width: 46px;
  height: 46px;
  border: 1px solid #f3f3f3;
  border-radius: 50%;
}

.chat-copy {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chat-title,
.chat-preview {
  margin: 0;
}

.chat-title {
  color: #2c2828;
  font-size: 16px;
  line-height: 22px;
  font-weight: 600;
}

.chat-preview {
  overflow: hidden;
  color: #999;
  font-size: 12px;
  line-height: 18px;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.chat-meta {
  flex-shrink: 0;
  min-height: 42px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8px;
}

.chat-time {
  color: #999;
  font-size: 12px;
  line-height: 18px;
}

.chat-badge {
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  background: #461c3a;
  color: #fff;
  text-align: center;
  font-size: 12px;
  line-height: 16px;
}

.chat-nav {
  position: absolute;
  inset: 0;
  z-index: 4;
  pointer-events: none;
}

.chat-nav-bg {
  position: absolute;
  top: 765px;
  left: 33px;
  width: 327px;
  height: 54px;
  border: 1px solid #fff;
  border-radius: 32px;
  background: rgba(255, 255, 255, 0.66);
  backdrop-filter: blur(20px);
  pointer-events: none;
}

.chat-nav-btn {
  position: absolute;
  top: 768px;
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  pointer-events: auto;
}

.chat-nav-btn-muted {
  background: rgba(0, 0, 0, 0.02);
}

.chat-nav-btn-active {
  background: #000;
}

.chat-nav-btn-user {
  left: 41px;
}

.chat-nav-btn-search {
  left: 113px;
}

.chat-nav-btn-ai {
  left: 177px;
}

.chat-nav-btn-trip {
  left: 240px;
}

.chat-nav-btn-chat {
  left: 305px;
}

.chat-nav-user-icon {
  width: 14.4px;
  height: 14.4px;
  filter: brightness(0);
}

.chat-nav-search-icon,
.chat-nav-chat-icon {
  width: 13px;
  height: 13px;
}

.chat-nav-ai-icon,
.chat-nav-trip-icon {
  width: 18px;
  height: 18px;
}


.chat-home-indicator-wrap {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 4;
  display: flex;
  justify-content: center;
  padding: 8px 124px;
}

.chat-home-indicator {
  width: 144px;
  height: 5px;
  border-radius: 100px;
  background: #2a2a2a;
}
</style>