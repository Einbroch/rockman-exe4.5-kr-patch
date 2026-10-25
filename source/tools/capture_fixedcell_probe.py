#!/usr/bin/env python3
"""Observe EXE4.5's fixed-cell parser and staging/upload boundary.

Investigation only: reuses the pinned controller/checkpoint runner without
changing it, the ROM, RAM, or save contents. Addresses are revision-specific
observed entries, not a complete call graph. --probe snapshot is required.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from build_visibility_poc import ROOT, require_hash, sha
from capture_save_qa import inventory
import run_mesen_segment as runner


PROBE = r'''
local fixedCalls={}
local fixedActive=nil
local function bytesAt(address,size)
 local parts={}
 for i=0,size-1 do parts[#parts+1]=string.char(emu.read(address+i,emu.memType.gbaMemory)) end
 return table.concat(parts)
end
local function hexAt(address,size)
 local parts={}
 for i=0,size-1 do parts[#parts+1]=string.format('%02X',emu.read(address+i,emu.memType.gbaMemory)) end
 return table.concat(parts)
end
emu.addMemoryCallback(function()
 if fixedActive~=nil or #fixedCalls>=1000 then error('fixed-cell probe nesting/limit') end
 local s=emu.getState()
 fixedActive={id=#fixedCalls+1,frame=frame,stream=s['cpu.r0'],stage=s['cpu.r2'],target=s['cpu.r3'],
  width=s['cpu.r4'],height=s['cpu.r5'],font=s['cpu.r6'],tint=s['cpu.r7'],caller=s['cpu.r14'],glyphs={}}
 fixedActive.prefix=hexAt(fixedActive.stream,64)
 fixedCalls[#fixedCalls+1]=fixedActive
end,emu.callbackType.exec,0x03006824,0x03006824)
emu.addMemoryCallback(function()
 if fixedActive==nil then return end
 local s=emu.getState()
 fixedActive.glyphs[#fixedActive.glyphs+1]=string.format('{"stream":%d,"index":%d,"destination":%d,"font":%d}',s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r6'])
end,emu.callbackType.exec,0x0300689C,0x0300689C)
emu.addMemoryCallback(function()
 if fixedActive==nil then error('fixed-cell exit without entry') end
 local s=emu.getState();local c=fixedActive
 c.copy_source=s['cpu.r0'];c.copy_target=s['cpu.r1'];c.bytes=s['cpu.r2']
 if c.bytes<0 or c.bytes>0x4000 then error('unbounded fixed-cell stage') end
 write(string.format('fixed_%04d_stage.bin',c.id),bytesAt(c.copy_source,c.bytes))
 c.complete=true;fixedActive=nil
end,emu.callbackType.exec,0x03006886,0x03006886)
local function dumpFixed(name)
 local rows={}
 for _,c in ipairs(fixedCalls) do
  rows[#rows+1]=string.format('{"id":%d,"frame":%d,"stream":%d,"stage":%d,"target":%d,"width":%d,"height":%d,"font":%d,"tint":%d,"caller_lr":%d,"prefix_hex":"%s","complete":%s,"copy_source":%d,"copy_target":%d,"bytes":%d,"glyphs":[%s]}',
   c.id,c.frame,c.stream,c.stage,c.target,c.width,c.height,c.font,c.tint,c.caller,c.prefix,c.complete and 'true' or 'false',c.copy_source or 0,c.copy_target or 0,c.bytes or 0,table.concat(c.glyphs,','))
 end
 write(name..'_fixedcells.json','{"calls":['..table.concat(rows,',')..']}')
 write(name..'_display_io.bin',bytesAt(0x04000000,96))
end
'''


def value(flag: str) -> str:
    try:
        return sys.argv[sys.argv.index(flag) + 1]
    except (ValueError, IndexError):
        raise ValueError(f"explicit {flag} required") from None


def main() -> int:
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    deps = config["development_dependencies"]["runtime_capture"]
    require_hash(ROOT / deps["tool"], deps["tool_sha256"])
    source_path = ROOT / config["source_profile"]["filename"]
    require_hash(source_path, config["source_profile"]["sha256"])
    rom = Path(value("--rom")).resolve()
    require_hash(rom, value("--expect-rom-sha256"))
    # Retain the native parser and copier throughout this observation baseline.
    source, product = source_path.read_bytes(), rom.read_bytes()
    for start, end in ((0x1EF724, 0x1EF790), (0x1EF79C, 0x1EF7C2)):
        if source[start:end] != product[start:end]:
            raise ValueError("native fixed-cell observation scope changed")
    emulator = Path(value("--mesen")).resolve()
    out = Path(value("--out")).resolve()
    require_hash(emulator, deps["mesen_sha256"])
    settings_path = emulator.parent / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8-sig"))["Preferences"]
    save_dir = Path(settings["SaveDataFolder"]).resolve()
    safe = (ROOT / "poc/runtime").resolve()
    if not settings["OverrideSaveDataFolder"] or any(not p.is_relative_to(safe) or p == safe for p in (save_dir, emulator, out)):
        raise ValueError("isolated project-local environment required")
    if value("--probe") != "snapshot" or out.exists():
        raise ValueError("fresh output and snapshot probe required")
    bios = emulator.parent / "Firmware/gba_bios.bin"
    require_hash(bios, "fd2547724b505f487e6dcb29ec2ecff3af35a841a77ab2e85fd87350abd36570")
    before = inventory(save_dir)
    for old, new in (
        ("local copyCalls={}", "local copyCalls={}\n" + PROBE),
        ("local function capture(name)\n", "local function capture(name)\n dumpFixed(name)\n"),
        ("local function finish()\n", "local function finish()\n dumpFixed('final')\n"),
    ):
        if runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError("runner injection anchor drift")
        runner.LUA_TEMPLATE = runner.LUA_TEMPLATE.replace(old, new, 1)
    result = runner.main()
    (out / "probe_environment.json").write_text(json.dumps({
        "policy": "read-only observations; normal controller input; isolated saves",
        "probe_sha256": sha(Path(__file__).read_bytes()), "runner_sha256": deps["tool_sha256"],
        "settings_sha256": sha(settings_path.read_bytes()), "bios_sha256": sha(bios.read_bytes()),
        "files_before": before, "files_after": inventory(save_dir),
        "save_directory": str(save_dir),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
