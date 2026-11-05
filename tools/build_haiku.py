#!/usr/bin/env python3
"""Build the Haiku edition (docs/haiku/) from the main app (docs/).

The Haiku edition gives feedback inside the app with Claude Haiku 5.5 through the
user's own API key. It installs as a separate app with its own name, icon, address
and saved records. Run this after changing docs/index.html so both stay in sync:

    python3 tools/build_haiku.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "docs"
OUT = SRC / "haiku"
ACCENT = "#0F766E"


def swap(text, old, new, count=1):
    found = text.count(old)
    if found != count:
        raise SystemExit(f"expected {count} match(es), found {found}: {old[:70]!r}")
    return text.replace(old, new)


def build_index():
    s = (SRC / "index.html").read_text()
    s = swap(s, "<title>Daily English Drill</title>", "<title>Daily English Drill Haiku</title>")
    s = swap(s, '<meta name="theme-color" content="#D3263C">', f'<meta name="theme-color" content="{ACCENT}">')
    s = swap(s, '<div class="brand">Daily English Drill<small', '<div class="brand">English Drill Haiku<small')
    s = swap(s, 'const MODEL = "claude-opus-5-5";', 'const MODEL = "claude-haiku-5-5";')
    s = swap(s, 'import("./vendor/anthropic.mjs")', 'import("../vendor/anthropic.mjs")')

    # Haiku 5.5 has no server-side refusal fallback, so call the plain Messages API.
    s = swap(s, '''    const res = await c.beta.messages.create({
      model: MODEL,
      max_tokens: 16000,
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
''', '''    const res = await c.messages.create({
      model: MODEL,
      max_tokens: 16000,
''')

    # In-app feedback comes first; the Claude-app hand-off stays as the free fallback.
    s = swap(s, '''        <button class="btn" type="button" id="sp-claude">Claude로 피드백 받기</button>
        <button class="btn" type="button" id="sp-feedback" hidden>앱에서 바로 피드백</button>''',
             '''        <button class="btn" type="button" id="sp-feedback">피드백 받기 (Haiku)</button>
        <button class="btn ghost" type="button" id="sp-claude">Claude 앱으로 피드백 (무료)</button>''')
    s = swap(s, '''        <button class="btn" type="button" id="wr-claude">Claude로 첨삭 받기</button>
        <button class="btn" type="button" id="wr-feedback" hidden>앱에서 바로 첨삭</button>''',
             '''        <button class="btn" type="button" id="wr-feedback">첨삭 받기 (Haiku)</button>
        <button class="btn ghost" type="button" id="wr-claude">Claude 앱으로 첨삭 (무료)</button>''')
    s = swap(s, '''    // Free Claude-app handoff is always offered; the in-app API button appears once a key exists.
    $("sp-feedback").hidden = !has; $("wr-feedback").hidden = !has;
    $("sp-claude").className = has ? "btn ghost" : "btn"; $("wr-claude").className = has ? "btn ghost" : "btn";
''', '''    $("key-banner").hidden = has;
''')
    s = swap(s, '''    if (!state.settings.apiKey) {
      addEntry(entry);
      showStatus(st, "API 키가 없어 피드백 없이 기록만 저장했어요. 설정 탭에서 키를 넣으면 피드백을 받을 수 있어요.");
      return;
    }''', '''    if (!state.settings.apiKey) {
      showStatus(st, "설정 탭에서 Claude API 키를 먼저 넣어 주세요. 키 없이 받으려면 'Claude 앱으로 피드백 (무료)'을 누르세요.", true);
      return;
    }''')
    s = swap(s, '''    <div class="banner" id="notice" hidden>''', '''    <div class="banner" id="key-banner" hidden>
      <span>앱에서 바로 피드백을 받으려면 Claude API 키를 넣어 주세요.</span>
      <button class="btn quiet" type="button" data-go="alarm">키 넣기</button>
    </div>
    <div class="banner" id="notice" hidden>''')

    # Settings copy.
    s = swap(s, "<h3>Claude API 키 (선택)</h3>", "<h3>Claude API 키</h3>")
    s = swap(s, '''<p class="small">키가 없어도 <b>"Claude로 피드백 받기"</b> 버튼으로 Claude 앱에서 무료로 피드백을 받을 수 있어요. 키를 넣으면 앱 안에서 바로 피드백을 받고, AI 새 문제도 만들 수 있어요.</p>''',
             '''<p class="small">이 버전은 <b>Claude Haiku 5.5</b>로 앱 안에서 바로 피드백을 받아요. 키를 넣으면 AI 새 문제도 만들 수 있어요.</p>''')
    s = swap(s, "Claude Opus 5.5를 씁니다. 키를 쓰면 피드백 1회에 대략 50~100원 정도 들고, Claude 구독과는 별도로 결제돼요.",
             "Claude Haiku 5.5를 써서 피드백 1회에 대략 1~3원 정도 들어요. Claude 구독과는 별도로 결제돼요.")
    s = swap(s, "이 API 키로는 Claude Opus 5.5를 쓸 수 없어요.", "이 API 키로는 Claude Haiku 5.5를 쓸 수 없어요.")

    # Separate saved records and settings from the main edition (same web origin).
    s = re.sub(r'"ded\.', '"dedh.', s)
    s = swap(s, "download: `english-drill-${dayKey()}.json`", "download: `english-drill-haiku-${dayKey()}.json`")

    # Accent color for the edition.
    s = swap(s, "  --omr: #D3263C;", f"  --omr: {ACCENT};")
    s = swap(s, "  --rule: #F1B9C0;", "  --rule: #A7D8D3;")
    s = swap(s, "  --soft: #FCEDEF;", "  --soft: #E6F4F2;")
    s = s.replace("--rule: #5C2B35; --soft: #2A1820; --omr: #FF5D71; --on-omr: #1A0A0E;",
                  "--rule: #1F4A47; --soft: #10262A; --omr: #3CC7B8; --on-omr: #06201D;")
    (OUT / "index.html").write_text(s)


def build_sw():
    s = (SRC / "sw.js").read_text()
    s = re.sub(r'const VERSION = "ded-v(\d+)";', r'const VERSION = "dedh-v\1";', s)
    s = swap(s, '"./vendor/anthropic.mjs"', '"../vendor/anthropic.mjs"')
    (OUT / "sw.js").write_text(s)


def build_manifest():
    m = json.loads((SRC / "manifest.webmanifest").read_text())
    m.update({
        "name": "Daily English Drill Haiku",
        "short_name": "Drill Haiku",
        "description": "TOEIC 800 영어 말하기·쓰기 연습 (Claude Haiku 5.5 피드백)",
        "theme_color": ACCENT,
    })
    (OUT / "manifest.webmanifest").write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n")


def build_icons():
    from PIL import Image, ImageDraw

    (OUT / "icons").mkdir(parents=True, exist_ok=True)
    bg = tuple(int(ACCENT[i:i + 2], 16) for i in (1, 3, 5)) + (255,)

    def icon(size, pad, name):
        big = size * 4
        im = Image.new("RGBA", (big, big), bg)
        d = ImageDraw.Draw(im)
        c, r = big / 2, big * (0.5 - pad)
        d.ellipse([c - r, c - r, c + r, c + r], outline=(255, 255, 255, 255), width=max(4, int(big * 0.06)))
        r2 = r * 0.58
        d.ellipse([c - r2, c - r2, c + r2, c + r2], fill=(255, 255, 255, 255))
        im.resize((size, size), Image.LANCZOS).save(OUT / "icons" / name)

    icon(192, 0.22, "icon-192.png")
    icon(512, 0.22, "icon-512.png")
    icon(512, 0.30, "maskable-512.png")
    icon(180, 0.22, "apple-touch-icon.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_index()
    build_sw()
    build_manifest()
    build_icons()
    print(f"built {OUT.relative_to(ROOT)}")
