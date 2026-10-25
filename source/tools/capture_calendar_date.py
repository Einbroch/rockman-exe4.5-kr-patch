"""Read-only current-date buffer glyph draws plus normal/fixed observers."""
import json,sys
from pathlib import Path
import capture_roll_calendar_dialogue as base
from build_visibility_poc import sha
def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());ar=next(a for a in m['archives'] if a['archive']=='65F11C');pool=0x08000000+ar['rom_offset']
    code=r'''
local dateDraws={}
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=s['cpu.r5'];local stream=s['cpu.r4']
 if ctx~=0x0200FA20 or stream<0x02000000 or stream>=0x02040000 or emu.read(ctx+1,emu.memType.gbaMemory)~=0 then return end
 local root=0;for i=0,3 do root=root+emu.read(ctx+0x30+i,emu.memType.gbaMemory)*2^(8*i) end
 if root~=DATE_POOL then return end
 if #dateDraws>=1000 then error('date observer overflow') end
 dateDraws[#dateDraws+1]=string.format('{"frame":%d,"stream":%d,"byte":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}',frame,stream,emu.read(stream,emu.memType.gbaMemory),s['cpu.r1'],s['cpu.r6'],ctx,emu.read(ctx+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
local function dumpDate(name)
 write(name..'_date_ram.json','{"observer_only":true,"draws":['..table.concat(dateDraws,',')..']}')
end
'''.replace('DATE_POOL',str(pool))
    marker='local function capture(name)\n';runner=base.fixed.runner
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('date observer anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpDate(name)\n',1);rc=base.main();out=Path(sys.argv[sys.argv.index('--out')+1]);(out/'date_environment.json').write_text(json.dumps({'observer_only':True,'rom_sha256':m['output_sha256'],'pool':pool,'self_sha256':sha(Path(__file__).read_bytes()),'base_probe_sha256':sha(Path(base.__file__).read_bytes())},indent=2),encoding='utf-8');return rc
if __name__=='__main__':raise SystemExit(main())
