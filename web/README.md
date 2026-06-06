# 🌐 Web 前端应用 - 智能周末闲时规划助手

这是智能周末闲时规划助手的 Web 前端部分，基于 **Vue 3** 和 **TypeScript** 构建，使用 **Vite** 作为现代化的构建工具。

## 🛠️ 技术栈

- **框架**: Vue 3 with Composition API + `<script setup>` SFC
- **语言**: TypeScript
- **构建**: Vite 8.x
- **包管理**: npm / pnpm
- **开发工具**: vue-tsc（TypeScript 类型检查）

## 📋 项目结构

```
web/
├── src/
│   ├── App.vue                    # 根组件
│   ├── main.ts                    # 应用入口
│   ├── style.css                  # 全局样式
│   ├── components/                # Vue 组件
│   │   ├── HelloWorld.vue         # 示例组件
│   │   └── PreferenceSelector.vue # 偏好选择器组件
│   └── assets/                    # 静态资源
├── public/
│   └── cards/                     # 卡片资源文件
├── index.html                     # HTML 入口文件
├── package.json                   # 项目元数据和依赖
├── vite.config.ts                 # Vite 配置文件
├── tsconfig.json                  # TypeScript 配置
├── tsconfig.app.json              # 应用专用 TS 配置
├── tsconfig.node.json             # Node 环境 TS 配置
└── patch-*.mjs                    # 构建辅助脚本
    ├── patch-conditions.mjs       # 条件补丁脚本
    ├── patch-customize-cond.mjs   # 自定义条件补丁
    ├── patch-pages.mjs            # 页面补丁脚本
    ├── patch-styles.mjs           # 样式补丁脚本
    └── patch-template.mjs         # 模板补丁脚本
```

## 🚀 快速开始

### 前置要求
- **Node.js 18.0+** 或更高版本
- **npm 9.0+** 或 **pnpm 8.0+**（推荐使用 pnpm）

### 安装与运行

1. **安装依赖**
   ```bash
   npm install
   # 或使用 pnpm
   pnpm install
   ```

2. **启动开发服务器**
   ```bash
   npm run dev
   ```
   访问 `http://localhost:5173` 查看应用（实际端口可能因配置而异）

3. **TypeScript 类型检查**
   ```bash
   npm run build  # 包含 vue-tsc 类型检查
   ```

4. **构建生产版本**
   ```bash
   npm run build
   ```
   输出文件位于 `dist/` 目录

5. **预览生产构建**
   ```bash
   npm run preview
   ```

## 📚 核心文件说明

### `src/App.vue`
主应用组件，定义了应用的顶层结构和样式。

### `src/components/PreferenceSelector.vue`
偏好选择器组件，用于用户选择活动偏好和筛选条件。

### `vite.config.ts`
Vite 构建配置，定义了构建参数、别名和优化设置。

### `patch-*.mjs` 脚本集
一系列 Node.js 构建辅助脚本，用于自动化条件、样式、页面和模板的处理。

## 🎨 开发工作流

### 创建新组件

1. 在 `src/components/` 目录下创建新的 `.vue` 文件
2. 使用 Vue 3 `<script setup>` 语法
3. 编写样式和模板
4. 在 `App.vue` 中导入使用

示例：
```vue
<template>
  <div class="my-component">
    <h1>{{ title }}</h1>
    <button @click="handleClick">Click me</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const title = ref('My Component')

const handleClick = () => {
  console.log('Clicked!')
}
</script>

<style scoped>
.my-component {
  padding: 1rem;
}
</style>
```

## 📖 推荐资源

- [Vue 3 官方文档](https://vuejs.org/)
- [Vue 3 TypeScript 指南](https://vuejs.org/guide/typescript/overview.html)
- [Vite 官方文档](https://vitejs.dev/)
- [TypeScript 手册](https://www.typescriptlang.org/docs/)

## 🔗 相关文档

- [项目总览](../README.md)
- [设计规范](../DESIGN.md)
- [后端 API 规范](../backend-api.md)
- [功能清单](../click_function.md)
