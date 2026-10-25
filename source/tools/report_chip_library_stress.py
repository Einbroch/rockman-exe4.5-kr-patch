#!/usr/bin/env python3
"""Recheck normal timing versus explicitly substituted 56-cell/icon fixtures."""
import argparse
from collections import Counter
import json
import statistics
import struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT, require_hash, sha
from fixedcell_font import unpack_pixels
from report_fixedcell_runtime import verify_route

BUILD = "ce839b60c8125da7ca8ce0240bcdfc82a8e8f5604202449af1acffa80158cbff"
ROUTES = {
    "timing-native": "d452b8b5c745d8e76f67cc88a1eb3cec80598ebae550099c46ba037d53da4162",
    "stress56-icons-v2": "6a3027c2813d479531b13cf06f6a55ab5b2892ee586643ce5a23310237d0537e",
    "stress56-tabs": "8b7de3e4f43770daac0d0cc72421355ad7ec6fe239f06ba9034245e33cb2c31f",
}


def read(p):
    return json.loads(p.read_text(encoding="utf-8"))


def require(value, message):
    if not value:
        raise ValueError(message)


def stats(rows):
    values = [r["cycles"] for r in rows]
    require(bool(values) and min(values) > 0, "empty/invalid timing")
    return {"count": len(values), "min": min(values), "median": statistics.median(values), "max": max(values)}


def pixel_masks(shot, glyph, sx, sy):
    pixels = unpack_pixels(glyph)
    colors = []
    for role in (1, 2):
        mask = {(x, y) for y in range(16) for x in range(8) if pixels[y][x] == role}
        colors_seen = {shot.getpixel((sx + x, sy + y)) for x, y in mask}
        require(len(colors_seen) == 1, "stress screenshot color mismatch")
        color = next(iter(colors_seen))
        actual = {(x, y) for y in range(16) for x in range(8) if shot.getpixel((sx + x, sy + y)) == color}
        require(actual == mask, "stress screenshot glyph mask mismatch")
        colors.append(color)
    require(colors[0] != colors[1], "stress ink/shadow lost contrast")


def visible(path, step, rom, font, icon_base, icon_source):
    prefix = f"step_{step:03d}"
    vram = (path / f"{prefix}_gbaVideoRam.bin").read_bytes()
    io = (path / f"{prefix}_display_io.bin").read_bytes()
    state = read(path / f"{prefix}_state.json")["state"]
    shot = Image.open(path / f"{prefix}.png").convert("RGB")
    ctrl = struct.unpack_from("<H", io, 10)[0]
    require(not ctrl & 0xC080 and ((ctrl >> 2) & 3) == 1 and all(state[f"ppu.bgLayers[1].scroll{a}"] == 0 for a in ("X", "Y")), "unsupported stress background geometry")
    mp = ((ctrl >> 8) & 31) * 0x800
    cells = []
    for row in range(7):
        for col in range(8):
            entries = [struct.unpack_from("<H", vram, mp + (4 + row * 2 + dy) * 64 + (17 + col) * 2)[0] for dy in (0, 1)]
            tile = 514 + row * 16 + col * 2
            require(entries == [0xE000 + tile, 0xE001 + tile], "stress name map mismatch")
            index = row * 8 + col
            if index == 55:
                index = 11171
            glyph = rom[font + index * 64:font + (index + 1) * 64]
            actual = vram[0x8040 + row * 512 + col * 64:0x8040 + row * 512 + (col + 1) * 64]
            require(actual == glyph, "stress cache residency mismatch")
            pixel_masks(shot, glyph, 136 + col * 8, 32 + row * 16)
            cells.append({"row": row, "column": col, "index": index, "glyph_sha256": sha(glyph)})
        native_icon = rom[icon_source - 0x08000000:icon_source - 0x08000000 + 128]
        base = icon_base + row * 128
        require(vram[base:base + 128] == native_icon, "icon residency mismatch")
        for dy in (0, 1):
            for dx in (0, 1):
                entry = struct.unpack_from("<H", vram, mp + (4 + row * 2 + dy) * 64 + (15 + dx) * 2)[0]
                require(entry == 0x4000 + (base - 0x4000) // 32 + dy * 2 + dx, "icon map does not reference its native tiles")
    return {"step": step, "screenshot_sha256": sha((path / f"{prefix}.png").read_bytes()), "visible_hangul_cells": cells, "native_icons": 7, "icon_base": icon_base}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="analysis/exe45_chip_library_stress_v1.json")
    args = ap.parse_args()
    out = ROOT / args.out
    require(not out.exists(), "refusing to overwrite evidence")
    rom_path = ROOT / "poc/output/exe45_ko_development_chip_library_v1.gba"
    require_hash(rom_path, BUILD)
    rom = rom_path.read_bytes()
    manifest = read(rom_path.with_suffix(".json"))
    font = manifest["chip_library_extension"]["font_offset"]
    seen, reports = set(), {}
    for name, digest in ROUTES.items():
        path = ROOT / "poc/runtime" / ("chip-ko-v1-" + name)
        require_hash(path / "result.json", digest)
        result = verify_route(path, BUILD, seen)
        require(result["return_code"] == 0 and not (path / "fixture_failed.txt").exists(), "runtime assertion failed")
        require(result["state_origin"] == str(ROOT / "poc/runtime/chip-ko-v1-input-lifetime/result.json"), "wrong timing comparison origin")
        env = read(path / "probe_environment.json")
        save_changes = []
        for filename, before in env["files_before"].items():
            if filename.endswith(".sav"):
                after = env["files_after"].get(filename)
                if after != before:
                    require(name == "timing-native" and filename == "exe45_ko_development_chip_library_v1.sav"
                            and before["sha256"] == "99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470"
                            and after["sha256"] == "71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063", "unexpected disk-save mutation")
                    save_changes.append({"file": filename, "before": before, "after": after,
                        "status": "isolated test save regressed after older checkpoint; NOT a save-preservation pass; restored separately from retained snapshot"})
        data = read(path / "final_timing.json")
        is_stress = name != "timing-native"
        copies_per_group = 56 if is_stress else 7
        require(all(g["rows"] == 7 and g["copies"] == copies_per_group for g in data["groups"]), "timing workload differs")
        require(len(data["copies"]) == len(data["groups"]) * copies_per_group and len(data["rows"]) == len(data["groups"]) * 7, "incomplete timing denominator")
        for item in data["groups"] + data["rows"] + data["copies"] + data["updates"]:
            require(item["cycles"] == item["end"]["clock"] - item["start"]["clock"], "clock subtraction mismatch")
        for copy in data["copies"]:
            src, dst = copy["source"] - 0x08000000 - font, copy["destination"] - 0x06008040
            require(0 <= src < 11172 * 64 and src % 64 == 0 and 0 <= dst < 3584 and dst % 64 == 0, "glyph copy out of range")
            if is_stress:
                index = dst // 64
                require(src // 64 == (11171 if index == 55 else index), "substituted byte did not select intended glyph")
        visuals = []
        if is_stress:
            require(result["normal_play_checkpoint_eligible"] is False and "checkpoint.mss" not in result["artifacts"] and "diagnostic_checkpoint.mss" in result["artifacts"], "fixture checkpoint not quarantined")
            intervention = read(path / "stress_environment.json")
            require_hash(ROOT / "tools/capture_chip_library_stress.py", intervention["tool_sha256"])
            require_hash(ROOT / "tools/capture_chip_library_timing.py", intervention["timing_tool_sha256"])
            require_hash(ROOT / "analysis/CHIP_LIBRARY_STRESS_PLAN.md", intervention["plan_sha256"])
            fixture = read(path / "final_stress.json")
            require(fixture["verified_rows"] == len(data["rows"]) and fixture["descriptor_read_substitutions"] == len(data["groups"]) * 28 and fixture["name_byte_substitutions"] == len(data["groups"]) * 7 * 33, "fixture read substitution denominator failed")
            require(all(d["before"] == d["after"] for d in fixture["descriptors"]), "fixture changed backing descriptors")
            require(len(data["icons"]) == len(data["groups"]) * 7, "not seven real icons per group")
            sources = {i["source"] for i in data["icons"]}
            require(len(sources) == 1, "chip-1 icon fixture selected unexpected source")
            icon_source = next(iter(sources))
            bases = (0x6200, 0x6600, 0x6A00) if name == "stress56-tabs" else (0x6200,)
            destinations = {0x06000000 + base + row * 128 for base in bases for row in range(7)}
            require({i["destination"] for i in data["icons"]} == destinations and max(destinations) + 128 <= 0x06008040, "icon/cache ranges overlap or missing tab")
            for step, base in ([(3, 0x6200), (4, 0x6200)] if name == "stress56-icons-v2" else [(4, 0x6200), (5, 0x6600), (6, 0x6A00), (7, 0x6600), (8, 0x6200)]):
                visuals.append(visible(path, step, rom, font, base, icon_source))
        else:
            require(not data["icons"], "normal comparison workload changed")
            intervention = read(path / "timing_environment.json")
            require_hash(ROOT / "tools/capture_chip_library_timing.py", intervention["tool_sha256"])
        cadence = Counter(b["start"]["frame"] - a["start"]["frame"] for a, b in zip(data["groups"], data["groups"][1:]))
        reports[name] = {"result_sha256": digest, "scope": result["scope"], "actions": result["actions"],
            "environment_hashes": {p.name: sha(p.read_bytes()) for p in sorted(path.glob("*environment.json"))},
            "groups": stats(data["groups"]), "glyph_copies": stats(data["copies"]), "library_updates": stats(data["updates"]),
            "icon_copies": len(data["icons"]), "save_changes": save_changes, "start_frame_deltas": dict(sorted(cadence.items())),
            "copies_touching_visible_scanlines": sum(c["start"]["scanline"] < 160 or c["end"]["scanline"] < 160 for c in data["copies"]),
            "group_start_scanlines": sorted({g["start"]["scanline"] for g in data["groups"]}), "visible": visuals}
    baseline = reports["timing-native"]["start_frame_deltas"]
    stressed = reports["stress56-icons-v2"]["start_frame_deltas"]
    require(baseline == {1: 193} and stressed == {1: 191, 2: 1}, "recorded startup cadence finding changed")
    report = {"schema": 1, "build_sha256": BUILD, "verifier_sha256": sha(Path(__file__).read_bytes()),
        "status": "56-cell/icon data and visible pixel checks PASS; startup cadence regression OPEN; no overall performance pass",
        "routes": reports, "open_issue": {"id": "CHIP-CACHE-TIMING-001", "state": "open",
        "observation": "Same-start first entry: native 194 groups with one-frame spacing; fixture 193 groups with one two-frame gap after the second group. Visible-scanline glyph writes increase substantially.",
        "cause_status": "extra unconditional glyph transfers are a candidate cause; separate single-factor/short-copy experiment required before fixing",
        "next": "isolate glyph count versus icon load, then investigate avoiding redundant copies or changing transfer schedule without shrinking vocabulary"},
        "rejected_attempts": [{"directory": "poc/runtime/chip-ko-v1-stress56-icons", "status": "fixture failed; excluded"},
            {"directory": "poc/runtime/chip-ko-v1-stress56-icons-diagnostic", "status": "fixture failed; glyph sources exposed ignored floating-point low-byte returns"}],
        "limits": ["Substituted CPU reads bypass chip acquisition/selection; not normal gameplay coverage or a new translation.",
        "Instrumentation does not write ROM/RAM/save contents or CPU registers. The normal timing run did roll back its isolated .sav after loading an older checkpoint; this side effect is recorded, not a preservation pass. Fixture checkpoints quarantined.",
        "Stable screenshots and post-copy byte checks do not prove absence of transient tearing for changing names.",
        "Mesen with muted audio, not hardware or audio synchronization evidence.",
        "Populated P.A/five-row and other exit paths remain unverified."],
        "api_source": "https://github.com/SourMesen/Mesen2/blob/master/Core/Debugger/ScriptingContext.cpp"}
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Verified 56-cell/7-icon fixtures across standard/mega/giga; startup cadence issue remains OPEN")


if __name__ == "__main__":
    main()
