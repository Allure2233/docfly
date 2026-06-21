<p align="center">
  <img src="static/logo.svg" alt="docfly" width="96" height="96">
</p>

<h1 align="center">docfly</h1>

<p align="center">
  <b>One command turns a Markdown folder into a beautiful doc site with live preview.</b>
  <br>
  <sub>一条命令，把 Markdown 文件夹变成漂亮的文档站，实时预览。</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-≥3.10-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

---

## Why / 为什么

You're writing project docs in Markdown. You want to see them rendered nicely — sidebar navigation, code highlighting, dark mode — without configuring MkDocs, Docusaurus, or VitePress. You want to hit save and see the change instantly. **`docfly` is that.** No config. No build step. One command.

你在用 Markdown 写项目文档。你想看到漂亮的渲染效果 — 但不想要 MkDocs / Docusaurus 那样复杂的配置。你想保存即看。**`docfly` 就是这个。**

## Install / 安装

```bash
pip install docfly
```

## Usage / 使用

```bash
docfly ./docs            # 启动 / Start on :8080
docfly ./docs --open     # 自动打开浏览器 / Open browser
docfly ./docs -p 3000    # 自定义端口 / Custom port
docfly ./docs --no-watch # 关闭实时预览 / No live reload
```

## Features / 功能

| Feature 功能 | Description 说明 |
|---|---|
| ⚡ **Live reload / 实时预览** | Edit `.md` → browser refreshes instantly (WebSocket) |
| 🎨 **Code highlighting / 代码高亮** | Pygments monokai theme, 50+ languages |
| 🌓 **Dark & light / 深浅主题** | One-click toggle, preference saved |
| 📂 **Nested nav / 嵌套导航** | Sidebar mirrors your folder structure |
| 🏷️ **Front-matter** | `title`, `order` — control display name and sort |
| 📑 **Permalinks / 标题锚点** | Every heading gets an anchor link |

## Folder Structure / 目录结构

```
docs/
├── index.md            → /
├── getting-started.md  → /getting-started
└── api/
    ├── overview.md     → /api/overview
    └── auth.md         → /api/auth
```

## Front-matter

```yaml
---
title: Getting Started  # or: 快速开始
order: 1
---
```

## Tech Stack / 技术栈

FastAPI + Jinja2 + WebSocket + watchfiles + Pygments. ~250 lines of core logic / 核心逻辑约 250 行。

## License / 开源协议

MIT
