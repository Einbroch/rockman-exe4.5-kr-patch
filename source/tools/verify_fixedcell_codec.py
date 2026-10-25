#!/usr/bin/env python3
"""Artifact verification of all Hangul boundaries in the mmbn45s consumer.

Each syllable is checked at script start and after each native F9 family.
This is encoding evidence, not runtime coverage of all 11,172 glyphs.
"""
import argparse
import json
from pathlib import Path
from build_visibility_poc import ROOT, run_textpet, sha
from korean_codec import HANGUL_BASE, HANGUL_COUNT, encode_character
from textpet_korean import command, prepare_plugins
from tpl_literals import literals, skeleton


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()
    work, report = ROOT / args.work, ROOT / args.report
    if work.exists() or report.exists():
        raise ValueError("refusing to overwrite codec evidence")
    work.mkdir(parents=True)
    profile = prepare_plugins(work / "plugins", {","})
    common = command(work / "plugins")
    cases = []
    for start in range(0, HANGUL_COUNT, 2048):
        chars = [chr(HANGUL_BASE + i) for i in range(start, min(start + 2048, HANGUL_COUNT))]
        name = f"fixed-{start:05d}"
        scripts = [f'script {i} mmbn45s {{\n\t"{ch}"\n\tprintShortString\n\t"{ch}"\n\tprintTextInput\n\t\tcapitalizeFirst = false\n\t\tcapitalizeAll = false\n\t"{ch}"\n\tend\n}}\n' for i, ch in enumerate(chars)]
        tpl = work / (name + ".tpl")
        text = f"@archive {name}\n@size {len(chars)}\n" + "".join(scripts)
        tpl.write_text(text, encoding="utf-8")
        binary, reverse, rebuilt = [work / (name + suffix) for suffix in (".msg", "-reverse.tpl", "-rebuilt.msg")]
        expected = b"".join((2 * len(chars) + 18 * i).to_bytes(2, "little") for i in range(len(chars)))
        expected += b"".join(encode_character(ch) + b"\xf9\0" + encode_character(ch) + b"\xf9\1\0" + encode_character(ch) + b"\xe5" for ch in chars)
        run_textpet(common + ["Read-Text-Archives", str(tpl), "--format", "tpl", "Write-Text-Archives", str(binary), "--format", "bin"], work / (name + "-compile.log"))
        if binary.read_bytes() != expected:
            raise ValueError("mmbn45s byte contract failed")
        run_textpet(common + ["Read-Text-Archives", str(binary), "--format", "bin", "Write-Text-Archives", str(reverse), "--format", "tpl"], work / (name + "-decode.log"))
        decoded = reverse.read_text(encoding="utf-8-sig")
        if ([(x.language, x.text) for x in literals(decoded)] != [("mmbn45s", ch) for ch in chars for _ in range(3)]
                or skeleton(decoded) != skeleton(text)):
            raise ValueError("mmbn45s controls/literals semantic roundtrip failed")
        run_textpet(common + ["Read-Text-Archives", str(reverse), "--format", "tpl", "Write-Text-Archives", str(rebuilt), "--format", "bin"], work / (name + "-rebuild.log"))
        if rebuilt.read_bytes() != expected:
            raise ValueError("mmbn45s binary roundtrip failed")
        cases.append({"first_index": start, "syllables": len(chars), "bytes": len(expected), "sha256": sha(expected)})
    result = {"schema": 1, "status": "pass", "consumer": "mmbn45s", "hangul_syllables": HANGUL_COUNT,
              "positions_per_syllable": ["script start", "after F9 00", "after F9 01 00"],
              "plugin": profile, "cases": cases, "tool_sha256": sha(Path(__file__).read_bytes()),
              "scope": "static full encoding boundary coverage, no full-repertoire runtime claim"}
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: mmbn45s {HANGUL_COUNT} syllables at three command boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
