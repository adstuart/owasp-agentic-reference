"""Generate each ASI folder's script.txt, index.html, hyperframes.json, meta.json
from scripts/threats.py and shared/theme.css.

Run this AFTER narrations are synthesised (or at least a first pass) so that
the audio data-duration matches the actual .wav length — the pre-render QA
gate compares them.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from threats import THREATS

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
THEME_CSS = (ROOT / "shared" / "theme.css").read_text()

# -- scene timing plan (seconds) ------------------------------------------
# Narration measured at 58-62s. We pad to 60s and allocate:
#   S1 intro         0.0 -> 10.5   (kicker + big title)
#   S2 predecessor  10.1 -> 24.0   (LLM Top-10 2025 explainer)
#   S3 evolution    23.6 -> 40.0   (from/to + bullets)
#   S4 mitigations  39.6 -> 54.5   (one big card + optional secondary)
#   S5 closing      54.1 -> 60.0   (URL)
# 0.4s overlap between scenes enables crossfade via gsap.from opacity.

SCENES = [
    {"id": "s1", "start": 0.0,  "duration": 10.8, "track": 1},
    {"id": "s2", "start": 10.4, "duration": 13.9, "track": 2},
    {"id": "s3", "start": 23.9, "duration": 16.4, "track": 1},
    {"id": "s4", "start": 39.9, "duration": 14.8, "track": 2},
    {"id": "s5", "start": 54.3, "duration": 5.7,  "track": 1},
]
COMP_DURATION = 60.0

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1920, height=1080" />
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <style>
{theme_css}

/* composition-scoped tweaks */
.scene {{ z-index: 1; }}
body {{ background: var(--bg-0); }}
</style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
</head>
<body>

<div id="root" data-composition-id="main" data-start="0" data-duration="{comp_duration}" data-width="1920" data-height="1080">

  <audio id="narration" src="audio/narration.wav" data-start="0" data-duration="{audio_duration}" data-track-index="0" data-volume="1"></audio>

  <!-- Scene 1: title card -->
  <div id="s1" class="clip scene {accent_class}" data-start="{s1_start}" data-duration="{s1_duration}" data-track-index="{s1_track}">
    <div class="accent-bar"></div>
    <div class="kicker">OWASP Agentic Top-10 / 2026</div>
    <div class="headline">{asi_id}</div>
    <div class="headline small" style="margin-top:16px">{threat_title}</div>
    <div class="subtitle">Threat {asi_num} of 10 — mapped to its 2025 LLM predecessor<br/>with Adam's pick of top Microsoft mitigation</div>
    <div class="scene-footer"><span>adstuart / owasp-agentic-reference</span><span>{asi_id}</span></div>
  </div>

  <!-- Scene 2: LLM 2025 predecessor -->
  <div id="s2" class="clip scene {accent_class}" data-start="{s2_start}" data-duration="{s2_duration}" data-track-index="{s2_track}">
    <div class="accent-bar"></div>
    <div class="kicker">Previously in the LLM Top-10 / 2025</div>
    <div class="headline small" style="margin-top:20px">{pred_name}</div>
    <div class="body-text">{pred_text}</div>
    <div class="scene-footer"><span>{asi_id} — Previous Generation</span><span>LLM Top-10 · 2025</span></div>
  </div>

  <!-- Scene 3: evolution -->
  <div id="s3" class="clip scene {accent_class}" data-start="{s3_start}" data-duration="{s3_duration}" data-track-index="{s3_track}">
    <div class="accent-bar"></div>
    <div class="kicker">How it evolves</div>
    <div class="headline small" style="margin-top:20px">{threat_title}</div>
    <div class="evolve-row">
      <div class="evolve-side">
        <div class="tag">LLM · 2025</div>
        <div class="label">{from_label}</div>
      </div>
      <div class="evolve-arrow">&#x2192;</div>
      <div class="evolve-side agent">
        <div class="tag">Agent · 2026</div>
        <div class="label">{to_label}</div>
      </div>
    </div>
    <div class="bullet-list">
      <div class="bullet" id="b1"><div class="dot"></div><div>{bullet1}</div></div>
      <div class="bullet" id="b2"><div class="dot"></div><div>{bullet2}</div></div>
      <div class="bullet" id="b3"><div class="dot"></div><div>{bullet3}</div></div>
    </div>
    <div class="scene-footer"><span>{asi_id} — Evolution</span><span>agentic · 2026</span></div>
  </div>

  <!-- Scene 4: mitigation(s) -->
  <div id="s4" class="clip scene {accent_class}" data-start="{s4_start}" data-duration="{s4_duration}" data-track-index="{s4_track}">
    <div class="accent-bar"></div>
    <div class="kicker">Top Microsoft mitigation</div>
    <div class="headline small" style="margin-top:20px">Defence of choice</div>
    {mitigation_cards}
    <div class="scene-footer"><span>{asi_id} — Mitigation</span><span>microsoft.com/security</span></div>
  </div>

  <!-- Scene 5: closing -->
  <div id="s5" class="clip scene {accent_class} outro" data-start="{s5_start}" data-duration="{s5_duration}" data-track-index="{s5_track}">
    <div class="accent-bar"></div>
    <div class="kicker" style="text-align:center">Full mapping</div>
    <div class="big">{asi_id} — {threat_title}</div>
    <div class="url">github.com/adstuart/owasp-agentic-reference</div>
  </div>

</div>

<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});

// -------- Scene 1: title card ({s1_start}s) --------
tl.from("#s1", {{ opacity: 0, duration: 0.5, ease: "sine.inOut" }}, {s1_start});
tl.from("#s1 .kicker", {{ y: -20, opacity: 0, duration: 0.6, ease: "power2.out" }}, {s1_start} + 0.3);
tl.from("#s1 .headline", {{ y: 40, opacity: 0, duration: 0.8, ease: "expo.out" }}, {s1_start} + 0.5);
tl.from("#s1 .headline.small", {{ y: 30, opacity: 0, duration: 0.7, ease: "power3.out" }}, {s1_start} + 0.9);
tl.from("#s1 .subtitle", {{ opacity: 0, y: 20, duration: 0.6, ease: "sine.out" }}, {s1_start} + 1.4);
tl.from("#s1 .scene-footer", {{ opacity: 0, duration: 0.5 }}, {s1_start} + 1.9);
tl.from("#s1 .accent-bar", {{ scaleY: 0, transformOrigin: "top", duration: 0.5, ease: "power3.out" }}, {s1_start} + 0.1);

// -------- Scene 2: predecessor ({s2_start}s) --------
tl.from("#s2", {{ opacity: 0, duration: 0.5, ease: "sine.inOut" }}, {s2_start});
tl.from("#s2 .accent-bar", {{ scaleY: 0, transformOrigin: "top", duration: 0.5, ease: "power3.out" }}, {s2_start} + 0.05);
tl.from("#s2 .kicker", {{ x: -30, opacity: 0, duration: 0.5, ease: "power2.out" }}, {s2_start} + 0.2);
tl.from("#s2 .headline", {{ y: 40, opacity: 0, duration: 0.7, ease: "expo.out" }}, {s2_start} + 0.4);
tl.from("#s2 .body-text", {{ opacity: 0, y: 20, duration: 0.8, ease: "power2.out" }}, {s2_start} + 0.8);
tl.from("#s2 .scene-footer", {{ opacity: 0, duration: 0.5 }}, {s2_start} + 1.2);

// -------- Scene 3: evolution ({s3_start}s) --------
tl.from("#s3", {{ opacity: 0, duration: 0.5, ease: "sine.inOut" }}, {s3_start});
tl.from("#s3 .accent-bar", {{ scaleY: 0, transformOrigin: "top", duration: 0.5, ease: "power3.out" }}, {s3_start} + 0.05);
tl.from("#s3 .kicker", {{ y: -20, opacity: 0, duration: 0.5, ease: "power2.out" }}, {s3_start} + 0.2);
tl.from("#s3 .headline", {{ y: 30, opacity: 0, duration: 0.6, ease: "expo.out" }}, {s3_start} + 0.4);
tl.from("#s3 .evolve-row .evolve-side:not(.agent)", {{ x: -60, opacity: 0, duration: 0.6, ease: "power3.out" }}, {s3_start} + 0.9);
tl.from("#s3 .evolve-arrow", {{ scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2)" }}, {s3_start} + 1.3);
tl.from("#s3 .evolve-side.agent", {{ x: 60, opacity: 0, duration: 0.6, ease: "power3.out" }}, {s3_start} + 1.4);
tl.from("#s3 #b1", {{ x: -30, opacity: 0, duration: 0.5, ease: "power2.out" }}, {s3_start} + 2.4);
tl.from("#s3 #b2", {{ x: -30, opacity: 0, duration: 0.5, ease: "power2.out" }}, {s3_start} + 2.8);
tl.from("#s3 #b3", {{ x: -30, opacity: 0, duration: 0.5, ease: "power2.out" }}, {s3_start} + 3.2);
tl.from("#s3 .scene-footer", {{ opacity: 0, duration: 0.5 }}, {s3_start} + 3.8);

// -------- Scene 4: mitigation ({s4_start}s) --------
tl.from("#s4", {{ opacity: 0, duration: 0.5, ease: "sine.inOut" }}, {s4_start});
tl.from("#s4 .accent-bar", {{ scaleY: 0, transformOrigin: "top", duration: 0.5, ease: "power3.out" }}, {s4_start} + 0.05);
tl.from("#s4 .kicker", {{ y: -20, opacity: 0, duration: 0.5, ease: "power2.out" }}, {s4_start} + 0.2);
tl.from("#s4 .headline", {{ y: 30, opacity: 0, duration: 0.6, ease: "expo.out" }}, {s4_start} + 0.4);
{mitigation_tweens}
tl.from("#s4 .scene-footer", {{ opacity: 0, duration: 0.5 }}, {s4_start} + 3.5);

// -------- Scene 5: closing ({s5_start}s) --------
tl.from("#s5", {{ opacity: 0, duration: 0.6, ease: "sine.inOut" }}, {s5_start});
tl.from("#s5 .accent-bar", {{ scaleY: 0, transformOrigin: "top", duration: 0.5, ease: "power3.out" }}, {s5_start} + 0.05);
tl.from("#s5 .kicker", {{ opacity: 0, duration: 0.5, ease: "sine.out" }}, {s5_start} + 0.2);
tl.from("#s5 .big", {{ scale: 0.92, opacity: 0, duration: 0.7, ease: "power3.out" }}, {s5_start} + 0.5);
tl.from("#s5 .url", {{ y: 20, opacity: 0, duration: 0.6, ease: "power2.out" }}, {s5_start} + 1.0);
// final fade-out is allowed on the last scene
tl.to("#s5", {{ opacity: 0, duration: 0.6, ease: "sine.inOut" }}, {comp_duration_minus_06});

window.__timelines["main"] = tl;
</script>

</body>
</html>
"""


def _mitigation_card_html(idx: int, m: dict) -> str:
    # idx: 1 or 2
    return (
        f'    <div class="mitigation-card" id="mit{idx}">\n'
        f'      <div class="product">{m["product"]}</div>\n'
        f'      <div class="name">{m["name"]}</div>\n'
        f'      <div class="why">{m["why"]}</div>\n'
        f'    </div>'
    )


def _mitigation_tweens(count: int, s4_start: float) -> str:
    lines = []
    if count >= 1:
        lines.append(
            f'tl.from("#mit1", {{ y: 40, opacity: 0, duration: 0.7, ease: "power3.out" }}, {s4_start} + 1.0);'
        )
    if count >= 2:
        lines.append(
            f'tl.from("#mit2", {{ y: 40, opacity: 0, duration: 0.7, ease: "power3.out" }}, {s4_start} + 2.2);'
        )
    return "\n".join(lines)


def build_one(threat: dict) -> None:
    asi_id = threat["id"]
    out_dir = SRC / asi_id
    (out_dir / "audio").mkdir(parents=True, exist_ok=True)

    # script.txt
    (out_dir / "script.txt").write_text(threat["script"], encoding="utf-8")

    # Probe actual narration duration if it exists; otherwise use composition duration.
    wav = out_dir / "audio" / "narration.wav"
    if wav.exists():
        try:
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nk=1:nw=1", str(wav)],
                capture_output=True, text=True, check=True,
            )
            audio_duration = round(float(r.stdout.strip()), 3)
        except Exception:
            audio_duration = COMP_DURATION
    else:
        audio_duration = COMP_DURATION

    # hyperframes.json + meta.json
    (out_dir / "hyperframes.json").write_text(
        json.dumps({
            "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
            "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        }, indent=2) + "\n"
    )
    (out_dir / "meta.json").write_text(
        json.dumps({"id": asi_id.lower() + "-" + re.sub(r"[^a-z0-9]+", "-", threat["title"].lower()).strip("-"),
                    "name": f"{asi_id} — {threat['title']}"}, indent=2) + "\n"
    )

    # mitigation cards/tweens
    mits = threat["mitigations"]
    mitigation_cards = "\n".join(_mitigation_card_html(i + 1, m) for i, m in enumerate(mits))
    mit_tweens = _mitigation_tweens(len(mits), SCENES[3]["start"])

    ev = threat["evolution"]
    html = HTML_TEMPLATE.format(
        title=f"{asi_id} — {threat['title']}",
        threat_title=threat["title"],
        asi_id=asi_id,
        asi_num=str(int(asi_id[3:])),
        theme_css=THEME_CSS,
        comp_duration=COMP_DURATION,
        audio_duration=audio_duration,
        comp_duration_minus_06=round(COMP_DURATION - 0.6, 2),
        accent_class="red" if threat["accent"] == "red" else "",
        pred_name=threat["pred_name"],
        pred_text=threat["pred_text"],
        from_label=ev["from_label"],
        to_label=ev["to_label"],
        bullet1=ev["bullets"][0],
        bullet2=ev["bullets"][1],
        bullet3=ev["bullets"][2],
        mitigation_cards=mitigation_cards,
        mitigation_tweens=mit_tweens,
        s1_start=SCENES[0]["start"], s1_duration=SCENES[0]["duration"], s1_track=SCENES[0]["track"],
        s2_start=SCENES[1]["start"], s2_duration=SCENES[1]["duration"], s2_track=SCENES[1]["track"],
        s3_start=SCENES[2]["start"], s3_duration=SCENES[2]["duration"], s3_track=SCENES[2]["track"],
        s4_start=SCENES[3]["start"], s4_duration=SCENES[3]["duration"], s4_track=SCENES[3]["track"],
        s5_start=SCENES[4]["start"], s5_duration=SCENES[4]["duration"], s5_track=SCENES[4]["track"],
    )
    (out_dir / "index.html").write_text(html, encoding="utf-8")


def main() -> int:
    for t in THREATS:
        build_one(t)
        print(f"  built {t['id']} — {t['title']}")
    print(f"\n✅ generated {len(THREATS)} compositions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
