#!/usr/bin/env python3
"""生成 pages.html：原型截图 + 页面 prompt + 生成过程。

数据全部取自设计文档第 9 章（§9.2 / §9.3 / §9.4–§9.6 / §9.8 / §9.9），本脚本不写任何内容判断。
用法（在本仓库根目录）：
  python3 tools/build_gallery.py [../card-lottery-docs/docs/breaking-platform.md]
截图先用 tools/shoot.mjs 生成到 shots/。
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "card-lottery-docs/docs/breaking-platform.md"

# 页面 → (原型链接, [(截图, 标签)])
PAGES = {
    "UI-01": ("ui-01-home.html", [("ui-01-home-mobile", "手机"), ("ui-01-home-desktop", "桌面")]),
    "UI-02": ("ui-02-lottery.html#L001", [("ui-02-lottery-mobile", "手机"), ("ui-02-lottery-desktop", "桌面")]),
    "UI-03": ("ui-03-pick.html#L005", [("ui-03-pick-mobile", "手机 · 已选 #03 #05"), ("ui-03-pick-desktop", "桌面")]),
    "UI-04": ("ui-04-checkout.html#L005-3-5", [("ui-04-checkout-mobile", "手机"), ("ui-04-checkout-desktop", "桌面")]),
    "UI-05": ("ui-05-my-slots.html#ready", [("ui-05-my-slots-mobile", "マイ枠 · 手机"), ("ui-05-my-slots-desktop", "マイ枠 · 桌面"),
                                            ("ui-05-progress-mobile", "进度页 · 手机"), ("ui-05-progress-desktop", "进度页 · 桌面")]),
    "UI-07": ("ui-07-recording.html#L011-t754", [("ui-07-recording-mobile", "手机"), ("ui-07-recording-desktop", "桌面")]),
    "UI-08": ("ui-08-result.html#L011", [("ui-08-result-mobile", "手机"), ("ui-08-result-desktop", "桌面")]),
    "UI-09": ("ui-09-verify.html#L015", [("ui-09-verify-mobile", "手机 · 验证完成"), ("ui-09-verify-desktop", "桌面")]),
    "UI-10": ("ui-10-collection.html#stored", [("ui-10-collection-mobile", "手机"), ("ui-10-collection-desktop", "桌面")]),
    "UI-11": ("ui-11-welcome.html", [("ui-11-welcome-mobile", "手机"), ("ui-11-welcome-desktop", "桌面")]),
    "UI-12": ("ui-12-spending.html", [("ui-12-spending-mobile", "手机"), ("ui-12-spending-desktop", "桌面")]),
    "UI-13": ("ui-13-merchant-wizard.html", [("ui-13-merchant-wizard-desktop", "桌面 · 步骤 2 分位编辑")]),
    "UI-14": ("ui-14-station.html", [("ui-14-station-tablet", "平板 1024×768 · 录像中")]),
    "UI-15": ("ui-15-attribution.html#L009", [("ui-15-attribution-desktop", "桌面 · 选中一行")]),
    "UI-16": ("ui-16-warehouse.html#pack", [("ui-16-warehouse-desktop", "桌面 · 梱包扫码中")]),
    "UI-17": ("ui-17-dashboard.html", [("ui-17-dashboard-desktop", "桌面")]),
}
GROUPS = [("用户端", ["UI-01", "UI-02", "UI-03", "UI-04", "UI-05", "UI-07", "UI-08", "UI-09", "UI-10", "UI-11", "UI-12"]),
          ("商家端", ["UI-13"]), ("运营端", ["UI-14", "UI-15", "UI-16", "UI-17"])]

doc = DOC.read_text(encoding="utf-8")
ch9 = doc[doc.index("## 第 9 章"):doc.index("## 附录 A")]


def section(start, end):
    i = ch9.index(start)
    j = ch9.index(end, i + len(start))
    body = ch9[i + len(start):j]
    return body.split("\n", 1)[1]  # 去掉标题行剩余部分


def first_code(text):
    m = re.search(r"```text\n(.*?)\n```", text, re.S)
    return m.group(1) if m else ""


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(text):
    rows = [l for l in text.splitlines() if l.startswith("|")]
    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    tb = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'


def paras(text):
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        if block.startswith("|") or block.startswith("```") or block.startswith("#"):
            continue
        out.append(f"<p>{inline(''.join(l.strip() for l in block.splitlines()))}</p>")
    return "".join(out)


# 页面 prompt
prompts, titles = {}, {}
for m in re.finditer(r"^#### (UI-\d\d) (.+)$", ch9, re.M):
    code = m.group(1)
    rest = ch9[m.end():]
    nxt = re.search(r"^#{2,4} ", rest, re.M)
    prompts[code] = first_code(rest[:nxt.start()] if nxt else rest)
    titles[code] = m.group(2).strip()

# 生成过程 §9.9
s99 = section("### 9.9 ", "### 9.10 ")
process = {}
for line in s99.splitlines():
    if line.startswith("| UI-") or line.startswith("| 全局"):
        c = cells(line)
        process[c[0].split()[0]] = c
global_row = process.pop("全局")
s99_conclusion = s99[s99.index("**结论**"):]

s981 = section("#### 9.8.1 ", "#### 9.8.2 ")
s982 = section("#### 9.8.2 ", "#### 9.8.3 ")
s983 = section("#### 9.8.3 ", "### 9.9 ")
s992 = first_code(section("### 9.2 ", "### 9.3 "))
s993 = first_code(section("### 9.3 ", "### 9.4 "))
s97 = section("### 9.7 ", "### 9.8 ")


def pre(t):
    return f"<pre>{html.escape(t, quote=False)}</pre>"


def page_block(code):
    href, shots = PAGES[code]
    figs = []
    for name, label in shots:
        kind = "m" if name.endswith("-mobile") else ("t" if name.endswith("-tablet") else "d")
        figs.append(f'<figure class="f-{kind}"><a href="shots/{name}.jpg" target="_blank" rel="noopener">'
                    f'<img src="shots/{name}.jpg" alt="{html.escape(code)} {html.escape(label)} 截图" loading="lazy"></a>'
                    f"<figcaption>{html.escape(label)}</figcaption></figure>")
    p = process.get(code)
    proc = ""
    if p:
        proc = (f'<dl class="proc"><dt>暴露的问题</dt><dd>{inline(p[1])}</dd><dt>处理</dt><dd>{inline(p[2])}</dd>'
                f'<dt>回写</dt><dd>{inline(p[3])}</dd><dt>类</dt><dd>{inline(p[4])}</dd></dl>')
    return f'''<article class="page" id="{code}">
  <div class="ph"><span class="code">{code}</span><h3>{inline(titles[code])}</h3>
    <a class="open" href="prototype/{href}">打开原型 →</a></div>
  <div class="shots">{"".join(figs)}</div>
  {proc}
  <details><summary>页面 prompt（§9.4–§9.6 原文）</summary>{pre(prompts[code])}</details>
</article>'''


toc = " · ".join(f'<a href="#{c}">{c}</a>' for _, cs in GROUPS for c in cs)
groups_html = "".join(
    f'<section><div class="sec-h"><h2>{g}</h2><span>{len(cs)} 页</span></div>{"".join(page_block(c) for c in cs)}</section>'
    for g, cs in GROUPS)

out = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<!-- 由 tools/build_gallery.py 从设计文档第 9 章生成，不要手改。 -->
<title>原型截图与 Prompt</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&family=Noto+Sans+JP:wght@700;900&family=JetBrains+Mono:wght@500;700&display=swap">
<style>
:root{{
  --bg:#FAFAF7; --surface:#FFFFFF; --ink:#1A1A1A; --ink-2:#6B6B6B; --line:#E6E5DE; --track:#ECEBE4;
  --accent:#3B3FD8; --accent-ink:#FFFFFF; --accent-soft:#ECEDFC; --trust:#0F9D8A; --trust-soft:#E1F3F0;
  --sans:"Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif;
  --jp:"Noto Sans JP","Hiragino Sans",sans-serif;
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{color-scheme:dark;
  --bg:#111214; --surface:#1A1B1E; --ink:#F2F2F2; --ink-2:#A0A0A0; --line:#2A2B2F; --track:#2A2B2F;
  --accent:#8E91F7; --accent-ink:#111214; --accent-soft:#23244A; --trust:#3CC4B0; --trust-soft:#15302C;}}}}
:root[data-theme="dark"]{{color-scheme:dark;
  --bg:#111214; --surface:#1A1B1E; --ink:#F2F2F2; --ink-2:#A0A0A0; --line:#2A2B2F; --track:#2A2B2F;
  --accent:#8E91F7; --accent-ink:#111214; --accent-soft:#23244A; --trust:#3CC4B0; --trust-soft:#15302C;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.65;padding:40px 16px 64px}}
a{{color:inherit}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:3px;border-radius:8px}}
.wrap{{max-width:1080px;margin:0 auto;display:flex;flex-direction:column;gap:44px}}
h1,h2,h3{{margin:0;text-wrap:balance}}
header{{display:flex;flex-direction:column;gap:10px}}
.back{{font-size:13px;color:var(--ink-2);text-decoration:none}}
h1{{font-size:26px;font-weight:900}}
.lede{{margin:0;color:var(--ink-2);max-width:68ch}}
.toc{{font-family:var(--mono);font-size:12.5px;color:var(--ink-2);line-height:2}}
.toc a{{text-decoration:none}} .toc a:hover{{color:var(--accent)}}
section{{display:flex;flex-direction:column;gap:18px}}
.sec-h{{display:flex;align-items:baseline;gap:12px;border-bottom:1px solid var(--line);padding-bottom:8px}}
.sec-h h2{{font-size:18px;font-weight:900}} .sec-h span{{font-size:12.5px;color:var(--ink-2)}}
h4{{margin:6px 0 0;font-size:15px}}
p{{margin:0}} section > p{{max-width:72ch}}
code{{font-family:var(--mono);font-size:.88em;background:var(--track);padding:0 4px;border-radius:4px}}
pre{{margin:0;font-family:var(--mono);font-size:12.5px;line-height:1.6;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px;overflow-x:auto;white-space:pre}}
.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--surface)}}
table{{border-collapse:collapse;width:100%;font-size:13.5px}}
th,td{{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}}
th{{font-size:12.5px;color:var(--ink-2);font-weight:700;white-space:nowrap}}
tr:last-child td{{border-bottom:0}}
details{{border:1px solid var(--line);border-radius:12px;background:var(--surface)}}
details > summary{{cursor:pointer;padding:10px 14px;font-size:13.5px;font-weight:700}}
details > pre{{border:0;border-top:1px solid var(--line);border-radius:0 0 12px 12px}}
.page{{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:18px;display:flex;flex-direction:column;gap:14px;scroll-margin-top:16px}}
.page details{{background:var(--bg)}}
.ph{{display:flex;align-items:center;flex-wrap:wrap;gap:8px 10px}}
.ph h3{{font-size:17px;font-weight:900}}
.code{{font-family:var(--mono);font-size:12px;font-weight:700;color:var(--accent);background:var(--accent-soft);padding:1px 7px;border-radius:5px}}
.open{{margin-left:auto;font-size:13px;font-weight:700;color:var(--accent);text-decoration:none}}
.shots{{display:flex;gap:12px;overflow-x:auto;padding-bottom:4px;align-items:flex-start}}
figure{{margin:0;flex:none;display:flex;flex-direction:column;gap:6px}}
figure a{{display:block;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--track)}}
figure img{{display:block;object-fit:cover;object-position:top}}
.f-m img{{width:180px;height:390px}}
.f-d img{{width:min(560px,78vw);aspect-ratio:1440/900}}
.f-t img{{width:min(500px,78vw);aspect-ratio:1024/768}}
figcaption{{font-size:12px;color:var(--ink-2)}}
.proc{{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0;font-size:13.5px}}
.proc dt{{color:var(--ink-2);font-size:12.5px;white-space:nowrap;padding-top:1px}}
.proc dd{{margin:0}}
.note{{font-size:13px;color:var(--ink-2)}}
footer{{font-size:12.5px;color:var(--ink-2);border-top:1px solid var(--line);padding-top:16px;display:flex;flex-direction:column;gap:4px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <a class="back" href="./">← 预览站首页</a>
    <h1>原型截图与 Prompt 过程</h1>
    <p class="lede">16 页原型的截图、生成它们的页面 prompt，以及每页生成中暴露的问题和回写位置。先看「方法」了解 prompt 的三层结构和页面模板，再按页浏览。内容取自设计文档第 9 章（§9.2–§9.9）。</p>
    <div class="toc">{toc}</div>
  </header>

  <section>
    <div class="sec-h"><h2>方法</h2><span>§9.8 Prompt 抽象</span></div>
    <h4>三层结构与回写闭环</h4>
    {table(s981)}
    {paras(s981)}
    <h4>页面 prompt 模板</h4>
    {pre(first_code(s982))}
    {paras(s982)}
    <h4>缺陷分类</h4>
    {table(s983)}
    <h4>结论</h4>
    {paras(s99_conclusion)}
    <p class="note">全局层面：{inline(global_row[1])} → {inline(global_row[2])}（回写 {inline(global_row[3])}）。</p>
  </section>

  {groups_html}

  <section>
    <div class="sec-h"><h2>项目层 prompt</h2><span>放进工具的项目级指令，所有页面共用</span></div>
    <details><summary>§9.2 全局设计系统与硬规则</summary>{pre(s992)}</details>
    <details><summary>§9.3 数据类型与 Mock 数据</summary>{pre(s993)}</details>
    <details><summary>§9.7 生成结果检查清单</summary>{table(s97)}</details>
  </section>

  <footer>
    <span>截图为 Playwright 自动生成（手机 390px · 2x / 桌面 1440×900 / 工位端 1024×768，浅色），点击看原图。UI-06 本轮不做。</span>
    <span>原型中的场次、价格、卡号、商家名均为示例；原型时钟统一为 2026-09-26 18:00 JST。</span>
  </footer>
</div>
</body>
</html>
'''
(ROOT / "pages.html").write_text(out, encoding="utf-8")
print("pages.html", len(out), "bytes;", len(prompts), "prompts;", len(process), "process rows")
