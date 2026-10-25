#!/usr/bin/env python3
"""Replay explicit PET interaction routes from a same-build tournament prompt.

These are input/observation plans, not an assertion that a captured screen
matches its expectation. Visual and behavioral review is recorded separately.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from build_visibility_poc import ROOT, require_hash


MENUS = ("tournament", "jack_in", "equipment", "library", "mail", "communication", "save")


def route(mode: str) -> list[tuple[str, int, int, str]]:
    # Savestate restore is scheduled on an execution callback; let input polling
    # resume before the first edge. This is controller timing, not a ROM fix.
    settle = [("none", 1, 60, "resume normal input polling after state load")]
    if mode == "prompts":
        steps = settle + [("right", 2, 30, "tournament: focus No"), ("a", 2, 90, "tournament: No returns to idle"),
                 ("a", 2, 60, "tournament: reopen confirmation"), ("b", 2, 90, "tournament: B cancels")]
        for menu in MENUS[1:]:
            steps.extend([("down", 2, 60, f"{menu}: focus menu item"),
                          ("a", 2, 60, f"{menu}: Korean confirmation with Yes focused"),
                          ("right", 2, 30, f"{menu}: focus No"),
                          ("a", 2, 90, f"{menu}: No returns to idle")])
        return steps
    if mode not in MENUS:
        raise ValueError("unknown PET QA route")
    steps = settle + [("b", 2, 90, "cancel initial tournament prompt")]
    steps.extend(("down", 2, 60, f"move to menu index {i + 1}") for i in range(MENUS.index(mode)))
    steps.extend([("a", 2, 60, f"{mode}: Korean confirmation"), ("a", 2, 180, f"{mode}: accept Yes"),
                  ("none", 1, 180, f"{mode}: resulting screen"), ("b", 2, 150, f"{mode}: Back/cancel where supported")])
    return steps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="poc/output/exe45_ko_development_pet_v2.json")
    ap.add_argument("--origin", default="poc/runtime/pet-ko-v2-cold")
    ap.add_argument("--mode", choices=("prompts",) + MENUS, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mesen", required=True)
    args = ap.parse_args()
    manifest_path, origin, out = ROOT / args.manifest, ROOT / args.origin, ROOT / args.out
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    deps = config["development_dependencies"]["runtime_capture"]
    require_hash(ROOT / deps["tool"], deps["tool_sha256"])
    require_hash(Path(args.mesen), deps["mesen_sha256"])
    require_hash(manifest_path.with_suffix(".gba"), manifest["output_sha256"])
    steps = route(args.mode)
    base = 0x08000000 + manifest["extension"]["normal_font_offset"]
    end = base + (442 + 11172 + manifest["extension"]["extra_glyph_count"]) * 96
    command = [sys.executable, "-X", "utf8", str(ROOT / deps["tool"]), "--rom", str(manifest_path.with_suffix(".gba")),
               "--mesen", args.mesen, "--out", str(out), "--expect-rom-sha256", manifest["output_sha256"],
               "--state", str(origin / "checkpoint.mss"), "--state-origin", str(origin / "result.json"),
               "--actions", ",".join(f"{key}:{held}:{wait}" for key, held, wait, _ in steps),
               "--probe", "fontread", "--font-base", str(base), "--font-end", str(end), "--font-stride", "96", "--timeout", "120"]
    subprocess.run(command, check=True, cwd=ROOT)
    plan = {"policy": "expected observations only; inspect images before claiming pass", "mode": args.mode,
            "manifest": str(manifest_path.relative_to(ROOT)), "build_sha256": manifest["output_sha256"],
            "steps": [{"step": i, "input": f"{key}:{held}:{wait}", "expected": note,
                       "screenshot": f"step_{i:03d}.png"} for i, (key, held, wait, note) in enumerate(steps, 1)]}
    (out / "route_expectations.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
