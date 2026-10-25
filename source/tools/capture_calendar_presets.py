"""Read-only fixed-cell, default copy, commit and transient dialogue-name observer."""
import json
from pathlib import Path
import capture_fixedcell_probe as fixed
from build_visibility_poc import sha

EXTRA=r'''
local presetCalls={};local presetDraws={}
local function hexAt(a,n)
 local t={};for i=0,n-1 do t[#t+1]=string.format('%02X',emu.read(a+i,emu.memType.gbaMemory)) end
 return table.concat(t)
end
for _,pc in ipairs({0x08032AC6,0x08032AD4,0x08032F9A,0x08037366}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local regs={}
  for i=0,14 do regs[#regs+1]=tostring(s['cpu.r'..i]) end
  if #presetCalls>=1000 then error('preset calls overflow') end
  presetCalls[#presetCalls+1]=string.format('{"frame":%d,"pc":%d,"registers":[%s],"name_hex":"%s"}',frame,pc,table.concat(regs,','),hexAt(0x02026080,32))
 end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=s['cpu.r5'];local stream=s['cpu.r4']
 if ctx~=0x0200FA20 or stream<0x02010C40 or stream>=0x02010C60 then return end
 if #presetDraws>=1000 then error('preset draws overflow') end
 presetDraws[#presetDraws+1]=string.format('{"frame":%d,"stream":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}',frame,stream,s['cpu.r1'],s['cpu.r6'],ctx,emu.read(ctx+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
local function dumpPresets(name)
 write(name..'_preset_path.json','{"observer_only":true,"calls":['..table.concat(presetCalls,',')..'],"draws":['..table.concat(presetDraws,',')..']}')
end
'''

def main():
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('preset observer anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,EXTRA+marker+' dumpPresets(name)\n',1)
    rc=fixed.main();out=Path(fixed.value('--out'))
    (out/'preset_path_environment.json').write_text(json.dumps({'observer_only':True,'self_sha256':sha(Path(__file__).read_bytes()),'fixed_probe_sha256':sha(Path(fixed.__file__).read_bytes())},indent=2),encoding='utf-8');return rc

if __name__=='__main__':raise SystemExit(main())
