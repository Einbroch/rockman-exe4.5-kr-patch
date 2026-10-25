#!/usr/bin/env python3
"""Source-bound chip-name and shared VRAM investigation, not a patch builder.

Verifies retained native traces, inventories the two shared name archives, and
records resource lifetimes. No free-space or complete call-graph claim.
"""
import argparse
import json
import struct
from pathlib import Path

from archive_scripts import script_spans
from build_visibility_poc import ROOT, require_hash, sha
from extended_dialogue import Cs, CS_ARCH_ARM, CS_MODE_THUMB, Ks, KS_ARCH_ARM, KS_MODE_THUMB, CS_VERSION, KS_VERSION
from report_fixedcell_runtime import verify_route
from verify_tpi_index import parse_tpi, lz77_decompress


BASELINE = "68dd04f9e4b2a7db2e567cf5cc42ba3791a83ae378ef36cfef2f23f8d672dba4"
POOLS = {0x765190: 256, 0x765B18: 137}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def decode_name(blob, table):
    if not blob:
        return ""
    if blob[-1] != 0xE5 or any(c >= 0xE5 or c not in table for c in blob[:-1]):
        raise ValueError("not a simple native chip name")
    if len(blob) > 9:
        raise ValueError("native name exceeds eight cells")
    return "".join(table[c] for c in blob[:-1])


def source_assets(source):
    u32 = lambda at: struct.unpack_from("<I", source, at)[0]
    at, row, records = 0x427F8, 0, []
    while u32(at):
        pointer, destination = u32(at), u32(0x42884 + row * 4)
        if pointer & 0x80000000:
            offset = (pointer & 0x7FFFFFFF) - 0x08000000
            size = u32(at + 4)
            data = source[offset:offset + size]
            mode, at = "raw", at + 8
        else:
            offset = pointer - 0x08000000
            decoded, _ = lz77_decompress(source, offset)
            size = (int.from_bytes(decoded[:4], "little") >> 8) - 4
            if len(decoded) != size + 4:
                raise ValueError("inner graphic payload size mismatch")
            data, mode, at = decoded[4:], "LZ10 with inner size header", at + 4
        if len(data) != size or not destination:
            raise ValueError("invalid scene asset boundary")
        records.append({"source_offset": offset, "destination": destination,
                        "bytes": size, "end": destination + size,
                        "mode": mode, "delivered_sha256": sha(data)})
        row += 1
    if at != 0x4287C or row != 23:
        raise ValueError("scene asset table boundary changed")
    return records


def code_scopes(source):
    if (CS_VERSION, KS_VERSION) != ("5.0.7", "0.9.2"):
        raise ValueError("investigation toolchain changed")
    decoder, assembler = Cs(CS_ARCH_ARM, CS_MODE_THUMB), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    result = []
    for label, start, end in (
        ("library initialization", 0x42778, 0x427AA),
        ("packed-count row selector", 0x42E50, 0x42F14),
        ("five-row selector", 0x42F14, 0x42F94),
        ("native one-byte name parser", 0x42FB0, 0x42FE4),
        ("conditional seven-icon transfer", 0x43014, 0x4305C),
        ("scene asset loader", 0x29164, 0x291AA),
        ("native halfword CpuSet", 0x956, 0x968),
    ):
        blob = source[start:end]
        instructions = list(decoder.disasm(blob, 0x08000000 + start))
        if sum(i.size for i in instructions) != len(blob):
            raise ValueError("incomplete bounded source decoding")
        for i in instructions:
            code = ".syntax unified\n.cpu arm7tdmi\n.thumb\n" + i.mnemonic + " " + i.op_str
            if bytes(assembler.asm(code, i.address)[0]) != i.bytes:
                raise ValueError(f"source instruction roundtrip failed: {i.address:X}")
        result.append({"name": label, "start": start, "end": end, "sha256": sha(blob),
                       "instructions": [{"address": i.address, "hex": i.bytes.hex(),
                                         "mnemonic": i.mnemonic, "operands": i.op_str} for i in instructions]})
    return result


def verify_rows(rows, by_address, placeholder):
    observed, total = [], 0
    for row in rows:
        if row["stream"] in by_address:
            key, blob = by_address[row["stream"]]
        elif row["stream"] == placeholder[0]:
            key, blob = "library-header:4 (unknown entry)", placeholder[1]
        else:
            raise ValueError("unresolved native name stream")
        if (not row["prefix_hex"].startswith(blob.hex().upper()) or
                row["after_stream"] != row["stream"] + len(blob) - 1 or
                row["after_upper"] != row["upper"] + 16 or row["after_lower"] != row["lower"] + 16 or
                row["lower"] != row["upper"] + 16 or row["caller"] != 0x08042EE5 or
                row["upper"] not in range(0x0201E600, 0x0201E6E0, 32)):
            raise ValueError("native row consumption/ABI mismatch")
        for delta, field in ((0, "top_hex"), (1, "bottom_hex")):
            values = [row["base"] + c * 2 + delta for c in blob[:-1]]
            values.extend([0] * (8 - len(values)))
            if struct.pack("<8H", *values).hex().upper() != row[field]:
                raise ValueError("native name-to-tile transform mismatch")
        total += row["count"]
        observed.append({"source": key, "row": (row["upper"] - 0x0201E600) // 32,
                         "calls": row["count"], "palette_base": row["base"]})
    return {"calls": total, "distinct_stream_row_base_combinations": len(rows),
            "row_stride_bytes": 32, "cells_per_row": 8, "observed": observed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    if args.out.exists():
        raise ValueError("refusing to overwrite survey report")
    config = read(ROOT / "project.json")
    source_path = ROOT / config["source_profile"]["filename"]
    require_hash(source_path, config["source_profile"]["sha256"])
    source = source_path.read_bytes()
    product_path = ROOT / "poc/output/exe45_ko_development_library_v1.gba"
    require_hash(product_path, BASELINE)
    product = product_path.read_bytes()
    catalog = ROOT / config["text_catalog"]["path"]
    require_hash(catalog, config["text_catalog"]["sha256"])
    table_path = ROOT / config["textpet"]["plugins"] / "exe45-utf8.tbl"
    require_hash(table_path, config["textpet"]["plugin_sha256"][table_path.name])
    table = {int(k, 16): v for line in table_path.read_text(encoding="utf-8-sig").splitlines()
             if "=" in line for k, v in [line.split("=", 1)] if len(k) == 2}
    archive_records, by_address = [], {}
    for row in parse_tpi(catalog):
        at = row["offset"]
        if at not in POOLS:
            continue
        payload = source[at:at + row["size"]]
        if payload != product[at:at + len(payload)] or row["compressed"]:
            raise ValueError("shared native archive changed")
        spans = script_spans(payload, POOLS[at])
        offset, entries, decoded = POOLS[at] * 2, [], []
        rebuilt = bytearray()
        for i, blob in enumerate(spans):
            text = decode_name(blob, table)
            decoded.append(text)
            rebuilt.extend(offset.to_bytes(2, "little"))
            entries.append({"script": i, "bytes": len(blob), "cells": len(blob) - 1 if blob else 0,
                            "source_offset": at + offset, "sha256": sha(blob)})
            if blob:
                by_address[0x08000000 + at + offset] = (f"{at:X}:{i}", blob)
            offset += len(blob)
        rebuilt.extend(b"".join(spans))
        if rebuilt != payload:
            raise ValueError("source name archive byte roundtrip failed")
        for pointer in row["pointers"]:
            expected = (0x08000000 + at).to_bytes(4, "little")
            if source[pointer:pointer + 4] != expected or product[pointer:pointer + 4] != expected:
                raise ValueError("shared source pointer changed")
        archive_records.append({"offset": at, "bytes": len(payload), "sha256": sha(payload),
                                "scripts": len(spans), "nonempty": sum(bool(t) for t in decoded),
                                "unique_nonempty": len(set(decoded) - {""}),
                                "source_cells": sum(len(b) - 1 for b in spans if b),
                                "maximum_cells": max(len(b) - 1 for b in spans if b),
                                "maximum_source_code": max(c for b in spans for c in b[:-1]),
                                "pointers": row["pointers"], "byte_roundtrip": True, "entries": entries})
    if len(archive_records) != 2:
        raise ValueError("missing shared source archive")
    header_at = int.from_bytes(product[0x428E0:0x428E4], "little") - 0x08000000
    header, _ = lz77_decompress(product, header_at)
    placeholder = (0x02024000 + int.from_bytes(header[8:10], "little"), script_spans(header, 5)[4])
    evidence, seen = {}, set()
    for name in ("chip-library-survey-v4", "chip-library-lifetime-v1"):
        path = ROOT / "poc/runtime" / name
        receipt = verify_route(path, BASELINE, seen)
        survey = read(path / "final_chip_survey.json")
        environment = read(path / "probe_environment.json")
        before_saves = {k: v for k, v in environment["files_before"].items() if k.endswith(".sav")}
        after_saves = {k: v for k, v in environment["files_after"].items() if k.endswith(".sav")}
        if before_saves != after_saves:
            raise ValueError("survey modified a persistent save")
        if survey["checked_frames"] <= 0 or survey["control_map_write_count"] <= 0:
            raise ValueError("no positive runtime observation control")
        evidence[name] = {"result_sha256": sha((path / "result.json").read_bytes()),
                          "actions": receipt["actions"], "frames": survey["checked_frames"],
                          "probe_environment_sha256": sha((path / "probe_environment.json").read_bytes()),
                          "chip_probe_environment_sha256": sha((path / "chip_probe_environment.json").read_bytes()),
                          "persistent_saves_unchanged": True,
                          "row_transform": verify_rows(survey["rows"], by_address, placeholder),
                          "candidate_write_count": survey.get("candidate_write_count", len(survey["candidate_writes"])),
                          "candidate_map_tile_histogram": survey["candidate_map_tile_histogram"],
                          "control_map_write_count": survey["control_map_write_count"],
                          "overlapping_copies": [c for c in survey["copies"] if
                              c["destination"] < 0x06009000 and c["destination"] + c["bytes"] > 0x06008000]}
    in_library = evidence["chip-library-survey-v4"]
    if in_library["candidate_write_count"] or any(r["tile_address"] != 0x06008000 for r in in_library["candidate_map_tile_histogram"]):
        raise ValueError("counterevidence to the bounded library residency observation")
    input_vram = (ROOT / "poc/runtime/chip-library-lifetime-v1/step_016_gbaVideoRam.bin").read_bytes()
    if input_vram[0x8000:0x9000] != source[0x63ABF4:0x63BBF4]:
        raise ValueError("name-entry graphics do not restore the entire candidate window")
    evidence["chip-library-lifetime-v1"]["name_entry_candidate_window_equals_source"] = True
    first, second = archive_records
    if len(first["pointers"]) != 9 or second["pointers"] != [p + 4 for p in first["pointers"]]:
        raise ValueError("shared root-pair relationship changed")
    native_scopes = code_scopes(source)
    for scope in native_scopes:
        if source[scope["start"]:scope["end"]] != product[scope["start"]:scope["end"]]:
            raise ValueError("native survey code differs from source")
    icon_ranges = []
    for label, literal in (("standard", 0x42C38), ("mega", 0x42CC0), ("giga", 0x42D40)):
        start = int.from_bytes(source[literal:literal + 4], "little")
        icon_ranges.append({"tab": label, "literal": literal, "start": start, "end": start + 7 * 128,
                            "condition": "per-row descriptor byte +3 nonzero", "runtime_transfer_observed": False})
    report = {"schema": 1, "status": "native evidence; chip-name Korean implementation NOT adopted",
              "source_sha256": sha(source), "baseline_rom_sha256": BASELINE,
              "shared_name_pools": archive_records, "bounded_code": native_scopes,
              "shared_root_pairs": list(zip(first["pointers"], second["pointers"])),
              "initialization_assets": source_assets(source), "conditional_icon_footprints": icon_ranges,
              "runtime": evidence,
              "candidate_assessment": {
                  "range": [0x06008000, 0x06009000], "globally_free": False,
                  "library_only_observation": "no writes; one initialization frame references tile 06008000",
                  "later_owner": "name-input BG graphics; 9600 bytes reloaded at 06008000 from ROM 0863ABF4 before observed map use",
                  "alternative_to_investigate": "56 private row/cell glyphs at 06008040..06008E3F, excluding the observed transition tile; not an adopted allocation",
                  "capacity_only": {"rows": 7, "cells": 8, "glyph_bytes": 64, "demand_bytes": 3584}},
              "limits": ["393 physical scripts, not 393 reachable or unique library chips",
                         "nine catalog root pairs verified, not a whole-engine reference-completeness proof",
                         "five-row parser caller not executed by these routes; PA list empty in the test save",
                         "conditional chip icon transfers not reached; their footprints are static evidence",
                         "no Korean chip names, no ROM modification, no new release eligibility",
                         "VRAM lifetime evidence is limited to the recorded library, PET, and name-input route"],
              "rejected_evidence": [
                  {"route": "chip-library-survey-v1", "reason": "emulator launch failed: missing runtime files; no captures"},
                  {"route": "chip-library-survey-v2", "reason": "Lua dump function shadowed by existing runner name; screenshots exist but chip observations were not serialized"},
                  {"route": "chip-library-survey-v3", "reason": "early reference list capped at 32; superseded by complete per-tile histogram in v4"}],
              "next": ["retain source name pools and all nine root pairs; use a scoped private lookup if a hook is adopted",
                       "close initialization/update/exit/reentry residency for the private glyph working set",
                       "verify an eight-cell Hangul/mixed-digit maximum and scrolling, palette, clear, five-row fallback before expanding translations"]}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Verified 393 source scripts, two runtime routes and native row transforms: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
