#!/usr/bin/env python3
"""Bind inspected introduction captures and font consumption to an exact build.

The image notes below apply to the inspected v2 route, not arbitrary captures.
This records developer runtime QA, never human wording approval.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from build_visibility_poc import ROOT, require_hash, sha


VERIFIED_BUILD = "a1b3078664809acfd001b3e293cc5b24d3aa6d722dc9d8968af15a122c9811fa"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="poc/output/exe45_ko_development_intro_v2.json")
    ap.add_argument("--first", default="poc/runtime/intro-ko-v2-first")
    ap.add_argument("--advance", default="poc/runtime/intro-ko-v2-advance")
    ap.add_argument("--repro", default="poc/output/exe45_ko_development_intro_v2_repro.gba")
    ap.add_argument("--out", default="analysis/exe45_intro_ko_runtime.json")
    args = ap.parse_args()
    manifest_path = ROOT / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["output_sha256"] != VERIFIED_BUILD:
        raise SystemExit("visual observations need re-review for this build")
    require_hash(manifest_path.with_suffix(".gba"), VERIFIED_BUILD)
    require_hash(ROOT / args.repro, VERIFIED_BUILD)
    translation = ROOT / manifest["translation_path"]
    require_hash(translation, manifest["translation_sha256"])
    wording = json.loads(translation.read_text(encoding="utf-8"))
    first, advance = ROOT / args.first, ROOT / args.advance
    evidence = {}
    for directory in (first, advance):
        result_path = directory / "result.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if not result["complete"] or result["rom_sha256"] != VERIFIED_BUILD:
            raise SystemExit("incomplete or wrong-build runtime")
        for name, expected in result["artifacts"].items():
            require_hash(directory / name, expected)
        evidence[str(directory.relative_to(ROOT))] = {
            "result_sha256": sha(result_path.read_bytes()), "scope": result["scope"],
            "actions": result["actions"], "captures": result["steps_captured"],
            "emulator_sha256": result["emulator_sha256"],
        }
    first_result = json.loads((first / "result.json").read_text(encoding="utf-8"))
    next_result = json.loads((advance / "result.json").read_text(encoding="utf-8"))
    if first_result["state_origin"] is not None or next_result["state_sha256"] != sha((first / "checkpoint.mss").read_bytes()):
        raise SystemExit("runtime route does not form a cold-boot continuation chain")
    reads = json.loads((first / "fontread_final.json").read_text(encoding="utf-8"))
    records = {x["index"]: x for x in reads["records"]}
    unit = next(u for u in wording["units"] if u["id"] == "65A578:1:0")
    needed = Counter(ch for ch in unit["translation"] if 0xAC00 <= ord(ch) <= 0xD7A3)
    glyphs = []
    for ch, count in sorted(needed.items()):
        index = ord(ch) - 0xAC00 + manifest["extension"]["legacy_index_view"]
        record = records.get(index)
        if record is None or record["reads"] < 24 * count:
            raise SystemExit(f"missing glyph consumption: {ch}")
        glyphs.append({"character": ch, "index": index, "occurrences": count, **record})
    inspected = {
        first / "step_045.png": "All three Korean introduction lines visible inside the original box; no clipped glyphs observed.",
        advance / "step_001.png": "A advances to the next Japanese greeting; Korean text is cleared.",
        advance / "step_003.png": "Subsequent Japanese page remains readable after multiple key waits.",
        advance / "step_008.png": "PET tournament confirmation and yes/no selector remain visible after the introduction.",
    }
    report = {
        "schema": 1, "status": "first-introduction-runtime-pass", "policy": "development; NON-DISTRIBUTION",
        "build_sha256": VERIFIED_BUILD, "source_sha256": manifest["source_sha256"],
        "manifest": str(manifest_path.relative_to(ROOT)), "manifest_sha256": sha(manifest_path.read_bytes()),
        "translation_sha256": manifest["translation_sha256"], "reproducible_rom_sha256": True,
        "tested_unit": unit["id"], "hangul_glyphs_consumed": glyphs, "font_read_sites": reads["sites"],
        "evidence": evidence,
        "inspected_screenshots": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p.read_bytes()), "observation": note}
                                  for p, note in inspected.items()],
        "runtime_asset_chain": {
            "storage": "276-byte archive at ROM 0x800000; catalog pointer 0x38098 updated",
            "selection": "new game -> Rockman installation -> original script 1 selection",
            "lookup": "F9 FC dispatch resolves U+AC00 syllable index plus legacy bias 442",
            "font": {"rom_offset": manifest["extension"]["normal_font_offset"], "record_bytes": 96},
            "residency": "direct Game Pak ROM font reads; existing renderer/copy path retained",
            "consumer": "IWRAM renderer font reads at reported pipeline PCs 0x03006B32/0x03006B34",
            "lifetime": "cold-boot entry, complete three-line page, key wait, clear, subsequent native pages",
        },
        "limits": ["script 2 reunion is byte-verified but has no runtime route yet",
                   "menu/battle/fixed-width/name input renderers not localized",
                   "no full-font runtime or full-game coverage claim", "wording needs human review"],
    }
    out = ROOT / args.out
    if out.exists():
        raise SystemExit("refusing to overwrite runtime report")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {len(glyphs)} Hangul glyphs consumed; intro/clear/advance; {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
