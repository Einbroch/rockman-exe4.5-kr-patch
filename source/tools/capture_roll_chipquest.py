"""Quarantined PET13 display and read-only external chip-name glyph trace."""
import json,sys
from pathlib import Path
import capture_roll_pet_license as base
from build_visibility_poc import ROOT,sha
from archive_scripts import script_spans

def main():
    a=sys.argv;out=Path(a[a.index('--out')+1]);script=int(a[a.index('--talk-script')+1]);rp=Path(a[a.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());ar=next(x for x in m['archives'] if x['archive']=='664E28');pool=0x08000000+ar['rom_offset'];end=pool+ar['compiled_bytes']
    if script!=13:raise ValueError('unregistered chip quest entry')
    original=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes();span=script_spans(original[0x664E28:0x664E28+2158],255)[13]
    base.normal.pet.PROBE+=f'''
local chipDraws={{}}
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=s['cpu.r5'];local stream=s['cpu.r4']
 if ctx~=0x0200FA20 or (stream>={pool} and stream<{end}) then return end
 local root=0;for i=0,3 do root=root+emu.read(ctx+0x30+i,emu.memType.gbaMemory)*2^(8*i) end
 if root~={pool} then return end
 chipDraws[#chipDraws+1]=string.format('{{"frame":%d,"stream":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}}',frame,stream,s['cpu.r1'],s['cpu.r6'],ctx,emu.read(ctx+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
local function dumpChip(name)
 write(name..'_chip_draws.json','{{"draws":['..table.concat(chipDraws,',')..']}}')
end
'''
    marker='local function capture(name)\n'
    if base.normal.pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('chip trace capture anchor')
    base.normal.pet.runner.LUA_TEMPLATE=base.normal.pet.runner.LUA_TEMPLATE.replace(marker,marker+' dumpChip(name)\n',1)
    base.SCRIPTS=[13];rc=base.main();p=out/'license_environment.json';e=json.loads(p.read_text());e.update(wrapper='capture_roll_chipquest.py',wrapper_sha256=sha(Path(__file__).read_bytes()),source_script_sha256=sha(span),scope='DIAGNOSTIC PET alias0 to13; printChip0/104 preserved, external glyph reads only. Not normal quest progression.');p.write_text(json.dumps(e,indent=2),encoding='utf-8');return rc

if __name__=='__main__':raise SystemExit(main())
