"""Guarded root/table read diagnostics, never AquaMan normal route evidence."""
import json,struct,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from archive_scripts import script_spans

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    lookup=Path(value('--lookup-evidence'));script=int(value('--aqua-script'))
    for k in ['--lookup-evidence','--aqua-script']:
        i=sys.argv.index(k);del sys.argv[i:i+2]
    if script not in [1,7]:raise ValueError('unregistered diagnostic script')
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes();verify_route(lookup,m['output_sha256'],set())
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);original=source.read_bytes()
    for a,b in [(0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB4C,0x4FC20)]:
        if rom[a:b]!=original[a:b]:raise ValueError('native caller drift')
    old=struct.unpack_from('<I',rom,0x382AC)[0];records=json.loads((lookup/'final_seasonal_lookup.json').read_text())['reads']
    matching=[r for r in records if r['address']==0x080382AC and r['value']==old and r['pc']==0x08037F20 and r['r0']==0x08038278 and r['r1']==1 and r['r3']==52]
    if len(matching)!=1:raise ValueError('need one observed native NumberMan seasonal lookup')
    ar=next(x for x in m['archives'] if x['archive']=='69C9F4');pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    if not script_spans(payload,21)[script].startswith(bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')):raise ValueError('AquaMan native window prefix')
    offset1=struct.unpack_from('<H',payload,2)[0];target=struct.unpack_from('<H',payload,script*2)[0]
    pet.ARCHIVE='69C9F4';pet.PROBE+=f'''
local aquaRoots=0;local aquaEntries=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if aquaRoots==0 and address==0x080382AC and value=={old} and s['cpu.pipeline.execute.address']==0x08037F20 and s['cpu.r0']==0x08038278 and s['cpu.r1']==1 and s['cpu.r3']==52 then
  aquaRoots=1;return {pool}
 end
end,emu.callbackType.read,0x080382AC,0x080382AF)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if {script}~=1 and aquaRoots==1 and aquaEntries==0 and address=={pool+2} and value=={offset1} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==2 and s['cpu.r5']==0x0200FA20 then
  aquaEntries=1;return {target}
 end
end,emu.callbackType.read,{pool+2},{pool+3})
local function dumpAquaAlias(name)
 write(name..'_aqua_alias.json','{{"root_aliases":'..aquaRoots..',"entry_aliases":'..aquaEntries..',"requested_script":1,"target_script":{script}}}')
end
'''
    for oldmarker,new in [('local function capture(name)\n','local function capture(name)\n dumpAquaAlias(name)\n'),('local function finish()\n',"local function finish()\n dumpAquaAlias('final')\n")]:
        if pet.runner.LUA_TEMPLATE.count(oldmarker)!=1:raise ValueError('capture anchor')
        pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(oldmarker,new,1)
    rc=pet.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_aqua_alias.json').read_text());passed=rc==0 and r['complete'] and d['root_aliases']==1 and d['entry_aliases']==int(script!=1)
    scope='DIAGNOSTIC guarded native NumberMan seasonal root read aliases to AquaMan pool; script7 also alias requested1 offset read. Same normal window/consumer, NumberMan portrait/caller remain. No ROM/RAM writes; NOT AquaMan normal unlock/portrait/date or gender/nickname route proof.'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf8')
    (out/'aqua_environment.json').write_text(json.dumps(dict(passed=passed,scope=scope,rom_sha256=m['output_sha256'],tool_sha256=sha(Path(__file__).read_bytes()),observer_sha256=sha(Path(pet.__file__).read_bytes()),lookup_evidence=str(lookup),lookup_sha256=sha((lookup/'final_seasonal_lookup.json').read_bytes()),native_observation=matching[0],pool=pool,target_offset=target,**d),indent=2),encoding='utf8')
    print('AquaMan renderer-only diagnostic',script,passed);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
