"""Read-only Roll return pool and native RAM nickname stream observation."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import require_hash

PROBE=r'''
local returnRamDraws={}
emu.addMemoryCallback(function()
 local s=emu.getState();local stream=s['cpu.r4'];local ctx=s['cpu.r5']
 if ctx~=0x0200FA20 or stream<0x02000000 or stream>=0x02040000 then return end
 local pool=0;for i=0,3 do pool=pool+emu.read(ctx+0x30+i,emu.memType.gbaMemory)*2^(8*i) end
 if pool~=RETURN_POOL then return end
 returnRamDraws[#returnRamDraws+1]=string.format('{"frame":%d,"stream":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}',frame,stream,s['cpu.r1'],s['cpu.r6'],ctx,emu.read(ctx+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
local function dumpReturn(name)
 write(name..'_return_ram.json','{"draws":['..table.concat(returnRamDraws,',')..']}')
end
'''

def main():
    a=sys.argv;rp=Path(a[a.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);ar=next((x for x in m['archives'] if x['archive']=='65FEC0'),None);pool=0x08000000+(ar['rom_offset'] if ar else 0x65FEC0);end=pool+(ar['compiled_bytes'] if ar else 123);ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE+PROBE.replace('RETURN_POOL',str(pool))
    for key,value in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',end)]:code=code.replace(key,str(value))
    marker='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('return capture anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpRollPet(name)\n dumpReturn(name)\n',1)
    return pet.runner.main()

if __name__=='__main__':raise SystemExit(main())
