#!/usr/bin/env python3
"""Read-only cumulative-ROM chip name, header and real BIOS transfer QA."""
import json
from pathlib import Path
import capture_library_qa as library
from build_visibility_poc import sha


PROBE = r'''
local chipKoActive=nil
local chipKoRows={}
local chipKoSeen={}
local chipKoCalls=0
local chipKoCopies=0
local chipKoCopy=nil
local chipKoCopyRows={}
local chipKoCopySeen={}
local function chipWord(at)
 return emu.read(at,emu.memType.gbaMemory)+256*emu.read(at+1,emu.memType.gbaMemory)
end
emu.addMemoryCallback(function()
 if chipKoActive~=nil then error('nested chip selector') end
 local s=emu.getState();local id=math.floor(s['cpu.r1']/0x1000000)
 local root=s['cpu.r0']
 local private=s['cpu.r9']==7 and s['cpu.r2']>=ROW_BUFFER and s['cpu.r2']<ROW_BUFFER+224 and s['cpu.r2']%32==0 and s['cpu.r3']==s['cpu.r2']+16 and s['cpu.r6']%4096==0 and root==SOURCE_POOL
 if private then root=PRIVATE_POOL end
 local stream=root+chipWord(root+id*2)
 local endAt=stream;local top={};local bottom={};local count=0
 while count<8 do
  local c=emu.read(endAt,emu.memType.gbaMemory)
  local tile=c*2
  if private and c==0xf9 and emu.read(endAt+1,emu.memType.gbaMemory)==0xfc then
   tile=TILE_START+(s['cpu.r2']-ROW_BUFFER)/2+count*2
   endAt=endAt+4
  elseif c<0xe5 then endAt=endAt+1
  else break end
  top[#top+1]=s['cpu.r6']+tile;bottom[#bottom+1]=s['cpu.r6']+tile+1;count=count+1
 end
 while #top<8 do top[#top+1]=0;bottom[#bottom+1]=0 end
 chipKoActive={s=s,root=root,id=id,stream=stream,endAt=endAt,top=top,bottom=bottom,private=private,frame=frame}
end,emu.callbackType.exec,INSTALL_ADDRESS,INSTALL_ADDRESS)
emu.addMemoryCallback(function()
 local c=chipKoActive
 if c==nil then error('chip selector return without entry') end
 local s=emu.getState();local b=c.s
 if s['cpu.r0']~=c.endAt or s['cpu.r1']~=emu.read(c.endAt,emu.memType.gbaMemory) or s['cpu.r2']~=b['cpu.r2']+16 or s['cpu.r3']~=b['cpu.r3']+16 or s['cpu.r14']~=CONTINUATION+1 then error('chip selector result ABI failure') end
 for r=4,13 do if s['cpu.r'..r]~=b['cpu.r'..r] then error('chip selector preserved register failure '..r) end end
 for i=0,7 do
  if chipWord(b['cpu.r2']+i*2)~=c.top[i+1] or chipWord(b['cpu.r3']+i*2)~=c.bottom[i+1] then error('chip tile/padding failure') end
 end
 chipKoCalls=chipKoCalls+1
 local key=c.root..':'..c.id..':'..b['cpu.r2']..':'..b['cpu.r6']
 local previous=chipKoSeen[key]
 if previous then previous.calls=previous.calls+1
 else
  c.calls=1;c.topHex=hexAt(b['cpu.r2'],16);c.bottomHex=hexAt(b['cpu.r3'],16)
  c.textHex=hexAt(c.stream,c.endAt-c.stream+1)
  chipKoRows[#chipKoRows+1]=c;chipKoSeen[key]=c
 end
 chipKoActive=nil
end,emu.callbackType.exec,CONTINUATION,CONTINUATION)
emu.addMemoryCallback(function()
 local s=emu.getState();local dst=s['cpu.r1']
 if dst<CACHE_START or dst>=CACHE_END then return end
 if chipKoCopy~=nil then error('nested chip glyph copy') end
 local src=s['cpu.r0']
 if s['cpu.r2']~=64 or dst+64>CACHE_END or (dst-CACHE_START)%64~=0 or src<FONT_START or src>=FONT_START+11172*64 or (src-FONT_START)%64~=0 then error('chip glyph copy outside contract') end
 chipKoCopy={src=src,dst=dst,frame=frame}
end,emu.callbackType.exec,COPY_HELPER,COPY_HELPER)
emu.addMemoryCallback(function()
 local c=chipKoCopy
 if c==nil then error('chip glyph copy returned without entry') end
 if bytesAt(c.src,64)~=bytesAt(c.dst,64) then error('real BIOS glyph transfer mismatch') end
 chipKoCopies=chipKoCopies+1
 local key=c.src..':'..c.dst
 if not chipKoCopySeen[key] then
  chipKoCopyRows[#chipKoCopyRows+1]=string.format('{"source":%d,"destination":%d,"frame":%d}',c.src,c.dst,c.frame)
  chipKoCopySeen[key]=true
 end
 chipKoCopy=nil
end,emu.callbackType.exec,COPY_RETURN,COPY_RETURN)
local function dumpChipKo(name)
 local rows={}
 for _,c in ipairs(chipKoRows) do
  rows[#rows+1]=string.format('{"root":%d,"script":%d,"stream":%d,"upper":%d,"base":%d,"private":%s,"frame":%d,"calls":%d,"text_hex":"%s","top_hex":"%s","bottom_hex":"%s"}',c.root,c.id,c.stream,c.s['cpu.r2'],c.s['cpu.r6'],c.private and 'true' or 'false',c.frame,c.calls,c.textHex,c.topHex,c.bottomHex)
 end
 write(name..'_chip_ko.json','{"abi_calls":'..chipKoCalls..',"verified_bios_copies":'..chipKoCopies..',"rows":['..table.concat(rows,',')..'],"copy_pairs":['..table.concat(chipKoCopyRows,',')..']}')
end
'''


def main():
    fixed = library.fixed
    rom = Path(fixed.value("--rom")).resolve()
    manifest = json.loads(rom.with_suffix(".json").read_text(encoding="utf-8"))
    ext = manifest["chip_library_extension"]
    spec = json.loads((library.ROOT / "tools/specs/exe45_chip_library_v1.json").read_text(encoding="utf-8"))
    render = ext["machine_code"][0]
    returns = [i["address"] for i in render["instructions"] if i["mnemonic"] == "pop" and i["operands"] == "{r0, r2, r3}"]
    if len(returns) != 1:
        raise ValueError("glyph copy-return boundary changed")
    substitutions = {"ROW_BUFFER": ext["buffer"]["start"], "SOURCE_POOL": 0x08000000 + spec["pool"]["offset"],
                     "PRIVATE_POOL": 0x08000000 + ext["clone_offset"], "TILE_START": (ext["vram"]["start"] - ext["vram"]["char_base"]) // 32,
                     "INSTALL_ADDRESS": 0x08000000 + ext["install"]["offset"], "CONTINUATION": ext["install"]["continuation"] & ~1,
                     "CACHE_START": ext["vram"]["start"], "CACHE_END": ext["vram"]["start"] + ext["vram"]["bytes"],
                     "FONT_START": 0x08000000 + ext["font_offset"], "COPY_HELPER": spec["copy_helper"] & ~1, "COPY_RETURN": returns[0]}
    code = PROBE
    for key, value in substitutions.items():
        code = code.replace(key, str(value))
    fixed.PROBE += code
    for old, new in (("local function capture(name)\n", "local function capture(name)\n dumpChipKo(name)\n"),
                     ("local function finish()\n", "local function finish()\n dumpChipKo('final')\n")):
        if fixed.runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError("chip capture anchor drift")
        fixed.runner.LUA_TEMPLATE = fixed.runner.LUA_TEMPLATE.replace(old, new, 1)
    result = library.main()
    out = Path(fixed.value("--out")).resolve()
    receipt = json.loads((out / "result.json").read_text(encoding="utf-8"))
    if receipt["complete"]:
        observed = json.loads((out / "final_chip_ko.json").read_text(encoding="utf-8"))
        if not observed["abi_calls"] or not observed["verified_bios_copies"]:
            raise ValueError("route completed without Korean chip-name evidence")
    (out / "chip_ko_environment.json").write_text(json.dumps({
        "probe_sha256": sha(Path(__file__).read_bytes()), "manifest_sha256": sha(rom.with_suffix(".json").read_bytes()),
        "substitutions": substitutions, "policy": "read-only normal-play ABI, tile, real BIOS pixel-copy assertions"
    }, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
