#!/usr/bin/env python3
"""Build a full-syllable, extended-encoding EXE4.5 dialogue PoC."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from build_visibility_poc import (
    ARCHIVE_OFFSET,
    ARCHIVE_SIZE,
    FONT_SHA256,
    LICENSE_SHA256,
    ROOT,
    bdf_glyphs,
    require_hash,
    run_textpet,
    sha,
)
from extended_dialogue import HANGUL_COUNT, construct


def main() -> int:
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    profile = config["source_profile"]
    rom_path = ROOT / profile["filename"]
    require_hash(rom_path, profile["sha256"])
    source = rom_path.read_bytes()

    textpet = ROOT / config["textpet"]["exe"]
    dll = ROOT / config["textpet"]["dll"]
    require_hash(textpet, config["textpet"]["exe_sha256"])
    require_hash(dll, config["textpet"]["dll_sha256"])
    plugin_source = ROOT / config["textpet"]["plugins"]
    for name, expected in config["textpet"]["plugin_sha256"].items():
        require_hash(plugin_source / name, expected)

    font = ROOT / "external" / "fonts" / "Galmuri11.bdf"
    license_path = ROOT / "external" / "fonts" / "LICENSE-Galmuri.txt"
    require_hash(font, FONT_SHA256)
    require_hash(license_path, LICENSE_SHA256)
    wanted = {chr(0xAC00 + i) for i in range(HANGUL_COUNT)}
    glyphs = bdf_glyphs(font, wanted)

    wording_path = ROOT / "translations" / "poc_megaman_intro_ko.json"
    wording = json.loads(wording_path.read_text(encoding="utf-8"))
    if wording["state"] != "functional_poc" or wording["translation"] != "한글":
        raise SystemExit("PoC wording policy changed")
    baseline_tpl = ROOT / "analysis" / "tpl_baseline" / "65A578.tpl"
    original_tpl = baseline_tpl.read_text(encoding="utf-8-sig")
    if original_tpl.count(wording["source"]) != 1:
        raise SystemExit("protected source literal is missing or ambiguous")
    translated_tpl = original_tpl.replace(wording["source"], wording["translation"], 1)

    work = ROOT / "poc" / "visibility" / "work-extended-v3"
    if work.exists():
        raise SystemExit(f"refusing to overwrite existing work directory: {work}")
    plugins = work / "plugins"
    tpl_dir = work / "tpl"
    compiled_dir = work / "compiled"
    roundtrip_dir = work / "roundtrip"
    for directory in (tpl_dir, compiled_dir, roundtrip_dir):
        directory.mkdir(parents=True, exist_ok=False)
    shutil.copytree(plugin_source, plugins)

    table_path = plugins / "exe45-utf8.tbl"
    table = table_path.read_text(encoding="utf-8-sig").rstrip("\r\n") + "\n"
    for ch in sorted(set(wording["translation"])):
        syllable = ord(ch) - 0xAC00
        if not 0 <= syllable < HANGUL_COUNT:
            raise SystemExit(f"not a precomposed Hangul syllable: {ch!r}")
        code = "F9FC" + syllable.to_bytes(2, "little").hex().upper()
        table += f"{code}={ch}\n"
    table_path.write_text(table, encoding="utf-8", newline="\n")
    (tpl_dir / "65A578.tpl").write_text(translated_tpl, encoding="utf-8", newline="\n")

    common = [str(textpet), "Load-Plugins", str(plugins), "Game", config["textpet"]["game"]]
    compiled = compiled_dir / "65A578.msg"
    run_textpet(
        common + ["Read-Text-Archives", str(tpl_dir), "--format", "tpl",
                  "Write-Text-Archives", str(compiled), "--format", "bin"],
        work / "compile.log",
    )
    payload = compiled.read_bytes()
    if len(payload) > 0xFFFF:
        raise SystemExit(f"compiled archive is implausibly large: {len(payload)}")

    reexport = roundtrip_dir / "65A578.tpl"
    run_textpet(
        common + ["Read-Text-Archives", str(compiled), "--format", "bin",
                  "Write-Text-Archives", str(reexport), "--format", "tpl"],
        work / "reexport.log",
    )
    encoded = b"".join(
        b"\xF9\xFC" + (ord(ch) - 0xAC00).to_bytes(2, "little")
        for ch in wording["translation"]
    )
    if payload.count(encoded) != 1:
        raise SystemExit("independent F9 FC wording bytes are absent or ambiguous")
    reverse_text = reexport.read_text(encoding="utf-8-sig")
    if "printString" not in reverse_text:
        raise SystemExit("expected TextPet F9 FC reverse-parser collision changed")

    spec_path = ROOT / "tools" / "specs" / "exe45_dialogue_extension_v1.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    appended, patches, extension = construct(source, spec, payload, glyphs)
    writes: list[dict[str, object]] = []

    def plan(offset: int, final: bytes, writer: str) -> None:
        if offset < 0 or offset + len(final) > len(source):
            raise ValueError(f"out-of-bounds planned write: {writer}")
        writes.append({"offset": offset, "expected": source[offset:offset + len(final)],
                       "final": final, "writer": writer})

    pointer_offset = 0x38098
    expected_pointer = 0x08000000 + ARCHIVE_OFFSET
    if int.from_bytes(source[pointer_offset:pointer_offset + 4], "little") != expected_pointer:
        raise SystemExit("archive 65A578 pointer anchor changed")
    plan(pointer_offset, (0x08000000 + len(source)).to_bytes(4, "little"),
         "relocate raw archive 65A578 to expansion start")
    for offset, final, writer in patches:
        plan(offset, final, writer)
    intervals = sorted((int(w["offset"]), int(w["offset"]) + len(w["final"])) for w in writes)
    if any(end > next_start for (_, end), (next_start, _) in zip(intervals, intervals[1:])):
        raise SystemExit("planned writes overlap")

    target = bytearray(source + appended)
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
    if any(a != b and not allowed[i] for i, (a, b) in enumerate(zip(source, target))):
        raise SystemExit("unexplained difference inside original ROM extent")
    if target[:0xC0] != source[:0xC0]:
        raise SystemExit("GBA header changed")

    output = ROOT / "poc" / "output" / "exe45_extended_hangul_visibility_poc.gba"
    manifest_path = output.with_suffix(".json")
    if output.exists() or manifest_path.exists():
        raise SystemExit("refusing to overwrite existing extended PoC output")
    output.write_bytes(target)
    manifest = {
        "schema": 1,
        "policy": "development/PoC; NON-DISTRIBUTION",
        "source_sha256": sha(source),
        "output_sha256": sha(target),
        "output_bytes": len(target),
        "encoding": "F9 FC + uint16 LE Hangul syllable offset from U+AC00",
        "hangul_syllables": HANGUL_COUNT,
        "wording": wording,
        "compiled_archive_bytes": len(payload),
        "compiled_archive_sha256": sha(payload),
        "compiled_archive_original_slot_bytes": ARCHIVE_SIZE,
        "compiled_archive_relocated_offset": len(source),
        "textpet_forward_compile": True,
        "encoded_wording_hex": encoded.hex().upper(),
        "encoded_wording_unique_in_archive": True,
        "textpet_reverse_roundtrip": False,
        "textpet_reverse_collision": "F9 FC is decoded as the native printString command; custom Korean codec support is still required",
        "spec": str(spec_path.relative_to(ROOT)),
        "spec_sha256": sha(spec_path.read_bytes()),
        "extension": extension,
        "font": {"path": str(font.relative_to(ROOT)), "sha256": FONT_SHA256,
                 "license": str(license_path.relative_to(ROOT))},
        "expected_writes": [
            {"offset": f"0x{int(w['offset']):X}", "size": len(w["final"]),
             "changed_bytes": sum(a != b for a, b in zip(w["expected"], w["final"])),
             "writer": w["writer"], "expected_sha256": sha(bytes(w["expected"])),
             "final_sha256": sha(bytes(w["final"]))}
            for w in writes
        ] + [{"offset": f"0x{len(source):X}", "size": len(appended),
              "writer": "relocated archive, full Hangul font, width table, and verified Thumb handlers",
              "final_sha256": sha(appended)}],
        "final_diff_audited": True,
        "known_limit": "normal dialogue and cumulative-width path only; TextPet reverse decoding, other text consumers, F9 FC collision population, whole-game translation, and full QA remain open",
        "runtime": "pending",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"built {output}")
    print(f"sha256 {manifest['output_sha256']}")
    print(f"size {len(target)}; appended {len(appended)}; archive {len(payload)}/{ARCHIVE_SIZE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
