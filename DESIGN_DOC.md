# Weekendgo 设计文档

## 1. Planning 策略

### 1.1 多 Agent 协商架构

```
群聊规划请求
    │
    ▼
┌─────────────────────────────────┐
│  协调 Agent (Coordinator)        │
│  System: "你是群聊协调器..."      │
└─────────────────────────────────┘
    │ 并行调用
    ├──→ analyze_user_profile(u1)  ← 从美团消费记录动态生成
    ├──→ analyze_user_profile(u2)  ← 非硬编码，纯数据驱动
    ├──→ analyze_user_profile(u3)
    │
    ▼
  汇总约束 → 冲突检测 → 搜索POI → 查团购 → 读评论 → 查排队
    │
    ▼
  generate_trip_plan → 统一方案
    │
    ▼
  用户确认 → execute_actions (一键预订+下单+配送)
```

**关键设计决策**：
- **Agent 间不互相直接对话**，而是由协调 Agent 并行获取各成员画像后统一协商
- **所有画像从数据库动态生成**（`analyze_user_profile` 读取消费记录），零硬编码
- **冲突解决**：预算差异 → 高低搭配；口味冲突 → 找平衡餐厅；社交/独处 → 混合安排

### 1.2 Agent Loop（Hermes 模式）

```
prefetch memories → system prompt + tools → LLM
    ↓
  tool_calls? ──Yes──→ execute tools → append results → loop (max 6)
    │                                                    │
    No                                              iter=4: 强制提示"请生成最终方案"
    │
    ▼
  text reply → sync memories → return
```

**异常处理**：
- LLM API 不可用 → 关键词规则引擎 fallback（`_fallback_chat`）
- Tool 执行失败 → 返回 error JSON，LLM 自行调整
- 循环超过上限 → 返回已收集信息的部分方案
- 数据库无数据 → 提示放宽筛选条件

---

## 2. 工具调用链路

### 2.1 14 个工具清单

| 类别 | 工具 | 数据来源 | Mock 策略 |
|------|------|----------|-----------|
| **用户理解** | `analyze_user_profile` | 美团消费记录(23条) | 动态统计 |
| | `get_consumption_history` | 到店+外卖+团购 | 按时间排序 |
| **搜索发现** | `search_pois` | 美团商户库(96家) | 真实上海坐标 |
| | `get_poi_detail` | 大众点评详情 | POI 字段 |
| | `search_deals` | 美团团购(10个) | 折扣+已售数 |
| | `get_events` | 周末活动(20个) | 日期范围 |
| | `read_reviews` | 大众点评评价 | 基于POI标签生成 |
| **规划执行** | `get_weather` | 天气 | 随机4种天气 |
| | `generate_trip_plan` | AI编排 | 时间+预算计算 |
| | `check_availability` | 餐厅实时状态 | 评分/时段/人数 |
| | `save_trip` | 确认保存 | DB写入 |
| | `execute_actions` | 一键执行 | Mock确认码 |
| **社交** | `find_social_matches` | 共同消费+标签 | 交集计算 |

### 2.2 典型调用链：家庭出游

```
用户: "下午带老婆孩子出去玩"
  → analyze_user_profile(小明)  // 画像: 轻松休闲, ¥200
  → analyze_user_profile(老婆)  // 画像: 减肥中, 亲子
  → analyze_user_profile(小宝)  // 画像: 5岁, 不能吃辣
  → get_weather()               // 晴天 28°C
  → search_pois(category=户外+亲子)  // 世纪公园...
  → search_deals(category=轻食)     // GREEN&SAFE 团购
  → read_reviews(poi_050)            // 好评: 有机/新鲜
  → check_availability(poi_050, 18:00, 3)  // 需提前取号
  → generate_trip_plan([poi_170, poi_050]) // 世纪公园→GREEN&SAFE
  → [用户确认]
  → execute_actions([
      reserve_restaurant(poi_050, 18:00, 3),
      order_delivery("鲜花", "GREEN&SAFE")
    ])
  → 发消息给老婆: "搞定了，下午2点出发，世纪公园→晚餐GREEN&SAFE"
```

### 2.3 数据模型

```
POI (96商户)  ←─  TripStop (行程节点)
  │                    │
  ├── Deal (团购券)     Trip (行程)
  ├── ConsumptionRecord   │
  │     (消费记录)        User (用户)
  │         │               │
  │         └── UserProfile (AI动态生成)
  │
  └── Event (活动)
```

---

## 3. 关键技术决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| LLM | DeepSeek v4-pro | 1M上下文, 支持tool call, ¥3/6 per M |
| 框架 | Flask + SQLite | 零配置部署，Demo 够用 |
| Tool格式 | OpenAI compatible | DeepSeek 兼容，可切换模型 |
| 画像生成 | 动态分析消费记录 | 零硬编码，可扩展 |
| 多Agent | 协调器+并行画像 | 避免 Agent 间通信复杂度 |
| Fallback | 关键词规则引擎 | LLM不可用时仍可服务 |
| 前端 | Vue3 + Vite | 已有设计稿，iPhone 外壳 |
