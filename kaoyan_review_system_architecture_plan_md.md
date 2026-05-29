# 考研知识点复习系统 —— 项目级结构规划

## 一、项目定位

一个支持：

- 每日知识点上传
- 智能复习
- 历史管理
- 数据分析
- AI辅助学习

的 Web 学习系统。

适合作为：

- 个人长期学习工具
- 软件工程课程设计
- Flask/Vue 全栈项目
- 简历项目
- 后期毕业设计基础

---

# 二、整体系统架构

```text
前端（Vue / HTML）
        ↓
后端 API（Flask）
        ↓
数据库（MySQL / SQLite）
        ↓
文件存储（图片 / PDF）
```

---

# 三、系统模块划分

整个系统建议拆分为以下模块：

```text
1. 用户系统
2. 知识点管理系统
3. 智能复习系统
4. 文件上传系统
5. 搜索系统
6. 数据分析系统
7. AI辅助系统
8. 系统设置模块
```

---

# 四、推荐项目目录结构

## Flask 单体项目结构（推荐第一版）

```text
study-review-system/
│
├── app/
│   ├── routes/                 # 路由层
│   │   ├── auth.py
│   │   ├── notes.py
│   │   ├── review.py
│   │   └── statistics.py
│   │
│   ├── services/               # 业务逻辑层
│   │   ├── auth_service.py
│   │   ├── note_service.py
│   │   ├── review_service.py
│   │   └── ai_service.py
│   │
│   ├── models/                 # 数据模型层
│   │   ├── user.py
│   │   ├── note.py
│   │   ├── review_record.py
│   │   └── tag.py
│   │
│   ├── utils/                  # 工具类
│   │   ├── ocr.py
│   │   ├── scheduler.py
│   │   ├── file_handler.py
│   │   └── security.py
│   │
│   ├── static/                 # 静态资源
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/
│   │
│   ├── templates/              # HTML页面
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── upload.html
│   │   ├── history.html
│   │   └── statistics.html
│   │
│   └── config.py
│
├── database/
│   ├── init.sql
│   └── migration/
│
├── tests/
│
├── requirements.txt
├── run.py
└── README.md
```

---

# 五、核心模块设计

# 1. 用户系统

## 功能

- 用户注册
- 用户登录
- Session / JWT 认证
- 修改密码
- 用户信息管理

---

## users 数据表

```sql
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    password_hash TEXT,
    email TEXT,
    avatar TEXT,
    created_at TEXT
);
```

---

# 2. 知识点管理系统（核心模块）

## 功能

支持：

- 上传知识点
- Markdown 编辑
- 图片上传
- PDF上传
- 标签系统
- 科目分类
- 掌握程度标记
- 易错知识点标记

---

## notes 数据表

```sql
CREATE TABLE notes(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    subject TEXT,
    chapter TEXT,
    title TEXT,
    content TEXT,
    difficulty INTEGER,
    mastery_level INTEGER,
    created_at TEXT,
    updated_at TEXT
);
```

---

## 标签系统

### tags 表

```sql
CREATE TABLE tags(
    id INTEGER PRIMARY KEY,
    tag_name TEXT
);
```

### note_tags 表

```sql
CREATE TABLE note_tags(
    note_id INTEGER,
    tag_id INTEGER
);
```

---

# 3. 文件上传系统

## 支持文件类型

- PNG/JPG
- PDF
- Word
- Markdown

---

## 文件目录结构

```text
uploads/
│
├── images/
├── pdf/
├── markdown/
└── temp/
```

---

## 上传流程

```text
用户上传
    ↓
文件校验
    ↓
UUID重命名
    ↓
保存本地/云端
    ↓
数据库记录路径
```

---

# 4. 智能复习系统（项目亮点）

## 功能

- 自动生成复习时间
- 艾宾浩斯遗忘曲线复习
- 今日待复习列表
- 已完成复习记录
- 动态调整复习周期

---

## 复习间隔

```text
1天
3天
7天
15天
30天
```

---

## review_plan 数据表

```sql
CREATE TABLE review_plan(
    id INTEGER PRIMARY KEY,
    note_id INTEGER,
    review_date TEXT,
    review_count INTEGER,
    status TEXT,
    next_review_date TEXT
);
```

---

## 算法流程

```text
新增知识点
    ↓
生成复习计划
    ↓
每天检查待复习内容
    ↓
用户完成复习
    ↓
重新计算下次复习时间
```

---

# 5. 搜索系统

## 功能

支持：

- 全文搜索
- 标签搜索
- 科目搜索
- 时间筛选
- 模糊查询

---

## 技术方案

### 第一版

- SQL LIKE

### 后期升级

- Elasticsearch

---

# 6. 数据分析系统

## 功能

### 学习统计

- 每日学习时长
- 每周知识点数量
- 科目占比
- 掌握率变化
- 学习热力图

---

## 图表类型

- 折线图
- 热力图
- 柱状图
- 雷达图

---

## 推荐技术

前端图表：

- Apache ECharts

---

# 7. AI辅助系统（高级功能）

# OCR识别

实现流程：

```text
上传手写笔记
    ↓
OCR识别文字
    ↓
自动生成知识点
```

---

## 推荐技术

- PaddleOCR

---

# AI总结功能

例如：

```text
输入：傅里叶变换笔记
输出：
- 核心公式
- 易错点
- 高频考点
```

---

## 推荐技术

- OpenAI API

---

# 8. 前端页面规划

## 页面结构

```text
登录页
注册页
主页 Dashboard
知识点上传页
历史记录页
知识点详情页
今日复习页
统计分析页
个人中心
```

---

## Dashboard 页面布局

```text
+----------------------+
| 今日学习概览          |
+----------------------+

今日上传：12
待复习：8
完成率：75%

------------------------

[最近知识点]

[学习热力图]

[复习提醒]
```

---

# 六、推荐技术栈

# 第一阶段（推荐）

## 后端

- Flask

## 数据库

- SQLite

## ORM

- SQLAlchemy

## 前端

- HTML / CSS / JavaScript

---

# 第二阶段升级

## 前端框架

- Vue.js

## UI框架

- Element Plus

---

# 第三阶段高级版

## 后端

- FastAPI

## 数据库

- MySQL / PostgreSQL

## 缓存

- Redis

## 搜索引擎

- Elasticsearch

---

# 七、推荐开发顺序

# 第一阶段（最小可运行版本）

目标：先跑通核心功能。

## 功能

- 登录
- 上传知识点
- 数据库存储
- 历史查看

---

# 第二阶段

## 增加功能

- 图片上传
- 搜索功能
- 标签系统
- Markdown 编辑

---

# 第三阶段

## 增加功能

- 智能复习
- 数据统计
- 图表分析

---

# 第四阶段（项目亮点）

## 增加功能

- OCR识别
- AI总结
- AI问答
- 自动生成错题本

---

# 八、未来扩展方向

# 1. 手机端

可扩展为：

- 微信小程序
- Android App
- iOS App

---

# 2. 多端同步

例如：

```text
电脑上传知识点
手机进行复习
```

---

# 3. AI学习助手

例如：

```text
“帮我总结通信原理重点”
“生成408模拟题”
“分析我的薄弱章节”
```

---

# 4. 知识图谱

例如：

```text
信号系统
   ↓
傅里叶变换
   ↓
拉普拉斯变换
   ↓
卷积
```

---

# 九、最终项目名称建议

推荐名称：

## 《智能考研知识点管理与复习系统》

适用于：

- 软件工程项目
- 课程设计
- 简历项目
- 毕业设计基础项目

---

# 十、最终建议

推荐采用：

```text
Flask + SQLite + HTML/CSS/JS
```

先做出：

- 上传知识点
- 历史查看
- 智能复习

的最小可运行版本。

之后再逐步升级：

- Vue
- OCR
- AI功能
- 数据分析
- 多端同步

这样开发压力最小，同时成长路线最清晰。

