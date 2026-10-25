#!/usr/bin/env python3
"""Read-only chip-name/VRAM residency survey on the unchanged library-v1 ROM.

No runtime patch or free-space adoption. Full active BG maps are checked each
frame after library initialization; helper copies and candidate writes provide
independent positive/negative observations. Observation remains active after
library initialization, including exit, so a candidate cannot hide a later user.
"""
import json
from pathlib import Path
import capture_fixedcell_probe as fixed
from build_visibility_poc import ROOT, require_hash, sha


PROBE = r'''
local chipRows={}
local chipActive=nil
local chipSeen={}
local copies={}
local copySeen={}
local libraryActive=false
local checkedFrames=0
local mapRefs={}
local candidateWrites={}
local candidateWriteCount=0
local candidateWriteSites={}
local mapTileCounts={}
local mapTileFirst={}
local mapTileLast={}
local controlWrites=0
local function u16(at)
 return emu.read(at,emu.memType.gbaMemory)+emu.read(at+1,emu.memType.gbaMemory)*256
end
emu.addMemoryCallback(function() libraryActive=true end,emu.callbackType.exec,0x080427A8,0x080427A8)
emu.addMemoryCallback(function()
 if chipActive~=nil then error('nested chip parser') end
 local s=emu.getState()
 chipActive={stream=s['cpu.r0'],upper=s['cpu.r2'],lower=s['cpu.r3'],base=s['cpu.r6'],caller=s['cpu.r14'],frame=frame,prefix=hexAt(s['cpu.r0'],24)}
end,emu.callbackType.exec,0x08042FB0,0x08042FB0)
emu.addMemoryCallback(function()
 if chipActive==nil then error('chip parser exit without entry') end
 local s=emu.getState();local c=chipActive
 local key=c.stream..':'..c.upper..':'..c.lower..':'..c.base
 local old=chipSeen[key]
 if old then old.count=old.count+1
 else
  c.count=1;c.after_stream=s['cpu.r0'];c.after_upper=s['cpu.r2'];c.after_lower=s['cpu.r3']
  c.top=hexAt(c.upper,16);c.bottom=hexAt(c.lower,16)
  chipRows[#chipRows+1]=c;chipSeen[key]=c
 end
 chipActive=nil
end,emu.callbackType.exec,0x08042FE2,0x08042FE2)
for _,pc in ipairs({0x08000956,0x08000968,0x0800097C,0x08000850}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local dst=s['cpu.r1'];local size=s['cpu.r2']
  if dst<0x06000000 or dst>=0x06018000 then return end
  local key=pc..':'..s['cpu.r0']..':'..dst..':'..size..':'..s['cpu.r14']
  local old=copySeen[key]
  if old then old.count=old.count+1
  else
   local c={pc=pc,source=s['cpu.r0'],destination=dst,bytes=size,caller=s['cpu.r14'],count=1,frame=frame}
   copies[#copies+1]=c;copySeen[key]=c
  end
 end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function(address,value)
 if not libraryActive then return end
 candidateWriteCount=candidateWriteCount+1
 local s=emu.getState();local pc=s['cpu.r15']
 candidateWriteSites[pc]=(candidateWriteSites[pc] or 0)+1
 if #candidateWrites<32 then
  candidateWrites[#candidateWrites+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d}',frame,address,value,s['cpu.r15'])
 end
end,emu.callbackType.write,0x06008000,0x06008FFF)
emu.addMemoryCallback(function()
 if libraryActive then controlWrites=controlWrites+1 end
end,emu.callbackType.write,0x0600E000,0x0600FFFF)
emu.addEventCallback(function()
 if not libraryActive then return end
 checkedFrames=checkedFrames+1
 local disp=u16(0x04000000)
 if disp%8~=0 then error('survey only supports mode 0') end
 for bg=0,3 do
  if math.floor(disp/2^(8+bg))%2==1 then
   local ctl=u16(0x04000008+bg*2)
   if math.floor(ctl/128)%2~=0 then error('survey only supports 4bpp BG') end
   local cb=math.floor(ctl/4)%4*0x4000
   -- A base below 0x4000 cannot address the 0x8000 candidate with 10-bit tiles.
   if cb>=0x4000 then
    local sb=math.floor(ctl/256)%32*0x800
    local mode=math.floor(ctl/0x4000)%4
    local blocks=mode==3 and 4 or (mode==0 and 1 or 2)
    for i=0,blocks*1024-1 do
     local tile=u16(0x06000000+sb+i*2)%1024
     local at=cb+tile*32
     if at>=0x8000 and at<0x9000 then
      local key=at
      mapTileCounts[key]=(mapTileCounts[key] or 0)+1
      mapTileFirst[key]=mapTileFirst[key] or frame
      mapTileLast[key]=frame
      if #mapRefs<32 then
       mapRefs[#mapRefs+1]=string.format('{"frame":%d,"bg":%d,"map_offset":%d,"tile_address":%d,"control":%d,"dispcnt":%d}',frame,bg,sb+i*2,0x06000000+at,ctl,disp)
      end
     end
    end
   end
  end
 end
end,emu.eventType.endFrame)
local function dumpLibraryChipSurvey(name)
 local rows={};local copyRows={};local mapTiles={};local writeSites={}
 for _,c in ipairs(chipRows) do
  rows[#rows+1]=string.format('{"stream":%d,"upper":%d,"lower":%d,"base":%d,"caller":%d,"frame":%d,"count":%d,"after_stream":%d,"after_upper":%d,"after_lower":%d,"prefix_hex":"%s","top_hex":"%s","bottom_hex":"%s"}',c.stream,c.upper,c.lower,c.base,c.caller,c.frame,c.count,c.after_stream,c.after_upper,c.after_lower,c.prefix,c.top,c.bottom)
 end
 for _,c in ipairs(copies) do
  copyRows[#copyRows+1]=string.format('{"pc":%d,"source":%d,"destination":%d,"bytes":%d,"caller":%d,"frame":%d,"count":%d}',c.pc,c.source,c.destination,c.bytes,c.caller,c.frame,c.count)
 end
 for at=0x8000,0x8FE0,32 do
  if mapTileCounts[at] then
   mapTiles[#mapTiles+1]=string.format('{"tile_address":%d,"map_entry_frame_count":%d,"first_frame":%d,"last_frame":%d}',0x06000000+at,mapTileCounts[at],mapTileFirst[at],mapTileLast[at])
  end
 end
 for pc,count in pairs(candidateWriteSites) do
  writeSites[#writeSites+1]=string.format('{"pc":%d,"count":%d}',pc,count)
 end
 write(name..'_chip_survey.json','{"rows":['..table.concat(rows,',')..'],"copies":['..table.concat(copyRows,',')..'],"checked_frames":'..checkedFrames..',"candidate_writes":['..table.concat(candidateWrites,',')..'],"candidate_write_count":'..candidateWriteCount..',"candidate_write_sites":['..table.concat(writeSites,',')..'],"candidate_map_references":['..table.concat(mapRefs,',')..'],"candidate_map_tile_histogram":['..table.concat(mapTiles,',')..'],"control_map_write_count":'..controlWrites..'}')
end
'''


def main():
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    source_path = ROOT / config["source_profile"]["filename"]
    require_hash(source_path, config["source_profile"]["sha256"])
    source = source_path.read_bytes()
    product = Path(fixed.value("--rom")).read_bytes()
    # This observer assumes the exact native row parser, callers and copy helpers.
    native_ranges = ((0x42E50, 0x43078), (0x42778, 0x428E4), (0x850, 0x888),
                     (0x94C, 0x992))
    for start, end in native_ranges:
        if source[start:end] != product[start:end]:
            # The library title pointer at 428E0 is the sole allowed difference.
            if (start, end) != (0x42778, 0x428E4) or source[start:0x428E0] != product[start:0x428E0]:
                raise ValueError(f"native chip survey code changed at {start:X}")
    fixed.PROBE += PROBE
    for old, new in (("local function capture(name)\n", "local function capture(name)\n dumpLibraryChipSurvey(name)\n"),
                     ("local function finish()\n", "local function finish()\n dumpLibraryChipSurvey('final')\n")):
        if fixed.runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError("runner anchor drift")
        fixed.runner.LUA_TEMPLATE = fixed.runner.LUA_TEMPLATE.replace(old, new, 1)
    result = fixed.main()
    out = Path(fixed.value("--out"))
    receipt = json.loads((out / "result.json").read_text(encoding="utf-8"))
    if receipt.get("complete"):
        survey = json.loads((out / "final_chip_survey.json").read_text(encoding="utf-8"))
        if not survey["rows"] or not survey["copies"] or survey["checked_frames"] == 0:
            raise ValueError("completed segment has no chip survey coverage")
    (out / "chip_probe_environment.json").write_text(json.dumps({
        "probe_sha256": sha(Path(__file__).read_bytes()),
        "fixedcell_probe_sha256": sha(Path(fixed.__file__).read_bytes()),
        "native_ranges": [{"start": start, "end": end, "source_sha256": sha(source[start:end])}
                          for start, end in native_ranges],
        "scope": "read-only native chip parser, transfer footprints, per-frame active BG maps; candidate 06008000..06008FFF is NOT adopted by this probe"
    }, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
