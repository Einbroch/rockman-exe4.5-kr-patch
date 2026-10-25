#!/usr/bin/env python3
"""Factorial synthetic consumer-input experiment, separate emulator/save folder.

No product bytes or progression flags are changed. Zero Hangul means eight
native digit cells per row, not an empty workload. Frozen v1 probes stay intact.
"""
import argparse
import json
import shutil
import struct
import sys
from pathlib import Path
import capture_library_qa as library
from capture_chip_library_timing import PROBE
from capture_chip_library_stress import FIXTURE
from build_visibility_poc import ROOT, require_hash, sha


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError("fixture transformation anchor drift: " + old)
    return text.replace(old, new, 1)


def prepare_environment():
    src = ROOT / "poc/runtime/isolated-mesen-chip-survey"
    dst = ROOT / "poc/runtime/isolated-mesen-chip-matrix"
    saves = ROOT / "poc/runtime/chip-matrix-saves"
    if not dst.exists():
        dst.mkdir()
        for path in src.iterdir():
            if path.is_file() and path.name != "settings.json":
                shutil.copy2(path, dst / path.name)
        (dst / "Firmware").mkdir()
        shutil.copy2(src / "Firmware/gba_bios.bin", dst / "Firmware/gba_bios.bin")
        saves.mkdir(exist_ok=True)
        settings = json.loads((src / "settings.json").read_text(encoding="utf-8-sig"))
        settings["Preferences"]["SaveDataFolder"] = str(saves)
        (dst / "settings.json").write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    return dst / "Mesen.exe"


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--hangul", type=int, choices=(0, 56), required=True)
    ap.add_argument("--icons", type=int, choices=(0, 7), required=True)
    args, rest = ap.parse_known_args()
    sys.argv = [sys.argv[0]] + rest
    if "--mesen" in rest:
        raise ValueError("matrix owns its separate emulator/save environment")
    sys.argv += ["--mesen", str(prepare_environment())]
    fixed = library.fixed
    rom = Path(fixed.value("--rom")).resolve()
    require_hash(rom, fixed.value("--expect-rom-sha256"))
    m = json.loads(rom.with_suffix(".json").read_text(encoding="utf-8"))
    if sha(rom.read_bytes()) != m["output_sha256"]:
        raise ValueError("manifest/ROM mismatch")
    e = m["chip_library_extension"]
    require_hash(ROOT / "tools/capture_chip_library_timing.py", "6a076f1a5812ef803f08306fbf865d997ea499aa08443bb01455e58605197789")
    require_hash(ROOT / "tools/capture_chip_library_stress.py", "c50953f8c06396608e231e6e3166e85edb4b760fb18a723419010ac6b5727318")
    blob = rom.read_bytes()
    stream = 0x08000000 + e["clone_offset"] + struct.unpack_from("<H", blob, e["clone_offset"] + 2)[0]
    render = e["machine_code"][0]
    ret = [i["address"] for i in render["instructions"] if i["mnemonic"] == "pop" and i["operands"] == "{r0, r2, r3}"]
    if len(ret) != 1:
        raise ValueError("copy return changed")
    fixture = FIXTURE
    if not args.icons:
        fixture = replace_once(fixture, "local off=(address-stressDesc)%4", "local off=(address-stressDesc)%4\n if pc==0x0804302C and off==3 then stressReads=stressReads+1;return 0 end")
    if not args.hangul:
        fixture = replace_once(fixture, "if n==32 then return 0xE5 end", "if n==8 then return 0xE5 elseif n<8 then return 2 else stressFail('native fixture overflow') end")
        fixture = replace_once(fixture, "s['cpu.r0']~=TEST_STREAM+32", "s['cpu.r0']~=TEST_STREAM+8")
        fixture = replace_once(fixture, "top~=0xE202+row*16+col*2", "top~=0xE004")
        fixture = replace_once(fixture, "if bytesAt(0x06008040+row*512+col*64,64)~=", "if false and bytesAt(0x06008040+row*512+col*64,64)~=")
    code = "local function stressFail(s) write('fixture_failed.txt',s);emu.stop(1);error(s) end\n" + PROBE.replace("error(", "stressFail(") + fixture
    for key, value in {"COPY_RETURN": ret[0], "RENDER_START": render["address"], "RENDER_END": render["address"] + render["code_bytes"], "TEST_STREAM": stream, "FONT_START": 0x08000000 + e["font_offset"]}.items():
        code = code.replace(key, str(value))
    fixed.PROBE += code
    for old, new in (("local function capture(name)\n", "local function capture(name)\n dumpTiming(name)\n if timingGroups[1] then dumpStress(name) end\n"),
                     ("local function finish()\n", "local function finish()\n dumpTiming('final')\n dumpStress('final')\n")):
        fixed.runner.LUA_TEMPLATE = replace_once(fixed.runner.LUA_TEMPLATE, old, new)
    rc = library.main()
    out = Path(fixed.value("--out")).resolve()
    scope = f"DIAGNOSTIC factorial read substitution: {args.hangul} Hangul cells, {args.icons} icons, seven chip-1 descriptors; NOT normal play"
    receipt = json.loads((out / "result.json").read_text(encoding="utf-8"))
    receipt["scope"], receipt["normal_play_checkpoint_eligible"] = scope, False
    if (out / "checkpoint.mss").exists():
        (out / "checkpoint.mss").rename(out / "diagnostic_checkpoint.mss")
        receipt["artifacts"]["diagnostic_checkpoint.mss"] = receipt["artifacts"].pop("checkpoint.mss")
    if (out / "fixture_failed.txt").exists():
        receipt["complete"], rc = False, 1
    (out / "result.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    for name in ("probe_environment.json", "library_environment.json"):
        env = json.loads((out / name).read_text(encoding="utf-8"))
        env["scope"] = env["policy"] = scope
        (out / name).write_text(json.dumps(env, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "matrix_environment.json").write_text(json.dumps({"tool_sha256": sha(Path(__file__).read_bytes()), "rom_sha256": sha(blob),
        "scope": scope, "hangul": args.hangul, "icons": args.icons,
        "timing_tool_sha256": sha((ROOT / "tools/capture_chip_library_timing.py").read_bytes()),
        "fixture_tool_sha256": sha((ROOT / "tools/capture_chip_library_stress.py").read_bytes())}, indent=2), encoding="utf-8")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
