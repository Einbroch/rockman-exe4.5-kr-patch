#!/usr/bin/env python3
"""Bind manually inspected PET screens, input routes and font reads to one ROM.

Completion of a capture route is not a visual pass. Exact reviewed screenshots
and their observations live in analysis/pet_runtime_observations_v2.json.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from build_visibility_poc import ROOT, require_hash, sha
from korean_codec import EXTRA_CHARACTER_INDICES, HANGUL_BASE, HANGUL_COUNT


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="poc/output/exe45_ko_development_pet_v2.json")
    ap.add_argument("--repro", default="poc/output/exe45_ko_development_pet_v2_repro.gba")
    ap.add_argument("--observations", default="analysis/pet_runtime_observations_v2.json")
    ap.add_argument("--out", default="analysis/exe45_pet_ko_runtime.json")
    args = ap.parse_args()
    out = ROOT / args.out
    check(not out.exists(), "refusing to overwrite runtime report")
    manifest_path, observed_path = ROOT / args.manifest, ROOT / args.observations
    manifest, observed = read(manifest_path), read(observed_path)
    config = read(ROOT / "project.json")
    build = observed["build_sha256"]
    check(manifest["output_sha256"] == build, "observations belong to another build")
    check(manifest["source_sha256"] == observed["source_sha256"] == config["source_profile"]["sha256"],
          "source revision mismatch")
    require_hash(ROOT / config["source_profile"]["filename"], manifest["source_sha256"])
    require_hash(manifest_path.with_suffix(".gba"), build)
    require_hash(ROOT / args.repro, build)
    check(manifest["translated_units"] == 49 and manifest["unchanged_archives"] == 730,
          "development scope changed")
    assets = {}
    for asset in manifest["translation_assets"]:
        require_hash(ROOT / asset["path"], asset["sha256"])
        assets[asset["archive"]] = read(ROOT / asset["path"])
    codec_path = ROOT / "analysis/exe45_korean_codec_roundtrip_v3.json"
    codec = read(codec_path)
    check(codec["status"] == "pass" and codec["source_sha256"] == manifest["source_sha256"],
          "codec report source/status mismatch")
    check(codec["plugin"]["derived_plugin_sha256"] == manifest["plugin"]["derived_plugin_sha256"],
          "codec and candidate plugins differ")
    check(codec["native_payload_identical"] == 732 and codec["repertoire"]["total_characters"] == 11173,
          "codec denominator changed")

    # Result-file hashes are pinned by the reviewed observation record. Validate
    # every artifact, then validate each continuation's same-ROM parent chain.
    results, evidence = {}, []
    emulator_sha = config["development_dependencies"]["runtime_capture"]["mesen_sha256"]
    for item in observed["results"]:
        path = ROOT / item["path"]
        require_hash(path, item["sha256"])
        result = read(path)
        check(result["complete"] and result["return_code"] == 0
              and result["steps_captured"] == result["steps_expected"], "incomplete capture route")
        check(result["rom_sha256"] == item["rom_sha256"] and item["rom_sha256"] in (build, manifest["source_sha256"]),
              "runtime ROM mismatch")
        check(result["emulator_sha256"] == emulator_sha, "runtime emulator mismatch")
        for name, digest in result["artifacts"].items():
            require_hash(path.parent / name, digest)
        results[path.resolve()] = result
        evidence.append({**item, "scope": result["scope"], "actions": result["actions"],
                         "captures": result["steps_captured"], "audio_enabled": result["audio_enabled"]})
    for path, result in results.items():
        if result["state_origin"] is None:
            check(result["state_sha256"] is None, "unbound initial state")
            continue
        parent_path = Path(result["state_origin"]).resolve()
        check(parent_path in results, "unreviewed continuation parent")
        parent = results[parent_path]
        check(parent["rom_sha256"] == result["rom_sha256"], "cross-ROM continuation")
        check(parent["artifacts"]["checkpoint.mss"] == result["state_sha256"], "continuation state differs")
        require_hash(path.parent / "input.mss", result["state_sha256"])
    for shot in observed["screenshots"]:
        path = ROOT / shot["path"]
        result = results[(path.parent / "result.json").resolve()]
        check(result["artifacts"][path.name] == shot["sha256"], "reviewed screenshot not in pinned result")
        require_hash(path, shot["sha256"])

    # Font reads support the inspected visible words; they do not substitute for
    # the screenshots or prove all duplicate script instances were executed.
    wording_by_id = {w["id"]: w for w in assets["65A608"]["wordings"]}
    check(set(observed["pet_wordings_observed"]) | set(observed["pet_wordings_runtime_open"]) == set(wording_by_id),
          "PET wording coverage partition changed")
    check(not set(observed["pet_wordings_observed"]) & set(observed["pet_wordings_runtime_open"]),
          "ambiguous wording coverage status")
    intro = next(u["translation"] for u in assets["65A578"]["units"] if u["id"] == "65A578:1:0")
    visible = intro + "".join(wording_by_id[key]["translation"] for key in observed["pet_wordings_observed"])
    needed = {ch for ch in visible if HANGUL_BASE <= ord(ch) < HANGUL_BASE + HANGUL_COUNT or ch in EXTRA_CHARACTER_INDICES}
    reads, sites = Counter(), Counter()
    base = 0x08000000 + manifest["extension"]["normal_font_offset"]
    for name in ("pet-ko-v2-cold", "pet-ko-v2-prompts-settled"):
        directory = ROOT / "poc/runtime" / name
        result = results[(directory / "result.json").resolve()]
        check(result["rom_sha256"] == build and result["probe"] == "fontread"
              and int(result["font_base"], 16) == base and result["font_stride"] == 96, "font probe differs")
        trace = read(directory / "fontread_final.json")
        reads.update({r["index"]: r["reads"] for r in trace["records"]})
        sites.update({r["pc"]: r["reads"] for r in trace["sites"]})
    consumed = []
    for ch in sorted(needed):
        index = EXTRA_CHARACTER_INDICES[ch] if ch in EXTRA_CHARACTER_INDICES else ord(ch) - HANGUL_BASE
        record = index + manifest["extension"]["legacy_index_view"]
        check(reads[record] >= 24, f"missing full-record consumption for {ch}")
        consumed.append({"character": ch, "record_index": record, "reads": reads[record]})
    report = {
        "schema": 1, "status": "selected-PET-scenes-runtime-pass; branch-coverage-incomplete",
        "policy": "development-draft; NON-DISTRIBUTION", "build_sha256": build,
        "source_sha256": manifest["source_sha256"], "manifest": args.manifest,
        "manifest_sha256": sha(manifest_path.read_bytes()), "reproducible_rom_sha256": True,
        "observations": args.observations, "observations_sha256": sha(observed_path.read_bytes()),
        "codec_report": str(codec_path.relative_to(ROOT)), "codec_report_sha256": sha(codec_path.read_bytes()),
        "translated_units_byte_verified": 49, "pet_units_byte_verified": 45,
        "pet_wordings_observed": observed["pet_wordings_observed"],
        "pet_wordings_runtime_open": observed["pet_wordings_runtime_open"],
        "font_glyphs_consumed": consumed, "font_read_sites": dict(sites),
        "evidence": evidence, "inspected_screenshots": observed["screenshots"],
        "input_boundary": "First immediate right input after diagnostic state load was ignored in both source and candidate. A neutral 61-frame segment precedes inputs in the passing route; no game-code repair was made for this test-harness boundary.",
        "limits": observed["limits"] + ["Translation wording still needs human review; not a release candidate."],
    }
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {len(observed['screenshots'])} inspected captures; {len(consumed)} glyph records; exact ROM reproduction")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
