"""Read-only native Navi selection and normal dialogue/font observations."""
import json
from pathlib import Path
import capture_fixedcell_probe as fixed
from build_visibility_poc import sha,require_hash

PROBE=r'''
local escapeSelections={}
local escapeDraws={}
local escapeFont={}
local function escapeWord(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(i*8) end;return v
end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']~=ESCAPE_POOL then error('Navi selector pool changed') end
 escapeSelections[#escapeSelections+1]=string.format('{"frame":%d,"pool":%d,"script":%d,"sp":%d,"return_lr":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r13'],escapeWord(s['cpu.r13']))
end,emu.callbackType.exec,0x080212E4,0x080212E4)
emu.addMemoryCallback(function()
 local s=emu.getState();local stream=s['cpu.r4']
 if stream<ESCAPE_POOL or stream>=ESCAPE_END then return end
 escapeDraws[#escapeDraws+1]=string.format('{"frame":%d,"stream":%d,"glyph_index":%d,"context":%d,"offset":%d,"color":%d}',frame,stream,s['cpu.r1'],s['cpu.r5'],s['cpu.r6'],emu.read(s['cpu.r5']+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
emu.addMemoryCallback(function(address)
 local index=math.floor((address-NORMAL_FONT)/96)
 escapeFont[index]=(escapeFont[index] or 0)+1
end,emu.callbackType.read,NORMAL_FONT,NORMAL_FONT_END-1)
local function dumpEscape(name)
 local rows={};for index,count in pairs(escapeFont) do rows[#rows+1]=string.format('{"index":%d,"reads":%d}',index,count) end
 write(name..'_escape.json','{"selections":['..table.concat(escapeSelections,',')..'],"draws":['..table.concat(escapeDraws,',')..'],"font_reads":['..table.concat(rows,',')..']}')
end
'''

def main():
    rom=Path(fixed.value('--rom'));m=json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'));require_hash(rom,m['output_sha256'])
    ar=next(a for a in m['archives'] if a['archive']=='76C944');ext=m['extension'];font=0x08000000+ext['normal_font_offset']
    code=PROBE
    for key,value in [('ESCAPE_END',0x08000000+ar['rom_offset']+ar['compiled_bytes']),('ESCAPE_POOL',0x08000000+ar['rom_offset']),
            ('NORMAL_FONT_END',font+(ext['legacy_index_view']+ext['hangul_syllables']+ext['extra_glyph_count'])*96),('NORMAL_FONT',font)]:code=code.replace(key,str(value))
    fixed.PROBE+=code
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpEscape(name)\n'),
            ('local function finish()\n',"local function finish()\n dumpEscape('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('escape capture anchor drift')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=fixed.main();out=Path(fixed.value('--out'));route=json.loads((out/'result.json').read_text());records=json.loads((out/'final_escape.json').read_text())
    env={'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'passed':rc==0 and route['complete'],
        'selected_scripts':sorted({s['script'] for s in records['selections']}),'normal_draws':len(records['draws']),
        'scope':'normal controller input; read-only native Navi selector and normal-dialogue source/font observations; not all escape outcomes'}
    (out/'escape_environment.json').write_text(json.dumps(env,indent=2),encoding='utf-8')
    print('escape observed:',env['selected_scripts'],'normal draws:',env['normal_draws'])
    return rc

if __name__=='__main__':raise SystemExit(main())
