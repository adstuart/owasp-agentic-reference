"""Synthesise narration WAVs for all ASI threat videos via CNV V2 direct.

Reads src/ASI{01..10}/script.txt, builds SSML, posts to the custom-voice
endpoint using managed identity, writes audio/narration.wav.

Single session — the CNV V2 endpoint costs $4.04/hr while active, so we do
all 10 in one invocation to avoid repeated warmup.
"""
from __future__ import annotations

import sys
import time
import urllib.request
from pathlib import Path

# Import cnv_direct from the private azure-video-factory repo.
sys.path.insert(0, str(Path.home() / "azure-video-factory" / "scripts"))
import cnv_direct  # type: ignore

PROXY = "https://app-cnv-voice-proxy.azurewebsites.net"


def _proxy_call(path: str, method: str = "GET") -> str:
    req = urllib.request.Request(f"{PROXY}{path}", method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def ensure_started() -> None:
    """Block until V2 endpoint is Succeeded (running). Warmup takes ~90s."""
    print("→ ensuring V2 endpoint is running...")
    _proxy_call("/api/endpoint/start?model=v2", method="POST")
    for _ in range(30):
        body = _proxy_call("/api/endpoint/status?model=v2")
        if '"Succeeded"' in body:
            print(f"  ✅ {body}")
            return
        time.sleep(10)
    raise RuntimeError("V2 endpoint did not reach Succeeded within 5 minutes")


def suspend() -> None:
    """Suspend V2 endpoint to stop $4.04/hr billing."""
    print("→ suspending V2 endpoint (stops $4.04/hr billing)...")
    try:
        print(f"  {_proxy_call('/api/endpoint/stop?model=v2', method='POST')}")
    except Exception as e:
        print(f"  ⚠ suspend failed: {e} — CHECK MANUALLY")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

PROSODY_RATE = "-5%"
PROSODY_PITCH = "-2%"


def _synth_one(threat_dir: Path) -> bool:
    script_path = threat_dir / "script.txt"
    audio_dir = threat_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    out_path = audio_dir / "narration.wav"

    if not script_path.exists():
        print(f"  ⚠ no script.txt in {threat_dir.name}, skipping")
        return False

    text = script_path.read_text(encoding="utf-8").strip()
    ssml = cnv_direct.build_ssml(
        text,
        prosody_rate=PROSODY_RATE,
        prosody_pitch=PROSODY_PITCH,
    )
    print(f"[{threat_dir.name}] {len(text.split())} words -> {out_path.name}")
    ok = cnv_direct.synthesize(ssml, out_path)
    if ok:
        size_kb = out_path.stat().st_size / 1024
        print(f"  ✅ {size_kb:,.0f} KB")
    return ok


def main(argv: list[str]) -> int:
    targets = argv[1:] if len(argv) > 1 else sorted(p.name for p in SRC.glob("ASI*") if p.is_dir())
    failed: list[str] = []
    try:
        ensure_started()
        for name in targets:
            d = SRC / name
            if not d.is_dir():
                print(f"  ⚠ not a directory: {d}")
                failed.append(name); continue
            if not _synth_one(d):
                failed.append(name)
    finally:
        suspend()
    if failed:
        print(f"\n❌ failed: {failed}")
        return 1
    print(f"\n✅ synthesised {len(targets) - len(failed)} narrations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
