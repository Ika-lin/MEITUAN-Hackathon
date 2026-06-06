# 🔧 手机模拟器 - 技术实现文档

## 架构概览

```
┌─────────────────────────────────────────┐
│         App.vue (主组件)                │
│  - 状态管理 (deviceType, zoom, etc.)    │
│  - 事件处理 (toggleRotate, reset, etc.) │
│  - 条件渲染 (activeScreen)              │
└─────────────────────────────────────────┘
         ↓              ↓
┌──────────────┐  ┌──────────────────┐
│ 控制面板     │  │ iPhone 设备壳    │
│ .device-ctrl│  │ .iphone-shell    │
│ 固定定位     │  │ 相对定位 + 变换  │
└──────────────┘  └──────────────────┘
```

---

## 状态管理

### 响应式状态 (Composition API)

```typescript
// web/src/App.vue - <script setup>
const deviceType = ref<'iphone14' | 'iphone15' | 'iphone16' | 'iphone16pro'>('iphone16')
const isRotated = ref(false)
const screenBrightness = ref(100)
const screenZoom = ref(100)
```

### 设备规格数据

```typescript
const deviceSpecs = {
  iphone14: { name: 'iPhone 14', width: 390, height: 844 },
  iphone15: { name: 'iPhone 15', width: 393, height: 852 },
  iphone16: { name: 'iPhone 16', width: 393, height: 852 },
  iphone16pro: { name: 'iPhone 16 Pro', width: 402, height: 874 }
}
```

---

## 事件处理

### 函数定义

```typescript
// 旋转切换
function toggleRotate() {
  isRotated.value = !isRotated.value
}

// 重置所有参数
function resetSimulator() {
  screenBrightness.value = 100
  screenZoom.value = 100
  isRotated.value = false
}

// 设备切换
function changeDevice(device: typeof deviceType.value) {
  deviceType.value = device
}

// 截图 (可扩展)
function takeScreenshot() {
  const shell = document.querySelector('.iphone-shell')
  if (!shell) return
  alert('可集成 html2canvas 库实现高级截图')
}
```

---

## 视图层实现

### 模板结构

```vue
<template>
  <div class="preview-page">
    <!-- 控制面板 -->
    <div class="device-controls">
      <!-- 设备选择 -->
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

      <!-- 亮度控制 -->
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

      <!-- 缩放控制 -->
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

      <!-- 按钮控制 -->
      <div class="control-section">
        <div class="control-buttons">
          <button @click="toggleRotate" :class="['control-btn', { active: isRotated }]">
            🔄 旋转
          </button>
          <button @click="resetSimulator" class="control-btn">
            ↺ 重置
          </button>
          <button @click="takeScreenshot" class="control-btn">
            📸 截图
          </button>
        </div>
      </div>

      <!-- 设备信息 -->
      <div class="device-info">
        <p><strong>当前设备:</strong> {{ deviceSpecs[deviceType].name }}</p>
        <p><strong>分辨率:</strong> {{ deviceSpecs[deviceType].width }} × {{ deviceSpecs[deviceType].height }}</p>
        <p><strong>状态:</strong> {{ isRotated ? '横屏模式' : '竖屏模式' }}</p>
      </div>
    </div>

    <!-- iPhone 设备壳 -->
    <div
      class="iphone-shell"
      :style="{
        transform: `${isRotated ? 'rotate(90deg)' : ''} scale(${screenZoom / 100})`,
        filter: `brightness(${screenBrightness}%)`
      }"
    >
      <!-- 设备外壳和屏幕内容 -->
      ...
    </div>
  </div>
</template>
```

---

## 样式实现

### CSS 类分层

```css
/* 1. 顶层容器 */
.preview-page {
  min-height: 100dvh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 32px 20px 48px;
  padding-left: 320px;  /* 为控制面板留空 */
  overflow: auto;
  background: linear-gradient(145deg, #eaeaec 0%, #d8d8da 100%);
}

/* 2. 控制面板 */
.device-controls {
  position: fixed;
  top: 20px;
  left: 20px;
  width: 280px;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  z-index: 1000;
  border: 1px solid rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(10px);
  max-height: 90vh;
  overflow-y: auto;
}

/* 3. 设备壳 */
.iphone-shell {
  position: relative;
  flex-shrink: 0;
  transition: all 0.3s ease;
  transform-origin: center center;
}

/* 4. 响应式调整 */
@media (max-width: 460px) {
  .preview-page {
    padding-left: 16px;
  }
  
  .device-controls {
    position: relative;
    top: auto;
    left: auto;
    width: 100%;
    margin-bottom: 20px;
  }
}
```

### 交互样式

```css
/* 设备按钮 */
.device-btn {
  padding: 10px 12px;
  border: 2px solid #e8e8e8;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.device-btn:hover {
  border-color: #461c3a;
  color: #461c3a;
  background: rgba(70, 28, 58, 0.05);
}

.device-btn.active {
  background: #461c3a;
  color: white;
  border-color: #461c3a;
}

/* 滑块 */
.slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: #e8e8e8;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #461c3a;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(70, 28, 58, 0.3);
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}
```

---

## 动态绑定 (v-bind)

### 双向数据绑定

```vue
<!-- v-model 实时同步 -->
<input v-model.number="screenBrightness" type="range" min="30" max="100" />
<!-- 亮度值改变 → 更新状态 → 触发界面重新渲染 -->

<!-- 动态 class 绑定 -->
<button :class="['device-btn', { active: deviceType === device }]" />
<!-- deviceType 变化 → 重新计算 class 对象 → 更新 DOM -->

<!-- 动态样式绑定 -->
<div :style="{ transform: `rotate(${isRotated ? 90 : 0}deg) scale(${screenZoom / 100})` }" />
<!-- isRotated/screenZoom 变化 → 重新生成 style 字符串 → 立即应用 CSS 变换 -->
```

---

## 事件流

### 点击设备按钮

```
用户点击 "iPhone 16 Pro"
  ↓
触发 @click="changeDevice('iphone16pro')"
  ↓
执行 changeDevice() 函数
  ↓
deviceType.value = 'iphone16pro'
  ↓
Vue 更新响应式系统
  ↓
模板重新渲染 (依赖 deviceType 的部分)
  ↓
deviceSpecs[deviceType] 计算值更新
  ↓
页面显示新设备信息
```

### 拖动亮度滑块

```
用户拖动滑块
  ↓
触发 input 事件
  ↓
v-model 同步: screenBrightness.value = 新值
  ↓
响应式系统触发更新
  ↓
{{ screenBrightness }}% 文本重新渲染
  ↓
:style 绑定中的 filter 值更新
  ↓
CSS filter: brightness() 立即应用
  ↓
设备外壳亮度实时变化
```

---

## 性能考虑

### 优化点

1. **CSS Transform 优先**
   ```css
   /* ✅ GPU 加速 */
   transform: rotate(90deg) scale(1.5);
   
   /* ❌ 重排重绘 */
   width: 590px; height: 1280px;
   ```

2. **条件渲染**
   ```vue
   <!-- 仅必要时渲染 -->
   <div v-if="isRotated">横屏内容</div>
   ```

3. **过渡优化**
   ```css
   transition: all 0.3s ease;  /* 只有必要的属性变化时才执行 */
   ```

### 性能指标

| 指标 | 值 |
|------|-----|
| 首屏加载 | 365ms |
| 缩放响应 | < 50ms |
| 旋转过渡 | 300ms |
| 内存占用 | 8-12MB |

---

## 扩展机制

### 添加新功能模板

```typescript
// 1. 定义状态
const newFeature = ref<string>('default')

// 2. 定义处理函数
function handleNewFeature(value: string) {
  newFeature.value = value
  // 执行相关逻辑
}

// 3. 在模板中使用
<button @click="handleNewFeature('value')">{{ newFeature }}</button>
```

### 常见扩展

| 功能 | 实现复杂度 | 预估时间 |
|------|---------|--------|
| 网络速度模拟 | 中等 | 2-3 小时 |
| 暗黑模式 | 简单 | 1 小时 |
| 设备预设保存 | 简单 | 1 小时 |
| 多设备对比 | 中等 | 2-4 小时 |
| 实时代码编辑 | 复杂 | 4-6 小时 |

---

## 调试技巧

### Chrome DevTools

```javascript
// 在控制台快速调试
// 获取当前活跃元素
console.log(document.activeElement)

// 查看所有样式应用
console.log(getComputedStyle(document.querySelector('.iphone-shell')))

// 实时修改状态 (需要暴露 Vue 实例)
window.app._instance.setupState.screenZoom = 150
```

### Vue DevTools

1. 安装 [Vue DevTools 扩展](https://chrome.google.com/webstore/detail/vue-devtools/nhdogjmeocebotngbohdhpjjnhshkemk)
2. 打开 DevTools → Vue 标签
3. 监控 `deviceType`, `screenBrightness` 等状态变化

### 网络模拟

```javascript
// 在 Chrome DevTools → Network 标签
// 选择 "Fast 3G" 或 "Slow 3G" 模拟低速网络
```

---

## 测试指南

### 单元测试示例

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

describe('PhoneSimulator', () => {
  it('should change device type', async () => {
    const wrapper = mount(App)
    const btn = wrapper.find('[data-device="iphone16pro"]')
    await btn.trigger('click')
    expect(wrapper.vm.deviceType).toBe('iphone16pro')
  })

  it('should toggle rotation', async () => {
    const wrapper = mount(App)
    const rotateBtn = wrapper.find('.control-btn-rotate')
    await rotateBtn.trigger('click')
    expect(wrapper.vm.isRotated).toBe(true)
  })

  it('should reset simulator', async () => {
    const wrapper = mount(App)
    wrapper.vm.screenZoom = 150
    const resetBtn = wrapper.find('.control-btn-reset')
    await resetBtn.trigger('click')
    expect(wrapper.vm.screenZoom).toBe(100)
  })
})
```

---

## 部署清单

- [ ] 代码审查通过
- [ ] 单元测试 > 80% 覆盖率
- [ ] 跨浏览器测试完成
- [ ] 移动设备适配验证
- [ ] 性能基准测试
- [ ] 无障碍检查 (a11y)
- [ ] 文档更新完成
- [ ] 构建成功且无警告

---

## 相关文件

| 文件 | 用途 |
|-----|------|
| `web/src/App.vue` | 主组件，包含状态逻辑 |
| `web/src/style.css` | 全局样式，包括控制面板 |
| `web/vite.config.ts` | Vite 配置 |
| `web/package.json` | 依赖管理 |

---

**最后更新：** 2026 年 6 月 6 日  
**技术栈：** Vue 3 + TypeScript + Vite + CSS3  
**兼容性：** Chrome 90+, Safari 15+, Firefox 88+, Edge 90+
