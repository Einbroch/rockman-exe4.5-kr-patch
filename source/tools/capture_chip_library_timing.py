#!/usr/bin/env python3
"""Read-only scene/copy timing on the frozen cumulative ROM, muted Mesen only."""
import json
from pathlib import Path
import capture_chip_library_qa as chip
from build_visibility_poc import ROOT, require_hash, sha


PROBE = r'''
local timingGroups={}
local timingGroup=nil
local timingRow=nil
local timingRows={}
local timingCopy=nil
local timingCopies={}
local timingIcons={}
local timingIcon=nil
local timingUpdates={}
local timingUpdate=nil
local function timingPoint(s)
 return string.format('"clock":%d,"frame":%d,"scanline":%d,"cycle":%d',s.masterClock,s['ppu.frameCount'],s['ppu.scanline'],s['ppu.cycle'])
end
emu.addMemoryCallback(function()
 if timingGroup then error('nested name group') end
 local s=emu.getState()
 timingGroup={start=s,copies=0,rows=0,descriptor=s['cpu.r1']+s['cpu.r0']*4}
end,emu.callbackType.exec,0x08042E50,0x08042E50)
emu.addMemoryCallback(function()
 local s=emu.getState();local g=timingGroup
 if not g then error('name group exit without entry') end
 timingGroups[#timingGroups+1]=string.format('{"cycles":%d,"rows":%d,"copies":%d,"descriptor":%d,"start":{%s},"end":{%s}}',s.masterClock-g.start.masterClock,g.rows,g.copies,g.descriptor,timingPoint(g.start),timingPoint(s))
 timingGroup=nil
end,emu.callbackType.exec,0x08042F12,0x08042F12)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if not timingGroup or timingRow then error('invalid row nesting') end
 timingRow={start=s,copies=0,row=(s['cpu.r2']-0x0201E600)/32}
 timingGroup.rows=timingGroup.rows+1
end,emu.callbackType.exec,0x08042ED8,0x08042ED8)
emu.addMemoryCallback(function()
 local s=emu.getState();local r=timingRow
 if not r then error('row return without entry') end
 timingRows[#timingRows+1]=string.format('{"row":%d,"copies":%d,"cycles":%d,"start":{%s},"end":{%s}}',r.row,r.copies,s.masterClock-r.start.masterClock,timingPoint(r.start),timingPoint(s))
 timingRow=nil
end,emu.callbackType.exec,0x08042EE4,0x08042EE4)
emu.addMemoryCallback(function()
 local s=emu.getState();local dst=s['cpu.r1']
 if dst<0x06008040 or dst>=0x06008E40 then return end
 if not timingRow or timingCopy then error('copy nesting') end
 timingCopy=s
end,emu.callbackType.exec,0x08000956,0x08000956)
emu.addMemoryCallback(function()
 local s=emu.getState();local c=timingCopy
 if not c then error('copy return without entry') end
 local src,dst=c['cpu.r0'],c['cpu.r1']
 if c['cpu.r2']~=64 or bytesAt(src,64)~=bytesAt(dst,64) then error('real BIOS pixel-copy mismatch') end
 timingCopies[#timingCopies+1]=string.format('{"cycles":%d,"source":%d,"destination":%d,"start":{%s},"end":{%s}}',s.masterClock-c.masterClock,src,dst,timingPoint(c),timingPoint(s))
 timingRow.copies=timingRow.copies+1;timingGroup.copies=timingGroup.copies+1
 timingCopy=nil
end,emu.callbackType.exec,COPY_RETURN,COPY_RETURN)
for _,pair in ipairs({{0x08042BB4,0x08042C26},{0x08042C48,0x08042CBA},{0x08042CC8,0x08042D3A}}) do
 emu.addMemoryCallback(function()
  if timingUpdate then error('nested library update') end
  timingUpdate={start=emu.getState(),entry=pair[1]}
 end,emu.callbackType.exec,pair[1],pair[1])
 emu.addMemoryCallback(function()
  local s=emu.getState();local u=timingUpdate
  if not u then error('update return without entry') end
  timingUpdates[#timingUpdates+1]=string.format('{"entry":%d,"cycles":%d,"start":{%s},"end":{%s}}',u.entry,s.masterClock-u.start.masterClock,timingPoint(u.start),timingPoint(s))
  timingUpdate=nil
 end,emu.callbackType.exec,pair[2],pair[2])
end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if timingIcon then error('nested conditional icon') end
 timingIcon={start=s,source=0,destination=0}
end,emu.callbackType.exec,0x0804303A,0x0804303A)
emu.addMemoryCallback(function()
 if not timingIcon then return end
 local s=emu.getState()
 if s['cpu.r2']~=128 then error('icon copy length changed') end
 timingIcon.source=s['cpu.r0'];timingIcon.destination=s['cpu.r1']
end,emu.callbackType.exec,0x08000968,0x08000968)
emu.addMemoryCallback(function()
 local s=emu.getState();local c=timingIcon
 if not c or c.source==0 or bytesAt(c.source,128)~=bytesAt(c.destination,128) then error('icon BIOS transfer failed') end
 timingIcons[#timingIcons+1]=string.format('{"source":%d,"destination":%d,"cycles":%d}',c.source,c.destination,s.masterClock-c.start.masterClock)
 timingIcon=nil
end,emu.callbackType.exec,0x0804304C,0x0804304C)
local function dumpTiming(name)
 write(name..'_timing.json','{"groups":['..table.concat(timingGroups,',')..'],"rows":['..table.concat(timingRows,',')..'],"copies":['..table.concat(timingCopies,',')..'],"icons":['..table.concat(timingIcons,',')..'],"updates":['..table.concat(timingUpdates,',')..']}')
end
'''


def main():
    fixed = chip.library.fixed
    rom = Path(fixed.value("--rom")).resolve()
    require_hash(rom, "ce839b60c8125da7ca8ce0240bcdfc82a8e8f5604202449af1acffa80158cbff")
    manifest = json.loads(rom.with_suffix(".json").read_text(encoding="utf-8"))
    render = manifest["chip_library_extension"]["machine_code"][0]
    ret = [i["address"] for i in render["instructions"] if i["mnemonic"] == "pop" and i["operands"] == "{r0, r2, r3}"]
    if len(ret) != 1:
        raise ValueError("copy return boundary changed")
    fixed.PROBE += PROBE.replace("COPY_RETURN", str(ret[0]))
    for old, new in (("local function capture(name)\n", "local function capture(name)\n dumpTiming(name)\n"),
                     ("local function finish()\n", "local function finish()\n dumpTiming('final')\n")):
        if fixed.runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError("timing capture anchor drift")
        fixed.runner.LUA_TEMPLATE = fixed.runner.LUA_TEMPLATE.replace(old, new, 1)
    result = chip.main()
    out = Path(fixed.value("--out")).resolve()
    data = json.loads((out / "final_timing.json").read_text(encoding="utf-8"))
    if not data["groups"] or not data["copies"]:
        raise ValueError("missing positive timing controls")
    (out / "timing_environment.json").write_text(json.dumps({"tool_sha256": sha(Path(__file__).read_bytes()),
        "rom_sha256": sha(rom.read_bytes()), "scope": "read-only Mesen masterClock observations; muted; no hardware or worst-case claim"}, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
