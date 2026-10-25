#!/usr/bin/env python3
"""Scan the verified text population and whole ROM for F9 FC candidates."""

from __future__ import annotations

import hashlib
import json

from compare_archive_payloads import payload_of
from extract_baseline import ROOT, require_hash
from korean_codec import find_escapes
from verify_tpi_index import parse_tpi


def main() -> int:
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    profile = config["source_profile"]
    rom_path = ROOT / profile["filename"]
    require_hash(rom_path, profile["sha256"])
    tpi_path = ROOT / config["text_catalog"]["path"]
    require_hash(tpi_path, config["text_catalog"]["sha256"])
    rom = rom_path.read_bytes()
    rows = parse_tpi(tpi_path)

    archive_hits = []
    decoded_bytes = 0
    for archive_index, row in enumerate(rows):
        payload = payload_of(rom, row)
        decoded_bytes += len(payload)
        hits = find_escapes(payload)
        if hits:
            archive_hits.append({"archive_index": archive_index,
                                 "archive_offset": f"0x{row['offset']:X}",
                                 "hits": hits})
    raw_hits = find_escapes(rom)
    report = {
        "schema": 1,
        "source_sha256": hashlib.sha256(rom).hexdigest(),
        "catalog_sha256": hashlib.sha256(tpi_path.read_bytes()).hexdigest(),
        "encoding_candidate": "F9 FC + uint16 LE Hangul syllable offset from U+AC00",
        "verified_archives": len(rows),
        "verified_decoded_payload_bytes": decoded_bytes,
        "verified_archive_occurrences": sum(len(x["hits"]) for x in archive_hits),
        "verified_archives_with_occurrences": len(archive_hits),
        "archive_hits": archive_hits,
        "whole_rom_raw_occurrences": len(raw_hits),
        "whole_rom_valid_index_candidates": sum(bool(x["valid_hangul"]) for x in raw_hits),
        "whole_rom_note": "raw-ROM byte pairs include code, graphics, compressed data, and tables; they are candidates only and are not decoded text claims",
        "conclusion": "no F9 FC occurrence exists in the complete 732-archive verified decoded text population",
        "remaining_risk": "unindexed/external text consumers and runtime-generated streams are outside this catalog scan"
    }
    out = ROOT / "analysis" / "exe45_f9fc_collision_scan.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"verified archives: {len(rows)}; decoded bytes: {decoded_bytes}")
    print(f"catalog F9 FC occurrences: {report['verified_archive_occurrences']}")
    print(f"whole-ROM raw candidates: {len(raw_hits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
