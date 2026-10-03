# Box Rush 预览（团队内部）

Box Rush（BOXラッシュ）的产品模块示意图与界面原型，静态 HTML。

**访问地址：https://box-rush.github.io/preview/**（GitHub Pages，`main` 分支根目录）

> ⚠️ 本仓库与站点均为**公开**：拿到链接的任何人都能访问。只放模块图与示例数据原型，
> 不要放财务数据、法务细节或未公开的决策。

| 文件 | 内容 | 原件在哪 |
|---|---|---|
| `index.html` | 导航页 | 本仓库 |
| `modules.html` | 产品模块示意图（25 模块 / 153 功能点） | **本仓库**（与 `card-lottery-docs` 第 8 章同步） |
| `prototype/ui-*.html` | 界面原型 | **`card-lottery-docs/prototype/`**，这里是副本 |
| `pages.html` | 原型截图 + 页面 prompt + 生成过程 | 由 `tools/build_gallery.py` 从 `card-lottery-docs` 第 9 章生成，**不要手改** |
| `shots/*.jpg` | 原型截图 | 由 `tools/shoot.mjs`（Playwright）生成 |

## 更新方式

- **原型**：在 `card-lottery-docs` 里修改 `prototype/`，再把文件原样复制到本仓库的 `prototype/`。
  不要只改这里的副本，否则两边会不一致。
- **模块示意图**：直接改 `modules.html`；改之前先与 `card-lottery-docs` 的 `docs/breaking-platform.md` 第 8 章
  逐模块比对功能点数量与优先级。
- **新增原型**：放进 `prototype/`，并在 `index.html` 的"界面原型"区加卡片、从"待生成"里移除。
- **截图与汇总页**：原型或第 9 章变更后，在仓库根目录依次运行
  `node tools/shoot.mjs`（需 `npm i -D playwright && npx playwright install chromium`，不要提交 `node_modules`）
  与 `python3 tools/build_gallery.py`。新增页面要在两个脚本的页面表里各加一行。

## claude.ai 私有预览（可选）

`tools/build_artifact.py <原型文件> <输出> rel=url ...`：去掉 `<meta>` 与注释、取 `<head>`/`<body>` 内容，
把相对链接换成对应的 claude.ai 预览链接，用于发布私有预览。预览站本身不需要这一步。

## 约定

- 纯静态文件，不引入构建工具；`.nojekyll` 让 Pages 原样提供文件。
- 所有页面带 `noindex`，`robots.txt` 禁止抓取。这只能阻止搜索引擎收录，**不能阻止持有链接的人访问**。
- 页面中的场次、价格、卡号、商家名均为示例数据；所有原型统一使用原型时钟 2026-09-26 18:00 JST。
