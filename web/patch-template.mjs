import { readFileSync, writeFileSync } from 'fs'

const file = 'f:\\文档\\GitHub\\MEITUAN-Hackathon-main\\web\\src\\App.vue'
let c = readFileSync(file, 'utf8')

// 找到 "<!-- Placeholder sections for other tabs -->" 之前的位置，插入新的 customize 页面
const insertBefore = `        <!-- Placeholder sections for other tabs -->`
const customizePage = `
        <!-- Customize Plan Page (方案选择) -->
        <section v-if="currentPage === 'customize'" class="customize-page">
          <div class="customize-overlay" />
          <div class="customize-container">
            <button class="back-btn" aria-label="返回" @click="backToInput">
              <span>✕</span>
            </button>
            <h1 class="customize-title">有空了，现在想怎么放松？</h1>
            <p class="customize-subtitle">不知道去哪没关系，告诉我你的时间和心情，我来帮你安排</p>
            <div class="plan-types">
              <button
                v-for="type in planTypes"
                :key="type"
                class="plan-type-btn"
                :class="{ 'plan-type-active': selectedPlanType === type }"
                @click="selectPlanType(type)"
              >
                <span class="type-icon">🎯</span>
                <span class="type-name">{{ type }}</span>
              </button>
            </div>
            <button class="confirm-btn" @click="currentPage = 'input'">
              确认选择
            </button>
          </div>
        </section>

`

if (c.includes(insertBefore)) {
  c = c.replace(insertBefore, customizePage + insertBefore)
  console.log('✓ Added customize page template')
} else {
  console.log('✗ Placeholder marker not found')
}

writeFileSync(file, c, 'utf8')
