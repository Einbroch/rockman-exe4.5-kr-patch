"""Read-only outer native caller/context at the fixed-cell wrapper boundary."""
import json
from pathlib import Path
import capture_library_qa as library
from build_visibility_poc import sha


def main():
    fixed=library.fixed
    fixed.PROBE+=r'''
local monoParents={}
local function parentWord(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(i*8) end;return v
end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r6']~=0x08619EF8 then return end
 local sp=s['cpu.r13'];local root=parentWord(s['cpu.r10']);local menu=parentWord(s['cpu.r10']+0x34)
 monoParents[#monoParents+1]=string.format('{"stream":%d,"width":%d,"height":%d,"sp":%d,"saved_r9":%d,"saved_r8":%d,"outer_lr":%d,"wrapper_lr":%d,"context":%d,"root_job":%d,"menu":%d,"phase":%d}',s['cpu.r0'],s['cpu.r4'],s['cpu.r5'],sp,parentWord(sp),parentWord(sp+4),parentWord(sp+8),s['cpu.r14'],s['cpu.r10'],emu.read(root,emu.memType.gbaMemory),emu.read(menu,emu.memType.gbaMemory),emu.read(menu+1,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006824,0x03006824)
local function dumpMonoParents(name)
 write(name..'_mono_parents.json','{"calls":['..table.concat(monoParents,',')..']}')
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpMonoParents(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpMonoParents('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1: raise ValueError('mono parent capture anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=library.main();out=Path(fixed.value('--out'))
    r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_mono_parents.json').read_text())
    valid=rc==0 and r['complete'] and bool(d['calls'])
    (out/'mono_parent_environment.json').write_text(json.dumps({'rom_sha256':r['rom_sha256'],
        'tool_sha256':sha(Path(__file__).read_bytes()),'passed':valid,
        'scope':'normal controller input, read-only outer caller/context; no script/acquisition or RAM edits'},indent=2),encoding='utf-8')
    print('mono native parent:',valid,[(hex(c['outer_lr']),c['menu'],c['phase']) for c in d['calls']])
    return rc if valid else 1


if __name__=='__main__': raise SystemExit(main())
