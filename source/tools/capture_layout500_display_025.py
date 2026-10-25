"""025 raw page/choice diagnostic; native control path, quarantined aliases."""
import struct,sys
from pathlib import Path
import capture_layout500_display_024 as raw
import capture_roll_pet as pet
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from compare_archive_payloads import payload_of
from archive_scripts import script_spans

CASES={'choice-three-row':('766134',4),'nickname':('67D44C',2)}

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    case=value('--display-case')
    if case not in CASES:raise ValueError('025 finite display cases')
    arc,script=CASES[case];rp=Path(value('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    manifest=read('analysis/pending_insertion_500_025_carry_v1/preflight.json');record=next(r for r in manifest['archives'] if r['archive']==arc)
    if script not in record['new_scripts']:raise ValueError('025 newly inserted display identity')
    count=record['script_count'];native=script_spans(payload_of(source,record['source_row']),count)[script]
    if case=='choice-three-row':
        if native[:2]!=bytes.fromhex('f400') or native[3:5]!=bytes.fromhex('e700'):raise ValueError('025 exact mugshot+normal initializer')
        prefix=native[:5]
    else:
        prefix=bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')
        if not native.startswith(prefix):raise ValueError('025 exact PET initializer')
    raw.CASES={case:(arc,count,script,prefix)}
    # Existing025 ROM handlers are observed, never replaced or invoked directly.
    sites=[]
    for op in (0xEA,0xEC,0xE5):
        sites.append((op,struct.unpack_from('<I',rom,0x50098+4*(op-0xE5))[0]&~1))
    sites.append((0x1EA,struct.unpack_from('<I',rom,0x50100+4*(0xEA-0xE5))[0]&~1))
    sites.extend((op,pc) for op,pc in ((0x2EC,0x080506A4),(0x3EC,0x0805070A),(0x4EC,0x080506F8)))
    lua='\nlocal choiceTrace={}\n'
    for op,pc in sites:
        if not 0x08000000<=pc<0x08800000:raise ValueError('025 native control handler range')
        lua+=f'''
emu.addMemoryCallback(function()
 local s=emu.getState();local p=s['cpu.r4']
 if p<PET_POOL or p>=PET_END then return end
 local bytes={{}};for i=0,215 do bytes[#bytes+1]=string.format('%02X',emu.read(s['cpu.r5']+i,emu.memType.gbaMemory)) end
 choiceTrace[#choiceTrace+1]=string.format('{{"frame":%d,"op":{op},"pc":{pc},"stream":%d,"context":%d,"hex":"%s"}}',frame,p,s['cpu.r5'],table.concat(bytes))
end,emu.callbackType.exec,{pc},{pc})
'''
    # raw.main substitutes PET constants in pet.PROBE; its capture dump is already called.
    lua+='''
local oldDumpRollPet=dumpRollPet
dumpRollPet=function(name)
 oldDumpRollPet(name)
 write(name..'_choice_trace.json','{"events":['..table.concat(choiceTrace,',')..']}')
end
'''
    pet.PROBE+=lua
    return raw.main()

if __name__=='__main__':raise SystemExit(main())
