"""Read-only lookup probe layered on quarantined PET13 display."""
import json,sys,struct
from pathlib import Path
import capture_roll_chipquest as base
from build_visibility_poc import ROOT,sha

def main():
    source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes();at=0x08765190+struct.unpack_from('<H',source,0x765190+208)[0]
    pairs=[0x1F7F0,0x22AF8,0x3866C,0x3CB98,0x42F98,0x4CAA8,0x4E6A4,0x4E79C,0x51664]
    code='''
local chipLookup={}
local function recordChipRead(address,value)
 if #chipLookup>=160 then return end
 local s=emu.getState()
 chipLookup[#chipLookup+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"r5":%d,"r6":%d,"r7":%d,"lr":%d}',frame,address,value or 0,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r5'],s['cpu.r6'],s['cpu.r7'],s['cpu.r14'])
end
local function dumpChipLookup(name)
 write(name..'_chip_lookup.json','{"reads":['..table.concat(chipLookup,',')..']}')
end
'''
    for p in pairs:code+=f'emu.addMemoryCallback(recordChipRead,emu.callbackType.read,{0x08000000+p},{0x08000000+p+7})\n'
    for lo,hi in [(0x08765190+208,0x08765190+209),(at,at+8)]:code+=f'emu.addMemoryCallback(recordChipRead,emu.callbackType.read,{lo},{hi})\n'
    base.base.normal.pet.PROBE+=code;marker='local function capture(name)\n';runner=base.base.normal.pet.runner
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('lookup probe capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,marker+' dumpChipLookup(name)\n',1)
    rc=base.main();a=sys.argv;out=Path(a[a.index('--out')+1]);(out/'chip_lookup_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),'chip104_rom_stream':at,'pairs':pairs,'observer_read_only':True},indent=2),encoding='utf-8');return rc

if __name__=='__main__':raise SystemExit(main())
