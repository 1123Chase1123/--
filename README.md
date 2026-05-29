# 📚 考研知识点管理与复习系统

基于 **Flask + PyWebView** 的桌面级考研复习工具，支持知识点管理、艾宾浩斯智能复习、数据分析。**无需部署服务器、无需买域名**，双击即用。

---

## ✨ 功能一览

| 功能 | 说明 |
|------|------|
| **知识点管理** | Markdown 编辑器、科目分类、标签系统、难度/掌握程度标记 |
| **智能复习** | 基于艾宾浩斯遗忘曲线，自动生成 1/3/7/15/30 天复习计划 |
| **数据统计** | ECharts 图表展示学习趋势、科目分布、掌握程度 |
| **文件上传** | 支持图片/PDF/Markdown 附件，UUID 重命名防冲突 |
| **全文搜索** | 标题+内容全文检索，支持科目/标签/时间多条件筛选 |
| **动态科目** | 上传知识点时可随时新建科目，自动持久化 |
| **易错标记** | 标记易错知识点，重点突破 |

---

## 🚀 快速部署到你的电脑

### 环境要求

- **Windows 10/11**（或其他系统，但推荐 Windows）
- **Python 3.10+**（推荐 3.12）
- **Git**

### 步骤一：克隆仓库

```bash
git clone https://github.com/1123Chase1123/--.git
cd --
```

### 步骤二：安装依赖

```bash
# 推荐使用虚拟环境（可选但推荐）
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤三：运行应用

**方式 A：桌面模式（推荐）**

弹出原生桌面窗口，像真正的软件一样使用：

```bash
python desktop_app.py
```

**方式 B：网页模式**

在浏览器中打开，适合调试或双屏使用：

```bash
python run.py
# 然后浏览器访问 http://127.0.0.1:5000
```

---

## 📦 打包为独立 .exe（发给别人用）

如果想让你的朋友**不用装 Python 也能用**，可以打包成单个可执行文件：

```bash
# 1. 安装打包工具
pip install pyinstaller

# 2. 执行打包脚本
python build_exe.py

# 3. 打包完成后
#    dist/ReviewSystem/ReviewSystem.exe  ← 双击运行
```

> **注意**：打包后的 exe 依赖 WebView2 运行时。Windows 10/11 通常自带，如果没有会自动从微软下载。

---

## 🗂️ 项目结构

```
├── app/                        # 核心代码
│   ├── __init__.py             # Flask 应用工厂
│   ├── config.py               # 配置（数据库/上传/密钥）
│   ├── routes/                 # 路由层
│   │   ├── auth.py             # 登录/注册/修改密码
│   │   ├── notes.py            # 知识点 CRUD/历史/搜索
│   │   ├── review.py           # 今日复习/完成复习
│   │   └── statistics.py       # 数据统计 API
│   ├── services/               # 业务逻辑层
│   │   ├── auth_service.py     # 认证逻辑
│   │   └── note_service.py     # 知识点+标签+复习计划
│   ├── models/                 # 数据模型层
│   │   ├── user.py             # 用户模型
│   │   ├── note.py             # 知识点模型
│   │   ├── tag.py              # 标签模型
│   │   └── review_plan.py      # 复习计划模型
│   ├── static/                 # 静态资源（CSS/JS/上传文件）
│   ├── templates/              # 12个 Jinja2 页面模板
│   └── utils/                  # 工具类
│       ├── security.py         # 输入验证
│       ├── file_handler.py     # 文件上传处理
│       └── subject_manager.py  # 科目动态管理
│
├── database/                   # 数据库目录
│   ├── init.sql                # 建表脚本
│   └── subjects.json           # 科目配置文件
│
├── desktop_app.py              # 🔥 桌面应用启动器（双击这个）
├── run.py                      # 网页模式启动器
├── build_exe.py                # PyInstaller 打包脚本
├── requirements.txt            # Python 依赖列表
└── README.md                   # 本文件
```

---

## ⚙️ 用户数据存储位置

- **开发模式**：数据存储在项目根目录的 `database/` 文件夹
- **打包 exe 模式**：数据存储在 `exe文件所在目录/_data/` 文件夹
  - `_data/database/study_review.db` — 你的所有知识点
  - `_data/database/subjects.json` — 你自定义的科目

> 💡 备份时复制 `_data/` 文件夹即可迁移所有数据

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Flask 3.x |
| 数据库 | SQLite + SQLAlchemy ORM |
| 前端 | HTML / CSS / JavaScript + Jinja2 |
| 图表 | Apache ECharts |
| 桌面包装 | PyWebView 6.x + WebView2 |
| 打包 | PyInstaller |

---

## 📜 License

MIT
