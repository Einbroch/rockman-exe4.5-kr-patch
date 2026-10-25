#!/usr/bin/env python3
"""Verify frozen library-header runtime evidence; never drives the emulator."""
import argparse
import json
import struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT, require_hash, sha
from fixedcell_font import bdf_cells, unpack_pixels
from report_fixedcell_runtime import verify_route, transfer_evidence
from tpl_literals import resolve_units
from verify_tpi_index import lz77_decompress


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def visible_title(directory, step, text, cells, native, table):
    prefix = f"step_{step:03d}"
    vram = (directory / f"{prefix}_gbaVideoRam.bin").read_bytes()
    io = (directory / f"{prefix}_display_io.bin").read_bytes()
    state = read(directory / f"{prefix}_state.json")["state"]
    shot = Image.open(directory / f"{prefix}.png").convert("RGB")
    control = struct.unpack_from("<H", io, 8)[0]
    if control & 0xC080 or any(state[f"ppu.bgLayers[0].scroll{axis}"] for axis in ("X", "Y")):
        raise ValueError("unexpected title background geometry")
    char_base, screen_base = ((control >> 2) & 3) * 0x4000, ((control >> 8) & 31) * 0x800
    records = []
    for j, char in enumerate(text):
        entries = [struct.unpack_from("<H", vram, screen_base + (2 + dy) * 64 + (12 + j) * 2)[0] for dy in (0, 1)]
        if any(e & 0xC00 or e >> 12 != 12 for e in entries):
            raise ValueError("title tile flip/palette changed")
        actual = b"".join(vram[char_base + (e & 1023) * 32:char_base + (e & 1023) * 32 + 32] for e in entries)
        if char in cells:
            expected = cells[char]
        else:
            code = table[char]
            index = code[0] if len(code) == 1 else 0xE4 + code[1]
            expected = native[0x601738 + index * 64:0x601738 + (index + 1) * 64]
        if expected != actual:
            raise ValueError("title tilemap consumed wrong glyph")
        pixels = unpack_pixels(actual)
        colors = []
        for role in (1, 2):
            mask = {(x, y) for y in range(16) for x in range(8) if pixels[y][x] == role}
            observed = {shot.getpixel(((12 + j) * 8 + x, 16 + y)) for x, y in mask}
            if len(observed) != 1:
                raise ValueError("title screenshot ink/shadow color mismatch")
            color = next(iter(observed))
            shot_mask = {(x, y) for y in range(16) for x in range(8) if shot.getpixel(((12 + j) * 8 + x, 16 + y)) == color}
            if shot_mask != mask:
                raise ValueError("title screenshot pixel mask mismatch")
            colors.append(color)
        if colors[0] == colors[1]:
            raise ValueError("title ink/shadow contrast lost")
        records.append({"character": char, "xy": [(12 + j) * 8, 16], "glyph_sha256": sha(actual), "pixel_masks_match": True})
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--observations", default="analysis/library_runtime_observations_v1.json")
    ap.add_argument("--out", default="analysis/exe45_library_ko_runtime.json")
    args = ap.parse_args()
    out, ledger_path = ROOT / args.out, ROOT / args.observations
    if out.exists():
        raise ValueError("refusing to overwrite runtime evidence")
    ledger = read(ledger_path)
    manifest_path = ROOT / ledger["manifest"]
    require_hash(manifest_path, ledger["manifest_sha256"])
    manifest = read(manifest_path)
    build = ledger["build_sha256"]
    if build != manifest["output_sha256"] or "fixedcell_visibility" in manifest:
        raise ValueError("wrong build or temporary font replacement")
    rom_path = manifest_path.with_suffix(".gba")
    require_hash(rom_path, build)
    require_hash(ROOT / ledger["reproduction"], build)
    config = read(ROOT / "project.json")
    source_path = ROOT / config["source_profile"]["filename"]
    require_hash(source_path, manifest["source_sha256"])
    source, rom = source_path.read_bytes(), rom_path.read_bytes()
    require_hash(ROOT / ledger["old_scope_regression"], ledger["old_scope_sha256"])
    if source[0x601738:0x603F38] != rom[0x601738:0x603F38]:
        raise ValueError("Japanese preloaded big-font slots changed")
    for asset in manifest["translation_assets"]:
        require_hash(ROOT / asset["path"], asset["sha256"])
    title_asset = next(a for a in manifest["translation_assets"] if a["archive"] == "6D9EC0")
    titles = [u["translation"] for u in resolve_units(read(ROOT / title_asset["path"]))]
    header = next(a for a in manifest["archives"] if a["archive"] == "6D9EC0")
    payload = lz77_decompress(rom, header["rom_offset"])[0]
    if len(payload) != header["compiled_bytes"] or sha(payload) != header["compiled_sha256"]:
        raise ValueError("header payload identity changed")
    extension = manifest["fixedcell_extension"]
    font = extension["font"]
    for field, key in (("path", "sha256"), ("license", "license_sha256")):
        require_hash(ROOT / font[field], font[key])
    cells = bdf_cells(ROOT / font["path"], {chr(i) for i in range(0xAC00, 0xD7A4)}, extension["raster"])
    font_blob = b"".join(cells[chr(i)] for i in range(0xAC00, 0xD7A4))
    if rom[extension["font_offset"]:extension["font_offset"] + len(font_blob)] != font_blob:
        raise ValueError("full fixed-cell font supply differs")
    table = {}
    for line in (ROOT / "external/textpet-plugins/exe45-utf8.tbl").read_text(encoding="utf-8-sig").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if len(value) == 1:
                table[value] = bytes.fromhex(key)
    seen, routes, loads, hooks, legacy, screenshots = set(), [], [], [], {}, []
    for row in ledger["routes"]:
        directory = ROOT / row["directory"]
        require_hash(directory / "result.json", row["result_sha256"])
        result = verify_route(directory, build, seen)
        for name, digest in row["environments"].items():
            require_hash(directory / name, digest)
        env_name = "probe_environment.json" if (directory / "probe_environment.json").exists() else "save_environment.json"
        env = read(directory / env_name)
        for name, before in env["files_before"].items():
            allowed_save = row.get("save_write", False) and name == ledger.get("written_test_save")
            if name.endswith(".sav") and not allowed_save and env["files_after"].get(name) != before:
                raise ValueError("unrelated isolated save changed")
        if (directory / "library_environment.json").exists():
            libenv = read(directory / "library_environment.json")
            require_hash(ROOT / "tools/capture_library_qa.py", libenv["library_probe_sha256"])
            require_hash(ROOT / "tools/capture_fixedcell_probe.py", libenv["fixedcell_probe_sha256"])
            observed = read(directory / "final_library.json")
            for load in observed["loads"]:
                before = (directory / f"library_load_{load['id']:02d}_before.bin").read_bytes()
                after = (directory / f"library_load_{load['id']:02d}_after.bin").read_bytes()
                end = 0x24000 + len(payload)
                if (len(before) != 0x40000 or len(after) != 0x40000 or after[0x24000:end] != payload
                        or before[:0x24000] != after[:0x24000] or before[end:] != after[end:] or load["outside_changed_bytes"] != 0):
                    raise ValueError("BIOS output/whole-EWRAM guard failed")
                loads.append({"directory": row["directory"], **load, "payload_bytes": len(payload)})
            if any(not call["abi_pass"] for call in observed["hook_calls"]):
                raise ValueError("Hangul hook live-state contract failed")
            hooks.extend(observed["hook_calls"])
            for key, count in observed["legacy_f9"].items():
                legacy[key] = legacy.get(key, 0) + count
        for observation in row["observations"]:
            name = f"step_{observation['step']:03d}.png"
            require_hash(directory / name, observation["sha256"])
            screenshots.append({"directory": row["directory"], **observation})
        routes.append({"directory": row["directory"], "result_sha256": row["result_sha256"], "scope": result["scope"], "actions": result["actions"]})
    transfers, visible = [], []
    for row in ledger["title_routes"]:
        directory = ROOT / row["directory"]
        transferred = transfer_evidence(directory, row["entry_step"], rom)
        if len(transferred) != 5:
            raise ValueError("four titles and one description transfer denominator changed")
        ram = (directory / f"step_{row['entry_step']:03d}_gbaExtWorkRam.bin").read_bytes()
        vram = (directory / f"step_{row['entry_step']:03d}_gbaVideoRam.bin").read_bytes()
        if ram[0x24000:0x24000 + len(payload)] != payload or vram[0x4000:0x6800] != source[0x601738:0x603F38]:
            raise ValueError("header residency or untouched Japanese font preload failed")
        transfers.append({"directory": row["directory"], "records": transferred})
        for step, title in row["title_steps"]:
            visible.append({"directory": row["directory"], "step": step, "text": titles[title],
                            "cells": visible_title(directory, step, titles[title], cells, source, table)})
    if len(loads) != len(ledger["title_routes"]) or not hooks or not legacy.get("1"):
        raise ValueError("missing load, new hook, or native F9 01 route evidence")
    disk = ledger["disk_save_edge"]
    saved_env = read(ROOT / disk["saved_route"] / "save_environment.json")
    reboot_env = read(ROOT / disk["reboot_route"] / "save_environment.json")
    reboot_result = read(ROOT / disk["reboot_route"] / "result.json")
    name = ledger["written_test_save"]
    if (reboot_result["state_origin"] is not None
            or saved_env["files_after"][name]["sha256"] != disk["sha256"]
            or reboot_env["files_before"][name] != saved_env["files_after"][name]
            or reboot_env["files_after"][name] != reboot_env["files_before"][name]):
        raise ValueError("disk-save to fresh-boot identity edge failed")
    codec_path = ROOT / ledger["fixedcell_codec_report"]
    require_hash(codec_path, ledger["fixedcell_codec_report_sha256"])
    codec = read(codec_path)
    if codec["hangul_syllables"] != 11172 or codec["status"] != "pass" or codec["plugin"]["derived_plugin_sha256"] != manifest["plugin"]["derived_plugin_sha256"]:
        raise ValueError("codec/build plugin binding failed")
    result = {"schema": 1, "status": "library headers normal-input runtime pass; partial development build",
              "policy": manifest["policy"], "build_sha256": build, "manifest_sha256": sha(manifest_path.read_bytes()),
              "observations_sha256": sha(ledger_path.read_bytes()), "translated_units": manifest["translated_units"],
              "unchanged_archives": manifest["unchanged_archives"], "reproduction_verified": True,
              "native_preloaded_font_unchanged": True, "loader_checks": loads, "hook_abi_calls_passed": len(hooks),
              "legacy_f9_counts": legacy, "transfers": transfers, "visible_titles": visible,
              "runtime_hangul_syllables": sorted(set("".join(titles)) & cells.keys()),
              "static_font_syllables": len(cells), "codec_report": ledger["fixedcell_codec_report"],
              "screenshots": screenshots, "routes": routes, "disk_save_edge": disk, "limits": ledger["limits"]}
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {len(loads)} loads, {len(hooks)} hook ABI calls, {len(visible)} title captures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
