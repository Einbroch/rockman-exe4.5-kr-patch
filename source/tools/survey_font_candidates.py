#!/usr/bin/env python3
"""Measure font-region candidates from the exact EXE4.5 source ROM.

The offsets and extents originate in the public English patch's relocatable
file map.  This tool only promotes facts independently visible in the target
ROM: range contents and aligned literal references.  Renderer meaning remains
unresolved until runtime consumption is traced.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = [
    {"id": "font-candidate-big", "offset": 0x601738, "size": 0x6800,
     "record_size": 64, "upstream_label": "bigfont"},
    {"id": "font-candidate-variable", "offset": 0x608758, "size": 0xA560,
     "record_size": 96, "upstream_label": "vwfont"},
    {"id": "font-candidate-mono", "offset": 0x619EF8, "size": 0x7000,
     "record_size": 64, "upstream_label": "monofont"},
]


def aligned_literal_sites(rom: bytes, value: int) -> list[int]:
    needle = value.to_bytes(4, "little")
    return [i for i in range(0, len(rom) - 3, 4) if rom[i:i + 4] == needle]


def main() -> int:
    profile = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))["source_profile"]
    rom_path = ROOT / profile["filename"]
    rom = rom_path.read_bytes()
    if hashlib.sha256(rom).hexdigest() != profile["sha256"]:
        raise SystemExit("source ROM hash mismatch")

    rows = []
    for spec in CANDIDATES:
        start = spec["offset"]
        end = start + spec["size"]
        data = rom[start:end]
        records = [data[i:i + spec["record_size"]]
                   for i in range(0, len(data), spec["record_size"])]
        nibbles = sorted({byte & 0xF for byte in data} | {byte >> 4 for byte in data})
        rows.append({
            **spec,
            "end": end,
            "records": len(records),
            "unique_records": len(set(records)),
            "uniform_records": sum(len(set(record)) == 1 for record in records),
            "nibble_values": nibbles,
            "sha256": hashlib.sha256(data).hexdigest(),
            "aligned_literal_references": aligned_literal_sites(rom, 0x08000000 + start),
            "status": "candidate",
        })

    report = {
        "rom_sha256": profile["sha256"],
        "source_of_candidate_ranges": {
            "repository": "https://github.com/RockmanEXEZone/MMBN45-English-Translation",
            "commit": "61c8df305f76b3b94395cf58cee16d816b56eaaa",
            "file": "files.ext.asm",
        },
        "claim": "measured ROM ranges and literal references only; consumer semantics unresolved",
        "candidates": rows,
    }
    out = ROOT / "analysis" / "exe45_font_candidates.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    for row in rows:
        print(f"{row['id']}: {row['records']} records, "
              f"{len(row['aligned_literal_references'])} aligned references, "
              f"nibbles={row['nibble_values']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
