"""Quarantined FC0F->cache->F90C diagnostic; no natural caller/save claim.

Temporary valid native friend records and enable flag restored after reader.
"""
import sys
from pathlib import Path
import capture_layout500_display_024 as raw
import capture_roll_pet as pet
from build_visibility_poc import require_hash
from cumulative_batch500 import read
from bench_profile_arrays_029 import ROM_SHA

def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);require_hash(rp,ROM_SHA)
    meta=read(rp.with_suffix('.json'))
    evidence=read('analysis/pending_insertion_500_029_array_cpu_v1/cpu.json')
    if not evidence['passed'] or evidence['baseline_sha256']!=ROM_SHA:raise ValueError('029 producer CPU prerequisite')
    f=next(x for x in evidence['fields'] if x['provider']=='printFriend')
    ar=next(x for x in meta['archives'] if x['archive']=='69B134')
    prefix=bytes.fromhex('fc0f0713fff6000a0c01e702f6025c6e03f604e18d')
    raw.CASES={'array-friend':('69B134',ar['script_count'],18,prefix)}
    marker='if stream<PET_POOL or stream>=PET_END then return end'
    if pet.PROBE.count(marker)!=1:raise ValueError('029 draw observer anchor')
    pet.PROBE=pet.PROBE.replace(marker,'if (stream<PET_POOL or stream>=PET_END) and (stream<0x02010AC0 or stream>=0x02010B40) then return end')
    base,cap,count,cache,size,index=f['base'],f['cap'],f['count'],f['cache'],f['size'],f['index']
    flag=f['flag'];length=count*(2*cap+2);mask=0x80>>(flag%8)
    pet.PROBE+=f'''
local arrayEvents={{}};local savedArray=nil;local flagAddress=nil;local savedFlag=nil;local sourceStream=nil;local selectedSource=nil
local function rd32(p) local v=0;for i=0,3 do v=v+emu.read(p+i,emu.memType.gbaMemory)*2^(8*i) end;return v end
local function hexBytes(p,n) local v={{}};for i=0,n-1 do v[#v+1]=string.format('%02X',emu.read(p+i,emu.memType.gbaMemory)) end;return table.concat(v) end
emu.addMemoryCallback(function()
 local s=emu.getState();local p=s['cpu.r4']
 if p<PET_POOL or p>=PET_END or emu.read(p+2,emu.memType.gbaMemory)~={index} then return end
 if savedArray~=nil then error('029 nested native array intervention') end
 sourceStream=p;savedArray={{}};for i=0,{length}-1 do savedArray[i+1]=emu.read({base}+i,emu.memType.gbaMemory) end
 flagAddress=rd32(s['cpu.r10']+0x48)+{flag//8};savedFlag=emu.read(flagAddress,emu.memType.gbaMemory)
 if math.floor(savedFlag/{mask})%2==0 then emu.write(flagAddress,savedFlag+{mask},emu.memType.gbaMemory) end
 for j=0,{count}-1 do
  local p={base}+j*{2*cap+2};emu.write(p,1,emu.memType.gbaMemory)
  for k=0,{cap}-1 do emu.write(p+1+k*2,0xE4,emu.memType.gbaMemory);emu.write(p+2+k*2,6,emu.memType.gbaMemory) end
  emu.write(p+{2*cap+1},0xE5,emu.memType.gbaMemory)
 end
end,emu.callbackType.exec,0x08051DD4,0x08051DD4)
emu.addMemoryCallback(function()
 if savedArray==nil then return end
 local s=emu.getState();selectedSource=s['cpu.r0']
 if s['cpu.r1']~={cache} or selectedSource<{base}+1 or selectedSource>={base+length} or (selectedSource-{base}-1)%{2*cap+2}~=0 then error('029 native selected record ABI') end
end,emu.callbackType.exec,0x08032AC6,0x08032AC6)
emu.addMemoryCallback(function()
 if savedArray==nil then return end
 local s=emu.getState();local p=s['cpu.r4']
 if p~=sourceStream+5+16 or emu.read(p+2,emu.memType.gbaMemory)~={index} then error('029 actual source first reader path') end
 if hexBytes({cache},{size})~='{('e406'*cap+'e5').upper()}' then error('029 native cache output') end
end,emu.callbackType.exec,0x080517D0,0x080517D0)
emu.addMemoryCallback(function()
 if savedArray==nil then return end
 local s=emu.getState();local dest=s['cpu.r0']
 if dest~=0x02010AC0 or hexBytes(dest,{size})~='{('e406'*cap+'e5').upper()}' then error('029 native F90C copied value') end
 for i=0,{length}-1 do emu.write({base}+i,savedArray[i+1],emu.memType.gbaMemory) end
 emu.write(flagAddress,savedFlag,emu.memType.gbaMemory)
 for i=0,{length}-1 do if emu.read({base}+i,emu.memType.gbaMemory)~=savedArray[i+1] then error('029 record restoration') end end
 if emu.read(flagAddress,emu.memType.gbaMemory)~=savedFlag then error('029 flag restoration') end
 arrayEvents[#arrayEvents+1]=string.format('{{"frame":%d,"stream":%d,"selected_source":%d,"cache":{cache},"output":%d,"hex":"%s","records_and_flag_restored":true}}',frame,sourceStream,selectedSource,dest,hexBytes(dest,{size}))
 savedArray=nil
end,emu.callbackType.exec,0x08051816,0x08051816)
local previousDump=dumpRollPet
dumpRollPet=function(name)
 previousDump(name)
 if savedArray~=nil then error('029 snapshot during temporary records') end
 write(name..'_array_trace.json','{{"events":['..table.concat(arrayEvents,',')..']}}')
end
'''
    return raw.main()

if __name__=='__main__':raise SystemExit(main())
