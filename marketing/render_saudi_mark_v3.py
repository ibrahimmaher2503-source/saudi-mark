from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "marketing" / "saudi-mark-ai-women-instagram-tiktok-plan-v3-ar.md"
OUT_HTML = ROOT / "exports" / "saudi-mark-ai-women-instagram-tiktok-plan-v3-ar.html"
OUT_PDF = ROOT / "exports" / "saudi-mark-ai-women-instagram-tiktok-plan-v3-ar.pdf"
CHARACTER = ROOT / "assets" / "brand" / "saudi-mark-character-reference.jpg"
APP_UI = ROOT / "assets" / "app-ui"


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)
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
        row = row + [""] * max(0, len(header) - len(row))
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
            out.append(f'<h1 class="plan-title">{inline(line[2:])}</h1>')
        elif line.startswith("## "):
            out.append(f'<h2>{inline(line[3:])}</h2>')
        elif line.startswith("### "):
            out.append(f'<h3>{inline(line[4:])}</h3>')
        elif line.startswith("#### "):
            out.append(f'<h4>{inline(line[5:])}</h4>')
        elif line == "---":
            out.append('<hr>')
        elif line.startswith("> "):
            out.append(f'<blockquote>{inline(line[2:])}</blockquote>')
        elif line.strip():
            out.append(f'<p>{inline(line)}</p>')
        i += 1
    flush_list()
    return "\n".join(out)


def image_uri(path: Path) -> str:
    return path.as_uri()


def build() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    body = markdown_to_html(source)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    app_images = sorted(APP_UI.glob("*.jpg"))
    app_cards = "".join(
        f'<figure><img src="{image_uri(p)}" alt="مرجع واجهة تطبيق Saudi Mark"><figcaption>{p.stem.replace("-", " ")}</figcaption></figure>'
        for p in app_images
    )
    document = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>Saudi Mark — خطة AI للسيدات على Instagram وTikTok v3</title>
<style>
@page {{ size:A4; margin:14mm 12mm 16mm; }}
:root {{ --ink:#152437; --muted:#647487; --line:#d7e1e8; --navy:#092a3b; --teal:#087f8c; --blue:#1261a0; --yellow:#f5b841; --soft:#f3f8fa; --paper:#fff; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; padding:0; background:#e8eef2; color:var(--ink); font-family:"DejaVu Sans",Arial,sans-serif; direction:rtl; }}
body {{ font-size:9.4pt; line-height:1.68; }}
.page {{ max-width:210mm; margin:0 auto; background:var(--paper); }}
.cover {{ min-height:267mm; page-break-after:always; color:white; padding:27mm 22mm 18mm; position:relative; overflow:hidden; display:flex; flex-direction:column; justify-content:space-between; background:linear-gradient(135deg,#071e2e 0%,#0b4258 53%,#087f8c 100%); }}
.cover:before {{ content:""; position:absolute; width:200mm; height:200mm; border:1px solid rgba(255,255,255,.13); border-radius:50%; left:-100mm; bottom:-96mm; }}
.cover:after {{ content:""; position:absolute; width:95mm; height:95mm; border:1px solid rgba(245,184,65,.38); border-radius:50%; right:-55mm; top:-38mm; }}
.cover .mark {{ position:relative; z-index:1; display:flex; align-items:center; gap:8mm; }}
.cover .mark img {{ width:28mm; height:28mm; object-fit:cover; border-radius:50%; border:2px solid rgba(255,255,255,.75); }}
.cover .eyebrow {{ position:relative; z-index:1; color:#ffd166; font-size:9pt; font-weight:bold; letter-spacing:.1em; }}
.cover h1 {{ position:relative; z-index:1; max-width:160mm; font-size:31pt; line-height:1.34; margin:14mm 0 6mm; }}
.cover .subtitle {{ position:relative; z-index:1; max-width:142mm; font-size:15pt; line-height:1.65; color:#e2f0f2; }}
.cover .positioning {{ position:relative; z-index:1; border-right:4px solid var(--yellow); padding:4mm 5mm; margin-top:10mm; max-width:150mm; background:rgba(255,255,255,.08); font-size:12pt; font-weight:bold; }}
.cover .meta {{ position:relative; z-index:1; border-top:1px solid rgba(255,255,255,.35); padding-top:7mm; display:grid; grid-template-columns:1fr 1fr; gap:5mm; color:#d8e9ed; }}
.cover .meta strong {{ display:block; color:white; font-size:10pt; }}
.cover .badge {{ display:inline-block; position:relative; z-index:1; background:var(--yellow); color:#152437; padding:1.8mm 4mm; border-radius:20px; margin-top:7mm; font-weight:bold; }}
.content {{ padding:0 2mm 10mm; }}
.plan-title {{ display:none; }}
h2 {{ margin:11mm 0 4mm; padding:2.7mm 4mm 2.2mm; border-right:4px solid var(--yellow); background:linear-gradient(90deg,#eef7f8,transparent); color:#08495d; font-size:16pt; line-height:1.4; page-break-after:avoid; }}
h3 {{ margin:6.5mm 0 2mm; color:var(--teal); font-size:12.2pt; page-break-after:avoid; }}
h4 {{ margin:4mm 0 1.5mm; color:var(--blue); font-size:10.8pt; page-break-after:avoid; }}
p {{ margin:0 0 2.8mm; }}
a {{ color:var(--teal); text-decoration:none; font-weight:600; }}
hr {{ border:0; border-top:1px solid var(--line); margin:6mm 0; }}
blockquote {{ margin:4mm 0; padding:3.5mm 4.5mm; background:#edf8f8; border-right:4px solid var(--teal); color:#134e61; font-size:11.5pt; font-weight:600; page-break-inside:avoid; }}
.clean-list {{ margin:1mm 0 3.5mm; padding:0 6mm 0 0; }}
.clean-list li {{ margin:1mm 0; padding-right:1mm; }}
.numbered {{ margin:1.3mm 0; }}
.table-wrap {{ width:100%; overflow:visible; margin:3mm 0 5mm; page-break-inside:auto; }}
table {{ width:100%; border-collapse:collapse; table-layout:fixed; font-size:7.15pt; line-height:1.4; direction:rtl; }}
th {{ background:#0b4258; color:white; padding:1.9mm 1.5mm; border:1px solid #083548; font-weight:bold; vertical-align:top; }}
td {{ padding:1.7mm 1.45mm; border:1px solid var(--line); vertical-align:top; overflow-wrap:anywhere; }}
tr:nth-child(even) td {{ background:#f5f8fa; }}
thead {{ display:table-header-group; }}
tr {{ page-break-inside:avoid; }}
pre {{ direction:ltr; text-align:left; background:#142534; color:#d9f1f0; padding:3mm; border-radius:2mm; font-size:7.5pt; white-space:pre-wrap; }}
code {{ font-family:"DejaVu Sans Mono",monospace; font-size:.88em; }}
del {{ color:#8c3b35; }}
.asset-page {{ page-break-before:always; padding-top:8mm; }}
.asset-page h2 {{ margin-top:0; }}
.asset-intro {{ color:var(--muted); }}
.character-card {{ display:grid; grid-template-columns:48mm 1fr; gap:7mm; align-items:center; margin:5mm 0 8mm; padding:5mm; background:var(--soft); border:1px solid var(--line); }}
.character-card img {{ width:48mm; height:45mm; object-fit:cover; border-radius:5mm; }}
.character-card strong {{ color:#08495d; font-size:12pt; }}
.app-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:5mm; margin-top:5mm; }}
.app-grid figure {{ margin:0; padding:2.5mm; background:#f7fafb; border:1px solid var(--line); border-radius:3mm; break-inside:avoid; }}
.app-grid img {{ display:block; width:100%; height:65mm; object-fit:cover; object-position:top; border-radius:2mm; }}
.app-grid figcaption {{ font-size:7.3pt; color:var(--muted); margin-top:1.5mm; text-align:center; }}
@media print {{ html,body {{ background:#fff; }} .page {{ max-width:none; }} a {{ color:inherit; }} }}
</style>
</head>
<body>
<div class="page">
<section class="cover">
  <div>
    <div class="mark"><img src="{image_uri(CHARACTER)}" alt="Saudi Mark brand character"><span class="eyebrow">SAUDI MARK · GROWTH PLAYBOOK</span></div>
    <h1>خطة AI للسيدات</h1>
    <div class="subtitle">نسخة v3 لمحتوى Instagram وTikTok، مبنية على AI Motion ومواقف دقيقة للسيدات في جدة.</div>
    <div class="positioning">عناية سيارات متنقلة فاخرة في جدة، بموعد واضح ونتيجة يمكن رؤيتها.</div>
    <div class="badge">نسخة v3 · AI Content · Instagram + TikTok · 2026</div>
  </div>
  <div class="meta">
    <div><strong>الإيقاع</strong>3 فيديوهات + Carousel أسبوعيًا</div>
    <div><strong>الإعلانات</strong>2,400 SAR خلال 8 أسابيع</div>
    <div><strong>السوق الأساسي</strong>جدة أولًا</div>
    <div><strong>نسخة الخطة</strong>v3 · 13 أغسطس 2026</div>
  </div>
</section>
<section class="content">
{body}
</section>
<section class="asset-page content">
  <h2>مرجع الهوية والتطبيق المستخدم في الخطة</h2>
  <p class="asset-intro">الأصول التالية مملوكة/مقدمة من صاحب البراند، وتُستخدم كمرجع بصري للمحتوى، الإعلانات، العروض، وتجربة الحجز. الأسعار والأرقام الظاهرة في واجهات التطبيق ليست اعتمادًا إنتاجيًا.</p>
  <div class="character-card"><img src="{image_uri(CHARACTER)}" alt="Saudi Mark character"><div><strong>كارتكتر Saudi Mark الرسمي</strong><p>قط أبيض ودود بكاب أزرق ونظارة حماية وشال أزرق وخرطوم أزرق/أصفر. يظهر في الـmotion والـStories والتغليف دون استبدال لقطات الخدمة الحقيقية.</p></div></div>
  <h3>Application UI references</h3>
  <div class="app-grid">{app_cards}</div>
</section>
</div>
</body>
</html>'''
    OUT_HTML.write_text(document, encoding="utf-8")
    print(OUT_HTML)


if __name__ == "__main__":
    build()
