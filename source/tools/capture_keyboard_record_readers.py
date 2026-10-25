"""Observe CPU readers of the weak-subject record on a normal input route.

No emulator RAM writes, aliases, script/flag forcing, or save edits.
"""
import json,sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha

def main():
    code=r'''
local recordReaders={}
emu.addMemoryCallback(function(a,v)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address'];local key=tostring(pc)
 local row=recordReaders[key]
 if row then row.hits=row.hits+1;row.last=frame
 else
  local metadata=''
  if pc==0x08038BB4 and s['cpu.r6']>=0x08000000 and s['cpu.r6']<0x08800000 then
   local b={};for i=0,15 do b[#b+1]=string.format('%02x',emu.read(s['cpu.r6']+i,emu.memType.gbaMemory)) end;metadata=table.concat(b)
  end
  recordReaders[key]={pc=pc,hits=1,first=frame,last=frame,address=a,value=v,r0=s['cpu.r0'],r1=s['cpu.r1'],r2=s['cpu.r2'],r3=s['cpu.r3'],r4=s['cpu.r4'],r5=s['cpu.r5'],r6=s['cpu.r6'],r7=s['cpu.r7'],metadata=metadata,lr=s['cpu.r14']}
 end
end,emu.callbackType.read,0x020010A6,0x020010AF)
local function dumpRecordReaders(name)
 local rows={}
 for _,r in pairs(recordReaders) do
  rows[#rows+1]=string.format('{"pc":%d,"hits":%d,"first":%d,"last":%d,"address":%d,"value":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"r5":%d,"r6":%d,"r7":%d,"metadata_hex":"%s","lr":%d}',r.pc,r.hits,r.first,r.last,r.address,r.value,r.r0,r.r1,r.r2,r.r3,r.r4,r.r5,r.r6,r.r7,r.metadata,r.lr)
 end
 write(name..'_record_readers.json','{"record_window":[33558694,33558703],"readers":['..table.concat(rows,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpRecordReaders(name)\n',1)
    rc=native.main()
    out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'record_readers_environment.json').write_text(json.dumps(dict(observer_only=True,tool_sha256=sha(Path(__file__).read_bytes()),native_observer_sha256=sha(Path(native.__file__).read_bytes()),limits=['One field and one normal route only; no complete reader population/record width/marker proof.','No Hangul implementation or ROM change.']),indent=2),encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
