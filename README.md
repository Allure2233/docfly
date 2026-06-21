<p align="center">
  <img src="static/logo.svg" alt="docfly" width="128" height="128">
</p>

<h1 align="center">docfly</h1>

<p align="center">
  <b>One command, a folder of Markdown, and you've got a beautiful doc site with live preview.</b>
  <br>
  一条命令，把 Markdown 文件夹变成漂亮的文档站，实时预览。
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-≥3.10-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

---

[English](#english) | [中文](#中文)

---

## English

### Why

You're writing project docs in Markdown. You want to see them rendered nicely — sidebar navigation, code highlighting, dark mode — without configuring MkDocs, Docusaurus, or VitePress. You want to hit save and see the change instantly.

`docfly` is that. No config. No build step. One command.

### Install

```bash
pip install docfly
```

### Usage

```bash
docfly ./docs            # Start server on :8080
docfly ./docs --open     # Auto-open browser
docfly ./docs -p 3000    # Custom port
docfly ./docs --no-watch # Disable live reload
```

### Features

| Feature | Description |
|---|---|
| ⚡ **Live reload** | Edit any `.md` file — browser refreshes instantly via WebSocket |
| 🎨 **Code highlighting** | Pygments with monokai theme, 50+ languages |
| 🌓 **Dark & light** | One-click toggle, preference saved |
| 📂 **Nested nav** | Sidebar mirrors your folder structure |
| 🏷️ **Front-matter** | `title`, `order` — control display name and sort |
| 📑 **Permalinks** | Every heading gets an anchor link |

### Folder Structure

```
docs/
├── index.md          →  /
├── getting-started.md → /getting-started
└── api/
    ├── overview.md   → /api/overview
    └── auth.md       → /api/auth
```

### Front-matter

```yaml
---
title: Getting Started
order: 1
---
```

### Tech Stack

FastAPI + Jinja2 + WebSocket + watchfiles + Pygments. ~250 lines of core logic.

### License

MIT

---

## 中文

### 为什么用它

你在用 Markdown 写项目文档。你想看到漂亮的渲染效果——侧边栏导航、代码高亮、深色模式——但不想折腾 MkDocs、Docusaurus 或 VitePress。你想保存即看。

`docfly` 就是干这个的。零配置，零构建，一条命令。

### 安装

```bash
pip install docfly
```

### 使用

```bash
docfly ./docs            # 启动服务，默认 8080 端口
docfly ./docs --open     # 自动打开浏览器
docfly ./docs -p 3000    # 自定义端口
docfly ./docs --no-watch # 关闭实时预览
```

### 功能

| 功能 | 说明 |
|---|---|
| ⚡ **实时预览** | 编辑 Markdown 保存 → 浏览器即时刷新（WebSocket） |
| 🎨 **代码高亮** | Pygments monokai 主题，50+ 语言自动着色 |
| 🌓 **深色浅色** | 一键切换主题，偏好自动记忆 |
| 📂 **嵌套导航** | 左侧栏自动按文件夹结构生成目录 |
| 🏷️ **Front-matter** | `title`、`order` 控制标题和排序 |
| 📑 **标题锚点** | 每个标题自动生成可点击的 permalink |

### 目录结构

```
docs/
├── index.md            → /
├── getting-started.md  → /getting-started
└── api/
    ├── overview.md     → /api/overview
    └── auth.md         → /api/auth
```

### Front-matter

```yaml
---
title: 快速开始
order: 1
---
```

### 技术栈

FastAPI + Jinja2 + WebSocket + watchfiles + Pygments。核心逻辑约 250 行。

### 开源协议

MIT
