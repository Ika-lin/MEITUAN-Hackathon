import { readFileSync, writeFileSync } from 'fs'

const file = 'f:\\文档\\GitHub\\MEITUAN-Hackathon-main\\web\\src\\App.vue'
let c = readFileSync(file, 'utf8')

// ---- 1. 在 Data 部分添加新的 refs 和常量
// 找到 const activeTab 那行，在前面插入新数据
const dataInsert = `
// Page state: 'input' = 输入筛选, 'plans' = 方案选择, 'customize' = 定制方案选择
const currentPage = ref<'input' | 'plans' | 'customize'>('input')

const planTypes = ['景点打卡', '美食探店', '文化体验', '户外活动'] as const
const selectedPlanType = ref<(typeof planTypes)[number]>('景点打卡')
`

c = c.replace(
  /const activeTab = ref<'discover' \| 'plan' \| 'trip' \| 'me'>\('plan'\)/,
  dataInsert + "\nconst activeTab = ref<'discover' | 'plan' | 'trip' | 'me'>('plan')"
)

// ---- 2. 修改 generatePlan 函数，让它进入方案选择页面而不是显示 toast
const oldGeneratePlan = `function generatePlan() {
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
}`

const newGeneratePlan = `function generatePlan() {
  if (!canGenerate.value || isGenerating.value) {
    return
  }
  isGenerating.value = true
  aiStatusText.value = '正在结合你的位置和偏好生成中...'
  window.setTimeout(() => {
    isGenerating.value = false
    aiStatusText.value = '已为你生成多条可执行方案'
    currentPage.value = 'customize'
  }, 1100)
}

function backToInput() {
  currentPage.value = 'input'
  isGenerating.value = false
}

function selectPlanType(type: (typeof planTypes)[number]) {
  selectedPlanType.value = type
  toastText.value = '已选择 ' + type
  window.setTimeout(() => {
    toastText.value = ''
  }, 1000)
}`

c = c.replace(oldGeneratePlan, newGeneratePlan)

writeFileSync(file, c, 'utf8')
console.log('✓ Added page state and plan types')
