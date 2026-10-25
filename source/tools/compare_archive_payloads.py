#!/usr/bin/env python3
"""Compare the consumed payload of every message archive between two ROM builds.

LZ77 has no unique byte representation, so a re-packed ROM is not expected to be
byte-identical to the original.  The equivalence criterion this checks is the one
the game actually consumes: for every archive, the bytes the engine ends up with
after decompression (or the raw slice, for uncompressed archives) must be
identical between the two builds.

Entries are normally matched between two indexes by their pointer list.  For a
no-change TextPet round trip, --tpi-b may be omitted: output archive offsets are
then recovered from the catalogued pointer words in ROM B.  Pointer-less rows
remain at their source offsets because they cannot be relocated by the writer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_tpi_index import lz77_decompress, parse_tpi  # noqa: E402


def payload_of(rom: bytes, row: dict) -> bytes:
    off = row["offset"]
    if row["compressed"]:
        decoded, _ = lz77_decompress(rom, off)
        return decoded
    size = row["size"]
    if size is None:
        raise ValueError("uncompressed row without a size")
    return rom[off : off + size]


def key_of(row: dict):
    claims = tuple(p for p in row["pointers"] if p != 0)
    return claims


def build_map(rows: list) -> tuple[dict, list]:
    keyed = {}
    unkeyed = []
    for row in rows:
        key = key_of(row)
        if key:
            if key in keyed:
                raise ValueError("duplicate pointer list %r" % (key,))
            keyed[key] = row
        else:
            unkeyed.append(row)
    return keyed, unkeyed


def rows_from_output_pointers(rows: list, rom: bytes) -> tuple[list, list]:
    """Return a catalog relocated according to pointer values stored in ROM."""
    relocated = []
    errors = []
    for row in rows:
        copy = dict(row)
        claims = [p for p in row["pointers"] if p != 0]
        if claims:
            targets = set()
            for ptr in claims:
                if ptr + 4 > len(rom):
                    errors.append({"line": row["line"], "ptr_at": ptr,
                                   "error": "pointer out of range"})
                    continue
                targets.add(int.from_bytes(rom[ptr:ptr + 4], "little") - 0x08000000)
            if len(targets) != 1:
                errors.append({"line": row["line"], "pointer_targets": sorted(targets),
                               "error": "catalogued pointers disagree"})
            elif 0 <= next(iter(targets)) < len(rom):
                copy["offset"] = next(iter(targets))
            else:
                errors.append({"line": row["line"], "pointer_targets": sorted(targets),
                               "error": "target out of ROM range"})
        relocated.append(copy)
    return relocated, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-a", required=True)
    ap.add_argument("--tpi-a", required=True)
    ap.add_argument("--rom-b", required=True)
    ap.add_argument("--tpi-b")
    ap.add_argument("--output", required=True)
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    rom_a = Path(args.rom_a).read_bytes()
    rom_b = Path(args.rom_b).read_bytes()
    rows_a = parse_tpi(Path(args.tpi_a))
    pointer_errors = []
    if args.tpi_b:
        rows_b = parse_tpi(Path(args.tpi_b))
    else:
        rows_b, pointer_errors = rows_from_output_pointers(rows_a, rom_b)

    keyed_a, unkeyed_a = build_map(rows_a)
    keyed_b, unkeyed_b = build_map(rows_b)

    report = {
        "label": args.label,
        "rom_a": Path(args.rom_a).name,
        "rom_a_sha256": hashlib.sha256(rom_a).hexdigest(),
        "rom_a_size": len(rom_a),
        "rom_b": Path(args.rom_b).name,
        "rom_b_sha256": hashlib.sha256(rom_b).hexdigest(),
        "rom_b_size": len(rom_b),
        "rows_a": len(rows_a),
        "rows_b": len(rows_b),
        "matched": 0,
        "payload_identical": 0,
        "payload_differs": [],
        "unmatched_a": [],
        "unmatched_b": [],
        "relocated": 0,
        "in_place": 0,
        "stored_size_delta_total": 0,
        "payload_bytes_total": 0,
        "decode_errors": [],
        "output_pointer_errors": pointer_errors,
    }

    if len(unkeyed_a) != len(unkeyed_b):
        report["unmatched_a"].append(
            {"error": "pointer-less row count differs",
             "a": len(unkeyed_a), "b": len(unkeyed_b)}
        )

    pairs = []
    for key, row_a in keyed_a.items():
        row_b = keyed_b.get(key)
        if row_b is None:
            report["unmatched_a"].append({"offset": row_a["offset"], "key": list(key)})
            continue
        pairs.append((row_a, row_b))
    for key in keyed_b:
        if key not in keyed_a:
            report["unmatched_b"].append({"offset": keyed_b[key]["offset"],
                                          "key": list(key)})
    # Pointer-less rows carry no stable identity and both indexes are sorted by
    # offset, so relocation can reorder them.  Pair them by payload instead, and
    # only fall back to position for whatever is left over.
    remaining_b = list(unkeyed_b)
    leftover_a = []
    for row_a in unkeyed_a:
        try:
            pa = payload_of(rom_a, row_a)
        except Exception:
            leftover_a.append(row_a)
            continue
        match = None
        for row_b in remaining_b:
            try:
                if payload_of(rom_b, row_b) == pa:
                    match = row_b
                    break
            except Exception:
                continue
        if match is None:
            leftover_a.append(row_a)
        else:
            remaining_b.remove(match)
            pairs.append((row_a, match))
    for row_a, row_b in zip(leftover_a, remaining_b):
        pairs.append((row_a, row_b))

    for row_a, row_b in pairs:
        report["matched"] += 1
        try:
            pa = payload_of(rom_a, row_a)
            pb = payload_of(rom_b, row_b)
        except Exception as exc:  # recorded as evidence
            report["decode_errors"].append(
                {"offset_a": row_a["offset"], "offset_b": row_b["offset"],
                 "error": str(exc)}
            )
            continue
        report["payload_bytes_total"] += len(pa)
        if row_a["offset"] == row_b["offset"]:
            report["in_place"] += 1
        else:
            report["relocated"] += 1
        if row_a["size"] is not None and row_b["size"] is not None:
            report["stored_size_delta_total"] += row_b["size"] - row_a["size"]
        if pa == pb:
            report["payload_identical"] += 1
        else:
            first = next((i for i, (x, y) in enumerate(zip(pa, pb)) if x != y),
                         min(len(pa), len(pb)))
            report["payload_differs"].append(
                {
                    "offset_a": row_a["offset"],
                    "offset_b": row_b["offset"],
                    "len_a": len(pa),
                    "len_b": len(pb),
                    "first_diff": first,
                    "sha_a": hashlib.sha256(pa).hexdigest()[:16],
                    "sha_b": hashlib.sha256(pb).hexdigest()[:16],
                }
            )

    report["verdict"] = (
        "PAYLOAD_EQUIVALENT"
        if report["matched"] == len(rows_a)
        and not report["payload_differs"]
        and not report["decode_errors"]
        and not report["unmatched_a"]
        and not report["unmatched_b"]
        and not report["output_pointer_errors"]
        else "NOT_EQUIVALENT"
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("%s: %s" % (args.label or "compare", report["verdict"]))
    print("  rows A/B           %d / %d" % (report["rows_a"], report["rows_b"]))
    print("  matched            %d" % report["matched"])
    print("  payload identical  %d" % report["payload_identical"])
    print("  payload differs    %d" % len(report["payload_differs"]))
    print("  decode errors      %d" % len(report["decode_errors"]))
    print("  in place / moved   %d / %d" % (report["in_place"], report["relocated"]))
    print("  stored size delta  %+d bytes" % report["stored_size_delta_total"])
    print("  payload bytes      %d" % report["payload_bytes_total"])
    print("  rom size delta     %+d bytes"
          % (report["rom_b_size"] - report["rom_a_size"]))
    return 0 if report["verdict"] == "PAYLOAD_EQUIVALENT" else 1


if __name__ == "__main__":
    sys.exit(main())
