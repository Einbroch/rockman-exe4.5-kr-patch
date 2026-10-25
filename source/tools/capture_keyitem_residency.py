"""Read-only both keyitem loaders/readers and their native selection state."""
import json,sys
from pathlib import Path
import capture_fixedcell_probe as fixed
import capture_gutsman_calendar_management as base
from build_visibility_poc import sha

PROBE=r'''
local keyResidency={}
local function keyEvent(kind)
 local s=emu.getState();local v={}
 for i=0,15 do v[#v+1]=string.format('"r%d":%d',i,s['cpu.r'..i]) end
 keyResidency[#keyResidency+1]=string.format('{"frame":%d,"kind":"%s","registers":{%s}}',frame,kind,table.concat(v,','))
end
emu.addMemoryCallback(function() keyEvent('ui-loader') end,emu.callbackType.exec,0x080349DC,0x080349DC)
emu.addMemoryCallback(function() keyEvent('other-loader') end,emu.callbackType.exec,0x0804C5B4,0x0804C5B4)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r1']==0x02020800 or s['cpu.r1']==0x02031000 then keyEvent('decompress') end
end,emu.callbackType.exec,0x080EC158,0x080EC158)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']==0x02020800 or s['cpu.r0']==0x02031000 then keyEvent('lookup') end
end,emu.callbackType.exec,0x0804FB4C,0x0804FB4C)
local function dumpKeyResidency(name)
 write(name..'_key_residency.json','{"observer_only":true,"events":['..table.concat(keyResidency,',')..']}')
end
'''
def main():
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('residency capture anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,PROBE+marker+' dumpKeyResidency(name)\n',1)
    result=base.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'key_residency_environment.json').write_text(json.dumps(dict(observer_only=True,self_sha256=sha(Path(__file__).read_bytes())),indent=2)+'\n',encoding='utf8')
    return result
if __name__=='__main__':raise SystemExit(main())
