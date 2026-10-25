"""Read-only native schedule pool and transient profile-buffer glyph observer."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,sha,require_hash

def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);ar=next(a for a in m['archives'] if a['archive']=='661754');pool=0x08000000+ar['rom_offset'];ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+ar['compiled_bytes'])]:code=code.replace(k,str(v))
    code+=f'''
local scheduleRamDraws={{}}
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=s['cpu.r5'];local stream=s['cpu.r4']
 if ctx~=0x0200FA20 or stream<0x02000000 or stream>=0x02040000 then return end
 local root=0;for i=0,3 do root=root+emu.read(ctx+0x30+i,emu.memType.gbaMemory)*2^(8*i) end
 if root~={pool} then return end
 scheduleRamDraws[#scheduleRamDraws+1]=string.format('{{"frame":%d,"stream":%d,"byte":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}}',frame,stream,emu.read(stream,emu.memType.gbaMemory),s['cpu.r1'],s['cpu.r6'],ctx,emu.read(ctx+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
local function dumpScheduleRam(name)
 write(name..'_schedule_ram.json','{{"draws":['..table.concat(scheduleRamDraws,',')..']}}')
end
'''
    marker='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('native schedule observer anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpRollPet(name)\n dumpScheduleRam(name)\n',1)
    rc=pet.runner.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'native_schedule_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'observer_only':True,'tool_sha256':sha(Path(__file__).read_bytes()),'probe_sha256':sha(Path(pet.__file__).read_bytes()),'pool':pool,'size':ar['compiled_bytes']},indent=2),encoding='utf-8');return rc

if __name__=='__main__':raise SystemExit(main())
