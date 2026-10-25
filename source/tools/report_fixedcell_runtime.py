#!/usr/bin/env python3
"""Bind native 8x16 consumer evidence and the temporary visibility experiment.

Checks exact retained artifacts; does not execute an emulator or approve a
font's style. The production development ROM remains the save-v1 artifact.
"""
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

from PIL import Image

from build_visibility_poc import ROOT, require_hash, sha
from compare_archive_payloads import payload_of
from fixedcell_font import bdf_cells, unpack_pixels
from verify_tpi_index import parse_tpi


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_route(path: Path, expected: str, seen: set[Path]) -> dict:
    result = read(path / "result.json")
    if not result["complete"] or result["rom_sha256"] != expected or result["steps_expected"] != result["steps_captured"]:
        raise ValueError("wrong/incomplete route")
    if path not in seen:
        for name, digest in result["artifacts"].items():
            require_hash(path / name, digest)
        seen.add(path)
        if result["state_origin"]:
            origin = Path(result["state_origin"]).parent
            previous = verify_route(origin, expected, seen)
            if result["state_sha256"] != previous["artifacts"]["checkpoint.mss"]:
                raise ValueError("checkpoint edge identity mismatch")
    return result


def transfer_evidence(directory: Path, step: int, rom: bytes) -> list[dict]:
    prefix = f"step_{step:03d}"
    vram = (directory / f"{prefix}_gbaVideoRam.bin").read_bytes()
    calls = read(directory / f"{prefix}_fixedcells.json")["calls"]
    records = []
    for call in calls:
        if not call["complete"] or call["tint"] != 0:
            raise ValueError("unresolved copy state/tint")
        if call["bytes"] != call["width"] * call["height"] * 64 or len(call["glyphs"]) * 64 != call["bytes"]:
            raise ValueError("fixed-cell count/clear extent mismatch")
        original = bytearray()
        for i, glyph in enumerate(call["glyphs"]):
            if glyph["destination"] != call["stage"] + i * 64:
                raise ValueError("non-contiguous fixed-cell stage")
            offset = glyph["font"] - 0x08000000 + glyph["index"] * 64
            if not 0 <= offset <= len(rom) - 64:
                raise ValueError("font read outside ROM")
            original.extend(rom[offset:offset + 64])
        staged = (directory / f"fixed_{call['id']:04d}_stage.bin").read_bytes()
        target = call["copy_target"] - 0x06000000
        if (bytes(original) != staged or vram[target:target + call["bytes"]] != staged
                or call["copy_source"] != call["stage"] or call["copy_target"] != call["target"]):
            raise ValueError("ROM -> stage -> VRAM link failed")
        records.append({k: call[k] for k in ("id", "stream", "stage", "target", "width", "height", "font", "bytes")})
    return records


def visible_cells(directory: Path, step: int, glyphs: dict[str, bytes]) -> list[dict]:
    prefix = f"step_{step:03d}"
    vram = (directory / f"{prefix}_gbaVideoRam.bin").read_bytes()
    io = (directory / f"{prefix}_display_io.bin").read_bytes()
    state = read(directory / f"{prefix}_state.json")["state"]
    screenshot = Image.open(directory / f"{prefix}.png").convert("RGB")
    evidence = []
    for label, layer, x, y, bank in (("category", 0, 12, 2, 12), ("chip-name", 1, 17, 4, 14)):
        control = struct.unpack_from("<H", io, 8 + layer * 2)[0]
        if control & 0xC080 or any(state[f"ppu.bgLayers[{layer}].scroll{axis}"] for axis in ("X", "Y")):
            raise ValueError("8x16 observation requires unscrolled 32x32 4-bpp background")
        char_base = ((control >> 2) & 3) * 0x4000
        screen_base = ((control >> 8) & 31) * 0x800
        for j, char in enumerate("한글"):
            entries = [struct.unpack_from("<H", vram, screen_base + (y + dy) * 64 + (x + j) * 2)[0] for dy in (0, 1)]
            if any(entry & 0xC00 or entry >> 12 != bank for entry in entries):
                raise ValueError("unexpected tile flip or palette bank")
            rendered = b"".join(vram[char_base + (entry & 1023) * 32:char_base + (entry & 1023) * 32 + 32] for entry in entries)
            if rendered != glyphs[char]:
                raise ValueError("tilemap does not consume intended top/bottom glyph tiles")
            pixels = unpack_pixels(rendered)
            colors = {}
            for role in (1, 2):
                expected = {(px, py) for py, row in enumerate(pixels) for px, value in enumerate(row) if value == role}
                observed_colors = {screenshot.getpixel(((x + j) * 8 + px, y * 8 + py)) for px, py in expected}
                if len(observed_colors) != 1:
                    raise ValueError("visible ink/shadow pixels disagree")
                color = next(iter(observed_colors))
                actual = {(px, py) for py in range(16) for px in range(8)
                          if screenshot.getpixel(((x + j) * 8 + px, y * 8 + py)) == color}
                if actual != expected:
                    raise ValueError("screenshot glyph mask differs from selected bitmap")
                colors[role] = list(color)
            if colors[1] == colors[2]:
                raise ValueError("ink and shadow lost distinction")
            evidence.append({"label": label, "character": char, "screen_xy": [(x + j) * 8, y * 8],
                             "bg": layer, "tile_entries": entries, "palette_bank": bank,
                             "glyph_sha256": sha(rendered), "screenshot_masks_match": True, "observed_colors": colors})
    return evidence


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="analysis/exe45_fixedcell_visibility_runtime.json")
    args = ap.parse_args()
    out = ROOT / args.out
    if out.exists():
        raise ValueError("refusing to overwrite evidence report")
    ledger_path = ROOT / "analysis/fixedcell_runtime_observations_v1.json"
    ledger = read(ledger_path)
    manifest = read(ROOT / "poc/output/exe45_fixedcell_visibility_v1.json")
    native_path = ROOT / "poc/output/exe45_ko_development_save_v1.gba"
    candidate_path = ROOT / "poc/output/exe45_fixedcell_visibility_v1.gba"
    source_profile = read(ROOT / "project.json")["source_profile"]
    source_path = ROOT / source_profile["filename"]
    require_hash(source_path, source_profile["sha256"])
    source = source_path.read_bytes()
    for path, digest in ((native_path, ledger["native_build_sha256"]), (candidate_path, ledger["candidate_build_sha256"]),
                         (ROOT / "poc/output/exe45_fixedcell_visibility_v1_repro.gba", ledger["candidate_build_sha256"]),
                         (ROOT / "poc/output/exe45_save_fixedcell_default_regression.gba", ledger["native_build_sha256"])):
        require_hash(path, digest)
    if manifest["policy"] != ledger["policy"] or manifest["output_sha256"] != ledger["candidate_build_sha256"]:
        raise ValueError("visibility policy/build binding failed")
    visibility = manifest["fixedcell_visibility"]
    spec_path = ROOT / visibility["spec_path"]
    require_hash(spec_path, visibility["spec_sha256"])
    spec = read(spec_path)
    for key, hash_key in (("path", "sha256"), ("license", "license_sha256")):
        require_hash(ROOT / spec["font"][key], spec["font"][hash_key])
    cells = bdf_cells(ROOT / spec["font"]["path"], {chr(i) for i in range(0xAC00, 0xD7A4)}, spec["raster"])
    native, candidate = native_path.read_bytes(), candidate_path.read_bytes()
    allowed = {r["rom_offset"] + i for r in visibility["replacements"] for i in range(64)}
    if len(native) != len(candidate) or any(a != b and i not in allowed for i, (a, b) in enumerate(zip(native, candidate))):
        raise ValueError("diagnostic changes outside the four declared glyph slots")
    for row in visibility["replacements"]:
        if candidate[row["rom_offset"]:row["rom_offset"] + 64] != cells[row["display"]]:
            raise ValueError("candidate glyph supply changed")
    verified, routes, observations = set(), [], 0
    for route in ledger["routes"]:
        directory = ROOT / route["directory"]
        require_hash(directory / "result.json", route["result_sha256"])
        require_hash(directory / "probe_environment.json", route["environment_sha256"])
        expected = ledger["native_build_sha256"] if directory.name.startswith("fixedcell-save-") else ledger["candidate_build_sha256"]
        result = verify_route(directory, expected, verified)
        environment = read(directory / "probe_environment.json")
        require_hash(ROOT / "tools/capture_fixedcell_probe.py", environment["probe_sha256"])
        for name, before in environment["files_before"].items():
            if name.endswith(".sav") and environment["files_after"].get(name) != before:
                raise ValueError("an existing isolated save changed during non-save font QA")
        for item in route["observations"]:
            if item["status"] not in ("pass", "reference", "not_reached"):
                raise ValueError("unknown observation status")
            require_hash(directory / f"step_{item['step']:03d}.png", item["screenshot_sha256"])
            observations += 1
        routes.append({"directory": route["directory"], "result_sha256": route["result_sha256"],
                       "actions": result["actions"], "scope": result["scope"]})
    cold = read(ROOT / "poc/runtime/fixedcell-v1-cold/result.json")
    if cold["state_origin"] is not None:
        raise ValueError("candidate initialization must cross cold boot")
    native_dir = ROOT / "poc/runtime/fixedcell-save-v1-library-idle"
    candidate_dir = ROOT / "poc/runtime/fixedcell-v1-library"
    transfers = {}
    archive = next(r for r in parse_tpi(ROOT / "external/textpet-indexes/exe45.tpi") if r["offset"] == 0x6D9EC0)
    headers = payload_of(source, archive)
    for label, directory, rom in (("native", native_dir, native), ("candidate", candidate_dir, candidate)):
        transfers[label] = transfer_evidence(directory, 7, rom)
        if len(transfers[label]) != 5:
            raise ValueError("adopted four category labels plus one description denominator changed")
        vram = (directory / "step_007_gbaVideoRam.bin").read_bytes()
        ram = (directory / "step_007_gbaExtWorkRam.bin").read_bytes()
        if vram[0x4000:0x6800] != rom[0x601738:0x603F38] or ram[0x24000:0x24000 + len(headers)] != headers:
            raise ValueError("font preload or compressed title archive load mismatch")
    visual = []
    for directory, steps in ((candidate_dir, (7, 9, 11)), (ROOT / "poc/runtime/fixedcell-v1-reentry-settled", (3, 8))):
        for step in steps:
            visual.append({"directory": str(directory.relative_to(ROOT)), "step": step,
                           "cells": visible_cells(directory, step, cells)})
    report = {
        "schema": 1, "status": "PASS: two-syllable visibility only; production encoding unresolved",
        "source_sha256": sha(source), "native_build_sha256": sha(native), "candidate_build_sha256": sha(candidate),
        "policy": ledger["policy"], "observations_sha256": sha(ledger_path.read_bytes()),
        "inspected_captures": observations, "routes": routes,
        "cell": spec["cell"], "candidate_font": spec["font"], "candidate_cells_fitting": len(cells),
        "candidate_font_bytes_for_all_syllables": sum(map(len, cells.values())),
        "runtime_syllables": ["한", "글"], "native_and_candidate_transfers": transfers,
        "header_archive": {"source_offset": archive["offset"], "compressed_bytes": archive["size"],
                           "payload_bytes": len(headers), "payload_sha256": sha(headers), "ram_address": 0x02024000},
        "preloaded_font_window": {"rom_offset": 0x601738, "vram_address": 0x06004000, "bytes": 0x2800,
                                  "records": 160, "limit": "observed resident window, NOT a proven total-font capacity"},
        "screen_links": visual, "exact_rebuild": True, "default_build_unchanged": True,
        "limits": ledger["limitations"],
        "next": "Preserve native slots. Trace chip-name tile-index parser, then design extended decoding and state-local glyph placement; separately expand fixed-cell F9 decoder and compressed header archive."
    }
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {observations} inspected captures; five native/candidate transfers; two BG pixel-mask paths; {len(cells)} static glyph cells")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
