#!/usr/bin/env python3
"""Run save QA in an explicitly isolated Mesen environment, recording disk state.

Controller actions are a test plan, not an automatic semantic pass. Save RAM is
never edited or imported by this tool. Existing user-emulator saves are outside
the allowed test-directory scope.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from build_visibility_poc import ROOT, require_hash, sha
from capture_pet_menu_qa import route


def inventory(directory: Path) -> dict:
    return {p.name: {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())}
            for p in sorted(directory.glob("*")) if p.is_file()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="poc/output/exe45_ko_development_save_v1.json")
    ap.add_argument("--mesen", default="poc/runtime/isolated-mesen-save-v1/Mesen.exe")
    ap.add_argument("--save-dir", default="poc/runtime/save-v1-persistence")
    ap.add_argument("--origin")
    ap.add_argument("--mode", choices=("enter", "commit", "custom"), required=True)
    ap.add_argument("--actions", help="explicit custom controller sequence")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    manifest_path, emulator, save_dir, out = [ROOT / value for value in (args.manifest, args.mesen, args.save_dir, args.out)]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    settings_path = emulator.parent / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8-sig"))["Preferences"]
    safe_root = (ROOT / "poc/runtime").resolve()
    for path in (emulator.resolve(), save_dir.resolve()):
        if not path.is_relative_to(safe_root) or path == safe_root:
            raise ValueError("save QA requires a project-local isolated environment")
    if not settings["OverrideSaveDataFolder"] or Path(settings["SaveDataFolder"]).resolve() != save_dir.resolve():
        raise ValueError("emulator save path is not the declared isolated test folder")
    if out.exists():
        raise ValueError("refusing to overwrite a QA route")
    dependencies = config["development_dependencies"]["runtime_capture"]
    require_hash(emulator, dependencies["mesen_sha256"])
    require_hash(ROOT / dependencies["tool"], dependencies["tool_sha256"])
    require_hash(manifest_path.with_suffix(".gba"), manifest["output_sha256"])
    bios = emulator.parent / "Firmware/gba_bios.bin"
    require_hash(bios, "fd2547724b505f487e6dcb29ec2ecff3af35a841a77ab2e85fd87350abd36570")
    if args.mode == "enter":
        if not args.origin or args.actions:
            raise ValueError("enter requires a tournament-prompt origin and no custom actions")
        actions = ",".join(f"{key}:{held}:{wait}" for key, held, wait, _ in route("save")[:-1])
    elif args.mode == "commit":
        if not args.origin or args.actions:
            raise ValueError("commit requires a fresh-save-confirmation origin")
        actions = "none:1:60,a:1:0,none:1:0,none:1:0,none:1:0,none:1:0,none:1:600,a:2:90"
    else:
        if not args.actions:
            raise ValueError("custom requires an explicit action sequence")
        actions = args.actions
    base = 0x08000000 + manifest["extension"]["normal_font_offset"]
    end = base + (manifest["extension"]["legacy_index_view"] + 11172 + manifest["extension"]["extra_glyph_count"]) * 96
    before = inventory(save_dir)
    command = [sys.executable, "-X", "utf8", str(ROOT / dependencies["tool"]),
               "--rom", str(manifest_path.with_suffix(".gba")), "--expect-rom-sha256", manifest["output_sha256"],
               "--mesen", str(emulator), "--out", str(out), "--actions", actions,
               "--probe", "fontread", "--font-base", str(base), "--font-end", str(end), "--font-stride", "96", "--timeout", "180"]
    if args.origin:
        origin = ROOT / args.origin
        command.extend(["--state", str(origin / "checkpoint.mss"), "--state-origin", str(origin / "result.json")])
    completed = subprocess.run(command, cwd=ROOT)
    after = inventory(save_dir)
    if out.exists():
        (out / "save_environment.json").write_text(json.dumps({
            "policy": "isolated test saves only; controller input and validated same-ROM checkpoints; no save RAM editing",
            "build_sha256": manifest["output_sha256"], "mode": args.mode, "actions": actions,
            "save_directory": str(save_dir.resolve()), "files_before": before, "files_after": after,
            "settings_sha256": sha(settings_path.read_bytes()), "bios_sha256": sha(bios.read_bytes()),
            "runner_sha256": dependencies["tool_sha256"], "emulator_sha256": dependencies["mesen_sha256"],
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        snapshots = out / "persistent_files_after"
        snapshots.mkdir()
        for name in after:
            (snapshots / name).write_bytes((save_dir / name).read_bytes())
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
