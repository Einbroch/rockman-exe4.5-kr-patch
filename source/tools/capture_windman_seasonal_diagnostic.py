"""Quarantined seasonal root read alias; not WindMan unlock/portrait/date proof."""
import json,struct,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from archive_scripts import script_spans

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    lookup=Path(value('--lookup-evidence'));i=sys.argv.index('--lookup-evidence');del sys.argv[i:i+2]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    verify_route(lookup,m['output_sha256'],set())
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);original=source.read_bytes()
    for a,b in [(0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB4C,0x4FC20)]:
        if rom[a:b]!=original[a:b]:raise ValueError('native caller drift')
    old=struct.unpack_from('<I',rom,0x382AC)[0]
    records=json.loads((lookup/'final_seasonal_lookup.json').read_text())['reads']
    matching=[r for r in records if r['address']==0x080382AC and r['value']==old and r['pc']==0x08037F20 and r['r0']==0x08038278 and r['r1']==1 and r['r3']==52]
    if len(matching)!=1:raise ValueError('need one observed native NumberMan seasonal entry')
    ar=next(x for x in m['archives'] if x['archive']=='66F78C');pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    if not script_spans(payload,21)[1].startswith(bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')):raise ValueError('WindMan native window prefix')
    pet.ARCHIVE='66F78C';pet.PROBE+=f'''
local windAliases=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if windAliases==0 and address==0x080382AC and value=={old} and s['cpu.pipeline.execute.address']==0x08037F20 and s['cpu.r0']==0x08038278 and s['cpu.r1']==1 and s['cpu.r3']==52 then
  windAliases=1;return {pool}
 end
end,emu.callbackType.read,0x080382AC,0x080382AF)
local function dumpWindAlias(name)
 write(name..'_wind_alias.json','{{"root_aliases":'..windAliases..',"requested_script":1,"target_script":1}}')
end
'''
    for oldmarker,new in [('local function capture(name)\n','local function capture(name)\n dumpWindAlias(name)\n'),('local function finish()\n',"local function finish()\n dumpWindAlias('final')\n")]:
        if pet.runner.LUA_TEMPLATE.count(oldmarker)!=1:raise ValueError('capture anchor')
        pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(oldmarker,new,1)
    rc=pet.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_wind_alias.json').read_text());passed=rc==0 and r['complete'] and d['root_aliases']==1
    scope='DIAGNOSTIC one observed native NumberMan seasonal root read aliases to WindMan script1. Same window/consumer, NumberMan portrait/caller retained. No ROM/RAM writes; NOT actual WindMan unlock, portrait, holiday selection or normal play proof.'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf8')
    (out/'wind_environment.json').write_text(json.dumps(dict(passed=passed,scope=scope,rom_sha256=m['output_sha256'],tool_sha256=sha(Path(__file__).read_bytes()),observer_sha256=sha(Path(pet.__file__).read_bytes()),lookup_evidence=str(lookup),lookup_sha256=sha((lookup/'final_seasonal_lookup.json').read_bytes()),native_observation=matching[0],pool=pool,**d),indent=2),encoding='utf8')
    print('WindMan renderer-only diagnostic',passed);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
