"""Synthesise narration WAVs for all ASI threat videos via CNV V2 direct.

Reads src/ASI{01..10}/script.txt, builds SSML, posts to the custom-voice
endpoint using managed identity, writes audio/narration.wav.

Single session — the CNV V2 endpoint costs $4.04/hr while active, so we do
all 10 in one invocation to avoid repeated warmup.
"""
from __future__ import annotations

import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path.home() / "azure-video-factory" / "scripts"))
import cnv_direct  # type: ignore

from azure.identity import DefaultAzureCredential  # type: ignore
import requests  # type: ignore

SPEECH_HOST = "speech-cnv-adam-voice.cognitiveservices.azure.com"
V2_ENDPOINT_ID = "d55b6dc0-cdd2-4288-84e1-2255cee85b88"
API_VERSION = "2024-02-01-preview"


def _token() -> str:
    return DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default").token


def _endpoint_status() -> str:
    url = f"https://{SPEECH_HOST}/customvoice/endpoints/{V2_ENDPOINT_ID}?api-version={API_VERSION}"
    r = requests.get(url, headers={"Authorization": f"Bearer {_token()}"}, timeout=15)
    r.raise_for_status()
    return r.json().get("status", "Unknown")


def ensure_started() -> None:
    """Resume V2 endpoint if not running; block until Succeeded. Warmup ~90s."""
    status = _endpoint_status()
    print(f"→ V2 endpoint status: {status}")
    if status == "Succeeded":
        return
    print("→ resuming endpoint...")
    url = f"https://{SPEECH_HOST}/customvoice/endpoints/{V2_ENDPOINT_ID}:resume?api-version={API_VERSION}"
    r = requests.post(url, headers={"Authorization": f"Bearer {_token()}"}, timeout=30)
    r.raise_for_status()
    for _ in range(36):
        time.sleep(10)
        s = _endpoint_status()
        print(f"  …{s}")
        if s == "Succeeded":
            return
    raise RuntimeError("V2 endpoint did not reach Succeeded within 6 minutes")


def suspend() -> None:
    """Suspend V2 endpoint — stops $4.04/hr billing."""
    print("→ suspending V2 endpoint...")
    try:
        url = f"https://{SPEECH_HOST}/customvoice/endpoints/{V2_ENDPOINT_ID}:suspend?api-version={API_VERSION}"
        r = requests.post(url, headers={"Authorization": f"Bearer {_token()}"}, timeout=30)
        r.raise_for_status()
        print(f"  ✅ suspend accepted (HTTP {r.status_code})")
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
