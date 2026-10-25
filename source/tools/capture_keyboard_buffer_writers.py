"""Normal native input: bounded cache/stage writers and protected intervals."""
import json,sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha


def main():
    if '--probe' not in sys.argv or sys.argv[sys.argv.index('--probe')+1]!='snapshot':raise ValueError('snapshot required')
    code=r'''
local wGroups={};local providerRows={};local providerPending=nil;local cacheActive=nil
local stagePending=false;local stageWindows=0;local stageClosed=0;local violations={}
local function wWord(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(8*i) end;return v
end
local function wHex(a,n)
 assert(n>=0 and n<=512);local t={};for i=0,n-1 do t[#t+1]=string.format('%02x',emu.read(a+i,emu.memType.gbaMemory)) end;return table.concat(t)
end
local function wEvent(kind,a,v)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 local phase=(kind=='cache' and cacheActive and 'consumption') or (kind=='stage' and stagePending and 'queued') or 'other'
 local key=string.format('%s:%08x:%s',kind,pc,phase);local g=wGroups[key]
 if not g then g={kind=kind,pc=pc,phase=phase,hits=0,min=a,max=a,first=frame,last=frame,lr=s['cpu.r14'],r0=s['cpu.r0'],r1=s['cpu.r1'],r2=s['cpu.r2']};wGroups[key]=g end
 g.hits=g.hits+1;g.min=math.min(g.min,a);g.max=math.max(g.max,a);g.last=frame
 if phase~='other' then
  assert(#violations<1000,'writer violation overflow')
  violations[#violations+1]=string.format('{"kind":"%s","pc":%d,"frame":%d,"address":%d,"value":%d}',kind,pc,frame,a,v)
 end
end
emu.addMemoryCallback(function(a,v) wEvent('cache',a,v) end,emu.callbackType.write,0x020155F0,0x020157EF)
emu.addMemoryCallback(function(a,v) wEvent('stage',a,v) end,emu.callbackType.write,0x0201E800,0x0201ECFF)
emu.addMemoryCallback(function()
 local s=emu.getState();assert(not providerPending,'nested native provider')
 local index=emu.read(s['cpu.r0']+2,emu.memType.gbaMemory);local slot=wWord(0x0200FC10)
 providerPending={frame=frame,index=index,slot=slot,script=s['cpu.r0'],sp=s['cpu.r13'],lr=s['cpu.r14']}
end,emu.callbackType.exec,0x03006A1C,0x03006A1C)
emu.addMemoryCallback(function()
 assert(providerPending,'provider entry missed');local s=emu.getState();local p=providerPending
 p.source=s['cpu.r6'];p.destination=s['cpu.r1'];p.bytes=s['cpu.r4'];p.copy_sp=s['cpu.r13']
 p.source_hex=wHex(p.source,p.bytes)
end,emu.callbackType.exec,0x03006A40,0x03006A40)
emu.addMemoryCallback(function()
 assert(providerPending,'provider copy missed');local p=providerPending
 p.cache_hex=wHex(p.destination,p.bytes)
end,emu.callbackType.exec,0x03006A4C,0x03006A4C)
emu.addMemoryCallback(function()
 assert(providerPending,'provider return missed');local p=providerPending;local s=emu.getState()
 p.result=s['cpu.r0'];p.return_sp=s['cpu.r13'];p.next_slot=wWord(0x0200FC10)
 providerRows[#providerRows+1]=p;assert(#providerRows<10000,'provider overflow');providerPending=nil
 if p.index==0 then
  assert(not cacheActive,'overlapping editor cache consumption')
  cacheActive={frame=frame,destination=p.destination,reads=0};p.editor_reads=cacheActive;p.cache41_hex=wHex(p.destination,41)
 end
end,emu.callbackType.exec,0x03006A64,0x03006A64)
emu.addMemoryCallback(function(a)
 if cacheActive and a>=cacheActive.destination and a<cacheActive.destination+41 then cacheActive.reads=cacheActive.reads+1 end
end,emu.callbackType.read,0x020155F0,0x020157EF)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r14']~=0x0300688C or s['cpu.r0']~=0x0201E800 then return end
 assert(cacheActive and cacheActive.frame==frame,'cache -> stage route missing')
 assert(not stagePending,'stage still queued before new render')
 cacheActive=nil;stagePending=true;stageWindows=stageWindows+1
end,emu.callbackType.exec,0x08000850,0x08000850)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if stagePending and s['cpu.r9']~=0 and wWord(s['cpu.r9'])==0x0201E800 then stagePending=false;stageClosed=stageClosed+1 end
end,emu.callbackType.exec,0x08000832,0x08000832)
local function dumpWriters(name)
 local groups={};for _,g in pairs(wGroups) do
  groups[#groups+1]=string.format('{"kind":"%s","pc":%d,"phase":"%s","hits":%d,"min":%d,"max":%d,"first":%d,"last":%d,"lr":%d,"r0":%d,"r1":%d,"r2":%d}',g.kind,g.pc,g.phase,g.hits,g.min,g.max,g.first,g.last,g.lr,g.r0,g.r1,g.r2)
 end
 local rows={};for _,p in ipairs(providerRows) do
  rows[#rows+1]=string.format('{"frame":%d,"index":%d,"slot":%d,"script":%d,"sp":%d,"lr":%d,"source":%d,"destination":%d,"bytes":%d,"copy_sp":%d,"result":%d,"return_sp":%d,"next_slot":%d,"source_hex":"%s","cache_hex":"%s","cache41_hex":"%s","editor_reads":%d}',p.frame,p.index,p.slot,p.script,p.sp,p.lr,p.source,p.destination,p.bytes,p.copy_sp,p.result,p.return_sp,p.next_slot,p.source_hex,p.cache_hex,p.cache41_hex or '',p.editor_reads and p.editor_reads.reads or 0)
 end
 write(name..'_buffer_writers.json','{"groups":['..table.concat(groups,',')..'],"providers":['..table.concat(rows,',')..'],"violations":['..table.concat(violations,',')..'],"stage_windows":'..stageWindows..',"stage_closed":'..stageClosed..',"stage_pending":'..(stagePending and 'true' or 'false')..',"cache_pending":'..(cacheActive and 'true' or 'false')..'}')
end
'''
    anchor='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpWriters(name)\n',1)
    rc=native.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'buffer_writers_environment.json').write_text(json.dumps(dict(observer_only=True,no_RAM_or_save_injection=True,tool_sha256=sha(Path(__file__).read_bytes()),native_observer_sha256=sha(Path(native.__file__).read_bytes()),watch_ranges={'cache':['0x020155F0','0x020157EF'],'stage':['0x0201E800','0x0201ECFF']},limits=['Bounded callback write-start addresses and native route only; not all-width bus tracing or static complete writer ownership.','Native descriptor0 consumption/queued stage intervals, not Hangul or cache41 allocation adoption.']),indent=2),encoding='utf8')
    return rc


if __name__=='__main__':raise SystemExit(main())
