"""Read-only relocated Roll PET root, glyph-stream and font consumption probe."""
import json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import require_hash
ARCHIVE='65FA58'

PROBE=r'''
local petDraws={};local petCalls={};local petFonts={}
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']~=PET_POOL then return end
 petCalls[#petCalls+1]=string.format('{"frame":%d,"root":%d,"script":%d,"lr":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'])
end,emu.callbackType.exec,0x0804F7B6,0x0804F7B6)
emu.addMemoryCallback(function()
 local s=emu.getState();local stream=s['cpu.r4'];if stream<PET_POOL or stream>=PET_END then return end
 petDraws[#petDraws+1]=string.format('{"frame":%d,"stream":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}',frame,stream,s['cpu.r1'],s['cpu.r6'],s['cpu.r5'],emu.read(s['cpu.r5']+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
emu.addMemoryCallback(function(address)
 local index=math.floor((address-PET_FONT)/96);petFonts[index]=(petFonts[index] or 0)+1
end,emu.callbackType.read,PET_FONT,PET_FONT_END-1)
local function dumpRollPet(name)
 local rows={};for index,count in pairs(petFonts) do rows[#rows+1]=string.format('{"index":%d,"reads":%d}',index,count) end
 write(name..'_roll_pet.json','{"calls":['..table.concat(petCalls,',')..'],"draws":['..table.concat(petDraws,',')..'],"font_reads":['..table.concat(rows,',')..']}')
end
'''

def main():
    import sys
    args=sys.argv;rp=Path(args[args.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    ar=next(a for a in m['archives'] if a['archive']==ARCHIVE);pool=0x08000000+ar['rom_offset'];ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=PROBE
    for key,value in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+ar['compiled_bytes'])]:code=code.replace(key,str(value))
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpRollPet(name)\n',1)
    return runner.main()

if __name__=='__main__':raise SystemExit(main())
