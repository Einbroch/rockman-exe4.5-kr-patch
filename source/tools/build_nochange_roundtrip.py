#!/usr/bin/env python3
"""Reinsert the untouched baseline and verify consumer-payload equivalence."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from extract_baseline import ROOT, require_hash


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=None)
    ap.add_argument("--tpl-dir", default="analysis/tpl_baseline")
    ap.add_argument("--out", default="poc/output/exe45_nochange_roundtrip.gba")
    ap.add_argument("--report", default="analysis/exe45_nochange_roundtrip.json")
    args = ap.parse_args()

    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    profile = config["source_profile"]
    rom = Path(args.rom) if args.rom else ROOT / profile["filename"]
    if not rom.is_absolute():
        rom = ROOT / rom
    require_hash(rom, profile["sha256"])

    textpet = ROOT / config["textpet"]["exe"]
    dll = ROOT / config["textpet"]["dll"]
    tpi = ROOT / config["text_catalog"]["path"]
    require_hash(textpet, config["textpet"]["exe_sha256"])
    require_hash(dll, config["textpet"]["dll_sha256"])
    require_hash(tpi, config["text_catalog"]["sha256"])
    plugin_dir = ROOT / config["textpet"]["plugins"]
    for name, expected in config["textpet"]["plugin_sha256"].items():
        require_hash(plugin_dir / name, expected)

    tpl_dir = ROOT / args.tpl_dir
    if len(list(tpl_dir.glob("*.tpl"))) != 732:
        raise SystemExit("baseline extraction must contain exactly 732 TPL files")
    out = ROOT / args.out
    report = ROOT / args.report
    out.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)

    build = [
        str(textpet), "Load-Plugins", str(ROOT / config["textpet"]["plugins"]),
        "Game", config["textpet"]["game"], "Load-File-Index", str(tpi),
        "Load-File", str(rom), "Read-Text-Archives", str(tpl_dir), "--format", "tpl",
        "Write-Text-Archives", str(out), "--format", "rom",
    ]
    subprocess.run(build, cwd=ROOT, check=True)

    verify = [
        "python", str(ROOT / "tools" / "compare_archive_payloads.py"),
        "--rom-a", str(rom), "--tpi-a", str(tpi), "--rom-b", str(out),
        "--output", str(report), "--label", "exe45-nochange-roundtrip",
    ]
    subprocess.run(verify, cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
