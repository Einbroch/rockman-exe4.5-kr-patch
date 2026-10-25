#!/usr/bin/env python3
"""Read-only library-header loader and F9 FC ABI observations.

Adds callbacks to the existing fixed-cell observer in memory. Does not edit
ROM, RAM, controller state, the pinned runner, or previous evidence tools.
"""
import json
from pathlib import Path
import capture_fixedcell_probe as fixed
from build_visibility_poc import ROOT, require_hash, sha


EXTRA = r'''
local loaderRows={}
local loaderBefore=nil
local hookActive=nil
local hookRows={}
local legacyF9={}
emu.addMemoryCallback(function()
 if loaderBefore~=nil then error('nested library load') end
 loaderBefore=bytesAt(0x02000000,0x40000)
end,emu.callbackType.exec,0x08042798,0x08042798)
emu.addMemoryCallback(function()
 if loaderBefore==nil then error('library return without load') end
 local after=bytesAt(0x02000000,0x40000)
 local outside=0
 for i=1,#after do
  local at=0x02000000+i-1
  if (at<0x02024000 or at>=0x02024000+HEADER_BYTES) and after:byte(i)~=loaderBefore:byte(i) then outside=outside+1 end
 end
 local id=#loaderRows+1
 write(string.format('library_load_%02d_before.bin',id),loaderBefore)
 write(string.format('library_load_%02d_after.bin',id),after)
 loaderRows[#loaderRows+1]=string.format('{"id":%d,"frame":%d,"outside_changed_bytes":%d}',id,frame,outside)
 loaderBefore=nil
end,emu.callbackType.exec,0x080427A0,0x080427A0)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if emu.read(s['cpu.r0']+1,emu.memType.gbaMemory)~=0xfc then return end
 if hookActive~=nil then error('nested Hangul hook') end
 hookActive=s
end,emu.callbackType.exec,HOOK_ADDRESS,HOOK_ADDRESS)
emu.addMemoryCallback(function()
 if hookActive==nil then return end
 local s=emu.getState();local b=hookActive
 local pass=s['cpu.r0']==b['cpu.r0']+4 and s['cpu.r2']==b['cpu.r2']+64 and s['cpu.r4']==b['cpu.r4']+1 and s['cpu.r5']==b['cpu.r5']+1 and s['cpu.r9']==b['cpu.r9']+1
 for _,r in ipairs({3,6,7,8,10,11,12,13}) do
  if s['cpu.r'..r]~=b['cpu.r'..r] then pass=false end
 end
 hookRows[#hookRows+1]=string.format('{"frame":%d,"stream":%d,"abi_pass":%s}',frame,b['cpu.r0'],pass and 'true' or 'false')
 hookActive=nil
end,emu.callbackType.exec,0x0300685C,0x0300685C)
emu.addMemoryCallback(function()
 local s=emu.getState();local cmd=emu.read(s['cpu.r0']+1,emu.memType.gbaMemory)
 legacyF9[cmd]=(legacyF9[cmd] or 0)+1
end,emu.callbackType.exec,0x030069D8,0x030069D8)
local function dumpLibrary(name)
 local legacy={}
 for k,v in pairs(legacyF9) do legacy[#legacy+1]=string.format('"%d":%d',k,v) end
 write(name..'_library.json','{"loads":['..table.concat(loaderRows,',')..'],"hook_calls":['..table.concat(hookRows,',')..'],"legacy_f9":{'..table.concat(legacy,',')..'}}')
end
'''


def main():
    rom = Path(fixed.value("--rom")).resolve()
    manifest_path = rom.with_suffix(".json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require_hash(rom, manifest["output_sha256"])
    ext = manifest["fixedcell_extension"]
    header = next(r for r in manifest["archives"] if r["archive"] == "6D9EC0")
    if header["compression"]["destination"] != 0x02024000:
        raise ValueError("library observation destination changed")
    code = EXTRA.replace("HEADER_BYTES", str(header["compiled_bytes"])).replace("HOOK_ADDRESS", str(0x08000000 + ext["hook_offset"]))
    fixed.PROBE += code
    for old, new in (("local function capture(name)\n", "local function capture(name)\n dumpLibrary(name)\n"),
                     ("local function finish()\n", "local function finish()\n dumpLibrary('final')\n")):
        if fixed.runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError("runner capture anchor drift")
        fixed.runner.LUA_TEMPLATE = fixed.runner.LUA_TEMPLATE.replace(old, new, 1)
    result = fixed.main()
    out = Path(fixed.value("--out")).resolve()
    (out / "library_environment.json").write_text(json.dumps({
        "manifest_sha256": sha(manifest_path.read_bytes()), "rom_sha256": manifest["output_sha256"],
        "library_probe_sha256": sha(Path(__file__).read_bytes()),
        "fixedcell_probe_sha256": sha(Path(fixed.__file__).read_bytes()),
        "scope": "normal input; read-only whole-EWRAM loader guard, F9FC ABI, legacy F9 counts and fixed-cell transfers"
    }, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
