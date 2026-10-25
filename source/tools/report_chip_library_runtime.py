#!/usr/bin/env python3
"""Recheck retained normal-input evidence for the frozen 72-unit chip build.

This is artifact verification, not a new emulator run or wording approval.
The route hashes pin controller/checkpoint/artifact identities. Observations
below record inspected screenshots; pixel checks independently verify names.
"""
import argparse
import json
import struct
from pathlib import Path

from PIL import Image
from build_visibility_poc import ROOT, require_hash, sha
from fixedcell_font import bdf_cells, unpack_pixels
from report_fixedcell_runtime import verify_route, transfer_evidence
from report_library_runtime import visible_title
from chip_library_extension import decode_name, compile_clone
from tpl_literals import resolve_units
from verify_tpi_index import lz77_decompress


BUILD = "ce839b60c8125da7ca8ce0240bcdfc82a8e8f5604202449af1acffa80158cbff"
MANIFEST = "3516a689f03df585e0779588b76b746a86d9d32a7f993662c921c1bb23c9a591"
ROUTES = {
    "cold-guarded": "4b9e7469a518650296aed9256f0924283c0f5a7ddb4f3e589cd7858c55ed1d9b",
    "tabs": "e3b28aa8ba296089495073e2f2f4d4b31c22ead01e3dfc74a668973095d1a0d3",
    "input-lifetime": "413f3488c44b2138f122ce0be17524d89cdcdd9db3c1cbf1f99b790f153c4763",
    "scroll-reentry": "9719b7fc0ce099c942b7c2136cc4ac2b20b2e62d827736e9ca75e7264130afe6",
    "save-entry": "d1146f69277dacfb7cd62f1e7123f543d2761eaf78bae8f2c295a121d1868f1d",
    "save-commit": "faad2204bd5519b2127f259e5a54869bfc7fbd44e1dc8b683c65762fe249c428",
    "save-finish": "e993439abad02d8bb6a862d111e5e6556d636bb8894a1afb079bd1260afaae7d",
    "save-reboot": "c8e6e01979e4141544928a102722a582c9c6480cd53dd3e9c2ed461493a17e3a",
}
OBSERVATIONS = {
    "cold-guarded": {45: "Korean introduction", 53: "tournament prompt"},
    "tabs": {7: "three chip names", 9: "unknown selection", 10: "mega", 11: "giga", 12: "empty P.A", 15: "standard return", 16: "PET exit dialogue"},
    "input-lifetime": {4: "hobby question", 6: "native kana input", 8: "PET return"},
    "scroll-reentry": {3: "names restored after name input", 12: "names moved to rows 1/2", 18: "seven unknown rows", 32: "first page restored", 33: "mega", 34: "giga", 35: "empty P.A", 38: "standard return", 39: "PET exit"},
    "save-entry": {10: "PET save-screen prompt"},
    "save-commit": {7: "save confirmation", 8: "saving warning"},
    "save-finish": {1: "save completed", 3: "PET return"},
    "save-reboot": {3: "fresh boot splash", 8: "saved Navi selection", 11: "saved PET and Korean idle dialogue"},
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def directory(name):
    return ROOT / "poc/runtime" / ("chip-ko-v1-" + name)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def visible_names(path, step, expected_rows, cells, native, table):
    prefix = f"step_{step:03d}"
    vram = (path / f"{prefix}_gbaVideoRam.bin").read_bytes()
    trace = read(path / f"{prefix}_chip_ko.json")
    io = (path / f"{prefix}_display_io.bin").read_bytes()
    state = read(path / f"{prefix}_state.json")["state"]
    shot = Image.open(path / f"{prefix}.png").convert("RGB")
    ctrl = struct.unpack_from("<H", io, 10)[0]
    require(not ctrl & 0xC080 and all(state[f"ppu.bgLayers[1].scroll{a}"] == 0 for a in ("X", "Y")), "chip BG geometry changed")
    char_base, map_base = ((ctrl >> 2) & 3) * 0x4000, ((ctrl >> 8) & 31) * 0x800
    require(char_base == 0x4000, "chip font base changed")
    records = []
    for row in range(7):
        text = expected_rows.get(row, "   ??")
        # This is scratch RAM: the description renderer has reused its first
        # rows by end-of-frame. Use the captured parser-return bytes, not a
        # later RAM snapshot, when comparing the retained BG tilemap.
        matches = [r for r in trace["rows"] if r["upper"] == 0x0201E600 + row * 32
                   and decode_name(bytes.fromhex(r["text_hex"]), {v[0]: k for k, v in table.items() if len(v) == 1}) == text]
        require(bool(matches), "missing parser-return row evidence")
        traced = [bytes.fromhex(matches[-1][key]) for key in ("top_hex", "bottom_hex")]
        for col in range(8):
            entries = [struct.unpack_from("<H", vram, map_base + (4 + 2 * row + dy) * 64 + (17 + col) * 2)[0] for dy in (0, 1)]
            buffered = [struct.unpack_from("<H", traced[dy], col * 2)[0] for dy in (0, 1)]
            require(entries == buffered, "chip parser-return bytes / BG map mismatch")
            if col >= len(text):
                require(entries == [0, 0], "chip trailing clear mismatch")
                continue
            ch = text[col]
            korean = ch in cells
            tile = 514 + row * 16 + col * 2 if korean else table[ch][0] * 2
            require(entries == [0xE000 + tile, 0xE001 + tile], "chip row/cell tile mapping mismatch")
            actual = b"".join(vram[char_base + (e & 1023) * 32:char_base + (e & 1023) * 32 + 32] for e in entries)
            glyph = cells[ch] if korean else native[0x601738 + tile * 32:0x601738 + tile * 32 + 64]
            require(actual == glyph, "chip glyph supply mismatch")
            if row not in expected_rows:
                continue  # Unknown-row map and padding checked, no text translation claim.
            pixels = unpack_pixels(actual)
            colors = []
            for role in (1, 2):
                mask = {(x, y) for y in range(16) for x in range(8) if pixels[y][x] == role}
                require(bool(mask), "empty chip ink/shadow mask")
                observed = {shot.getpixel(((17 + col) * 8 + x, (4 + row * 2) * 8 + y)) for x, y in mask}
                require(len(observed) == 1, "chip screenshot color mismatch")
                color = next(iter(observed))
                actual_mask = {(x, y) for y in range(16) for x in range(8) if shot.getpixel(((17 + col) * 8 + x, (4 + row * 2) * 8 + y)) == color}
                require(actual_mask == mask, "chip screenshot pixel mask mismatch")
                colors.append(color)
            require(colors[0] != colors[1], "chip ink/shadow contrast lost")
            records.append({"row": row, "column": col, "character": ch, "glyph_sha256": sha(actual), "pixel_masks_match": True})
    require(vram[0x4000:0x6800] == native[0x601738:0x603F38], "native font residency changed")
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="analysis/exe45_chip_library_ko_runtime.json")
    args = ap.parse_args()
    out = ROOT / args.out
    require(not out.exists(), "refusing to overwrite evidence report")
    mp = ROOT / "poc/output/exe45_ko_development_chip_library_v1.json"
    require_hash(mp, MANIFEST)
    m = read(mp)
    for path in (mp.with_suffix(".gba"), ROOT / "poc/output/exe45_ko_development_chip_library_v1_repro.gba"):
        require_hash(path, BUILD)
    rom = mp.with_suffix(".gba").read_bytes()
    config = read(ROOT / "project.json")
    sp = ROOT / config["source_profile"]["filename"]
    require_hash(sp, m["source_sha256"])
    source = sp.read_bytes()
    require(m["translated_units"] == 72 and m["unchanged_archives"] == 728, "scope changed")
    for a in m["translation_assets"]:
        require_hash(ROOT / a["path"], a["sha256"])
    ext = m["chip_library_extension"]
    spec_path = ROOT / "tools/specs/exe45_chip_library_v1.json"
    require_hash(spec_path, ext["spec_sha256"])
    spec = read(spec_path)
    table = {}
    for line in (ROOT / "external/textpet-plugins/exe45-utf8.tbl").read_text(encoding="utf-8-sig").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if len(value) == 1:
                table[value] = bytes.fromhex(key)
    native_table = {value[0]: key for key, value in table.items() if len(value) == 1}
    clone, clone_report = compile_clone(source, spec, read(ROOT / "translations/library_chip_names_ko.json"), native_table)
    require(rom[ext["clone_offset"]:ext["clone_offset"] + len(clone)] == clone and clone_report == ext["clone"], "private clone differs from selected inputs")
    for start, size in ((0x765190, 2437), (0x765B18, 1103)):
        require(rom[start:start + size] == source[start:start + size], "shared source pool changed")
    pointers = (0x1F7F0, 0x22AF8, 0x3866C, 0x3CB98, 0x42F98, 0x4CAA8, 0x4E6A4, 0x4E79C, 0x51664)
    for at in pointers:
        require(source[at:at + 8] == rom[at:at + 8] == struct.pack("<II", 0x08765190, 0x08765B18), "shared pointer pair changed")
    fixed = m["fixedcell_extension"]
    for field, key in (("path", "sha256"), ("license", "license_sha256")):
        require_hash(ROOT / fixed["font"][field], fixed["font"][key])
    cells = bdf_cells(ROOT / fixed["font"]["path"], {chr(i) for i in range(0xAC00, 0xD7A4)}, fixed["raster"])
    font_blob = b"".join(cells[chr(i)] for i in range(0xAC00, 0xD7A4))
    require(rom[ext["font_offset"]:ext["font_offset"] + len(font_blob)] == font_blob, "full Hangul bank mismatch")
    header = next(a for a in m["archives"] if a["archive"] == "6D9EC0")
    payload = lz77_decompress(rom, header["rom_offset"])[0]
    require(sha(payload) == header["compiled_sha256"], "title archive mismatch")
    titles = [u["translation"] for u in resolve_units(read(ROOT / "translations/library_headers_ko.json"))]
    seen, routes, loads, hooks, legacy, observations, chip = set(), [], [], [], {}, [], []
    save_name = "exe45_ko_development_chip_library_v1.sav"
    for name, digest in ROUTES.items():
        path = directory(name)
        require_hash(path / "result.json", digest)
        result = verify_route(path, BUILD, seen)
        require(result["return_code"] == 0, "emulator failed")
        for component, component_hash in result["emulator_components"].items():
            require_hash(Path(result["emulator_path"]).parent / component, component_hash)
        envs = {p.name: sha(p.read_bytes()) for p in sorted(path.glob("*environment.json"))}
        env = read(path / ("probe_environment.json" if (path / "probe_environment.json").exists() else "save_environment.json"))
        for filename, before in env["files_before"].items():
            if filename.endswith(".sav") and not (name in ("save-commit", "save-finish") and filename == save_name):
                require(env["files_after"].get(filename) == before, "unrelated save changed")
        if (path / "library_environment.json").exists():
            le = read(path / "library_environment.json")
            require(le["manifest_sha256"] == MANIFEST and le["rom_sha256"] == BUILD, "title observer binding mismatch")
            for filename, key in (("capture_library_qa.py", "library_probe_sha256"), ("capture_fixedcell_probe.py", "fixedcell_probe_sha256")):
                require_hash(ROOT / "tools" / filename, le[key])
            lib = read(path / "final_library.json")
            for load in lib["loads"]:
                before = (path / f"library_load_{load['id']:02d}_before.bin").read_bytes()
                after = (path / f"library_load_{load['id']:02d}_after.bin").read_bytes()
                end = 0x24000 + len(payload)
                require(len(before) == len(after) == 0x40000 and after[0x24000:end] == payload and before[:0x24000] == after[:0x24000] and before[end:] == after[end:] and load["outside_changed_bytes"] == 0, "title loader whole-EWRAM guard failed")
                loads.append({"route": name, **load})
            require(all(c["abi_pass"] for c in lib["hook_calls"]), "title hook ABI failure")
            hooks.extend(lib["hook_calls"])
            for key, count in lib["legacy_f9"].items():
                legacy[key] = legacy.get(key, 0) + count
        if (path / "chip_ko_environment.json").exists():
            ce = read(path / "chip_ko_environment.json")
            require_hash(ROOT / "tools/capture_chip_library_qa.py", ce["probe_sha256"])
            require(ce["manifest_sha256"] == MANIFEST, "chip observer binding failed")
            trace = read(path / "final_chip_ko.json")
            require(trace["abi_calls"] == sum(r["calls"] for r in trace["rows"]) > 0 and trace["verified_bios_copies"] > 0, "empty/incomplete chip observations")
            for row in trace["rows"]:
                text = decode_name(bytes.fromhex(row["text_hex"]), native_table)
                ri = (row["upper"] - 0x0201E600) // 32
                require(0 <= ri < 7 and (row["upper"] - 0x0201E600) % 32 == 0, "row buffer outside contract")
                top, bottom = [], []
                for col, ch in enumerate(text):
                    tile = 514 + ri * 16 + col * 2 if ch in cells else table[ch][0] * 2
                    top.append(row["base"] + tile)
                    bottom.append(row["base"] + tile + 1)
                top += [0] * (8 - len(top)); bottom += [0] * (8 - len(bottom))
                require(bytes.fromhex(row["top_hex"]) == struct.pack("<8H", *top) and bytes.fromhex(row["bottom_hex"]) == struct.pack("<8H", *bottom), "independent row/padding decode failed")
            for pair in trace["copy_pairs"]:
                src, dst = pair["source"] - 0x08000000 - ext["font_offset"], pair["destination"] - ext["vram"]["start"]
                require(0 <= src < 11172 * 64 and src % 64 == 0 and 0 <= dst < 3584 and dst % 64 == 0, "observed copy outside bank/cache")
            chip.append({"route": name, "abi_calls": trace["abi_calls"], "real_bios_copies": trace["verified_bios_copies"], "distinct_rows": len(trace["rows"]), "distinct_copy_pairs": len(trace["copy_pairs"])})
        for step, finding in OBSERVATIONS[name].items():
            observations.append({"route": name, "step": step, "finding": finding, "screenshot_sha256": sha((path / f"step_{step:03d}.png").read_bytes()), "authority": "agent technical observation, not user wording/style approval"})
        routes.append({"route": name, "result_sha256": digest, "environment_sha256": envs, "scope": result["scope"], "actions": result["actions"], "captures": result["steps_captured"]})
    require(len(loads) == 2 and hooks and legacy.get("1"), "missing title load/ABI/native F9 evidence")
    first = {0: "캐논", 3: "에어슛", 4: "발칸1"}
    visible, visible_titles, transfers = [], [], []
    for name, entry, samples, title_samples in (
        ("tabs", 7, [(7, first), (9, first), (15, first)], [(7, 0), (10, 1), (11, 2), (12, 3), (15, 0)]),
        ("scroll-reentry", 3, [(3, first), (12, {1: "에어슛", 2: "발칸1"}), (18, {}), (32, first), (38, first)], [(3, 0), (33, 1), (34, 2), (35, 3), (38, 0)]),
    ):
        path = directory(name)
        tr = transfer_evidence(path, entry, rom)
        require(len(tr) == 5, "title/description transfer denominator changed")
        transfers.append({"route": name, "records": tr})
        # Scene initialization legitimately reclaims native input/PET tiles.
        # Compare settled library snapshots only; this is not a write trace.
        initial = (path / f"step_{entry:03d}_gbaVideoRam.bin").read_bytes()
        for step, expected in samples:
            visible.append({"route": name, "step": step, "expected_rows": expected, "cells": visible_names(path, step, expected, cells, source, table)})
            vram = (path / f"step_{step:03d}_gbaVideoRam.bin").read_bytes()
            require(vram[0x8000:0x8040] == initial[0x8000:0x8040] and vram[0x8E40:0x9000] == initial[0x8E40:0x9000], "cache boundary snapshot changed")
        for step, index in title_samples:
            visible_titles.append({"route": name, "step": step, "text": titles[index], "cells": visible_title(path, step, titles[index], cells, source, table)})
    input_vram = (directory("input-lifetime") / "step_006_gbaVideoRam.bin").read_bytes()
    require(input_vram[0x8000:0x9000] == source[0x63ABF4:0x63BBF4], "native input graphics did not reclaim cache")
    saved = read(directory("save-finish") / "save_environment.json")
    reboot = read(directory("save-reboot") / "save_environment.json")
    disk_hash = "99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470"
    require(saved["files_after"][save_name]["sha256"] == disk_hash and saved["files_after"][save_name] == reboot["files_before"][save_name] == reboot["files_after"][save_name], "disk save -> reboot edge failed")
    for route in ("save-finish", "save-reboot"):
        require_hash(directory(route) / "persistent_files_after" / save_name, disk_hash)
    for route in ("cold-guarded", "save-reboot"):
        require(read(directory(route) / "result.json")["state_origin"] is None, "cold run used checkpoint")
    for name, digest in (("exe45_ko_development_library_v1.sav", "a4535c6bea9dc97dfe56790b0572d38c916cc7bdb871cb2d18b3912d1370bdc4"), ("exe45_ko_development_save_v1.sav", "de890e26c3709275c83cd66efaabe65cca9ece7e347394b6e609cff0398c100c")):
        require_hash(ROOT / "poc/runtime/save-v1-persistence" / name, digest)
    require_hash(ROOT / "poc/output/exe45_ko_development_library_v1.gba", "68dd04f9e4b2a7db2e567cf5cc42ba3791a83ae378ef36cfef2f23f8d672dba4")
    bench_path = ROOT / "analysis/exe45_chip_library_cpu_v1.json"
    require_hash(bench_path, "3039ba63e1601a10d1246ce9b677cdffa5e4b3f88cb9438eac1cb51da56adf6e")
    bench = read(bench_path)
    require(bench["rom_sha256"] == BUILD and bench["vectors"] == 11710 and bench["register_memory_tile_checks"], "CPU bench artifact mismatch")
    require_hash(ROOT / "tools/bench_chip_library.py", bench["tool_sha256"])
    report = {"schema": 1, "status": "PASS for recorded routes; partial NON-DISTRIBUTION development build", "build_sha256": BUILD,
              "manifest_sha256": MANIFEST, "verifier_sha256": sha(Path(__file__).read_bytes()), "source_sha256": sha(source),
              "translated_units": 72, "private_chip_units": ext["clone"]["units"], "reproduction_verified": True,
              "source_pools_preserved": 2, "source_pointers_preserved": 18, "unselected_clone_scripts": len(ext["clone"]["unselected_scripts"]),
              "static_hangul_glyphs": 11172, "routes": routes, "observations": observations, "chip_runtime": chip,
              "chip_abi_calls": sum(c["abi_calls"] for c in chip), "real_bios_glyph_copies": sum(c["real_bios_copies"] for c in chip),
              "visible_names": visible, "visible_titles": visible_titles, "title_transfers": transfers, "title_loads": loads,
              "title_hook_abi_calls": len(hooks), "native_f9_counts": legacy, "native_input_reclaimed_4096_bytes": True,
              "disk_save_sha256": disk_hash, "disk_save_fresh_reboot_verified": True, "prior_saves_and_69_unit_rom_preserved": True,
              "cpu_bench": bench, "limits": ["Three draft names only on guarded seven-row library path; other consumers remain native.",
              "Normal input and same-ROM checkpoints; no RAM/progress injection. Emulator audio disabled.",
              "CPU bench is synthetic, with substituted CpuSet; not gameplay, hardware timing, or worst-case 56-Hangul real-time proof.",
              "Conditional icons, populated P.A, five-row gameplay and other exit routes remain unverified.",
              "No global-free VRAM claim; boundary snapshots do not prove every transient write.",
              "Terminology/style review and full-game localization incomplete; no release eligibility."]}
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {len(routes)} routes, {report['chip_abi_calls']} chip ABI calls, {report['real_bios_glyph_copies']} real BIOS glyph copies, save/reboot")


if __name__ == "__main__":
    main()
