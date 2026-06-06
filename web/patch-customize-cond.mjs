import { readFileSync, writeFileSync } from 'fs'

const file = 'f:\\文档\\GitHub\\MEITUAN-Hackathon-main\\web\\src\\App.vue'
let c = readFileSync(file, 'utf8')

// 修复 customize 页面的 v-if 条件
c = c.replace(
  `        <!-- Customize Plan Page (方案选择) -->
        <section v-if="currentPage === 'customize'" class="customize-page">`,
  `        <!-- Customize Plan Page (方案选择) -->
        <section v-if="activeTab === 'plan' && currentPage === 'customize'" class="customize-page">`
)

writeFileSync(file, c, 'utf8')
console.log('✓ Fixed customize page condition')
