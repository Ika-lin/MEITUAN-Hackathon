# 🚀 智能周末闲时规划助手

**MEITUAN Hackathon 项目** - 帮助用户在碎片化空闲时间内快速发现和执行本地活动方案的全栈解决方案。

## 📱 项目概述

这是一个跨平台的智能周末规划系统，包含 **iOS 原生应用**和 **Web 管理后台**两个部分。

**核心特性**：
- 🎯 AI 智能推荐周末活动方案
- 📍 基于地理位置的本地活动发现
- 🗓️ 详细的行程规划与实时调整
- 💾 用户收藏与历史记录管理
- 🌙 深色模式完整支持
- ♿ 无障碍访问（VoiceOver）支持
- 🌐 Web 管理后台，支持内容和用户管理
- ⚡ 现代化技术栈（SwiftUI + Vue 3）

## 📚 项目结构

```
MEITUAN-Hackathon-main/
├── README.md                      # 项目总览文档
├── DESIGN.md                      # 设计规范与视觉标准
├── backend-api.md                 # 后端接口规范
├── CAROUSEL-VERIFICATION.md       # 轮播验证规范
├── click_function.md              # 功能清单模板
│
└── web/                           # Web 前端应用
    ├── README.md                  # Web 部分快速开始
    ├── package.json               # 项目依赖配置
    ├── vite.config.ts             # Vite 构建配置
    ├── tsconfig.json              # TypeScript 配置
    ├── src/
    │   ├── App.vue               # 主应用组件
    │   ├── main.ts               # 入口文件
    │   ├── style.css             # 全局样式
    │   ├── components/           # 组件库
    │   │   ├── HelloWorld.vue
    │   │   └── PreferenceSelector.vue
    │   └── assets/               # 静态资源
    ├── public/
    │   └── cards/                # 卡片资源
    └── patch-*.mjs               # 构建脚本集合
```

## 📖 文档结构

| 文件 | 说明 |
|-----|------|
| [DESIGN.md](DESIGN.md) | 应用整体设计规范（iPhone 16 标准） |
| [backend-api.md](backend-api.md) | 后端接口规范与数据契约 |
| [CAROUSEL-VERIFICATION.md](CAROUSEL-VERIFICATION.md) | 轮播验证规范 |
| [click_function.md](click_function.md) | 功能清单模板 |
| [web/README.md](web/README.md) | Web 前端快速开始指南 |

## 🚀 快速开始

### iOS 应用部分

#### 前置要求
- **Xcode 15.0+**
- **macOS 12.0+**
- **iOS 15.0+ 部署目标**

#### 步骤

1. **打开 Xcode 项目**
   ```bash
   open MeituanWeekend.xcodeproj
   ```

2. **选择目标设备**（iPhone 16/17 Pro 模拟器）

3. **构建并运行**
   - 按 **Cmd + R** 或点击 Run 按钮

4. **查看效果**
   - 在发现页面浏览活动卡片
   - 点击卡片查看详情
   - 使用筛选标签过滤活动
   - 通过底部导航栏切换规划、行程、我的页面

### Web 前端部分

#### 前置要求
- **Node.js 18.0+**
- **npm 9.0+ 或 pnpm 8.0+**

#### 快速开始
```bash
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

更详细的说明请查看 [web/README.md](web/README.md)

## 📖 主要文件说明

### MeituanWeekendApp.swift
应用的入口点，定义了主窗口和场景配置。

### ContentView.swift
主视图，包含底部标签栏和页面容器。使用 `selectedTab` 状态管理当前显示的页面。

### DiscoveryView.swift
发现页面，展示活动卡片的瀑布流列表、筛选标签、天气建议等。

### ActivityCard.swift
活动卡片数据结构，包含模拟数据生成方法。

### Extensions.swift
SwiftUI 和 Foundation 的扩展，提供便利的视图修饰符和工具方法。

## 🎨 设计系统

所有颜色、字体、间距都遵循 DESIGN.md 中定义的规范。

**主色：** `#8a7400` (brandPrimary)  
**背景：** `#f5f5f7` (bgBase)  
**字体：** PingFang SC（中文）/ SF Pro Display（英文）

## 🔧 开发工作流

### 创建新页面

1. 在 `Features/` 目录下创建新文件夹
2. 创建 `Views/YourView.swift`
3. 创建 `ViewModels/YourViewModel.swift`
4. 在 `ContentView.swift` 中添加对应的 Tab 导航

### 添加新组件

1. 在 `Components/` 目录下创建组件文件
2. 遵循 DESIGN.md 中的设计规范
3. 提供 PreviewProvider 用于快速预览

### 调试技巧

```swift
// 在 Xcode 控制台打印调试信息
print("DEBUG: \(value)")

// 使用 Preview 快速预览
#Preview {
    YourView()
}

// 检查是否在深色模式
@Environment(\.colorScheme) var colorScheme
```

## 📝 功能清单

参考 [click_function.md](click_function.md) 记录所有功能按钮及其实现状态。

| 序号 | 按钮 | 页面 | 功能 | 状态 |
|-----|-----|------|------|------|
| 1 | 返回 | 全局 | 返回上级页面 | ✅ |
| 2 | 收藏 | 行程详情 | 收藏行程 | 📝 |
| 3 | 分享 | 行程详情 | 分享行程链接 | 📝 |
| ... | ... | ... | ... | ... |

## 🌐 API 集成

应用将使用以下 API 端点（需配置）：

```
GET /api/v1/activities       # 获取活动列表
POST /api/v1/itinerary      # 生成行程
PUT /api/v1/favorites       # 收藏/取消收藏
```

详见 [iOS开发启动指南.md](iOS开发启动指南.md) 的 APIService 部分。

## 📦 依赖与第三方库

目前项目仅使用 SwiftUI 和 Foundation，无额外依赖。

**可选依赖**（开发中）：
- `Alamofire` - 网络请求（替代 URLSession）
- `SwiftyJSON` - JSON 解析
- `Kingfisher` - 图片加载缓存
- `Combine` - 异步编程

## 🧪 测试

创建单元测试：

```bash
# 在 Xcode 中
Product > Scheme > Edit Scheme
Test 标签页 > + 按钮 > 选择测试 Target
```

## 🚢 构建与发布

### 为模拟器构建

```bash
xcodebuild -scheme MeituanWeekend -configuration Release -sdk iphonesimulator
```

### 为真机构建

```bash
xcodebuild -scheme MeituanWeekend -configuration Release -sdk iphoneos
```

### 归档与上传 App Store

参考 Apple 官方文档：[Distributing Your App for Beta Testing and Releases](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)

## 📖 参考资源

- [Apple SwiftUI 官方文档](https://developer.apple.com/documentation/swiftui/)
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/ios/)
- [Xcode 使用指南](https://help.apple.com/xcode/)

## 🤝 贡献

1. 创建功能分支：`git checkout -b feature/your-feature`
2. 提交改动：`git commit -m 'Add your feature'`
3. 推送分支：`git push origin feature/your-feature`
4. 创建 Pull Request

## 📝 许可证

本项目为 MEITUAN Hackathon 项目。

## 📧 联系方式

如有问题，请联系开发团队。