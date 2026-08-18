from pathlib import Path
import subprocess
import shutil

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "app-ui"
WORK = ROOT / "exports" / "booking-journey-free-test-frames"
OUT = ROOT / "exports" / "saudi-mark-booking-journey-ai-mockup-free-test.mp4"
CHROME = shutil.which("google-chrome") or shutil.which("chromium")

SCENES = [
    {
        "id": "01",
        "screen": "01-splash-screen.jpg",
        "step": "UI Reference · Intro",
        "number": "رحلة الحجز في 15 ثانية",
        "title": "من التطبيق إلى الموعد",
        "body": "شرح بصري مختصر لخطوات الحجز",
        "accent": "Saudi Mark",
    },
    {
        "id": "02",
        "screen": "02-booking-date-slot-vehicle.jpg",
        "step": "UI Reference · 01 / 03",
        "number": "الخطوة الأولى",
        "title": "اختاري المنطقة والموعد",
        "body": "ابدئي بتحديد المنطقة واليوم والوقت من الشاشة المرجعية",
        "accent": "Date + Slot",
    },
    {
        "id": "03",
        "screen": "05-booking-vehicle-location.jpg",
        "step": "UI Reference · 02 / 03",
        "number": "الخطوة الثانية",
        "title": "حددي السيارة والموقع",
        "body": "راجعي السيارة ونقطة الخدمة قبل المتابعة",
        "accent": "Vehicle + Location",
    },
    {
        "id": "04",
        "screen": "04-booking-location-gifts.jpg",
        "step": "UI Reference · 03 / 03",
        "number": "الخطوة الأخيرة",
        "title": "أضيفي الإضافات وراجعي",
        "body": "راجعي التفاصيل المتاحة في شاشة واحدة قبل التأكيد",
        "accent": "Review first",
    },
    {
        "id": "05",
        "screen": "01-splash-screen.jpg",
        "step": "UI Reference · Saudi Mark CTA",
        "number": "الحجز يبدأ من سؤال واضح",
        "title": "لا تعرفي أي خطوة؟ اسألي",
        "body": "نسخة اختبارية باستخدام Mockups من واجهات التطبيق الحالية",
        "accent": "اكتبي: احجز",
    },
]

CSS = """
* { box-sizing: border-box; }
html, body { margin:0; width:1080px; height:1920px; overflow:hidden; }
body { font-family: Arial, "Noto Sans Arabic", sans-serif; background:#071d2b; color:#fff; }
.scene { width:1080px; height:1920px; position:relative; overflow:hidden; background:
  radial-gradient(circle at 82% 10%, rgba(16,112,159,.50), transparent 32%),
  linear-gradient(150deg,#061a28 0%,#08283a 58%,#0b4455 100%); }
.glow { position:absolute; width:800px; height:800px; border-radius:50%; right:-350px; bottom:-300px; background:rgba(245,184,65,.13); filter:blur(20px); }
.topline { position:absolute; top:66px; left:70px; right:70px; display:flex; align-items:center; justify-content:space-between; direction:rtl; }
.brand { font-size:25px; font-weight:700; letter-spacing:.4px; color:#f5b841; }
.ref { font-size:18px; color:#b8d1dc; direction:rtl; }
.copy { position:absolute; top:160px; right:70px; left:70px; direction:rtl; text-align:right; }
.kicker { color:#f5b841; font-weight:700; font-size:25px; margin-bottom:18px; }
h1 { margin:0 0 18px; font-size:58px; line-height:1.18; letter-spacing:-1px; }
.body { color:#d4e5eb; font-size:28px; line-height:1.5; max-width:860px; }
.phone { position:absolute; width:548px; height:1168px; left:266px; top:525px; border:13px solid #122f40; border-radius:58px; background:#102a39; box-shadow:0 30px 70px rgba(0,0,0,.48), 0 0 0 2px rgba(255,255,255,.12); padding:15px; }
.phone:before { content:""; position:absolute; width:130px; height:17px; background:#122f40; border-radius:0 0 14px 14px; top:-1px; left:calc(50% - 65px); z-index:3; }
.screen { width:100%; height:100%; object-fit:cover; border-radius:38px; display:block; }
.badge { position:absolute; right:70px; bottom:250px; padding:14px 22px; border:1px solid rgba(245,184,65,.65); border-radius:26px; color:#ffda83; background:rgba(12,39,54,.72); font-size:22px; direction:rtl; }
.footer { position:absolute; bottom:82px; right:70px; left:70px; display:flex; align-items:center; justify-content:space-between; direction:rtl; }
.cta { font-size:24px; font-weight:700; color:#fff; }
.dots { display:flex; gap:10px; direction:ltr; }
.dot { width:12px; height:12px; border-radius:50%; background:#557889; }
.dot.active { width:42px; border-radius:12px; background:#f5b841; }
.num { color:#abc8d2; font-size:20px; }
"""


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def html_for(scene):
    image_uri = (ASSETS / scene["screen"]).resolve().as_uri()
    active = int(scene["id"]) - 1
    dots = "".join(f'<span class="dot {"active" if i == active else ""}"></span>' for i in range(len(SCENES)))
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Saudi Mark booking test {scene["id"]}</title><style>{CSS}</style></head><body>
<div class="scene"><div class="glow"></div>
  <div class="topline"><span class="brand">SAUDI MARK</span><span class="ref">{esc(scene["step"])}</span></div>
  <div class="copy"><div class="kicker">{esc(scene["number"])}</div><h1>{esc(scene["title"])}</h1><div class="body">{esc(scene["body"])}</div></div>
  <div class="phone"><img class="screen" src="{image_uri}" alt="Application UI reference"></div>
  <div class="badge">{esc(scene["accent"])}</div>
  <div class="footer"><div class="cta">AI Motion Mockup Test</div><div class="dots">{dots}</div><div class="num">{scene["id"]} / {len(SCENES)}</div></div>
</div></body></html>'''


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    if not CHROME:
        raise SystemExit("Google Chrome/Chromium is required for Arabic HTML rendering")
    WORK.mkdir(parents=True, exist_ok=True)
    for old in WORK.glob("*"):
        old.unlink()
    html_files = []
    for scene in SCENES:
        html = WORK / f"scene-{scene['id']}.html"
        png = WORK / f"scene-{scene['id']}.png"
        html.write_text(html_for(scene), encoding="utf-8")
        html_files.append(html)
        run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", "--window-size=1080,1920", f"--screenshot={png}", html.as_uri()])
    concat = WORK / "concat.txt"
    concat_lines = []
    for scene in SCENES:
        scene_path = (WORK / f"scene-{scene['id']}.png").as_posix()
        concat_lines.extend([f"file '{scene_path}'", "duration 3"])
    last_scene_path = (WORK / f"scene-{SCENES[-1]['id']}.png").as_posix()
    concat_lines.append(f"file '{last_scene_path}'")
    concat.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    # Each still is held for 3 seconds; a short crossfade makes the mockups feel like a real explainer.
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat),
        "-vf", "scale=1080:1920:flags=lanczos,format=yuv420p,fps=30",
        "-r", "30", "-t", str(len(SCENES) * 3), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-movflags", "+faststart", str(OUT)
    ])
    # The concat image input has no duration metadata in some ffmpeg builds; normalize the final duration explicitly.
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(OUT), "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-movflags", "+faststart", str(OUT.with_suffix('.tmp.mp4'))])
    (OUT.with_suffix('.tmp.mp4')).replace(OUT)
    print(f"created={OUT}")
    print(f"scenes={len(SCENES)}")
    print(f"frames={len(list(WORK.glob('scene-*.png')))}")


if __name__ == "__main__":
    main()
