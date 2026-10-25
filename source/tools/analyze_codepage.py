#!/usr/bin/env python3
"""Cross-check EXE4.5's character table, 441-record font, and width tables."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FONT_BASE = 0x608758
GLYPH_COUNT = 441
GLYPH_BYTES = 96
WIDTH_TABLES = [0x5290C, 0x52FF0]


def main() -> int:
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    profile = config["source_profile"]
    rom = (ROOT / profile["filename"]).read_bytes()
    if hashlib.sha256(rom).hexdigest() != profile["sha256"]:
        raise SystemExit("source ROM hash mismatch")

    table_path = ROOT / "external" / "textpet-plugins" / "exe45-utf8.tbl"
    mappings = []
    ignored = []
    for lineno, raw in enumerate(table_path.read_text(encoding="utf-8-sig").splitlines(), 1):
        code, sep, text = raw.partition("=")
        if not sep or not code:
            continue
        raw_code = bytes.fromhex(code)
        if len(raw_code) == 1 and raw_code[0] <= 0xE3:
            index = raw_code[0]
        elif len(raw_code) == 2 and raw_code[0] == 0xE4:
            index = 0xE4 + raw_code[1]
        else:
            ignored.append({"line": lineno, "code": code, "text": text})
            continue
        mappings.append({"line": lineno, "code": code, "text": text, "glyph_index": index})

    indexes = [row["glyph_index"] for row in mappings]
    unmapped = sorted(set(range(GLYPH_COUNT)) - set(indexes))
    if len(mappings) != 440 or unmapped != [0x81] or len(set(indexes)) != len(indexes):
        raise SystemExit("unexpected character-table coverage")

    font = rom[FONT_BASE:FONT_BASE + GLYPH_COUNT * GLYPH_BYTES]
    widths = []
    for offset in WIDTH_TABLES:
        data = rom[offset:offset + GLYPH_COUNT * 4]
        values = [int.from_bytes(data[i:i + 4], "little") for i in range(0, len(data), 4)]
        if len(values) != GLYPH_COUNT or any(value < 1 or value > 16 for value in values):
            raise SystemExit(f"implausible width table at 0x{offset:X}")
        widths.append({
            "offset": offset,
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "distribution": dict(sorted(collections.Counter(values).items())),
        })

    report = {
        "rom_sha256": profile["sha256"],
        "table": str(table_path.relative_to(ROOT)).replace("\\", "/"),
        "table_sha256": hashlib.sha256(table_path.read_bytes()).hexdigest(),
        "mapping": {
            "single_byte": "00..E3 -> indexes 0..227",
            "lead_E4": "E4 xx -> indexes 228+xx",
            "mapped_glyphs": len(mappings),
            "unmapped_glyph_indices": unmapped,
            "index_min": min(indexes),
            "index_max": max(indexes),
            "coverage": "indexes 0..440 except reserved/unmapped 0x81",
            "non_glyph_table_entries": ignored,
        },
        "font": {
            "offset": FONT_BASE,
            "size": len(font),
            "record_bytes": GLYPH_BYTES,
            "records": GLYPH_COUNT,
            "sha256": hashlib.sha256(font).hexdigest(),
        },
        "width_tables": widths,
        "claim": "structural mapping established; runtime renderer consumption remains to verify",
    }
    out = ROOT / "analysis" / "exe45_codepage_and_font_structure.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("mapping: 440 assigned indexes in a 441-record space; 0x81 unmapped")
    print("font: 441 records x 96 bytes at 0x608758")
    for row in widths:
        print(f"widths 0x{row['offset']:X}: {row['distribution']}")
    print("non-glyph table entries:", ignored)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
