"""Read-only descriptor-0 copy/cache observation on the established native route."""
import json
import sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha


def main():
    if '--probe' not in sys.argv or sys.argv[sys.argv.index('--probe') + 1] != 'snapshot':
        raise ValueError('display-cache evidence requires --probe snapshot')
    code = r'''
local cacheCalls={};local cacheReads={};local cachePending=nil
local cacheConsumption={};local slotWrites={}
local function cHex(a,n)
 local rows={};for i=0,n-1 do rows[#rows+1]=string.format('%02x',emu.read(a+i,emu.memType.gbaMemory)) end;return table.concat(rows)
end
local function cWord(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(i*8) end;return v
end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r6']~=0x0200FC80 then return end
 if cachePending then error('unclosed descriptor0 copy') end
 cachePending={frame=frame,source=s['cpu.r6'],destination=s['cpu.r1'],length=s['cpu.r4'],context=s['cpu.r3'],slot=cWord(0x0200FC10),sp=s['cpu.r13'],source_hex=cHex(0x0200FC80,32)}
end,emu.callbackType.exec,0x03006A40,0x03006A40)
emu.addMemoryCallback(function()
 if not cachePending then return end
 local s=emu.getState();cachePending.after_hex=cHex(cachePending.destination,40)
 cachePending.copy_return_sp=s['cpu.r13'];cachePending.copy_return_lr=s['cpu.r14']
end,emu.callbackType.exec,0x03006A4C,0x03006A4C)
emu.addMemoryCallback(function()
 if not cachePending then return end
 local s=emu.getState();local p=cachePending
 if #cacheCalls>=10000 then error('display cache observation overflow') end
 cacheCalls[#cacheCalls+1]=string.format('{"frame":%d,"source":%d,"destination":%d,"length":%d,"context":%d,"slot":%d,"sp":%d,"copy_return_sp":%d,"copy_return_lr":%d,"result_pointer":%d,"next_slot":%d,"source_hex":"%s","after_hex":"%s"}',p.frame,p.source,p.destination,p.length,p.context,p.slot,p.sp,p.copy_return_sp,p.copy_return_lr,cWord(p.context+0x24),cWord(p.context+0x30),p.source_hex,p.after_hex)
 cachePending=nil
end,emu.callbackType.exec,0x03006A5E,0x03006A5E)
emu.addMemoryCallback(function(a,v)
 if #slotWrites>=10000 then error('cache slot observation overflow') end
 local s=emu.getState();slotWrites[#slotWrites+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d}',frame,a,v,s['cpu.pipeline.execute.address'])
end,emu.callbackType.write,0x0200FC10,0x0200FC13)
emu.addMemoryCallback(function(a)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address'];local key=string.format('%08x:%08x',pc,math.floor(a/128)*128)
 local p=cacheReads[key]
 if p then p.hits=p.hits+1;p.min=math.min(p.min,a);p.max=math.max(p.max,a)
 else cacheReads[key]={pc=pc,min=a,max=a,hits=1,first=frame,lr=s['cpu.r14']} end
 if #cacheCalls>0 and a>=0x020155F0 and a<0x02015610 then
  local index=#cacheCalls;local q=cacheConsumption[index]
  if not q then q={frame=frame,pc=pc,bytes={}};cacheConsumption[index]=q end
  if q.frame~=frame or q.pc~=pc then error('cache consumed outside observed per-frame provider') end
  q.bytes[#q.bytes+1]=string.format('%08x:%02x',a,emu.read(a,emu.memType.gbaMemory))
 end
end,emu.callbackType.read,0x020155F0,0x020157EF)
local function dumpDisplayCache(name)
 local rows={};for _,p in pairs(cacheReads) do rows[#rows+1]=string.format('{"pc":%d,"min":%d,"max":%d,"hits":%d,"first":%d,"lr":%d}',p.pc,p.min,p.max,p.hits,p.first,p.lr) end
 local consumed={};for i,p in pairs(cacheConsumption) do consumed[#consumed+1]=string.format('{"copy":%d,"frame":%d,"pc":%d,"reads":"%s"}',i,p.frame,p.pc,table.concat(p.bytes,',')) end
 write(name..'_display_cache.json','{"copies":['..table.concat(cacheCalls,',')..'],"reads":['..table.concat(rows,',')..'],"consumption":['..table.concat(consumed,',')..'],"slot_writes":['..table.concat(slotWrites,',')..']}')
end
'''
    anchor = 'local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor) != 1:
        raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE = native.runner.LUA_TEMPLATE.replace(
        anchor, code + anchor + ' dumpDisplayCache(name)\n', 1)
    rc = native.main()
    out = Path(sys.argv[sys.argv.index('--out') + 1])
    (out / 'display_cache_environment.json').write_text(json.dumps(dict(
        observer_only=True, no_RAM_or_save_injection=True,
        tool_sha256=sha(Path(__file__).read_bytes()),
        native_observer_sha256=sha(Path(native.__file__).read_bytes()),
        limits=['Descriptor0 fixed-cell copy and bounded cache reads on this normal Japanese route only.',
                'No Hangul integration, full cache ownership, or save claim.']), indent=2), encoding='utf8')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
