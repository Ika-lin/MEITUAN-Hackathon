import { readFileSync, writeFileSync } from 'fs'

const file = 'f:\\文档\\GitHub\\MEITUAN-Hackathon-main\\web\\src\\App.vue'
let c = readFileSync(file, 'utf8')

// 修改 plan 页面的 v-if 条件
c = c.replace(
  `        <!-- Plan Page (规划) -->
        <section v-if="activeTab === 'plan'" class="content">`,
  `        <!-- Plan Page (规划) -->
        <section v-if="activeTab === 'plan' && currentPage === 'input'" class="content">`
)

writeFileSync(file, c, 'utf8')
console.log('✓ Updated plan page condition')
