"""Read-only CPU access census around native keyboard state, not free RAM proof."""
import json,sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha

def main():
    extra=r'''
local workspaceAccess={}
local workspaceCount=0
local function observeWorkspace(kind,a,v)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address'];local bucket=math.floor(a/16)*16
 local key=string.format('%s:%08x:%08x',kind,pc,bucket);local r=workspaceAccess[key]
 if r then r.hits=r.hits+1;r.last=frame;r.min=math.min(r.min,a);r.max=math.max(r.max,a)
 else
  workspaceCount=workspaceCount+1
  if workspaceCount>10000 then error('workspace census limit') end
  workspaceAccess[key]={kind=kind,pc=pc,bucket=bucket,hits=1,first=frame,last=frame,min=a,max=a,lr=s['cpu.r14']}
 end
end
emu.addMemoryCallback(function(a,v) observeWorkspace('read',a,v) end,emu.callbackType.read,0x0200FC40,0x0200FFFF)
emu.addMemoryCallback(function(a,v) observeWorkspace('write',a,v) end,emu.callbackType.write,0x0200FC40,0x0200FFFF)
local function dumpWorkspace(name)
 local rows={}
 for _,r in pairs(workspaceAccess) do
  rows[#rows+1]=string.format('{"kind":"%s","pc":%d,"bucket":%d,"hits":%d,"first":%d,"last":%d,"min":%d,"max":%d,"lr":%d}',r.kind,r.pc,r.bucket,r.hits,r.first,r.last,r.min,r.max,r.lr)
 end
 write(name..'_workspace.json','{"observed_window":[33619008,33619967],"accesses":['..table.concat(rows,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(anchor,extra+anchor+' dumpWorkspace(name)\n',1)
    rc=native.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'workspace_environment.json').write_text(json.dumps(dict(observer_only=True,window=[0x0200fc40,0x0200ffff],tool_sha256=sha(Path(__file__).read_bytes()),native_observer_sha256=sha(Path(native.__file__).read_bytes()),limits=['Observed normal route access census only; absence does not prove unused or safely reservable RAM.','No RAM/record/script/progress edits or ROM modifications.']),indent=2),encoding='utf8');return rc

if __name__=='__main__':raise SystemExit(main())
