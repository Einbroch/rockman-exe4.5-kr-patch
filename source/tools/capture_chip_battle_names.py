"""Read-only native battle-name font612E38/caller observation, no hook changes."""
import json
from pathlib import Path
import capture_library_qa as library
from build_visibility_poc import sha


def main():
    fixed=library.fixed
    old=" if fixedActive~=nil or #fixedCalls>=1000 then error('fixed-cell probe nesting/limit') end\n local s=emu.getState()"
    new=" local s=emu.getState()\n if s['cpu.r6']~=0x08612E38 then return end\n if fixedActive~=nil or #fixedCalls>=1000 then error('fixed-cell probe nesting/limit') end"
    if fixed.PROBE.count(old)!=1: raise ValueError('battle name entry filter anchor')
    fixed.PROBE=fixed.PROBE.replace(old,new)
    old=" if fixedActive==nil then error('fixed-cell exit without entry') end"
    if fixed.PROBE.count(old)!=1: raise ValueError('battle name exit filter anchor')
    fixed.PROBE=fixed.PROBE.replace(old,' if fixedActive==nil then return end')
    fixed.PROBE+=r'''
local battleNameParents={}
local function battleNameWord(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(i*8) end;return v
end
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r6']~=0x08612E38 then return end
 local sp=s['cpu.r13'];local ctx=s['cpu.r10'];local root=battleNameWord(ctx);local menu=battleNameWord(ctx+0x34)
 battleNameParents[#battleNameParents+1]=string.format('{"stream":%d,"font":%d,"width":%d,"height":%d,"target":%d,"outer_lr":%d,"wrapper_lr":%d,"context":%d,"root_job":%d,"menu":%d,"phase":%d}',s['cpu.r0'],s['cpu.r6'],s['cpu.r4'],s['cpu.r5'],s['cpu.r3'],battleNameWord(sp+8),s['cpu.r14'],ctx,emu.read(root,emu.memType.gbaMemory),emu.read(menu,emu.memType.gbaMemory),emu.read(menu+1,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006824,0x03006824)
local function dumpBattleNameParents(name)
 write(name..'_battle_name_parents.json','{"calls":['..table.concat(battleNameParents,',')..']}')
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpBattleNameParents(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpBattleNameParents('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1: raise ValueError('battle name capture anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=library.main();out=Path(fixed.value('--out'))
    route=json.loads((out/'result.json').read_text());calls=json.loads((out/'final_battle_name_parents.json').read_text())['calls']
    valid=rc==0 and route['complete'] and bool(calls) and not list(out.glob('*failed*'))
    (out/'battle_name_environment.json').write_text(json.dumps({'rom_sha256':route['rom_sha256'],
        'tool_sha256':sha(Path(__file__).read_bytes()),'passed':valid,'calls':len(calls),
        'scope':'normal controller input; read-only native font612E38/source/caller/staging observation; not Korean implementation or complete name consumer coverage'},indent=2),encoding='utf-8')
    print('native battle-name calls:',len(calls),'passed:',valid)
    return rc if valid else 1


if __name__=='__main__': raise SystemExit(main())
