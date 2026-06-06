<script setup lang="ts">
import type { PlaceDetail } from '../data/placeDetails'

defineProps<{
  detail: PlaceDetail
}>()

const emit = defineEmits<{
  back: []
}>()

const levelsAsset = '/Levels.svg'

const paginationDots = Array.from({ length: 9 }, (_, index) => index)

const activeDotIndex = 1

function getAvatarLabel(name: string) {
  return name.slice(0, 1)
}

function getDisplayStars(rating: number) {
  return Array.from({ length: 5 }, (_, index) => index < rating)
}
</script>

<template>
  <div class="place-detail-page">
    <header class="place-detail-status-bar">
      <div class="place-detail-time">9:41</div>
      <div class="place-detail-island"></div>
      <img :src="levelsAsset" alt="" class="place-detail-levels" />
    </header>

    <div class="place-detail-top-actions">
      <button type="button" class="place-detail-top-btn" aria-label="返回" @click="emit('back')">
        <img src="/icon-park-outline_left.svg" alt="" />
      </button>
      <button type="button" class="place-detail-top-btn" aria-label="分享">
        <img src="/ShareNetwork.svg" alt="" />
      </button>
    </div>

    <div class="place-detail-scroll">
      <section class="place-detail-hero" :style="{ background: detail.heroBackground }">
        <div class="place-detail-hero-grain"></div>

        <div class="place-detail-hero-nav place-detail-hero-nav-left">
          <img src="/chevron-left.svg" alt="" />
        </div>
        <div class="place-detail-hero-nav place-detail-hero-nav-right">
          <img src="/chevron-left.svg" alt="" />
        </div>

        <div class="place-detail-hero-copy">
          <h1 class="place-detail-hero-wordmark">{{ detail.heroWordmark }}</h1>
          <p class="place-detail-hero-caption">{{ detail.heroCaption }}</p>
          <p class="place-detail-hero-marquee">{{ detail.heroMarquee }}</p>
        </div>

        <div class="place-detail-dots" aria-hidden="true">
          <span
            v-for="dot in paginationDots"
            :key="dot"
            class="place-detail-dot"
            :class="{ 'place-detail-dot-active': dot === activeDotIndex }"
          ></span>
        </div>
      </section>

      <section class="place-detail-content">
        <div class="place-detail-info-card">
          <div class="place-detail-heading-row">
            <div class="place-detail-heading-copy">
              <h2 class="place-detail-title">{{ detail.title }}</h2>
              <p class="place-detail-address">
                <img src="/map-pin.svg" alt="" />
                <span>{{ detail.address }}</span>
              </p>
            </div>

            <img src="/Group 121.svg" alt="" class="place-detail-heading-actions" />
          </div>

          <div class="place-detail-meta-row">
            <div class="place-detail-meta-pill">
              <img src="/clock.svg" alt="" />
              <span>{{ detail.hours }}</span>
            </div>
            <div class="place-detail-meta-pill">
              <img src="/user.svg" alt="" />
              <span>{{ detail.status }}</span>
            </div>
          </div>

          <p class="place-detail-description">{{ detail.description }}</p>

          <div class="place-detail-rating-row">
            <p class="place-detail-price">{{ detail.price }}</p>
            <div class="place-detail-rating">
              <img src="/Star.svg" alt="" />
              <span>{{ detail.rating }} ({{ detail.ratingCount }})</span>
            </div>
          </div>

          <div class="place-detail-cta-row">
            <button type="button" class="place-detail-cta place-detail-cta-dark">加入收藏</button>
            <button type="button" class="place-detail-cta place-detail-cta-gold">美团团购</button>
            <button type="button" class="place-detail-map-btn" aria-label="查看地图">
              <img src="/lucide_map.svg" alt="" />
            </button>
          </div>
        </div>

        <section class="place-detail-section">
          <h3 class="place-detail-section-title">评价</h3>

          <div class="place-detail-review-list">
            <article v-for="review in detail.reviews" :key="review.id" class="place-detail-review-card">
              <div class="place-detail-review-header">
                <div class="place-detail-reviewer">
                  <div class="place-detail-avatar" :style="{ background: review.avatarBg }">{{ getAvatarLabel(review.name) }}</div>

                  <div class="place-detail-reviewer-copy">
                    <p class="place-detail-reviewer-name">{{ review.name }}</p>
                    <p class="place-detail-reviewer-time">{{ review.time }}</p>
                  </div>
                </div>

                <div class="place-detail-stars">
                  <img
                    v-for="(filled, index) in getDisplayStars(review.rating)"
                    :key="`${review.id}-${index}`"
                    src="/Star.svg"
                    alt=""
                    :class="{ 'place-detail-star-dim': !filled }"
                  />
                </div>
              </div>

              <p class="place-detail-review-text">{{ review.text }}</p>

              <div class="place-detail-review-actions">
                <div class="place-detail-review-action">
                  <img src="/Like Icon.svg" alt="" />
                  <span>{{ review.likes }}</span>
                </div>

                <div class="place-detail-review-action">
                  <img src="/Dislike Icon.svg" alt="" />
                  <span>{{ review.dislikes }}</span>
                </div>
              </div>
            </article>
          </div>

          <button type="button" class="place-detail-load-more">
            <span class="place-detail-load-more-plus">+</span>
            <span>Load More</span>
          </button>
        </section>

        <section class="place-detail-section place-detail-reminder-section">
          <h3 class="place-detail-section-title place-detail-reminder-title">到店前提醒</h3>

          <div class="place-detail-reminder-grid">
            <div class="place-detail-reminder-column">
              <p v-for="item in detail.reminders" :key="item" class="place-detail-reminder-item">{{ item }}</p>
            </div>

            <div class="place-detail-reminder-note">{{ detail.reminderNote }}</div>
          </div>
        </section>

        <footer class="place-detail-home-indicator">
          <div class="place-detail-home-indicator-bar"></div>
        </footer>
      </section>
    </div>
  </div>
</template>

<style scoped>
.place-detail-page {
  position: relative;
  height: 100%;
  overflow: hidden;
  background: #ffffff;
}

.place-detail-scroll {
  height: 100%;
  overflow-y: auto;
  padding-bottom: 18px;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.place-detail-scroll::-webkit-scrollbar {
  display: none;
}

.place-detail-status-bar {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 12;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 54px;
}

.place-detail-time {
  width: 138px;
  text-align: center;
  font-size: 17px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: -0.51px;
  color: #111;
}

.place-detail-island {
  width: 104px;
  height: 28px;
  border-radius: 999px;
  background: #2c2828;
}

.place-detail-levels {
  width: 143px;
  height: 54px;
  object-fit: contain;
}

.place-detail-top-actions {
  position: absolute;
  left: 16px;
  right: 16px;
  top: 58px;
  z-index: 12;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.place-detail-top-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #f3f3f3;
  border-radius: 999px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(23, 23, 23, 0.04);
}

.place-detail-top-btn img {
  width: 16px;
  height: 16px;
}

.place-detail-hero {
  position: relative;
  height: 398px;
  overflow: hidden;
}

.place-detail-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0) 45%, rgba(255, 255, 255, 0.18) 100%);
}

.place-detail-hero-grain {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 24%, rgba(255, 255, 255, 0.25) 0 1px, transparent 1px 100%),
    radial-gradient(circle at 72% 42%, rgba(255, 255, 255, 0.14) 0 1px, transparent 1px 100%),
    radial-gradient(circle at 48% 64%, rgba(0, 0, 0, 0.06) 0 1px, transparent 1px 100%);
  opacity: 0.55;
}

.place-detail-hero-copy {
  position: absolute;
  left: 15px;
  right: 15px;
  top: 76px;
  z-index: 2;
  color: #2b2522;
}

.place-detail-hero-wordmark {
  margin: 0;
  font-size: clamp(36px, 12vw, 56px);
  line-height: 0.9;
  font-weight: 400;
  letter-spacing: -2.2px;
}

.place-detail-hero-caption {
  margin: 6px 0 0;
  font-size: 18px;
  line-height: 1.1;
  letter-spacing: 0.02em;
}

.place-detail-hero-marquee {
  display: inline-flex;
  margin: 12px 0 0;
  padding: 8px 12px;
  border-radius: 16px;
  background: rgba(42, 32, 24, 0.82);
  color: #f4d89f;
  font-size: 28px;
  line-height: 1;
  letter-spacing: 0.18em;
}

.place-detail-hero-nav {
  position: absolute;
  top: 146px;
  z-index: 2;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 0.5px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(2px);
}

.place-detail-hero-nav-left {
  left: 16px;
}

.place-detail-hero-nav-right {
  right: 16px;
  transform: scaleX(-1);
}

.place-detail-hero-nav img {
  width: 16px;
  height: 16px;
}

.place-detail-dots {
  position: absolute;
  left: 50%;
  bottom: 8px;
  z-index: 2;
  display: flex;
  gap: 4px;
  transform: translateX(-50%);
}

.place-detail-dot {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: #b2b2b2;
  backdrop-filter: blur(2px);
}

.place-detail-dot-active {
  width: 8px;
  height: 8px;
  background: #ffffff;
}

.place-detail-content {
  padding: 16px 16px 0;
}

.place-detail-info-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.place-detail-heading-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.place-detail-heading-copy {
  flex: 1;
  min-width: 0;
}

.place-detail-title {
  margin: 0;
  font-size: 16px;
  line-height: 22px;
  font-weight: 500;
  color: #000;
}

.place-detail-address {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 8px 0 0;
  color: #999999;
  font-size: 12px;
  line-height: 18px;
}

.place-detail-address img {
  width: 12px;
  height: 12px;
}

.place-detail-heading-actions {
  width: 98px;
  height: 28px;
  flex-shrink: 0;
}

.place-detail-meta-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.place-detail-meta-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  border: 1px solid #f7f7f7;
  border-radius: 999px;
  background: #f7f7f7;
  color: #b0b0b0;
  font-size: 12px;
  line-height: 18px;
}

.place-detail-meta-pill img {
  width: 12px;
  height: 12px;
}

.place-detail-description {
  margin: 0;
  color: #1e1e1e;
  font-size: 14px;
  line-height: 1.7;
}

.place-detail-rating-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.place-detail-price {
  margin: 0;
  color: #000;
  font-size: 11.5px;
  line-height: 1.3;
}

.place-detail-rating {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #999999;
  font-size: 12px;
  line-height: 18px;
}

.place-detail-rating img {
  width: 14px;
  height: 14px;
}

.place-detail-cta-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.place-detail-cta {
  height: 40px;
  padding: 0 18px;
  border: 0;
  border-radius: 166px;
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
}

.place-detail-cta-dark {
  width: 153px;
  background: #0b0b0b;
  color: #fff;
}

.place-detail-cta-gold {
  width: 153px;
  background: #ffc300;
  color: #000;
}

.place-detail-map-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #f0f0f0;
  border-radius: 999px;
  background: #fff;
}

.place-detail-map-btn img {
  width: 18px;
  height: 18px;
}

.place-detail-section {
  margin-top: 24px;
}

.place-detail-section-title {
  margin: 0 0 8px;
  color: rgba(44, 40, 40, 0.7);
  font-size: 18px;
  line-height: 1.2;
  font-weight: 500;
}

.place-detail-review-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.place-detail-review-card {
  padding: 8px;
  border: 1px solid #eeeeee;
  border-radius: 24px;
  background: #ffffff;
}

.place-detail-review-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.place-detail-reviewer {
  display: flex;
  align-items: center;
  gap: 8px;
}

.place-detail-avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #f3f3f3;
  border-radius: 999px;
  color: #2c2828;
  font-size: 16px;
  line-height: 22px;
  font-weight: 500;
}

.place-detail-reviewer-copy {
  min-width: 0;
}

.place-detail-reviewer-name,
.place-detail-reviewer-time,
.place-detail-review-text,
.place-detail-review-action span,
.place-detail-reminder-item,
.place-detail-reminder-note,
.place-detail-load-more {
  margin: 0;
}

.place-detail-reviewer-name {
  color: #2c2828;
  font-size: 16px;
  line-height: 22px;
  font-weight: 500;
}

.place-detail-reviewer-time {
  color: #999999;
  font-size: 12px;
  line-height: 18px;
}

.place-detail-stars {
  display: inline-flex;
  gap: 2px;
}

.place-detail-stars img {
  width: 14px;
  height: 14px;
}

.place-detail-star-dim {
  opacity: 0.32;
}

.place-detail-review-text {
  margin-top: 12px;
  color: #1e1e1e;
  font-size: 14px;
  line-height: 1.7;
}

.place-detail-review-actions {
  display: inline-flex;
  gap: 16px;
  margin-top: 12px;
  padding: 8px 16px;
  border-radius: 999px;
  background: #fafafa;
}

.place-detail-review-action {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #1e1e1e;
  font-size: 12px;
  line-height: 18px;
}

.place-detail-review-action img {
  width: 16px;
  height: 16px;
}

.place-detail-load-more {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: 16px;
  padding: 10px 12px;
  border: 0;
  border-radius: 166px;
  background: #fafafa;
  color: #1e1e1e;
  font-size: 14px;
  line-height: 1.7;
}

.place-detail-load-more-plus {
  font-size: 16px;
  line-height: 1;
}

.place-detail-reminder-section {
  position: relative;
  padding-bottom: 18px;
}

.place-detail-reminder-title {
  color: #6c6868;
}

.place-detail-reminder-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  position: relative;
}

.place-detail-reminder-grid::before,
.place-detail-reminder-grid::after {
  content: '';
  position: absolute;
  top: 4px;
  bottom: 4px;
  width: 1px;
  background: linear-gradient(180deg, rgba(111, 92, 161, 0.4) 0%, rgba(111, 92, 161, 0.15) 100%);
}

.place-detail-reminder-grid::before {
  left: 8px;
}

.place-detail-reminder-grid::after {
  left: calc(50% - 12px);
}

.place-detail-reminder-column {
  padding-left: 20px;
}

.place-detail-reminder-item {
  position: relative;
  color: #565656;
  font-size: 13px;
  line-height: 1.6;
}

.place-detail-reminder-item + .place-detail-reminder-item {
  margin-top: 12px;
}

.place-detail-reminder-item::before {
  content: '';
  position: absolute;
  left: -12px;
  top: 8px;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #7a5fa4;
}

.place-detail-reminder-note {
  padding-top: 12px;
  color: #565656;
  font-size: 12px;
  line-height: 1.55;
}

.place-detail-home-indicator {
  display: flex;
  justify-content: center;
  padding: 20px 0 8px;
}

.place-detail-home-indicator-bar {
  width: 144px;
  height: 5px;
  border-radius: 100px;
  background: #2c2828;
}
</style>