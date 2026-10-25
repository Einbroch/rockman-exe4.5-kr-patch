"""Read-only common confirmation renderer and candidate native record writer."""
import json,sys
from pathlib import Path
import capture_roll_family as base
from build_visibility_poc import sha

def main():
    code=r'''
local inputWrites={}
emu.addMemoryCallback(function(a,v)
 if #inputWrites>=50000 then error('input write observation overflow') end
 local s=emu.getState();inputWrites[#inputWrites+1]=string.format('{"frame":%d,"address":%d,"before":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"lr":%d}',frame,a,emu.read(a,emu.memType.gbaMemory),v,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r14'])
end,emu.callbackType.write,0x020010A6,0x020010AC)
local function dumpInputWrites(name)
 write(name..'_input_writes.json','{"writes":['..table.concat(inputWrites,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if base.pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('input capture anchor')
    base.pet.runner.LUA_TEMPLATE=base.pet.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpInputWrites(name)\n',1)
    base.ARCHIVE='6368E8';rc=base.main()
    out=Path(sys.argv[sys.argv.index('--out')+1]);rp=Path(sys.argv[sys.argv.index('--rom')+1])
    (out/'input_observer_environment.json').write_text(json.dumps(dict(observer_only=True,no_aliases=True,no_external_RAM_writes=True,rom_sha256=sha(rp.read_bytes()),self_sha256=sha(Path(__file__).read_bytes()),watched_write_range=[0x020010A6,0x020010AC],limits=['Candidate seven-byte window only; field identity, complete ABI, Hangul capacity and persistence remain unresolved.']),indent=2),encoding='utf8')
    return rc
if __name__=='__main__':raise SystemExit(main())
