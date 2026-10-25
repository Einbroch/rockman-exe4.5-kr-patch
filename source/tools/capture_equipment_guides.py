"""Read-only guide lookup, native ABI, glyph source and font-read observations."""
import json
from pathlib import Path
import capture_equipment_labels as labels
from build_visibility_poc import require_hash

PROBE=r'''
local guideEntries={};local guideCalls={};local guideReturns={};local guideDraws={};local guideFonts={};local guideLookups={}
local function wordAt(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(i*8) end;return v
end
local function regs(s)
 local r={};for i=0,15 do r[#r+1]=tostring(s['cpu.r'..i]) end;return '['..table.concat(r,',')..']'
end
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=wordAt(s['cpu.r10']+0x40);local navi=emu.read(ctx+1,emu.memType.gbaMemory)
 guideEntries[#guideEntries+1]=string.format('{"frame":%d,"navi":%d,"regs":%s}',frame,navi,regs(s))
end,emu.callbackType.exec,0x0803C478,0x0803C478)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r14']~=0x0803C485 then return end
 guideCalls[#guideCalls+1]=string.format('{"frame":%d,"regs":%s,"saved_lr":%d}',frame,regs(s),wordAt(s['cpu.r13']))
end,emu.callbackType.exec,0x0804F7B6,0x0804F7B6)
emu.addMemoryCallback(function()
 local s=emu.getState();guideReturns[#guideReturns+1]=string.format('{"frame":%d,"regs":%s,"saved_lr":%d}',frame,regs(s),wordAt(s['cpu.r13']))
end,emu.callbackType.exec,0x0803C484,0x0803C484)
emu.addMemoryCallback(function()
local s=emu.getState();local stream=s['cpu.r4'];if not (GUIDE_RANGES) then return end
 guideDraws[#guideDraws+1]=string.format('{"frame":%d,"stream":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}',frame,stream,s['cpu.r1'],s['cpu.r6'],s['cpu.r5'],emu.read(s['cpu.r5']+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
emu.addMemoryCallback(function()
 local s=emu.getState();local stream=s['cpu.r0'];if not (GUIDE_RANGES) then return end
 guideLookups[#guideLookups+1]=string.format('{"frame":%d,"root":%d,"script_offset":%d,"regs":%s}',frame,stream,s['cpu.r1'],regs(s))
end,emu.callbackType.exec,0x0804FB76,0x0804FB76)
emu.addMemoryCallback(function(address)
 local index=math.floor((address-GUIDE_FONT)/96);guideFonts[index]=(guideFonts[index] or 0)+1
end,emu.callbackType.read,GUIDE_FONT,GUIDE_FONT_END-1)
local function dumpGuides(name)
 local rows={};for index,count in pairs(guideFonts) do rows[#rows+1]=string.format('{"index":%d,"reads":%d}',index,count) end
 write(name..'_guides.json','{"entries":['..table.concat(guideEntries,',')..'],"calls":['..table.concat(guideCalls,',')..'],"returns":['..table.concat(guideReturns,',')..'],"draws":['..table.concat(guideDraws,',')..'],"lookups":['..table.concat(guideLookups,',')..'],"font_reads":['..table.concat(rows,',')..']}')
end
'''
def main():
    fixed=labels.fixed;rp=Path(fixed.value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    ar=m['equipment_guides']['archive'];pool=0x08000000+ar['rom_offset'];ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=PROBE
    archives=[ar]+([m['equipment_guides']['roll_archive']] if 'roll_archive' in m['equipment_guides'] else [])
    archives+=m.get('keyitem_rom',{}).get('equipment_archives',[])
    ranges=['(stream>=%d and stream<%d)'%(0x08000000+a['rom_offset'],0x08000000+a['rom_offset']+a['compiled_bytes']) for a in archives]
    code=code.replace('GUIDE_RANGES',' or '.join(ranges))
    for key,value in [('GUIDE_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('GUIDE_FONT',font),('GUIDE_POOL',pool),('GUIDE_END',pool+ar['compiled_bytes'])]:code=code.replace(key,str(value))
    fixed.PROBE+=code
    marker='local function capture(name)\n';fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,marker+' dumpGuides(name)\n',1)
    return labels.main()

if __name__=='__main__':raise SystemExit(main())
