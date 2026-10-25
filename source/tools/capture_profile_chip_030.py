"""Quarantined PET display diagnostic with finite valid max native records.

Only scoped root/table read aliases and temporary field bytes at the real
F90C reader. Native reader runs; original record restored before glyph draw.
No natural profile acquisition, native speaker, save or Hangul claim.
"""
import sys,struct
from pathlib import Path
import capture_layout500_display_024 as raw
import capture_roll_pet as pet
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from inspect_profile_chip_pools_030 import OUT as CENSUS,ROM_SHA

CASES={'standard1-max':('65CC78',73,'printFavStandardChip1')}


def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    case=value('--display-case')
    if case not in CASES:raise ValueError('027 finite field cases')
    arc,script,provider=CASES[case];rp=Path(value('--rom'));meta=read(rp.with_suffix('.json'));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(rp,ROM_SHA)
    census=read(CENSUS);cpu=read('analysis/pending_insertion_500_030_chip_cpu_v1/cpu.json')
    if not cpu['passed'] or cpu['baseline_sha256']!=ROM_SHA:raise ValueError('030 native producer CPU prerequisite')
    for p,h in census['dependencies'].items():require_hash(ROOT/p,h)
    record=next(r for r in meta['archives'] if r['archive']==arc)
    info=census['fields'][provider];field=info['field'];size=info['bytes'];index=info['index']
    fixture=next(r for r in census['names'] if r['advance']==88)
    encoded=bytes.fromhex(fixture['raw_hex']);cap=fixture['glyphs']
    if rom[fixture['source_offset']:fixture['source_offset']+len(encoded)]!=encoded:raise ValueError('030 exact native chip fixture')
    prefix=bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')
    raw.CASES={case:(arc,record['script_count'],script,prefix)}
    # Track RAM provider glyph consumption as well as literal ROM streams.
    marker='if stream<PET_POOL or stream>=PET_END then return end'
    if pet.PROBE.count(marker)!=1:raise ValueError('027 draw probe anchor')
    pet.PROBE=pet.PROBE.replace(marker,'if (stream<PET_POOL or stream>=PET_END) and (stream<0x02010AC0 or stream>=0x02010B40) then return end')
    pet.PROBE+=f'''
local fieldTrace={{}};local savedField=nil;local fieldStream=nil
emu.addMemoryCallback(function()
 local s=emu.getState();local p=s['cpu.r4']
 if p<PET_POOL or p>=PET_END then return end
 if emu.read(p+2,emu.memType.gbaMemory)~={index} then return end
 if savedField~=nil then error('027 overlapping temporary field intervention') end
 savedField={{}};for i=0,{size} do savedField[i+1]=emu.read({field}-1+i,emu.memType.gbaMemory) end
 emu.write({field}-1,1,emu.memType.gbaMemory)
 local nativeBytes={{{','.join(str(v) for v in encoded)}}}
 for i,v in ipairs(nativeBytes) do emu.write({field}+i-1,v,emu.memType.gbaMemory) end
 fieldStream=p
end,emu.callbackType.exec,0x080517D0,0x080517D0)
emu.addMemoryCallback(function()
 if savedField==nil then return end
 local s=emu.getState();local out=s['cpu.r0'];local bytes={{}}
 if s['cpu.r4']~=fieldStream+3 or out<0x02010AC0 or out+{size}>0x02010CC0 then error('027 reader ABI/destination') end
 for i=0,{size}-1 do bytes[#bytes+1]=string.format('%02X',emu.read(out+i,emu.memType.gbaMemory)) end
 for i=0,{size} do emu.write({field}-1+i,savedField[i+1],emu.memType.gbaMemory) end
 for i=0,{size} do if emu.read({field}-1+i,emu.memType.gbaMemory)~=savedField[i+1] then error('027 field restoration') end end
 fieldTrace[#fieldTrace+1]=string.format('{{"frame":%d,"stream":%d,"output":%d,"field":{field},"cap":{cap},"hex":"%s","restored":true}}',frame,fieldStream,out,table.concat(bytes))
 savedField=nil;fieldStream=nil
end,emu.callbackType.exec,0x08051816,0x08051816)
local oldDumpRollPet=dumpRollPet
dumpRollPet=function(name)
 oldDumpRollPet(name)
 if savedField~=nil then error('027 snapshot inside temporary reader intervention') end
 write(name..'_profile_trace.json','{{"events":['..table.concat(fieldTrace,',')..']}}')
end
'''
    return raw.main()


if __name__=='__main__':raise SystemExit(main())


