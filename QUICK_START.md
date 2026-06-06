# ⚡ 快速开始指南

## 📋 前置要求

- Node.js 16+
- npm 或 yarn
- 现代浏览器 (Chrome 90+, Safari 15+, Firefox 88+)

---

## 🚀 启动项目

### 1️⃣ 安装依赖

```bash
cd web
npm install
```

### 2️⃣ 启动开发服务器

```bash
npm run dev
```

**输出:**
```
VITE v5.x.x  ready in 365 ms

➜  Local:   http://localhost:5173/
```

### 3️⃣ 打开浏览器

访问 `http://localhost:5173/`

---

## 🎮 基本操作

### 选择设备

```
1. 点击左侧控制面板
2. 选择设备按钮 (iPhone 14/15/16/16 Pro)
3. 设备外壳自动更新
```

**支持的设备:**
- iPhone 14: 390×844px
- iPhone 15: 393×852px
- iPhone 16: 393×852px (默认)
- iPhone 16 Pro: 402×874px

### 调整亮度

```
1. 找到"屏幕亮度"滑块
2. 拖动从 30% → 100%
3. 设备屏幕亮度实时变化
```

### 调整缩放

```
1. 找到"缩放"滑块
2. 拖动从 50% → 150% (10% 步长)
3. 设备整体放大/缩小
```

### 旋转设备

```
1. 点击"🔄 旋转"按钮
2. 设备从竖屏 ↔ 横屏
3. 0.3 秒过渡动画
```

### 重置所有参数

```
1. 点击"↺ 重置"按钮
2. 一键恢复默认:
   - 设备: iPhone 16
   - 亮度: 100%
   - 缩放: 100%
   - 方向: 竖屏
```

### 截图 (可扩展)

```
1. 点击"📸 截图"按钮
2. 当前提示信息框
3. 后续可集成 html2canvas 实现下载
```

---

## 🖥️ 屏幕内容

### 当前可用页面

| 页面 | 路由 | 功能 |
|------|------|------|
| Home 1 | `/` | 主页列表 |
| Home 2 | `/home2` | 分类浏览 |
| AI 1 | `/ai1` | AI 推荐 |
| AI 5 | `/ai5` | AI 详情 |
| Itinerary | `/itinerary` | 行程路线(含地图) |

### 切换页面

使用屏幕底部导航栏切换页面，模拟器会实时显示内容。

---

## 📊 控制面板详解

```
┌─────────────────────────┐
│   设备控制面板          │
├─────────────────────────┤
│ 设备选择                │
│ [14] [15] [16] [Pro]    │  ← 点击选择
├─────────────────────────┤
│ 屏幕亮度: 100%          │
│ [▓▓▓▓▓▓▓▓▓░] ← 拖动    │
├─────────────────────────┤
│ 缩放: 100%              │
│ [▓▓▓▓▓▓▓░░░] ← 拖动    │
├─────────────────────────┤
│ [🔄 旋转] [↺ 重置]      │
│ [📸 截图]              │
├─────────────────────────┤
│ 设备信息:               │
│ • 当前设备: iPhone 16   │
│ • 分辨率: 393 × 852     │
│ • 状态: 竖屏模式        │
└─────────────────────────┘
```

---

## 🎯 常见操作场景

### 场景 1: 检查响应式设计

```bash
# 步骤
1. 选择 iPhone 14 (较小设备)
2. 旋转到横屏
3. 缩放到 150% 查看放大效果
4. 检查是否有布局错位
5. 返回竖屏，选择 iPhone 16 Pro 重复
```

### 场景 2: 低光环境测试

```bash
# 步骤
1. 降低亮度到 30-40%
2. 保持设备正常大小
3. 验证文字对比度是否足够
4. 检查颜色是否清晰可见
```

### 场景 3: 设备兼容性验证

```bash
# 步骤
1. 依次选择所有 4 种设备
2. 对每个设备进行竖/横屏测试
3. 记录任何布局或功能异常
4. 返回开发环境修复问题
```

### 场景 4: 无障碍检查

```bash
# 步骤
1. 缩放到 120-150% (模拟视力不佳)
2. 验证所有按钮大小 ≥ 44×44px
3. 检查是否能用键盘导航
4. 验证颜色对比度是否足够
```

---

## 🛠️ 开发工作流

### 修改代码 → 查看结果

```bash
# 1. 编辑 web/src/App.vue 或其他组件
# 2. 保存文件

# 3. Vite 自动检测变化并 Hot Reload
# 浏览器页面自动刷新，状态保留

# 4. 查看模拟器中的变化结果
```

### 构建生产版本

```bash
npm run build
```

**输出:**
```
web/dist/
├── index.html
├── assets/
│   ├── index-xxx.js
│   └── index-xxx.css
```

### 预览生产构建

```bash
npm run preview
# 访问: http://localhost:4173/
```

---

## 🔍 调试技巧

### Chrome DevTools

```javascript
// 打开 DevTools: F12 或 右键 → 检查

// 1. Elements 标签查看 DOM 结构
// 2. Console 标签执行 JavaScript
// 3. Network 标签查看网络请求
// 4. Performance 标签分析性能
```

### Vue DevTools

```
1. 安装 Vue DevTools 浏览器扩展
2. 打开 DevTools → Vue 标签
3. 监控 deviceType, screenBrightness 等状态
4. 实时查看组件树结构
```

### 快速测试命令

```bash
# 查看所有可用脚本
npm run

# 输出:
# build      √ vite build
# dev        √ vite
# preview    √ vite preview
# build:tsc  √ vue-tsc --noEmit
```

---

## ⚙️ 配置文件

### 关键配置位置

| 文件 | 用途 |
|------|------|
| `web/vite.config.ts` | Vite 构建配置 |
| `web/tsconfig.json` | TypeScript 配置 |
| `web/package.json` | 依赖管理 |
| `web/src/style.css` | 全局样式 |

### 修改设备配置

编辑 `web/src/App.vue`，找到 `deviceSpecs` 对象:

```typescript
const deviceSpecs = {
  iphone14: { name: 'iPhone 14', width: 390, height: 844 },
  iphone15: { name: 'iPhone 15', width: 393, height: 852 },
  // 添加新设备:
  iphone13: { name: 'iPhone 13', width: 390, height: 844 },
}
```

---

## 📁 项目结构

```
web/
├── src/
│   ├── components/
│   │   ├── ItineraryMap.vue      ← 地图组件
│   │   ├── PreferenceSelector.vue
│   │   └── HelloWorld.vue
│   ├── App.vue                   ← 主组件 (模拟器逻辑)
│   ├── style.css                 ← 全局样式
│   ├── main.ts                   ← 入口
│   └── ...
├── public/                        ← 静态资源
├── dist/                          ← 构建输出 (git ignore)
├── node_modules/                  ← 依赖 (git ignore)
├── vite.config.ts
├── tsconfig.json
├── package.json
└── package-lock.json

文档:
├── PHONE_SIMULATOR_GUIDE.md       ← 完整功能指南
├── PHONE_SIMULATOR_QUICK_GUIDE.md ← 快速参考
├── PHONE_SIMULATOR_TECHNICAL.md   ← 技术实现
├── SYSTEM_ARCHITECTURE.md         ← 系统架构
└── IMPLEMENTATION_SUMMARY.md      ← 项目总结
```

---

## 🐛 故障排除

### 问题 1: 页面加载空白

**症状:** 访问 localhost:5173 显示空白页

**解决:**
```bash
# 清理 node_modules 和缓存
rm -rf node_modules package-lock.json
npm install

# 重启开发服务器
npm run dev
```

### 问题 2: 模拟器控制面板不显示

**症状:** 左侧控制面板消失或隐藏

**解决:**
1. 检查浏览器宽度 (需 > 460px)
2. 刷新页面 (Ctrl+R / Cmd+R)
3. 清除浏览器缓存

### 问题 3: 设备旋转不工作

**症状:** 点击旋转按钮无反应

**解决:**
```bash
# 检查 TypeScript 编译
npm run build:tsc

# 检查浏览器控制台是否有错误
# F12 → Console 查看错误信息
```

### 问题 4: 样式显示不正确

**症状:** 按钮错位、颜色不对等

**解决:**
```bash
# 清理浏览器缓存
# Ctrl+Shift+Delete (Windows)
# Cmd+Shift+Delete (Mac)

# 或强制刷新
# Ctrl+F5 (Windows)
# Cmd+Shift+R (Mac)
```

---

## 📚 更多资源

### 文档
- ✅ `PHONE_SIMULATOR_GUIDE.md` - 详细功能说明
- ✅ `PHONE_SIMULATOR_QUICK_GUIDE.md` - 快速参考卡
- ✅ `PHONE_SIMULATOR_TECHNICAL.md` - 技术深潜
- ✅ `SYSTEM_ARCHITECTURE.md` - 架构设计

### 官方文档
- [Vue 3](https://vuejs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vitejs.dev/)
- [CSS Transform](https://developer.mozilla.org/en-US/docs/Web/CSS/transform)

### 社区支持
- GitHub Issues: 报告 bug
- Slack: 技术讨论
- Wiki: 最佳实践

---

## 💡 提示和技巧

### 快速键盘快捷键

| 操作 | 快捷键 |
|------|--------|
| 打开 DevTools | F12 |
| 强制刷新 | Ctrl+Shift+R |
| 清理缓存 | Ctrl+Shift+Delete |
| 放大页面 | Ctrl++ |
| 缩小页面 | Ctrl+- |

### 浏览器扩展推荐

- Vue DevTools
- React DevTools (如有 React 组件)
- JSONView
- ColorPicker

### 性能优化建议

```bash
# 1. 使用 Production Build
npm run build

# 2. 在 DevTools Network 模拟低速网络
# → Throttling: "Fast 3G"

# 3. 监控 Performance
# DevTools → Performance → Record

# 4. 检查内存泄漏
# DevTools → Memory → Heap Snapshots
```

---

## 🎓 学习路径

### 初级 (1-2 天)
- [ ] 了解基本操作
- [ ] 尝试改变设备和参数
- [ ] 查看不同页面

### 中级 (3-5 天)
- [ ] 阅读 PHONE_SIMULATOR_GUIDE.md
- [ ] 学习代码结构
- [ ] 修改简单配置

### 高级 (1-2 周)
- [ ] 学习 Vue 3 和 TypeScript
- [ ] 阅读 SYSTEM_ARCHITECTURE.md
- [ ] 扩展新功能

---

## ✅ 检查清单

启动前确认:

- [ ] Node.js 已安装 (`node --version`)
- [ ] npm 已安装 (`npm --version`)
- [ ] 进入 web 目录 (`cd web`)
- [ ] 依赖已安装 (`npm install`)
- [ ] 开发服务器启动 (`npm run dev`)
- [ ] 浏览器可访问 (`http://localhost:5173/`)

---

## 📞 获取帮助

### 遇到问题?

1. 检查常见问题部分
2. 查看浏览器控制台错误
3. 重启开发服务器
4. 清理缓存和重新安装依赖
5. 查看相关文档
6. 提交 GitHub Issue

### 联系方式

- 📧 Email: team@meituan.hackathon
- 💬 Slack: #phone-simulator
- 🐙 GitHub: [项目地址]

---

**版本:** 1.0  
**最后更新:** 2026-06-06  
**状态:** ✅ 生产就绪
