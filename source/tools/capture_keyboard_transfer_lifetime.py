"""Read-only observed descriptor0 pixels -> queued transfer -> VRAM route."""
import json, sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha


def main():
    if '--probe' not in sys.argv or sys.argv[sys.argv.index('--probe')+1]!='snapshot':raise ValueError('snapshot required')
    code=r'''
local lifeRows={};local lifeSlots={};local lifeActive=nil;local lifePending=nil;local lifeConsume=nil
local function lWord(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(i*8) end;return v
end
local function lHex(a,n)
 assert(n>=0 and n<=4096,'lifetime extent');local rows={}
 for i=0,n-1 do rows[#rows+1]=string.format('%02x',emu.read(a+i,emu.memType.gbaMemory)) end
 return table.concat(rows)
end
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']~=0x020155F0 then return end
 lifeActive={frame=frame,cell_stage=s['cpu.r2'],font=s['cpu.r6'],cell_counter=s['cpu.r5'],stream=lHex(s['cpu.r0'],32)}
end,emu.callbackType.exec,0x0300684A,0x0300684A)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r14']~=0x0300688C or not lifeActive or lifeActive.frame~=frame then return end
 local a=lifeActive;local src=s['cpu.r0'];local n=s['cpu.r2']
 if not(src<=a.cell_stage and a.cell_stage<src+n) then return end
 assert(not lifePending,'unclosed queue entry');assert(#lifeRows<5000,'lifetime observation overflow')
 lifePending={id=#lifeRows+1,frame=frame,source=src,target=s['cpu.r1'],bytes=n,queue_count_before=lWord(0x02010724),cell_stage=a.cell_stage,font=a.font,cell_counter=a.cell_counter,stream=a.stream,stage_at_enqueue=lHex(src,n)}
 lifeActive=nil
end,emu.callbackType.exec,0x08000850,0x08000850)
emu.addMemoryCallback(function()
 if not lifePending then return end
 local p=lifePending;local count=lWord(0x02010724);p.queue_count_after=count
 if count==p.queue_count_before+1 then
  p.entry=0x02012730+p.queue_count_before*20;p.entry_hex=lHex(p.entry,20)
  assert(not lifeSlots[p.entry],'unconsumed queue slot reused');lifeSlots[p.entry]=p
 else p.not_enqueued=true end
 lifeRows[#lifeRows+1]=p;lifePending=nil
end,emu.callbackType.exec,0x0800087C,0x0800087C)
emu.addMemoryCallback(function()
 local s=emu.getState();local p=lifeSlots[s['cpu.r9']];if not p then return end
 assert(not lifeConsume,'nested queue consumption');assert(not p.consumed_frame,'duplicate consumption')
 p.consumed_frame=frame;p.consume_source=s['cpu.r0'];p.consume_target=s['cpu.r1'];p.consume_bytes=s['cpu.r2']
 p.stage_at_consume=lHex(s['cpu.r0'],s['cpu.r2']);lifeConsume=p
end,emu.callbackType.exec,0x0800082E,0x0800082E)
emu.addMemoryCallback(function()
 if not lifeConsume then return end
 local p=lifeConsume;p.return_frame=frame;p.vram_after=lHex(p.consume_target,p.consume_bytes)
 lifeSlots[p.entry]=nil;lifeConsume=nil
end,emu.callbackType.exec,0x08000832,0x08000832)
local function dumpLifetime(name)
 local rows={};for _,p in ipairs(lifeRows) do
  rows[#rows+1]=string.format('{"id":%d,"frame":%d,"source":%d,"target":%d,"bytes":%d,"queue_count_before":%d,"queue_count_after":%d,"cell_stage":%d,"font":%d,"cell_counter":%d,"stream":"%s","entry":%d,"entry_hex":"%s","not_enqueued":%s,"consumed_frame":%d,"return_frame":%d,"consume_source":%d,"consume_target":%d,"consume_bytes":%d,"stage_at_enqueue":"%s","stage_at_consume":"%s","vram_after":"%s"}',p.id,p.frame,p.source,p.target,p.bytes,p.queue_count_before,p.queue_count_after,p.cell_stage,p.font,p.cell_counter,p.stream,p.entry or 0,p.entry_hex or '',p.not_enqueued and 'true' or 'false',p.consumed_frame or -1,p.return_frame or -1,p.consume_source or 0,p.consume_target or 0,p.consume_bytes or 0,p.stage_at_enqueue,p.stage_at_consume or '',p.vram_after or '')
 end
 write(name..'_transfer_lifetime.json','{"transfers":['..table.concat(rows,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpLifetime(name)\n',1)
    rc=native.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'transfer_lifetime_environment.json').write_text(json.dumps(dict(observer_only=True,no_RAM_or_save_injection=True,tool_sha256=sha(Path(__file__).read_bytes()),native_observer_sha256=sha(Path(native.__file__).read_bytes()),limits=['Observed Japanese descriptor0 and type2 queue consumer only; no Hangul integration or complete cache/writer ownership.']),indent=2),encoding='utf8')
    return rc


if __name__=='__main__':raise SystemExit(main())
