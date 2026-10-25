#!/usr/bin/env python3
"""Explicit read-substitution fixture; NOT normal play, no ROM/RAM/save edits."""
import json
import struct
from pathlib import Path
import capture_library_qa as library
from capture_chip_library_timing import PROBE
from build_visibility_poc import ROOT, require_hash, sha


FIXTURE = r'''
local stressDesc=nil
local stressReads=0
local stressNames=0
local stressRows=0
local stressOriginal={}
local function stressIndex(row,col)
 local v=row*8+col
 if v==55 then return 11171 end
 return v
end
emu.addMemoryCallback(function()
 if not timingGroup or timingGroup.descriptor<0x02000000 or timingGroup.descriptor+28>0x02040000 then stressFail('invalid descriptor precondition') end
 stressDesc=timingGroup.descriptor
 local key=tostring(stressDesc)
 if not stressOriginal[key] then stressOriginal[key]=hexAt(stressDesc,28) end
end,emu.callbackType.exec,0x08042E50,0x08042E50)
emu.addMemoryCallback(function(address,value)
 if not stressDesc or address<stressDesc or address>=stressDesc+28 then return end
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 local off=(address-stressDesc)%4
 if (pc==0x08042E84 and off==0) or (pc==0x08042EC8 and off==2) or (pc==0x0804302C and off==3) or (pc==0x0804303C and off==0) then
  stressReads=stressReads+1;return 1
 end
end,emu.callbackType.read,0x02000000,0x0203FFFF)
emu.addMemoryCallback(function(address,value)
 if not timingRow then return end
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 if pc<RENDER_START or pc>=RENDER_END then return end
 local n=address-TEST_STREAM
 if n<0 or n>32 then stressFail('fixture stream overflow') end
 stressNames=stressNames+1
 if n==32 then return 0xE5 end
 local index=stressIndex(timingRow.row,math.floor(n/4))
 local part=n%4
 -- Mesen accepts integer callback returns only; Lua '/' makes row a float.
 if part==0 then return 0xF9 elseif part==1 then return 0xFC elseif part==2 then return math.floor(index%256) else return math.floor(index/256) end
end,emu.callbackType.read,TEST_STREAM,TEST_STREAM+32)
emu.addMemoryCallback(function()
 local s=emu.getState();local row=(s['cpu.r2']-0x0201E600-16)/32
 if row%1~=0 or row<0 or row>6 or s['cpu.r1']~=0xE5 or s['cpu.r0']~=TEST_STREAM+32 then stressFail('stress row result failed') end
 local upper=0x0201E600+row*32
 for col=0,7 do
  local top=emu.read(upper+col*2,emu.memType.gbaMemory)+256*emu.read(upper+col*2+1,emu.memType.gbaMemory)
  local bot=emu.read(upper+16+col*2,emu.memType.gbaMemory)+256*emu.read(upper+17+col*2,emu.memType.gbaMemory)
  if top~=0xE202+row*16+col*2 or bot~=top+1 then stressFail('stress row tile failed') end
  if bytesAt(0x06008040+row*512+col*64,64)~=bytesAt(FONT_START+stressIndex(row,col)*64,64) then
   write('glyph_failure.json',string.format('{"row":%d,"column":%d,"expected_index":%d,"vram":"%s","font":"%s","copies":[%s]}',row,col,stressIndex(row,col),hexAt(0x06008040+row*512+col*64,64),hexAt(FONT_START+stressIndex(row,col)*64,64),table.concat(timingCopies,',')))
   stressFail('stress row glyph failed')
  end
 end
 stressRows=stressRows+1
end,emu.callbackType.exec,0x08042EE4,0x08042EE4)
local function dumpStress(name)
 if stressRows==0 or stressReads==0 or stressNames==0 then stressFail('missing fixture positive control') end
 local records={}
 for address,before in pairs(stressOriginal) do
  local after=hexAt(tonumber(address),28)
  if before~=after then stressFail('underlying descriptors changed') end
  records[#records+1]=string.format('{"address":%s,"before":"%s","after":"%s"}',address,before,after)
 end
 write(name..'_stress.json',string.format('{"descriptor_read_substitutions":%d,"name_byte_substitutions":%d,"verified_rows":%d,"descriptors":[%s]}',stressReads,stressNames,stressRows,table.concat(records,',')))
end
'''


def main():
    fixed = library.fixed
    rom = Path(fixed.value("--rom")).resolve()
    require_hash(rom, "ce839b60c8125da7ca8ce0240bcdfc82a8e8f5604202449af1acffa80158cbff")
    require_hash(ROOT / "tools/capture_chip_library_timing.py", "6a076f1a5812ef803f08306fbf865d997ea499aa08443bb01455e58605197789")
    m = json.loads(rom.with_suffix(".json").read_text(encoding="utf-8"))
    e = m["chip_library_extension"]
    blob = rom.read_bytes()
    stream = 0x08000000 + e["clone_offset"] + struct.unpack_from("<H", blob, e["clone_offset"] + 2)[0]
    render = e["machine_code"][0]
    ret = [i["address"] for i in render["instructions"] if i["mnemonic"] == "pop" and i["operands"] == "{r0, r2, r3}"]
    if len(ret) != 1:
        raise ValueError("copy-return boundary changed")
    code = "local function stressFail(s) write('fixture_failed.txt',s);emu.stop(1);error(s) end\n" + PROBE.replace("error(", "stressFail(") + FIXTURE
    for key, value in {"COPY_RETURN": ret[0], "RENDER_START": render["address"], "RENDER_END": render["address"] + render["code_bytes"], "TEST_STREAM": stream, "FONT_START": 0x08000000 + e["font_offset"]}.items():
        code = code.replace(key, str(value))
    fixed.PROBE += code
    for old, new in (("local function capture(name)\n", "local function capture(name)\n dumpTiming(name)\n if timingGroups[1] then dumpStress(name) end\n"),
                     ("local function finish()\n", "local function finish()\n dumpTiming('final')\n dumpStress('final')\n")):
        if fixed.runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError("fixture injection anchor changed")
        fixed.runner.LUA_TEMPLATE = fixed.runner.LUA_TEMPLATE.replace(old, new, 1)
    rc = library.main()
    out = Path(fixed.value("--out")).resolve()
    receipt = json.loads((out / "result.json").read_text(encoding="utf-8"))
    scope = "DIAGNOSTIC CPU read substitution: seven chip-1 descriptors, 56 Hangul cells and seven icons; acquisition/selection bypassed; NOT normal play"
    receipt["scope"] = scope
    receipt["normal_play_checkpoint_eligible"] = False
    checkpoint = out / "checkpoint.mss"
    if checkpoint.exists():
        checkpoint.rename(out / "diagnostic_checkpoint.mss")
        receipt["artifacts"]["diagnostic_checkpoint.mss"] = receipt["artifacts"].pop("checkpoint.mss")
    if (out / "fixture_failed.txt").exists():
        receipt["complete"] = False
        rc = 1
    for name in ("probe_environment.json", "library_environment.json"):
        env = json.loads((out / name).read_text(encoding="utf-8"))
        env["policy"] = scope
        env["scope"] = scope
        (out / name).write_text(json.dumps(env, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "result.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    env = json.loads((out / "probe_environment.json").read_text(encoding="utf-8"))
    if env["files_before"] != env["files_after"]:
        # RTC passage is normal; every disk save must still be identical.
        for name, before in env["files_before"].items():
            if name.endswith(".sav") and env["files_after"].get(name) != before:
                raise ValueError("fixture changed an isolated disk save")
    (out / "stress_environment.json").write_text(json.dumps({"scope": scope, "tool_sha256": sha(Path(__file__).read_bytes()),
        "timing_tool_sha256": sha((ROOT / "tools/capture_chip_library_timing.py").read_bytes()),
        "plan_sha256": sha((ROOT / "analysis/CHIP_LIBRARY_STRESS_PLAN.md").read_bytes()),
        "rom_sha256": sha(blob), "script_1_address": stream, "glyph_indices": list(range(55)) + [11171],
        "api_reference": "https://github.com/SourMesen/Mesen2/blob/master/Core/Debugger/ScriptingContext.cpp"}, indent=2), encoding="utf-8")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
