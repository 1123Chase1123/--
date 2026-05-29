# 📚 考研知识点管理与复习系统

基于 **Flask + PyWebView** 的桌面级考研复习工具，支持知识点管理、艾宾浩斯智能复习、数据分析。**无需部署服务器、无需买域名**，下载即用。

---

## ⚡ 快速安装（推荐）

### 方式一：下载安装包（无需装 Python）

> 从 [Releases 页面](https://github.com/1123Chase1123/--/releases) 下载最新版的 `考研复习系统_v1.0.zip`

```text
1. 下载 考研复习系统_v1.0.zip
2. 解压到任意文件夹
3. 双击 ReviewSystem.exe       ← 弹出桌面窗口，直接使用
```

> 💡 解压后整个文件夹约 60MB，包含运行所需的所有文件，**不需要安装 Python**。

### 方式二：从源码运行（需 Python）

适合想自己修改代码或二次开发的用户。

```bash
# 1. 克隆仓库
git clone https://github.com/1123Chase1123/--.git
cd --

# 2. 一键启动
双击 setup.bat                  ← 自动检查环境、安装依赖、启动应用

# 或者手动操作：
pip install -r requirements.txt
python desktop_app.py           ← 桌面窗口模式
```

### 方式三：自行打包成 .exe

```bash
pip install pyinstaller
python build_exe.py
# 输出: dist/ReviewSystem/ReviewSystem.exe
```

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

## 🗂️ 项目结构

```
├── app/                        # 核心代码
│   ├── routes/                 # 路由层
│   ├── services/               # 业务逻辑层
│   ├── models/                 # 数据模型层
│   ├── templates/              # 12个页面模板
│   ├── static/                 # CSS/JS
│   └── utils/                  # 工具类
├── desktop_app.py              # 🔥 桌面启动器
├── run.py                      # 网页模式入口
├── setup.bat                   # 一键启动脚本
├── build_exe.py                # PyInstaller 打包脚本
├── requirements.txt            # 依赖列表
└── README.md
```

---

## ⚙️ 用户数据存储位置

| 模式 | 数据位置 |
|------|---------|
| **源码运行** | 项目根目录 `database/` 文件夹 |
| **exe 运行** | `exe所在目录/_data/` 文件夹 |

> 💡 备份时复制 `_data/`（或 `database/`）文件夹即可迁移所有数据

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Flask 3.x + SQLAlchemy |
| 数据库 | SQLite |
| 前端 | HTML / CSS / JavaScript + ECharts |
| 桌面包装 | PyWebView 6.x + WebView2 |
| 打包 | PyInstaller |
