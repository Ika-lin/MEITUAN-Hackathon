---
title: 智能周末闲时规划后端接口规范
description: 面向后端开发的接口清单与数据契约，覆盖规划生成、行程执行、发现推荐和用户资产能力
author: Backend Team
ms.date: 2026-06-03
ms.topic: reference
keywords:
  - weekendgo
  - api
  - planning
  - itinerary
  - recommendation
estimated_reading_time: 12
---

## 1. 文档目标

本规范用于指导后端实现智能周末闲时规划能力，目标是先打通前端主流程，再按优先级扩展能力。

当前前端主流程如下：

1. 用户在规划页输入文本并选择筛选条件
2. 系统生成多个候选方案
3. 用户确认某个方案并创建行程
4. 用户在行程页逐步打卡，更新节点状态

## 2. 版本与环境

* API 版本：v1
* Base URL：/api/v1
* 传输协议：HTTPS
* 数据格式：application/json; charset=utf-8
* 时间格式：ISO 8601，示例 2026-06-03T20:16:00+08:00

## 3. 鉴权与通用约定

### 3.1 鉴权

* 登录用户：Authorization: Bearer <token>
* 匿名用户：请求体传 deviceId
* 兼容策略：userId 与 deviceId 至少有一个

### 3.2 幂等

写接口支持幂等键：

* Header：Idempotency-Key
* 场景：创建行程、打卡、收藏
* 规则：同键同请求体在 24 小时内返回同结果

### 3.3 统一响应结构

```json
{
  "code": 0,
  "message": "ok",
  "data": {},
  "requestId": "c7f0f5df8c30430bb00cc4a6a40f66d4",
  "timestamp": "2026-06-03T20:16:00+08:00"
}
```

### 3.4 业务错误码

| code | 含义 | 建议处理 |
| --- | --- | --- |
| 0 | 成功 | 正常处理 |
| 1001 | 参数校验失败 | 前端提示并保留输入 |
| 1002 | 鉴权失败 | 触发登录或匿名降级 |
| 1003 | 资源不存在 | 返回空态页 |
| 2001 | 方案生成失败 | 提示重试并建议调整条件 |
| 2002 | 方案已失效 | 触发重生成 |
| 3001 | 行程状态冲突 | 拉取最新行程后重试 |
| 3002 | 行程节点不可更新 | 提示节点已关闭 |
| 5000 | 系统内部错误 | 记录日志并提示稍后再试 |

## 4. 数据模型

### 4.1 规划生成请求 PlanGenerateRequest

```json
{
  "userId": "u_123",
  "deviceId": "d_123",
  "prompt": "想在静安区喝咖啡再逛逛",
  "timeType": "短时闲逛",
  "activities": ["喝咖啡", "城市散步"],
  "geographicRange": "地铁30分钟",
  "budget": "100-200元",
  "city": "上海",
  "currentTime": "2026-06-03T20:16:00+08:00"
}
```

### 4.2 方案卡片 PlanCard

```json
{
  "planId": "p_1001",
  "type": "美食探店",
  "title": "安福路咖啡和小食慢逛",
  "duration": "3 小时",
  "budgetText": "人均约 168 元",
  "tag": "热门",
  "color": "#ff8a65",
  "score": 92,
  "spots": [
    {
      "spotId": "s_1",
      "name": "武康路口咖啡店",
      "category": "咖啡",
      "address": "静安区安福路 100 号",
      "etaMinutes": 12
    }
  ]
}
```

### 4.3 行程详情 TripDetail

```json
{
  "tripId": "t_9001",
  "title": "安福路咖啡和小食慢逛",
  "city": "上海",
  "date": "2026-06-04",
  "totalBudget": "约 168 元",
  "status": "planned",
  "stops": [
    {
      "stopId": "ts_1",
      "index": 1,
      "time": "14:30",
      "name": "武康路口咖啡店",
      "desc": "出发点附近，步行可达",
      "done": false,
      "checkinTime": null
    }
  ]
}
```

### 4.4 行程总览 TripOverview

```json
{
  "tripId": "t_9001",
  "distanceKm": 1.8,
  "budgetRange": "230-350",
  "transportMode": "全程步行",
  "walkDurationMinutes": 25,
  "start": {
    "name": "上海徐汇区武康路 376 号附近",
    "lat": 31.2123,
    "lng": 121.4392
  },
  "end": {
    "name": "上海徐汇区上海图书馆地铁站",
    "lat": 31.2048,
    "lng": 121.4366
  }
}
```

### 4.5 行程节点候选 AlternativeStop

```json
{
  "stopId": "ts_1",
  "alternatives": [
    {
      "candidateId": "alt_1001",
      "name": "多抓鱼循环商店",
      "categoryTags": ["二手书", "阅读"],
      "priceRange": "60-70",
      "walkMinutes": 5,
      "reason": "离武康路更近，更适合轻松阅读"
    }
  ]
}
```

### 4.6 出发提醒 ReminderBundle

```json
{
  "tripId": "t_9001",
  "today": [
    "暴晒 25C",
    "RAC BAR 可能等位",
    "已预留缓冲 15 分钟"
  ],
  "packingChecklist": [
    "遮阳伞",
    "一台便携胶片相机",
    "充电宝"
  ]
}
```

### 4.7 地点详情 PoiDetail

```json
{
  "poiId": "poi_322",
  "name": "FILM电影时光书店",
  "heroImage": "https://cdn.example.com/poi/film-cover.jpg",
  "tags": ["电影主题", "安静翻阅", "胶片气质"],
  "rating": 5.0,
  "pricePerCapita": 43,
  "businessStatus": "open",
  "openHoursText": "周一至周日 09:00-19:00",
  "phone": "021-xxxx-xxxx",
  "address": "上海市徐汇区安福路 322 号",
  "about": "独立书店，提供咖啡和电影主题文创周边",
  "impressionTags": ["投影", "有咖啡厅", "环境很好", "网红店", "热门门店"],
  "userQuote": "店内主题感强，适合拍照和短暂停留",
  "suitableFor": ["一个人阅读", "短暂停留", "喜欢电影主题空间"],
  "attention": ["周末下午可能人多", "建议避开高峰时段"]
}
```

### 4.8 到店提示 ArrivalHint

```json
{
  "tripId": "t_9001",
  "stopId": "ts_1",
  "poiId": "poi_322",
  "queueRisk": "medium",
  "bestArrivalWindow": "14:00-15:00",
  "trafficNote": "周边停车紧张，建议步行或地铁",
  "weatherImpact": "晴天较晒，建议带遮阳伞"
}
```

## 5. 接口清单

### 5.1 P0 核心接口

#### 5.1.1 生成方案

* Method: POST
* Path: /api/v1/plan/generate
* 说明：根据输入条件返回候选方案列表

请求体：PlanGenerateRequest

响应 data：

```json
{
  "plans": [
    {
      "planId": "p_1001",
      "type": "美食探店",
      "title": "安福路咖啡和小食慢逛",
      "duration": "3 小时",
      "budgetText": "人均约 168 元",
      "tag": "热门",
      "color": "#ff8a65",
      "score": 92,
      "spots": []
    }
  ],
  "generatedAt": "2026-06-03T20:16:00+08:00"
}
```

#### 5.1.2 创建行程

* Method: POST
* Path: /api/v1/trip/create
* 说明：用户确认方案后创建行程

请求体：

```json
{
  "userId": "u_123",
  "deviceId": "d_123",
  "planId": "p_1001",
  "date": "2026-06-04"
}
```

响应 data：

```json
{
  "tripId": "t_9001",
  "trip": {
    "tripId": "t_9001",
    "title": "安福路咖啡和小食慢逛",
    "city": "上海",
    "date": "2026-06-04",
    "totalBudget": "约 168 元",
    "status": "planned",
    "stops": []
  }
}
```

#### 5.1.3 获取行程详情

* Method: GET
* Path: /api/v1/trip/{tripId}
* 说明：加载行程页数据

路径参数：tripId

响应 data：TripDetail

#### 5.1.4 更新行程节点状态

* Method: PATCH
* Path: /api/v1/trip/{tripId}/stops/{stopId}
* 说明：打卡或取消打卡

请求体：

```json
{
  "done": true,
  "actualTime": "2026-06-04T14:36:00+08:00"
}
```

响应 data：

```json
{
  "tripId": "t_9001",
  "stop": {
    "stopId": "ts_1",
    "done": true,
    "checkinTime": "2026-06-04T14:36:00+08:00"
  },
  "progress": {
    "total": 4,
    "done": 1
  }
}
```

#### 5.1.5 获取发现页分类

* Method: GET
* Path: /api/v1/discover/categories

响应 data：

```json
{
  "categories": ["全部", "美食", "艺术", "户外", "市集"]
}
```

#### 5.1.6 获取发现页内容

* Method: GET
* Path: /api/v1/discover/places
* Query：category、limit、cursor

响应 data：

```json
{
  "items": [
    {
      "itemId": "dp_1",
      "name": "武康路慢生活街区",
      "category": "艺术",
      "badge": "最热",
      "subtitle": "静安区，步行友好",
      "layout": "tall",
      "gradient": "#3a1f5d,#1f3c88"
    }
  ],
  "nextCursor": "c_2"
}
```

#### 5.1.7 获取活动列表

* Method: GET
* Path: /api/v1/discover/events
* Query：city、limit

响应 data：

```json
{
  "events": [
    {
      "eventId": "ev_1",
      "emoji": "🎨",
      "title": "周末手作市集",
      "subtitle": "静安，至 6 月 20 日",
      "badge": "火热进行中"
    }
  ]
}
```

#### 5.1.8 获取我的页信息

* Method: GET
* Path: /api/v1/user/profile

响应 data：

```json
{
  "userId": "u_123",
  "nickname": "周末散步家",
  "avatar": "https://example.com/a.png",
  "location": "上海",
  "stats": {
    "footprints": 12,
    "favorites": 8,
    "completedTrips": 5
  }
}
```

#### 5.1.9 获取行程总览

* Method: GET
* Path: /api/v1/trip/{tripId}/overview
* 说明：用于行程概览区块，返回总路程、预算、交通方式和步行时间

路径参数：tripId

响应 data：TripOverview

#### 5.1.10 获取行程路线图数据

* Method: GET
* Path: /api/v1/trip/{tripId}/route-map
* 说明：用于顶部路线图卡片，返回折线点位与节点标签

响应 data：

```json
{
  "tripId": "t_9001",
  "polyline": "xxxxxx",
  "markers": [
    {
      "stopId": "ts_1",
      "order": 1,
      "name": "武康路",
      "lat": 31.2123,
      "lng": 121.4392
    }
  ],
  "bounds": {
    "north": 31.215,
    "south": 31.203,
    "east": 121.445,
    "west": 121.431
  }
}
```

#### 5.1.11 获取单节点候选替换列表

* Method: GET
* Path: /api/v1/trip/{tripId}/stops/{stopId}/alternatives
* Query：limit、sortBy
* 说明：用于行程详情中的换一个功能

响应 data：AlternativeStop

#### 5.1.12 替换行程节点

* Method: POST
* Path: /api/v1/trip/{tripId}/stops/{stopId}/replace
* 说明：用候选点替换当前节点，并自动重算后续时间与预算

请求体：

```json
{
  "candidateId": "alt_1001",
  "reason": "用户点击换一个"
}
```

响应 data：

```json
{
  "tripId": "t_9001",
  "replacedStopId": "ts_1",
  "newStopId": "ts_1_new",
  "updatedStops": [],
  "updatedOverview": {
    "distanceKm": 2.0,
    "budgetRange": "240-360",
    "walkDurationMinutes": 30
  }
}
```

#### 5.1.13 获取出发提醒

* Method: GET
* Path: /api/v1/trip/{tripId}/reminders
* Query：date、city
* 说明：用于行程页出发前提醒区块

响应 data：ReminderBundle

#### 5.1.14 收藏行程

* Method: POST
* Path: /api/v1/trip/{tripId}/favorite
* 说明：对应行程页右上角收藏操作

请求体：

```json
{
  "favorite": true
}
```

#### 5.1.15 生成行程分享链接

* Method: POST
* Path: /api/v1/trip/{tripId}/share
* 说明：对应行程页右上角分享操作

响应 data：

```json
{
  "shareUrl": "https://weekendgo.example.com/share/t_9001",
  "shareCode": "A9XK2Q",
  "expiresAt": "2026-06-10T20:16:00+08:00"
}
```

#### 5.1.16 获取地点详情

* Method: GET
* Path: /api/v1/pois/{poiId}
* Query：tripId、stopId
* 说明：用于行程详情点击查看详情后的地点详情页

响应 data：PoiDetail

#### 5.1.17 获取地点评论洞察

* Method: GET
* Path: /api/v1/pois/{poiId}/review-insights
* Query：city、windowDays
* 说明：用于评价印象与用户常提到模块

响应 data：

```json
{
  "poiId": "poi_322",
  "rating": 5.0,
  "reviewCount": 326,
  "impressionTags": ["投影", "有咖啡厅", "环境很好", "网红店"],
  "highlights": [
    "适合短暂休息",
    "拍照友好"
  ],
  "riskNotes": [
    "周末 15:00-17:00 可能排队"
  ],
  "sampleQuote": "主题感强，安静好坐"
}
```

#### 5.1.18 获取地点到店提醒

* Method: GET
* Path: /api/v1/pois/{poiId}/arrival-hints
* Query：tripId、stopId、arrivalTime
* 说明：用于地点详情页的到店前提醒

响应 data：ArrivalHint

#### 5.1.19 获取地点联系方式

* Method: GET
* Path: /api/v1/pois/{poiId}/contact
* 说明：用于电话按钮和号码展示，支持脱敏号码

响应 data：

```json
{
  "poiId": "poi_322",
  "phoneMasked": "021-xxxx-xxxx",
  "phone": "021-12345678",
  "canCall": true,
  "callWindow": "09:00-19:00"
}
```

#### 5.1.20 上报地点详情页交互

* Method: POST
* Path: /api/v1/pois/{poiId}/actions
* 说明：用于收藏、分享、拨号等按钮行为上报

请求体：

```json
{
  "tripId": "t_9001",
  "stopId": "ts_1",
  "action": "call_click",
  "clientTime": "2026-06-03T21:00:00+08:00"
}
```

### 5.2 P1 扩展接口

#### 5.2.1 重生成方案

* POST /api/v1/plan/regenerate
* 入参：PlanGenerateRequest + excludePlanIds
* 用途：用户点击重新生成时避免重复

#### 5.2.2 方案可行性校验

* POST /api/v1/plan/validate
* 入参：planId、date、startTime
* 用途：校验营业状态、预算波动和可达性

#### 5.2.3 收藏与足迹

* POST /api/v1/user/favorites
* DELETE /api/v1/user/favorites/{poiId}
* GET /api/v1/user/favorites
* GET /api/v1/user/footprints
* POST /api/v1/user/checkins

#### 5.2.4 行程一键微调

* POST /api/v1/trip/{tripId}/adjust
* 入参：mode、constraint、userNote
* 用途：对应行程页底部轻一点、减少步行、避开排队、重新生成

请求体：

```json
{
  "mode": "reduce_walking",
  "constraint": {
    "maxWalkMinutes": 15
  },
  "userNote": "天气太热，希望多安排室内点位"
}
```

响应 data：

```json
{
  "tripId": "t_9001",
  "adjusted": true,
  "changeSummary": [
    "替换 1 个远距离点位",
    "总步行时长从 25 分钟降到 14 分钟"
  ],
  "trip": {}
}
```

#### 5.2.5 行程节点展开信息

* GET /api/v1/trip/{tripId}/stops/{stopId}/detail
* 用途：对应查看详情按钮，返回商户详情、推荐理由、营业状态和候选标签

#### 5.2.6 地点图文与营业信息刷新

* GET /api/v1/pois/{poiId}/live-status
* 用途：用于详情页驻留时刷新营业状态、排队热度、临时闭店等实时信息

### 5.3 P2 智能增强接口

#### 5.3.1 语音转文本

* POST /api/v1/ai/voice-to-text
* 入参：音频文件或音频 URL
* 出参：text、confidence

#### 5.3.2 自然语言解析

* POST /api/v1/ai/parse-prompt
* 入参：prompt、city
* 出参：解析后的 timeType、activities、budget、range

#### 5.3.3 埋点上报

* POST /api/v1/analytics/events
* 入参：事件数组，包含 eventName、properties、timestamp

## 6. 状态流与时序

### 6.1 主流程时序

1. 前端调用 /plan/generate 获取候选方案
2. 用户选择方案后调用 /trip/create
3. 前端进入行程页并调用 /trip/{tripId}
4. 每次打卡调用 /trip/{tripId}/stops/{stopId}
5. 发现页进入时调用 /discover/categories 和 /discover/places
6. 我的页进入时调用 /user/profile
7. 行程页进入后调用 /trip/{tripId}/overview 和 /trip/{tripId}/route-map
8. 点击换一个时调用 /trip/{tripId}/stops/{stopId}/alternatives 和 /replace
9. 点击轻一点或减少步行时调用 /trip/{tripId}/adjust
10. 打开出发前提醒时调用 /trip/{tripId}/reminders
11. 点击查看详情后调用 /pois/{poiId}、/pois/{poiId}/review-insights、/pois/{poiId}/arrival-hints
12. 点击收藏、分享、电话时调用 /pois/{poiId}/actions

### 6.2 状态机建议

* 方案状态：draft -> generated -> confirmed -> expired
* 行程状态：planned -> ongoing -> completed -> canceled
* 节点状态：pending -> done 或 skipped

## 7. 性能与可靠性建议

* 发现页接口建议 Redis 缓存，TTL 10 分钟
* 方案生成接口建议加并发限流，按 userId 或 deviceId 维度控制
* 所有写接口记录审计日志，便于排查冲突和重放
* 对外部 POI 服务增加熔断和降级策略

## 8. 联调清单

后端完成 P0 后，请提供如下联调产物：

1. 可用测试环境地址
2. Postman 或 Apifox 集合
3. 错误码字典与示例响应
4. 方案生成失败与行程冲突的模拟开关

前端联调验收标准：

1. 规划页可以稳定返回至少 3 个方案
2. 选择方案后可创建 tripId 并进入行程页
3. 行程节点打卡后进度可实时更新
4. 发现页和我的页接口在 300ms 到 800ms 内可用

## 9. 实施顺序建议

1. 先实现 P0 全部接口并打通主链路
2. 追加实现行程页增强接口，优先 overview、route-map、alternatives、replace、reminders
3. 再实现 P1 的重生成、微调、收藏足迹
4. 最后接入 P2 的语音、NLP 和埋点闭环
以上顺序可以保证最短路径上线，同时为后续智能推荐迭代预留扩展位。