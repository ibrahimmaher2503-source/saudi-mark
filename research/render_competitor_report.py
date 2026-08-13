from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "saudi-car-wash-competitive-report.md"
OUT_HTML = ROOT.parent / "exports" / "saudi-car-wash-competitive-report.html"


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def table_html(rows: list[str]) -> str:
    parsed = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if cells and not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            parsed.append(cells)
    if not parsed:
        return ""
    header, body = parsed[0], parsed[1:]
    out = ['<div class="table-wrap"><table><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in header]
    out += ['</tr></thead><tbody>']
    for row in body:
        if len(row) < len(header):
            row += [""] * (len(header) - len(row))
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row[: len(header)]) + "</tr>")
    out += ["</tbody></table></div>"]
    return "".join(out)


def markdown_to_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    list_items: list[str] = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            out.append('<ul class="clean-list">' + "".join(f"<li>{inline(x)}</li>" for x in list_items) + "</ul>")
            list_items = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_list()
            if not in_code:
                in_code = True
                code_lines = []
            else:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and lines[i + 1].startswith("|"):
            flush_list()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(table_html(rows))
            continue

        if line.startswith("- "):
            list_items.append(line[2:].strip())
            i += 1
            continue
        if re.match(r"^\d+\. ", line):
            flush_list()
            out.append(f'<p class="numbered">{inline(line)}</p>')
            i += 1
            continue

        flush_list()
        if line.startswith("# "):
            out.append(f'<h1 class="report-title">{inline(line[2:])}</h1>')
        elif line.startswith("## "):
            out.append(f'<h2>{inline(line[3:])}</h2>')
        elif line.startswith("### "):
            out.append(f'<h3>{inline(line[4:])}</h3>')
        elif line == "---":
            out.append('<hr>')
        elif line.startswith("> "):
            out.append(f'<blockquote>{inline(line[2:])}</blockquote>')
        elif line.strip():
            out.append(f'<p>{inline(line)}</p>')
        i += 1

    flush_list()
    return "\n".join(out)


def build() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    body = markdown_to_html(source)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>Saudi Mark — تقرير المنافسة وسوق غسيل السيارات</title>
<style>
@page {{ size: A4; margin: 15mm 13mm 16mm 13mm; }}
:root {{ --ink:#162235; --muted:#627084; --line:#d9e1ea; --accent:#0b7285; --accent2:#f0a202; --paper:#ffffff; --soft:#f4f8fa; }}
* {{ box-sizing:border-box; }}
html, body {{ margin:0; padding:0; background:#e9eef2; color:var(--ink); font-family:"DejaVu Sans", Arial, sans-serif; direction:rtl; }}
body {{ font-size:10.2pt; line-height:1.7; }}
.page {{ max-width:210mm; margin:0 auto; background:var(--paper); padding:0; }}
.cover {{ min-height:267mm; padding:34mm 24mm 22mm; display:flex; flex-direction:column; justify-content:space-between; background:linear-gradient(145deg,#0b2435 0%,#123f52 58%,#0b7285 100%); color:#fff; page-break-after:always; position:relative; overflow:hidden; }}
.cover:after {{ content:""; position:absolute; width:180mm; height:180mm; border:1px solid rgba(255,255,255,.15); border-radius:50%; left:-70mm; bottom:-70mm; }}
.cover .eyebrow {{ color:#ffd166; font-size:10pt; letter-spacing:.08em; font-weight:bold; }}
.cover h1 {{ font-size:32pt; line-height:1.35; margin:18mm 0 7mm; max-width:155mm; }}
.cover .subtitle {{ font-size:16pt; line-height:1.6; color:#dcecf1; max-width:142mm; }}
.cover .meta {{ border-top:1px solid rgba(255,255,255,.35); padding-top:8mm; display:grid; grid-template-columns:1fr 1fr; gap:6mm; color:#dcecf1; }}
.cover .meta strong {{ color:#fff; display:block; font-size:11pt; }}
.cover .badge {{ display:inline-block; background:#ffd166; color:#132333; padding:2mm 5mm; border-radius:30px; font-weight:bold; margin-top:8mm; }}
.content {{ padding:0 3mm 10mm; }}
.report-title {{ display:none; }}
h2 {{ margin:12mm 0 5mm; padding:3mm 4mm 2.5mm; border-right:4px solid var(--accent2); background:linear-gradient(90deg,#f1f7f8,transparent); color:#0b4254; font-size:18pt; line-height:1.4; page-break-after:avoid; }}
h3 {{ margin:7mm 0 2mm; color:#0b7285; font-size:13pt; page-break-after:avoid; }}
p {{ margin:0 0 3.2mm; }}
a {{ color:#0b7285; text-decoration:none; font-weight:600; }}
hr {{ border:0; border-top:1px solid var(--line); margin:7mm 0; }}
blockquote {{ margin:5mm 0; padding:4mm 5mm; background:#eef8f8; border-right:4px solid var(--accent); color:#164e63; font-size:12pt; font-weight:600; page-break-inside:avoid; }}
.clean-list {{ margin:1mm 0 4mm; padding:0 7mm 0 0; }}
.clean-list li {{ margin:1.2mm 0; padding-right:1mm; }}
.numbered {{ margin:1.5mm 0; }}
.table-wrap {{ width:100%; overflow:visible; margin:4mm 0 6mm; page-break-inside:auto; }}
table {{ width:100%; border-collapse:collapse; table-layout:fixed; font-size:7.7pt; line-height:1.45; direction:rtl; }}
th {{ background:#103b4c; color:#fff; padding:2.2mm 1.8mm; border:1px solid #0b3443; font-weight:bold; vertical-align:top; }}
td {{ padding:2mm 1.7mm; border:1px solid var(--line); vertical-align:top; overflow-wrap:anywhere; }}
tr:nth-child(even) td {{ background:#f5f8fa; }}
thead {{ display:table-header-group; }}
tr {{ page-break-inside:avoid; }}
pre {{ direction:ltr; text-align:left; background:#142534; color:#d9f1f0; padding:4mm; border-radius:3mm; font-size:8pt; white-space:pre-wrap; }}
code {{ font-family:"DejaVu Sans Mono", monospace; font-size:.9em; }}
.content > p:first-of-type {{ margin-top:3mm; }}
@media print {{ html, body {{ background:#fff; }} .page {{ max-width:none; }} a {{ color:inherit; }} }}
</style>
</head>
<body>
<div class="page">
<section class="cover">
  <div>
    <div class="eyebrow">SAUDI MARK · MARKET INTELLIGENCE</div>
    <h1>تقرير المنافسة وسوق غسيل السيارات المتنقل في السعودية</h1>
    <div class="subtitle">خريطة المنافسين، قنوات الحجز والسوشيال ميديا، نقاط القوة والضعف، وفرصة التموضع في جدة</div>
    <div class="badge">نسخة بحث موثقة من المصادر العامة</div>
  </div>
  <div class="meta">
    <div><strong>السوق الأساسي</strong>جدة مع سياق المملكة</div>
    <div><strong>تاريخ التحقق</strong>13 أغسطس 2026</div>
    <div><strong>نوع التقرير</strong>Desk research + strategic analysis</div>
    <div><strong>العلامة محل الدراسة</strong>Saudi Mark</div>
  </div>
</section>
<section class="content">
{body}
</section>
</div>
</body>
</html>'''
    OUT_HTML.write_text(document, encoding="utf-8")
    print(OUT_HTML)


if __name__ == "__main__":
    build()
