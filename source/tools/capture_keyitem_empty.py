"""Read-only native loader/lookup plus existing RAM glyph/font observations."""
import json,sys
from pathlib import Path
import capture_fixedcell_probe as fixed
import capture_gutsman_calendar_management as management
from build_visibility_poc import sha

PROBE=r'''
local keyLoads={};local keyLookups={}
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']~=KEY_ROOT then return end
 keyLoads[#keyLoads+1]=string.format('{"frame":%d,"root":%d,"destination":%d,"lr":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'])
end,emu.callbackType.exec,0x080EC158,0x080EC158)
emu.addMemoryCallback(function()
 local s=emu.getState();local r=s['cpu.r0']
 if r~=0x02020800 and r~=0x02031000 then return end
 keyLookups[#keyLookups+1]=string.format('{"frame":%d,"root":%d,"script":%d,"lr":%d}',frame,r,s['cpu.r1'],s['cpu.r14'])
end,emu.callbackType.exec,0x0804FB4C,0x0804FB4C)
local function dumpKeyitem(name)
 write(name..'_keyitem.json','{"observer_only":true,"loads":['..table.concat(keyLoads,',')..'],"lookups":['..table.concat(keyLookups,',')..']}')
end
'''

def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text())
    root=0x08000000+next(a['rom_offset']for a in m['archives']if a['archive']=='709408')
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('keyitem capture anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,PROBE.replace('KEY_ROOT',str(root))+marker+' dumpKeyitem(name)\n',1)
    rc=management.main()
    out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'keyitem_environment.json').write_text(json.dumps(dict(observer_only=True,root=root,
        self_sha256=sha(Path(__file__).read_bytes()),rom_sha256=m['output_sha256']),indent=2),encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
