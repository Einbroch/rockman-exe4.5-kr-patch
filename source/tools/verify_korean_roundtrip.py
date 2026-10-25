#!/usr/bin/env python3
"""Verify the complete Hangul repertoire and all 732 source archives."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from build_visibility_poc import ROOT, require_hash, run_textpet, sha
from korean_codec import HANGUL_BASE, HANGUL_COUNT, encode_character
from textpet_korean import command, prepare_plugins
from tpl_literals import literals


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--extra-characters", default="", help="explicit extra glyph characters, e.g. comma")
    args = ap.parse_args()
    work, report = ROOT / args.work, ROOT / args.report
    if work.exists() or report.exists():
        raise SystemExit("refusing to overwrite verification artifacts")
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    source = ROOT / config["source_profile"]["filename"]
    tpi = ROOT / config["text_catalog"]["path"]
    require_hash(source, config["source_profile"]["sha256"])
    require_hash(tpi, config["text_catalog"]["sha256"])
    work.mkdir(parents=True)
    extra_characters = set(args.extra_characters)
    profile = prepare_plugins(work / "plugins", extra_characters)
    common = command(work / "plugins")
    alphabet = "".join(chr(HANGUL_BASE + i) for i in range(HANGUL_COUNT)) + "".join(sorted(extra_characters))
    tpl = work / "hangul.tpl"
    tpl.write_text('@archive hangul\n@size 1\nscript 0 mmbn45 {\n\t"'
                   + alphabet + '"\n\tend\n}\n', encoding="utf-8")
    binary, reverse, rebuilt = work / "hangul.msg", work / "reverse.tpl", work / "rebuilt.msg"
    run_textpet(common + ["Read-Text-Archives", str(tpl), "--format", "tpl",
                         "Write-Text-Archives", str(binary), "--format", "bin"], work / "compile.log")
    expected = b"\x02\x00" + b"".join(encode_character(ch) for ch in alphabet) + b"\xE5"
    if binary.read_bytes() != expected:
        raise SystemExit("independent full-repertoire encoding check failed")
    run_textpet(common + ["Read-Text-Archives", str(binary), "--format", "bin",
                         "Write-Text-Archives", str(reverse), "--format", "tpl"], work / "decode.log")
    if alphabet not in reverse.read_text(encoding="utf-8-sig"):
        raise SystemExit("full-repertoire semantic re-extraction failed")
    run_textpet(common + ["Read-Text-Archives", str(reverse), "--format", "tpl",
                         "Write-Text-Archives", str(rebuilt), "--format", "bin"], work / "rebuild.log")
    if rebuilt.read_bytes() != expected:
        raise SystemExit("full-repertoire binary round trip failed")
    # A single continuous literal is insufficient: TextPet keeps reading table
    # entries within it and only consults commands again at a boundary. Exercise
    # EVERY syllable at script start and after keyWait as well as before end.
    boundary_cases = []
    for start in range(0, len(alphabet), 2048):
        chars = alphabet[start:start + 2048]
        name = f"boundaries-{start:05d}"
        case_tpl = work / (name + ".tpl")
        scripts = [f'script {i} mmbn45 {{\n\t"{ch}"\n\tkeyWait\n\t\tany = false\n\t"{ch}"\n\tend\n}}\n'
                   for i, ch in enumerate(chars)]
        case_tpl.write_text(f"@archive {name}\n@size {len(chars)}\n" + "".join(scripts), encoding="utf-8")
        case_bin = work / (name + ".msg")
        case_reverse = work / (name + "-reverse.tpl")
        case_rebuilt = work / (name + "-rebuilt.msg")
        # 4-byte glyph + 2-byte keyWait + 4-byte glyph + 1-byte end.
        expected_case = b"".join((2 * len(chars) + 11 * i).to_bytes(2, "little") for i in range(len(chars)))
        expected_case += b"".join(encode_character(ch) + b"\xE6\x00" + encode_character(ch) + b"\xE5" for ch in chars)
        run_textpet(common + ["Read-Text-Archives", str(case_tpl), "--format", "tpl",
                              "Write-Text-Archives", str(case_bin), "--format", "bin"], work / (name + "-compile.log"))
        if case_bin.read_bytes() != expected_case:
            raise SystemExit(f"independent boundary encoding failed: {name}")
        run_textpet(common + ["Read-Text-Archives", str(case_bin), "--format", "bin",
                              "Write-Text-Archives", str(case_reverse), "--format", "tpl"], work / (name + "-decode.log"))
        if [x.text for x in literals(case_reverse.read_text(encoding="utf-8-sig"))] != [ch for ch in chars for _ in range(2)]:
            raise SystemExit(f"boundary semantic re-extraction failed: {name}")
        run_textpet(common + ["Read-Text-Archives", str(case_reverse), "--format", "tpl",
                              "Write-Text-Archives", str(case_rebuilt), "--format", "bin"], work / (name + "-rebuild.log"))
        if case_rebuilt.read_bytes() != expected_case:
            raise SystemExit(f"boundary binary roundtrip failed: {name}")
        boundary_cases.append({"start_index": start, "characters": len(chars), "sha256": sha(expected_case)})
    native = work / "native"
    native.mkdir()
    run_textpet(common + ["Load-File-Index", str(tpi), "Read-Text-Archives", str(source),
                         "Write-Text-Archives", str(native), "--format", "tpl"], work / "extract.log")
    if len(list(native.glob("*.tpl"))) != 732:
        raise SystemExit("catalog extraction count changed")
    nochange = work / "native-roundtrip.gba"
    run_textpet(common + ["Load-File-Index", str(tpi), "Load-File", str(source),
                         "Read-Text-Archives", str(native), "--format", "tpl",
                         "Write-Text-Archives", str(nochange), "--format", "rom"], work / "native-rebuild.log")
    payload_report = work / "native-payloads.json"
    subprocess.run([sys.executable, str(ROOT / "tools/compare_archive_payloads.py"),
                    "--rom-a", str(source), "--tpi-a", str(tpi), "--rom-b", str(nochange),
                    "--output", str(payload_report), "--label", "korean-plugin-native-roundtrip"],
                   check=True, cwd=ROOT)
    native_result = json.loads(payload_report.read_text(encoding="utf-8"))
    if native_result["payload_identical"] != 732:
        raise SystemExit("native payload preservation failed")
    result = {
        "schema": 3, "status": "pass", "policy": "development; NON-DISTRIBUTION",
        "source_sha256": config["source_profile"]["sha256"], "plugin": profile,
        "repertoire": {"hangul_syllables": HANGUL_COUNT, "extra_characters": sorted(extra_characters),
                   "total_characters": len(alphabet), "semantic_roundtrip": True,
                   "binary_roundtrip": True, "bytes": len(expected), "sha256": sha(expected)},
        "command_boundary_tests": {"script_start_characters": len(alphabet),
                                   "after_keyWait_characters": len(alphabet), "cases": boundary_cases},
        "native_archives": 732, "native_payload_identical": 732,
        "native_payload_bytes": native_result["payload_bytes_total"],
        "work": str(work.relative_to(ROOT)),
        "limits": ["catalog only; not unindexed or generated streams",
                   "codec test, not 11172-glyph runtime verification", "other render consumers remain open"],
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {HANGUL_COUNT} Hangul syllables and 732 native archive payloads; {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
