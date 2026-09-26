# Box Rush 预览（团队内部）

Box Rush（BOXラッシュ）的产品模块示意图与界面原型，静态 HTML，由 GitHub Pages 提供访问。

| 文件 | 内容 | 原件在哪 |
|---|---|---|
| `index.html` | 导航页 | 本仓库 |
| `modules.html` | 产品模块示意图（25 模块 / 153 功能点） | **本仓库**（与 `card-lottery-docs` 第 8 章同步） |
| `prototype/ui-*.html` | 界面原型 | **`card-lottery-docs/prototype/`**，这里是副本 |

## 更新方式

- **原型**：在 `card-lottery-docs` 里修改 `prototype/`，再把文件原样复制到本仓库的 `prototype/`。
  不要只改这里的副本，否则两边会不一致。
- **模块示意图**：直接改 `modules.html`；改之前先与 `card-lottery-docs` 的 `docs/breaking-platform.md` 第 8 章
  逐模块比对功能点数量与优先级。
- **新增原型**：放进 `prototype/`，并在 `index.html` 的"界面原型"区加卡片、从"待生成"里移除。

## 约定

- 纯静态文件，不引入构建工具；`.nojekyll` 让 Pages 原样提供文件。
- 所有页面带 `noindex`，`robots.txt` 禁止抓取。这只能阻止搜索引擎收录，**不能阻止持有链接的人访问**。
- 页面中的场次、价格、卡号、商家名均为示例数据。
