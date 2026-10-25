"""Observe post-confirm string providers without editing RAM, ROM or saves."""
import json, sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha

def main():
    code=r'''
local rdEvents={};local rdPending=nil;local rdReads={}
local function rdHex(a,n)
 local t={};for i=0,n-1 do t[#t+1]=string.format('%02x',emu.read(a+i,emu.memType.gbaMemory)) end;return table.concat(t)
end
local function rdWord(a)
 local n=0;for i=0,3 do n=n+emu.read(a+i,emu.memType.gbaMemory)*2^(8*i) end;return n
end
local function rdAdd(row)
 assert(#rdEvents<20000,'redisplay observation overflow');rdEvents[#rdEvents+1]=row
end
emu.addMemoryCallback(function()
 local s=emu.getState();assert(not rdPending,'nested provider')
 local p=s['cpu.r0'];local index=emu.read(p+2,emu.memType.gbaMemory)
 rdPending={frame=frame,index=index,token=p,source=rdWord(0x080526D0+8*index),bound=rdWord(0x080526D4+8*index),slot=rdWord(0x0200FC10),sp=s['cpu.r13'],lr=s['cpu.r14']}
end,emu.callbackType.exec,0x03006A1C,0x03006A1C)
emu.addMemoryCallback(function()
 assert(rdPending,'provider return without entry');local p=rdPending;local s=emu.getState()
 rdAdd(string.format('{"kind":"provider","frame":%d,"index":%d,"token":%d,"source":%d,"bound":%d,"slot":%d,"sp":%d,"lr":%d,"result":%d,"next_slot":%d,"source_hex":"%s","cache_hex":"%s","record_hex":"%s","temporary_hex":"%s"}',p.frame,p.index,p.token,p.source,p.bound,p.slot,p.sp,p.lr,s['cpu.r0'],rdWord(0x0200FC10),rdHex(p.source,math.min(p.bound,41)),rdHex(s['cpu.r0'],41),rdHex(0x020010A6,10),rdHex(0x02014E74,41)))
 rdPending=nil
end,emu.callbackType.exec,0x03006A64,0x03006A64)
for _,pc in ipairs({0x08038B94,0x08032AC6,0x08035030}) do
 emu.addMemoryCallback(function()
  local s=emu.getState()
  rdAdd(string.format('{"kind":"call","frame":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"sp":%d,"lr":%d,"record_hex":"%s","temporary_hex":"%s"}',frame,pc,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r13'],s['cpu.r14'],rdHex(0x020010A6,10),rdHex(0x02014E74,41)))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpRedisplay(name)
 write(name..'_redisplay.json','{"events":['..table.concat(rdEvents,',')..'],"reads":['..table.concat(rdReads,',')..']}')
end
for _,r in ipairs({{0x020010A6,0x020010AF},{0x02014E74,0x02014E9C}}) do
 emu.addMemoryCallback(function(a,v)
  if frame<1075 then return end;assert(#rdReads<20000,'redisplay read overflow');local s=emu.getState()
  rdReads[#rdReads+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"lr":%d}',frame,a,v,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r14'])
 end,emu.callbackType.read,r[1],r[2])
end
'''
    anchor='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpRedisplay(name)\n',1)
    rc=native.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'redisplay_environment.json').write_text(json.dumps(dict(observer_only=True,no_RAM_or_save_injection=True,
        tool_sha256=sha(Path(__file__).read_bytes()),native_observer_sha256=sha(Path(native.__file__).read_bytes()),
        limits=['One native Japanese confirmation/continuation route, no Hangul hook or persistence.','Provider source/cache snapshots at return; not complete writer or lifetime proof.']),indent=2),encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
