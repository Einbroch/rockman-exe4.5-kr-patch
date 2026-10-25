#!/usr/bin/env python3
"""Build the fail-closed EXE4.5 Hangul visibility PoC.

This is a NON-DISTRIBUTION development artifact. It temporarily assigns two
existing glyph codes to Hangul, changes one literal in one raw archive, and
audits every byte that differs from the immutable retail source.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from extract_baseline import ROOT, require_hash


ARCHIVE_OFFSET = 0x65A578
ARCHIVE_SIZE = 143
FONT_BASE = 0x608758
WIDTH_BASES = (0x5290C, 0x52FF0)
RECORD_BYTES = 96
MAPPING = {"한": 0x81, "글": 0x84}
FONT_SHA256 = "99dc4e76f82b8419fa1d2c258d589208653ccba26163fe0213e48c5dccc63193"
LICENSE_SHA256 = "b4f6dac08752bbe546d32b1af06ee526f524201774a5e164c0a96fe4f6ff0902"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bdf_glyphs(path: Path, wanted: set[str], vertical_shifts: dict[str, int] | None = None) -> dict[str, bytes]:
    """Render Galmuri11 BDF glyphs into the measured 16x12, 4-bpp records."""
    found: dict[str, bytes] = {}
    for block in path.read_text(encoding="utf-8").split("STARTCHAR ")[1:]:
        lines = block.splitlines()
        cp = int(next(x.split()[1] for x in lines if x.startswith("ENCODING ")))
        ch = chr(cp)
        if ch not in wanted:
            continue
        width, height, xoff, yoff = map(
            int, next(x for x in lines if x.startswith("BBX ")).split()[1:]
        )
        start = lines.index("BITMAP") + 1
        bits = [int(x, 16) for x in lines[start : start + height]]
        top = 11 - height - yoff + (vertical_shifts or {}).get(ch, 0)
        if width > 11 or height > 11 or xoff < 0 or top < 0 or top + height > 11:
            raise ValueError(f"glyph does not fit measured cell: {ch!r}")
        ink = {
            (x + xoff, y + top)
            for y, row in enumerate(bits)
            for x in range(width)
            if row & (1 << (((width + 7) // 8) * 8 - 1 - x))
        }
        if not ink:
            raise ValueError(f"empty glyph: {ch!r}")
        grid = [[1] * 16 for _ in range(12)]
        for x, y in ink:
            if x + 1 < 12 and y + 1 < 12:
                grid[y + 1][x + 1] = 2
        for x, y in ink:
            grid[y][x] = 3
        found[ch] = bytes(
            grid[y][x] | (grid[y][x + 1] << 4)
            for y in range(12)
            for x in range(0, 16, 2)
        )
    if set(found) != wanted:
        raise ValueError(f"font is missing glyphs: {wanted - set(found)}")
    if any(len(record) != RECORD_BYTES for record in found.values()):
        raise ValueError("packed glyph record size mismatch")
    return found


def run_textpet(command: list[str], log: Path) -> None:
    run = subprocess.run(command, cwd=ROOT, capture_output=True)
    log.write_bytes(run.stdout + run.stderr)
    if run.returncode or b"FATAL:" in run.stdout + run.stderr:
        raise SystemExit(f"TextPet failed; see {log}")


def main() -> int:
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    profile = config["source_profile"]
    rom_path = ROOT / profile["filename"]
    require_hash(rom_path, profile["sha256"])
    source = rom_path.read_bytes()
    if len(source) != profile["size"]:
        raise SystemExit("source ROM size mismatch")

    textpet = ROOT / config["textpet"]["exe"]
    dll = ROOT / config["textpet"]["dll"]
    tpi = ROOT / config["text_catalog"]["path"]
    require_hash(textpet, config["textpet"]["exe_sha256"])
    require_hash(dll, config["textpet"]["dll_sha256"])
    require_hash(tpi, config["text_catalog"]["sha256"])
    plugin_source = ROOT / config["textpet"]["plugins"]
    for name, expected in config["textpet"]["plugin_sha256"].items():
        require_hash(plugin_source / name, expected)

    font = ROOT / "external" / "fonts" / "Galmuri11.bdf"
    license_path = ROOT / "external" / "fonts" / "LICENSE-Galmuri.txt"
    require_hash(font, FONT_SHA256)
    require_hash(license_path, LICENSE_SHA256)
    glyphs = bdf_glyphs(font, set(MAPPING))

    wording_path = ROOT / "translations" / "poc_megaman_intro_ko.json"
    wording = json.loads(wording_path.read_text(encoding="utf-8"))
    if wording["state"] != "functional_poc" or wording["archive"] != "65A578":
        raise SystemExit("PoC wording policy or scope changed")
    if wording["source"] != "はじめまして!" or wording["translation"] != "한글":
        raise SystemExit("PoC wording anchors changed")

    baseline_tpl = ROOT / "analysis" / "tpl_baseline" / "65A578.tpl"
    original_tpl = baseline_tpl.read_text(encoding="utf-8-sig")
    if original_tpl.count(wording["source"]) != 1:
        raise SystemExit("protected source literal is missing or ambiguous")
    translated_tpl = original_tpl.replace(wording["source"], wording["translation"], 1)

    work = ROOT / "poc" / "visibility" / "work-v2"
    if work.exists():
        raise SystemExit(f"refusing to overwrite existing PoC work directory: {work}")
    plugins = work / "plugins"
    tpl_dir = work / "tpl"
    compiled_dir = work / "compiled"
    roundtrip_dir = work / "roundtrip"
    for directory in (tpl_dir, compiled_dir, roundtrip_dir):
        directory.mkdir(parents=True, exist_ok=False)
    shutil.copytree(plugin_source, plugins)

    table_path = plugins / "exe45-utf8.tbl"
    table = table_path.read_text(encoding="utf-8-sig")
    table_lines = table.splitlines()
    if (any(line.startswith("81=") for line in table_lines)
            or table_lines.count("80=÷") != 1 or table_lines.count("84=現") != 1):
        raise SystemExit("temporary code-page anchors changed")
    table = table.replace("80=÷", "80=÷\n81=한", 1).replace("84=現", "84=글", 1)
    table_path.write_text(table, encoding="utf-8", newline="\n")
    (tpl_dir / "65A578.tpl").write_text(translated_tpl, encoding="utf-8", newline="\n")

    common = [str(textpet), "Load-Plugins", str(plugins), "Game", config["textpet"]["game"]]
    compiled = compiled_dir / "65A578.msg"
    run_textpet(
        common
        + ["Read-Text-Archives", str(tpl_dir), "--format", "tpl",
           "Write-Text-Archives", str(compiled), "--format", "bin"],
        work / "compile.log",
    )
    if not compiled.exists():
        raise SystemExit("TextPet did not create the compiled archive")
    payload = compiled.read_bytes()
    if len(payload) > ARCHIVE_SIZE:
        raise SystemExit(f"compiled archive exceeds fixed slot: {len(payload)} > {ARCHIVE_SIZE}")

    reexport = roundtrip_dir / "65A578.tpl"
    rebuilt = roundtrip_dir / "65A578.msg"
    run_textpet(
        common
        + ["Read-Text-Archives", str(compiled), "--format", "bin",
           "Write-Text-Archives", str(reexport), "--format", "tpl"],
        work / "reexport.log",
    )
    if "한글" not in reexport.read_text(encoding="utf-8-sig"):
        raise SystemExit("compiled archive did not re-export the exact Hangul wording")
    run_textpet(
        common
        + ["Read-Text-Archives", str(reexport), "--format", "tpl",
           "Write-Text-Archives", str(rebuilt), "--format", "bin"],
        work / "rebuild.log",
    )
    if rebuilt.read_bytes() != payload:
        raise SystemExit("compiled archive is not byte-reversible through TextPet")

    writes: list[dict[str, object]] = []

    def plan(offset: int, final: bytes, writer: str) -> None:
        if offset < 0 or offset + len(final) > len(source):
            raise ValueError(f"out-of-bounds planned write: {writer}")
        writes.append({"offset": offset, "expected": source[offset:offset + len(final)],
                       "final": final, "writer": writer})

    plan(ARCHIVE_OFFSET, payload, "TextPet-compiled archive 65A578")
    for ch, index in MAPPING.items():
        plan(FONT_BASE + index * RECORD_BYTES, glyphs[ch], f"temporary Galmuri11 glyph {ch}")
        for width_base in WIDTH_BASES:
            plan(width_base + index * 4, (12).to_bytes(4, "little"),
                 f"temporary width {ch}")

    intervals = sorted((int(w["offset"]), int(w["offset"]) + len(w["final"])) for w in writes)
    if any(end > next_start for (_, end), (next_start, _) in zip(intervals, intervals[1:])):
        raise SystemExit("planned writes overlap")

    target = bytearray(source)
    for write in writes:
        offset = int(write["offset"])
        expected = bytes(write["expected"])
        final = bytes(write["final"])
        if bytes(target[offset:offset + len(final)]) != expected:
            raise SystemExit(f"expected bytes changed before write at 0x{offset:X}")
        target[offset:offset + len(final)] = final

    allowed = bytearray(len(source))
    for write in writes:
        offset = int(write["offset"])
        allowed[offset:offset + len(write["final"])] = b"\x01" * len(write["final"])
    unexplained = [i for i, (a, b) in enumerate(zip(source, target)) if a != b and not allowed[i]]
    if unexplained:
        raise SystemExit(f"unexplained final ROM differences: {len(unexplained)}")
    if target[:0xC0] != source[:0xC0]:
        raise SystemExit("GBA header changed")

    output = ROOT / "poc" / "output" / "exe45_hangul_visibility_poc.gba"
    manifest_path = output.with_suffix(".json")
    if output.exists() or manifest_path.exists():
        raise SystemExit("refusing to overwrite existing PoC output")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(target)

    manifest = {
        "schema": 1,
        "policy": "development/PoC; NON-DISTRIBUTION",
        "hypothesis": "the 0x608758 bank is the normal 16x12 variable-width dialogue font and codes 0x81/0x84 select records 0x81/0x84",
        "pass_condition": "a normal-controller run reaches MegaMan introduction script 1 and visibly renders 한글 while the remaining Japanese lines and controls continue normally",
        "fail_condition": "the target screen cannot be reached, Hangul is absent/corrupt, or adjacent text/control flow regresses",
        "source_sha256": sha(source),
        "output_sha256": sha(target),
        "output_bytes": len(target),
        "archive": {
            "offset": ARCHIVE_OFFSET,
            "slot_bytes": ARCHIVE_SIZE,
            "compiled_bytes": len(payload),
            "source_payload_sha256": sha(source[ARCHIVE_OFFSET:ARCHIVE_OFFSET + ARCHIVE_SIZE]),
            "compiled_payload_sha256": sha(payload),
            "textpet_byte_roundtrip": True,
            "control_structure_source": str(baseline_tpl.relative_to(ROOT)),
        },
        "mapping": {ch: f"0x{code:02X}" for ch, code in MAPPING.items()},
        "font": {
            "path": str(font.relative_to(ROOT)), "sha256": FONT_SHA256,
            "license": str(license_path.relative_to(ROOT)),
            "font_base": f"0x{FONT_BASE:X}", "record_bytes": RECORD_BYTES,
            "width_bases": [f"0x{x:X}" for x in WIDTH_BASES], "advance_pixels": 12,
        },
        "translation_asset": str(wording_path.relative_to(ROOT)),
        "translation_asset_sha256": sha(wording_path.read_bytes()),
        "known_limit": "temporary global glyph reassignment for two characters only; not a whole-game encoding, translation, QA, or release build",
        "expected_writes": [
            {
                "offset": f"0x{int(w['offset']):X}", "size": len(w["final"]),
                "changed_bytes": sum(a != b for a, b in zip(w["expected"], w["final"])),
                "writer": w["writer"], "expected_sha256": sha(bytes(w["expected"])),
                "final_sha256": sha(bytes(w["final"])),
            }
            for w in writes
        ],
        "final_diff_audited": True,
        "runtime": "pending",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"built {output}")
    print(f"sha256 {manifest['output_sha256']}")
    print(f"compiled archive {len(payload)}/{ARCHIVE_SIZE} bytes; all diffs audited")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
