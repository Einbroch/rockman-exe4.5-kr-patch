"""Observe native editor ownership and call stacks; no game/ROM writes."""
import json,sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha

def main():
    code=r'''
local adapterCalls={};local adapterAccess={};local adapterCount=0
local function observeAdapter(kind,a)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address'];local sp=s['cpu.r13'];local lr=s['cpu.r14']
 local key=string.format('%s:%08x:%08x',kind,pc,math.floor(a/16)*16)
 local row=adapterAccess[key]
 if row then row.hits=row.hits+1;row.min=math.min(row.min,a);row.max=math.max(row.max,a);row.min_sp=math.min(row.min_sp,sp);row.max_sp=math.max(row.max_sp,sp)
 else
  adapterCount=adapterCount+1;if adapterCount>10000 then error('adapter observation overflow') end
  adapterAccess[key]={kind=kind,pc=pc,min=a,max=a,hits=1,min_sp=sp,max_sp=sp,lr=lr,first=frame}
 end
end
emu.addMemoryCallback(function(a) observeAdapter('read',a) end,emu.callbackType.read,0x0200FC60,0x0200FC9F)
emu.addMemoryCallback(function(a) observeAdapter('write',a) end,emu.callbackType.write,0x0200FC60,0x0200FC9F)
for _,pc in ipairs({0x080355B6,0x0803558C,0x080353B0,0x08035494,0x080354C8,0x080355F6,0x08035620,0x0803562C,0x08035038,0x08035000,0x08035344,0x080356D0}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local key=string.format('%08x:%08x:%08x',pc,s['cpu.r14'],s['cpu.r13'])
  local row=adapterCalls[key]
  if row then row.hits=row.hits+1 else
   adapterCalls[key]={pc=pc,lr=s['cpu.r14'],sp=s['cpu.r13'],hits=1,first=frame,r0=s['cpu.r0'],r1=s['cpu.r1'],r2=s['cpu.r2'],r3=s['cpu.r3'],r4=s['cpu.r4'],r5=s['cpu.r5']}
  end
 end,emu.callbackType.exec,pc,pc)
end
local function dumpAdapter(name)
 local calls={};local accesses={}
 for _,r in pairs(adapterCalls) do calls[#calls+1]=string.format('{"pc":%d,"lr":%d,"sp":%d,"hits":%d,"first":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"r5":%d}',r.pc,r.lr,r.sp,r.hits,r.first,r.r0,r.r1,r.r2,r.r3,r.r4,r.r5) end
 for _,r in pairs(adapterAccess) do accesses[#accesses+1]=string.format('{"kind":"%s","pc":%d,"lr":%d,"hits":%d,"min":%d,"max":%d,"min_sp":%d,"max_sp":%d,"first":%d}',r.kind,r.pc,r.lr,r.hits,r.min,r.max,r.min_sp,r.max_sp,r.first) end
 write(name..'_adapter.json','{"calls":['..table.concat(calls,',')..'],"accesses":['..table.concat(accesses,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpAdapter(name)\n',1)
    rc=native.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'adapter_environment.json').write_text(json.dumps(dict(observer_only=True,window=[0x0200fc60,0x0200fca0],tool_sha256=sha(Path(__file__).read_bytes()),native_observer_sha256=sha(Path(native.__file__).read_bytes()),limits=['Normal Japanese input route, bounded PCs and memory window; no full lifetime/allocator/IRQ stack proof.','No RAM/record/progress injection or ROM changes.']),indent=2),encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
