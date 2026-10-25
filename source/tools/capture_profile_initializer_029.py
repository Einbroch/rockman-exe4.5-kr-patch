"""Natural startup cache initialization plus aliased source PET consumption.

Seed valid native records before real initializer; restore records/flags
immediately after it. Never seed cache or reader scratch. No ROM edits.
"""
import sys,json
from pathlib import Path
import capture_layout500_display_024 as raw
import capture_roll_pet as pet
from build_visibility_poc import require_hash
from cumulative_batch500 import read
from bench_profile_arrays_029 import ROM_SHA

def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);require_hash(rp,ROM_SHA)
    meta=read(rp.with_suffix('.json'));cpu=read('analysis/pending_insertion_500_029_array_cpu_v2/cpu.json')
    if not cpu['passed'] or cpu['baseline_sha256']!=ROM_SHA:raise ValueError('029 initializer CPU prerequisite')
    ar=next(x for x in meta['archives'] if x['archive']=='65CC78')
    raw.CASES={'initializer-older-bro':('65CC78',ar['script_count'],5,bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d'))}
    rows=[]
    for f in cpu['fields']:
        rows.append('{base=%d,count=%d,cap=%d,cache=%d,size=%d,flag=%d,index=%d}'%(f['base'],f['count'],f['cap'],f['cache'],f['size'],f['flag'],f['index']))
    marker='if stream<PET_POOL or stream>=PET_END then return end'
    if pet.PROBE.count(marker)!=1:raise ValueError('029 initializer draw anchor')
    pet.PROBE=pet.PROBE.replace(marker,'if (stream<PET_POOL or stream>=PET_END) and (stream<0x02010AC0 or stream>=0x02010B40) then return end')
    pet.PROBE+='''
local nativeArrays={'''+','.join(rows)+'''}
local savedBytes={};local seeded=false;local restored=false;local initFrame=-1;local afterWrites={};local reads={}
local function r32(p) local v=0;for i=0,3 do v=v+emu.read(p+i,emu.memType.gbaMemory)*2^(i*8) end;return v end
local function saveByte(p) if savedBytes[p]==nil then savedBytes[p]=emu.read(p,emu.memType.gbaMemory) end end
local function expected(f,i) if i==2*f.cap then return 0xE5 elseif i%2==0 then return 0xE4 else return 6 end end
local function verifyCaches()
 for _,f in ipairs(nativeArrays) do for i=0,f.size-1 do if emu.read(f.cache+i,emu.memType.gbaMemory)~=expected(f,i) then error('029 initialized cache mismatch at '..tostring(f.cache+i)..' frame '..tostring(frame)) end end end
end
emu.addMemoryCallback(function()
 if seeded then error('029 unexpected second initialization') end
 local s=emu.getState();local flags=r32(s['cpu.r10']+0x48)
 for _,f in ipairs(nativeArrays) do
  local p=flags+math.floor(f.flag/8);saveByte(p)
  local bit=2^(7-f.flag%8);local value=emu.read(p,emu.memType.gbaMemory)
  if math.floor(value/bit)%2==0 then emu.write(p,value+bit,emu.memType.gbaMemory) end
  for j=0,f.count-1 do
   local at=f.base+j*(2*f.cap+2)
   for i=0,2*f.cap+1 do saveByte(at+i) end
   emu.write(at,1,emu.memType.gbaMemory)
   for i=0,f.size-1 do emu.write(at+1+i,expected(f,i),emu.memType.gbaMemory) end
  end
 end
 seeded=true;initFrame=frame
end,emu.callbackType.exec,0x080309EE,0x080309EE)
emu.addMemoryCallback(function()
 if not seeded or restored then error('029 initializer entry/return ordering') end
 verifyCaches()
 for p,v in pairs(savedBytes) do emu.write(p,v,emu.memType.gbaMemory) end
 for p,v in pairs(savedBytes) do if emu.read(p,emu.memType.gbaMemory)~=v then error('029 initializer userdata/flag restoration') end end
 restored=true
end,emu.callbackType.exec,0x080309F2,0x080309F2)
emu.addMemoryCallback(function(address,value)
 if not restored then return end
 for _,f in ipairs(nativeArrays) do
  if address>=f.cache and address<f.cache+f.size then
   local s=emu.getState();afterWrites[#afterWrites+1]=string.format('{"frame":%d,"pc":%d,"address":%d,"value":%d}',frame,s['cpu.pipeline.execute.address'],address,value)
  end
 end
end,emu.callbackType.write,0x020293E0,0x020294D0)
emu.addMemoryCallback(function()
 local s=emu.getState();local p=s['cpu.r4']
 if p<PET_POOL or p>=PET_END then return end
 if not restored then error('029 consumed before actual initializer return') end
 verifyCaches();local index=emu.read(p+2,emu.memType.gbaMemory)
 for _,f in ipairs(nativeArrays) do if index==f.index then
  reads[#reads+1]=string.format('{"frame":%d,"stream":%d,"index":%d,"cache":%d}',frame,p,index,f.cache)
 end end
end,emu.callbackType.exec,0x080517D0,0x080517D0)
local oldDump=dumpRollPet
dumpRollPet=function(name)
 oldDump(name)
 if restored then verifyCaches() end
 write(name..'_initializer_trace.json','{"seeded":'..tostring(seeded)..',"restored":'..tostring(restored)..',"init_frame":'..initFrame..',"after_writes":['..table.concat(afterWrites,',')..'],"reads":['..table.concat(reads,',')..']}')
end
'''
    return raw.main()

if __name__=='__main__':raise SystemExit(main())
