#!/usr/bin/env python3
"""Record bounded source/code/runtime evidence for the native library fonts.

No patch is installed here. This distinguishes the 64-byte fixed-cell route
from the already localized 96-byte dialogue route; it is not a whole-engine
control-flow or font-coverage claim.
"""

from __future__ import annotations

import json
from pathlib import Path

from build_visibility_poc import ROOT, require_hash, sha
from extended_dialogue import CS_VERSION, KS_VERSION, Cs, CS_ARCH_ARM, CS_MODE_THUMB, Ks, KS_ARCH_ARM, KS_MODE_THUMB


def main() -> int:
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    source_path = ROOT / config["source_profile"]["filename"]
    require_hash(source_path, config["source_profile"]["sha256"])
    source = source_path.read_bytes()
    build_sha = "a1b3078664809acfd001b3e293cc5b24d3aa6d722dc9d8968af15a122c9811fa"
    routes = {
        "mono": "poc/runtime/intro-ko-v2-library-confirmed-mono",
        "big": "poc/runtime/intro-ko-v2-library-big",
        "exec": "poc/runtime/intro-ko-v2-library-exectrace",
        "ram": "poc/runtime/intro-ko-v2-library-ram",
    }
    evidence = {}
    for key, name in routes.items():
        directory = ROOT / name
        result_path = directory / "result.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if not result["complete"] or result["rom_sha256"] != build_sha:
            raise SystemExit(f"wrong or incomplete runtime: {key}")
        for artifact, expected in result["artifacts"].items():
            require_hash(directory / artifact, expected)
        evidence[key] = {"directory": name, "result_sha256": sha(result_path.read_bytes()),
                         "actions": result["actions"], "scope": result["scope"]}
    mono = json.loads((ROOT / routes["mono"] / "fontread_final.json").read_text(encoding="utf-8"))
    big = json.loads((ROOT / routes["big"] / "fontread_final.json").read_text(encoding="utf-8"))
    execution = json.loads((ROOT / routes["exec"] / "exectrace_final.json").read_text(encoding="utf-8"))
    ram = (ROOT / routes["ram"] / "final_gbaIntWorkRam.bin").read_bytes()
    # Literal pools are deliberately excluded from the disassembly scopes.
    scopes = [("fixed-cell stream loop", 0x03006824, 0x03006890),
              ("64-byte glyph copy", 0x0300689C, 0x030068C2)]
    if CS_VERSION != "5.0.7" or KS_VERSION != "0.9.2":
        raise SystemExit("analysis toolchain version changed")
    assembler = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    code = []
    for name, start, end in scopes:
        ram_at = start - 0x03000000
        rom_at = 0x1EE700 + start - 0x03005800
        blob = source[rom_at:rom_at + end - start]
        if ram[ram_at:ram_at + len(blob)] != blob:
            raise SystemExit(f"ROM/IWRAM byte mapping mismatch: {name}")
        instructions = list(decoder.disasm(blob, start))
        if sum(i.size for i in instructions) != len(blob):
            raise SystemExit("incomplete instruction boundary decoding")
        for ins in instructions:
            assembly = ".syntax unified\n.cpu arm7tdmi\n.thumb\n" + ins.mnemonic + " " + ins.op_str
            if bytes(assembler.asm(assembly, ins.address)[0]) != ins.bytes:
                raise SystemExit(f"independent instruction roundtrip failed at {ins.address:X}")
        code.append({"name": name, "rom_offset": rom_at, "runtime_start": start, "runtime_end": end,
                     "sha256": sha(blob), "actual_iwram_matches_source": True,
                     "instructions": [{"address": i.address, "bytes": i.bytes.hex(),
                                       "mnemonic": i.mnemonic, "operands": i.op_str} for i in instructions]})
    if mono["total_reads"] != 480 or not any(x["pc"] == "0x030068B6" for x in mono["sites"]):
        raise SystemExit("expected mono-consumer observation changed")
    report = {
        "schema": 1, "status": "native-consumer-observed; Hangul implementation pending",
        "source_sha256": sha(source), "build_sha256": build_sha,
        "scene": "PET -> Data Library, then one Down input",
        "evidence": evidence,
        "banks": [
            {"source_label": "monofont", "rom_start": "0x619EF8", "rom_end": "0x620EF8",
             "record_bytes": 64, "total_reads": mono["total_reads"], "sites": mono["sites"]},
            {"source_label": "bigfont", "rom_start": "0x601738", "rom_end": "0x607F38",
             "record_bytes": 64, "total_reads": big["total_reads"], "sites": big["sites"]},
        ],
        "execution": execution, "verified_code_scopes": code,
        "established": [
            "native loop compares E5 command threshold, handles E4 as next byte plus 228",
            "glyph copier computes r6 + (index << 6), copies sixteen 32-bit words, advances destination by 64",
            "both fixed-cell banks reach the same runtime read site; font base is caller-supplied r6",
            "callback PC 0x030068B6 corresponds to load at 0x030068B2 plus Thumb pipeline offset 4",
            "captured IWRAM bytes match the two declared source ROM code scopes",
        ],
        "open": [
            "identify all callers, stream populations, glyph-cell dimensions, and destination/VRAM upload links",
            "separate big-font BIOS-address bulk reads from per-glyph renderer consumption",
            "F9 FC decoding, Hangul font selection, cell width, and clearing are not implemented for this path",
            "observed bank reads do not assign every visible library label to a bank",
            "battle, profile, name input, graphics text, and total consumer coverage remain open",
        ],
        "notes": ["earlier folder named library-mono actually entered Jack In; data-library-mono entered Equipment; neither is claimed as library evidence",
                  "runtime report uses the confirmed library route only; no source ROM edits or gameplay RAM injection"],
    }
    out = ROOT / "analysis/exe45_library_font_consumers.json"
    if out.exists():
        raise SystemExit("refusing to overwrite analysis report")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Recorded two native fixed-cell font banks and ROM/IWRAM code mapping: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
