#!/usr/bin/env python3
"""Verify exact reviewed save captures and the disk-save -> cold-boot edge."""

import argparse
import json
from collections import Counter
from pathlib import Path

from build_visibility_poc import ROOT, require_hash, sha
from archive_scripts import verify_untouched_scripts
from korean_codec import HANGUL_BASE, HANGUL_COUNT


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check(value, message):
    if not value:
        raise ValueError(message)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--observations", default="analysis/save_runtime_observations_v1.json")
    ap.add_argument("--out", default="analysis/exe45_save_ko_runtime.json")
    args = ap.parse_args()
    out, observation_path = ROOT / args.out, ROOT / args.observations
    check(not out.exists(), "refusing to overwrite evidence")
    observed = read(observation_path)
    manifest_path = ROOT / observed["manifest"]
    manifest = read(manifest_path)
    config = read(ROOT / "project.json")
    build = observed["build_sha256"]
    check(manifest["output_sha256"] == build, "wrong observed build")
    source_path = ROOT / config["source_profile"]["filename"]
    require_hash(source_path, manifest["source_sha256"])
    require_hash(manifest_path.with_suffix(".gba"), build)
    require_hash(ROOT / observed["reproduction"], build)
    assets = {}
    for item in manifest["translation_assets"]:
        require_hash(ROOT / item["path"], item["sha256"])
        assets[item["archive"]] = read(ROOT / item["path"])
    check(manifest["translated_units"] == 65 and manifest["unchanged_archives"] == 729, "scope mismatch")
    archive = next(a for a in manifest["archives"] if a["archive"] == "6DA21C")
    source, target = source_path.read_bytes(), manifest_path.with_suffix(".gba").read_bytes()
    protected = verify_untouched_scripts(source[0x6DA21C:0x6DA21C + 9008],
        target[archive["rom_offset"]:archive["rom_offset"] + archive["compiled_bytes"]], 120, {0, 1, 2, 3, 4})
    check(protected == archive["unselected_script_bytes_preserved"], "unselected script evidence differs")

    results, environments = {}, {}
    for item in observed["results"]:
        path = ROOT / item["path"]
        require_hash(path, item["sha256"])
        result = read(path)
        check(result["complete"] and result["return_code"] == 0 and result["rom_sha256"] == build
              and result["steps_expected"] == result["steps_captured"], "incomplete or foreign route")
        check(result["emulator_sha256"] == config["development_dependencies"]["runtime_capture"]["mesen_sha256"],
              "emulator differs")
        for name, digest in result["artifacts"].items():
            require_hash(path.parent / name, digest)
        results[path.resolve()] = result
        if "save_environment_sha256" in item:
            environment_path = path.parent / "save_environment.json"
            require_hash(environment_path, item["save_environment_sha256"])
            environment = read(environment_path)
            check(environment["build_sha256"] == build, "foreign save environment")
            for name, record in environment["files_after"].items():
                require_hash(path.parent / "persistent_files_after" / name, record["sha256"])
            environments[path.parent.name] = environment
    for path, result in results.items():
        if result["state_origin"] is not None:
            parent_path = Path(result["state_origin"]).resolve()
            check(parent_path in results, "unbound continuation")
            check(results[parent_path]["artifacts"]["checkpoint.mss"] == result["state_sha256"], "wrong continuation state")
            require_hash(path.parent / "input.mss", result["state_sha256"])
    for shot in observed["screenshots"]:
        path = ROOT / shot["path"]
        check(results[(path.parent / "result.json").resolve()]["artifacts"][path.name] == shot["sha256"],
              "capture not in reviewed route")
        require_hash(path, shot["sha256"])

    save_name = manifest_path.with_suffix(".sav").name
    def saved(route, when):
        return environments[route]["files_" + when][save_name]["sha256"]
    check(saved("save-v1-overwrite-cancel", "before") == saved("save-v1-overwrite-cancel", "after"),
          "No modified saved progress")
    check(saved("save-v1-overwrite-accept", "before") != saved("save-v1-overwrite-accept", "after"),
          "overwrite did not write a new save")
    reboot = (ROOT / "poc/runtime/save-v1-overwrite-reboot/result.json").resolve()
    check(results[reboot]["state_origin"] is None, "reboot used a diagnostic checkpoint")
    check(saved("save-v1-overwrite-accept", "after") == saved("save-v1-overwrite-reboot", "before")
          == saved("save-v1-overwrite-reboot", "after"), "disk save / cold boot identity mismatch")

    wordings = {w["id"]: w for w in assets["6DA21C"]["wordings"]}
    check(set(observed["save_wordings_observed"]) | set(observed["save_wordings_open"]) == set(wordings), "wording denominator")
    needed = {ch for key in observed["save_wordings_observed"] for ch in wordings[key]["translation"]
              if HANGUL_BASE <= ord(ch) < HANGUL_BASE + HANGUL_COUNT}
    reads = Counter()
    base = 0x08000000 + manifest["extension"]["normal_font_offset"]
    for path, result in results.items():
        if result["probe"] == "fontread":
            check(int(result["font_base"], 16) == base and result["font_stride"] == 96, "font probe differs")
            reads.update({r["index"]: r["reads"] for r in read(path.parent / "fontread_final.json")["records"]})
    glyphs = []
    for ch in sorted(needed):
        index = ord(ch) - HANGUL_BASE + manifest["extension"]["legacy_index_view"]
        check(reads[index] >= 24, f"missing visible save glyph {ch}")
        glyphs.append({"character": ch, "record_index": index, "reads": reads[index]})
    report = {"schema": 1, "status": "save-confirm-overwrite-persistence-runtime-pass; error-branches-open",
        "policy": "development-draft; NON-DISTRIBUTION", "build_sha256": build,
        "manifest": observed["manifest"], "manifest_sha256": sha(manifest_path.read_bytes()),
        "observations": args.observations, "observations_sha256": sha(observation_path.read_bytes()),
        "source_sha256": manifest["source_sha256"], "reproduction_verified": True,
        "translated_units_byte_verified": 65, "unselected_save_scripts_byte_identical": len(protected),
        "save_hangul_glyphs_consumed": glyphs,
        "save_wordings_observed": observed["save_wordings_observed"], "save_wordings_open": observed["save_wordings_open"],
        "disk_save": {"filename": save_name, "overwrite_sha256": saved("save-v1-overwrite-accept", "after"),
                      "cold_boot_without_checkpoint": True, "cancel_preserved_saved_progress": True},
        "inspected_screenshots": observed["screenshots"], "results": observed["results"],
        "diagnostics": observed["diagnostics"], "limits": observed["limits"]}
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {len(observed['screenshots'])} inspected captures; {len(glyphs)} save glyphs; disk-save/cold-boot edge")


if __name__ == "__main__":
    main()
