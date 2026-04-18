"""Render all 10 ASI threat videos with QA gates.

For each threat:
  1. pre-check assets (narration.wav present, duration matches HTML)
  2. run `npx hyperframes render`
  3. post-check the MP4 (resolution, duration, frame content, audio levels)
  4. copy MP4 into /out for publication

Abort the pipeline on first gate failure.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "out"


def render_one(asi_id: str) -> bool:
    d = SRC / asi_id
    html = d / "index.html"
    mp4_name = asi_id.lower() + ".mp4"
    renders_dir = d / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    mp4 = renders_dir / mp4_name

    # pre-check
    ok, rep = qa.pre_check(html)
    if not ok:
        print(f"❌ [{asi_id}] pre-check failed: {rep['problems']}")
        return False

    # render
    print(f"▶ [{asi_id}] rendering...")
    r = subprocess.run(
        ["npx", "hyperframes", "render",
         "--quality", "standard",
         "--output", str(mp4),
         "--quiet"],
        cwd=str(d),
        capture_output=True, text=True,
    )
    if r.returncode != 0 or not mp4.exists():
        print(f"❌ [{asi_id}] render failed (rc={r.returncode})")
        print(r.stderr[-2000:])
        return False

    # post-check
    ok, rep = qa.post_check(mp4)
    if not ok:
        print(f"❌ [{asi_id}] post-check failed: {rep['problems']}")
        return False

    # publish copy
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mp4, OUT / mp4_name)
    size_mb = mp4.stat().st_size / 1_048_576
    print(f"✅ [{asi_id}] {rep['duration_s']:.1f}s · {rep['resolution']} · "
          f"peak {rep['audio_peak_db']} dB · {size_mb:.1f} MB")
    return True


def main(argv: list[str]) -> int:
    targets = argv[1:] if len(argv) > 1 else sorted(p.name for p in SRC.glob("ASI*") if p.is_dir())
    failed = []
    for t in targets:
        if not render_one(t):
            failed.append(t)
            break  # abort on first failure
    if failed:
        print(f"\n❌ pipeline aborted — failed: {failed}")
        return 1
    print(f"\n✅ rendered {len(targets)} videos to {OUT}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
