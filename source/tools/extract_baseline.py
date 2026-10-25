#!/usr/bin/env python3
"""Extract the fixed EXE4.5 source profile with pinned TextPet inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as src:
        for block in iter(lambda: src.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_hash(path: Path, expected: str, algorithm: str = "sha256") -> None:
    actual = digest(path, algorithm)
    if actual.lower() != expected.lower():
        raise SystemExit(f"{path}: {algorithm} mismatch: {actual}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=None)
    ap.add_argument("--tpl-out", default="analysis/tpl_baseline")
    ap.add_argument("--txt-out", default="analysis/txt_baseline")
    args = ap.parse_args()

    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    profile = config["source_profile"]
    rom = Path(args.rom) if args.rom else ROOT / profile["filename"]
    if not rom.is_absolute():
        rom = ROOT / rom
    if rom.stat().st_size != profile["size"]:
        raise SystemExit(f"{rom}: size mismatch")
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

    tpl_out = ROOT / args.tpl_out
    txt_out = ROOT / args.txt_out
    for out in (tpl_out, txt_out):
        if out.exists() and any(out.iterdir()):
            raise SystemExit(f"refusing to overwrite non-empty extraction: {out}")
        out.mkdir(parents=True, exist_ok=True)

    command = [
        str(textpet), "Load-Plugins", str(ROOT / config["textpet"]["plugins"]),
        "Game", config["textpet"]["game"], "Load-File-Index", str(tpi),
        "Read-Text-Archives", str(rom),
        "Write-Text-Archives", str(tpl_out), "--format", "tpl",
        "Write-Text-Archives", str(txt_out), "--format", "txt",
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    tpl_count = len(list(tpl_out.glob("*.tpl")))
    txt_count = len(list(txt_out.glob("*.txt")))
    if tpl_count != 732 or txt_count != 732:
        raise SystemExit(f"unexpected archive count: tpl={tpl_count}, txt={txt_count}")
    print(f"extracted {tpl_count} TPL and {txt_count} text archives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
