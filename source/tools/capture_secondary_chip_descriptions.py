"""Diagnostic secondary IDs via descriptor reads; real native root selection."""
import json
from pathlib import Path
import capture_fixedcell_probe as fixed
from build_visibility_poc import sha

SCRIPTS=[0,1,7,16,22,29,88]

def main():
    fixed.PROBE+=r'''
local secondaryActive=false
local secondaryDesc=0
local secondaryReads=0
local secondaryChoices={256,257,263,272,278,285,344}
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r2']==0x0202A680 and s['cpu.r5']==7 then
  secondaryDesc=s['cpu.r1']+s['cpu.r0']*32
  secondaryActive=true
 end
end,emu.callbackType.exec,0x0803CB20,0x0803CB20)
emu.addMemoryCallback(function(address,value)
 if not secondaryActive then return end
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x0803CB48 then return end
 local row=math.floor((address-secondaryDesc)/32)
 if row<0 or row>6 or (address-secondaryDesc)%32~=8 then error('secondary descriptor bounds') end
 secondaryReads=secondaryReads+1
 return secondaryChoices[row+1]*128
end,emu.callbackType.read,0x02000000,0x0203FFFF)
emu.addMemoryCallback(function()
 if secondaryActive and emu.getState()['cpu.r4']==6 then secondaryActive=false end
end,emu.callbackType.exec,0x0803CB7A,0x0803CB7A)
local function dumpSecondary(name)
 write(name..'_secondary_reads.json',string.format('{"descriptor_reads":%d}',secondaryReads))
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpSecondary(name)\n'),('local function finish()\n',"local function finish()\n dumpSecondary('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('capture anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=fixed.main();out=Path(fixed.value('--out'));rom=Path(fixed.value('--rom'))
    m=json.loads(rom.with_suffix('.json').read_text());ar=next(x for x in m['archives'] if x['archive']=='76BC60')
    import struct
    data=rom.read_bytes();streams={0x08000000+ar['rom_offset']+struct.unpack_from('<H',data,ar['rom_offset']+i*2)[0]:i for i in SCRIPTS}
    calls=json.loads((out/'final_fixedcells.json').read_text())['calls']
    covered=sorted({streams[c['stream']] for c in calls if c['stream'] in streams and c['font']==0x08619EF8})
    result=json.loads((out/'result.json').read_text());valid=rc==0 and result['complete'] and covered==SCRIPTS
    result['normal_play_checkpoint_eligible']=False
    result['scope']='DIAGNOSTIC descriptor source IDs256+script; native secondary-root lookup, compiled text and mono rendering; not acquired chips; no ROM/text/save-RAM edits'
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
        result['artifacts']['diagnostic_checkpoint.mss']=result['artifacts'].pop('checkpoint.mss')
    if not valid:result['complete']=False
    (out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (out/'secondary_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'passed':valid,'covered_scripts':covered,'scope':result['scope']},indent=2),encoding='utf-8')
    print('secondary native descriptions:',valid,covered)
    return rc if valid else 1

if __name__=='__main__':raise SystemExit(main())
