"""Quarantined native first-meeting table-read alias to return script2."""
import json,struct,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,sha,require_hash

def main():
    args=sys.argv
    def value(k):return args[args.index(k)+1]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']
    require_hash(source,'588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8')
    if rom[0x4FB4C:0x4FC20]!=source.read_bytes()[0x4FB4C:0x4FC20]:raise ValueError('native init changed')
    ar=next(a for a in m['archives'] if a['archive']=='6872B8');pool=0x08000000+ar['rom_offset'];offset=struct.unpack_from('<H',rom,ar['rom_offset']+4)[0]
    pet.ARCHIVE='6872B8'
    pet.PROBE+=f'''
local returnAliasReads=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if returnAliasReads==0 and address=={pool+2} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==2 and s['cpu.r5']==0x0200FA20 then returnAliasReads=1;return {offset} end
end,emu.callbackType.read,{pool+2},{pool+3})
local function dumpReturnAlias(name)
 write(name..'_return_alias.json','{{"target_script":2,"requested_script":1,"read_aliases":'..returnAliasReads..'}}')
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpReturnAlias(name)\n'),('local function finish()\n',"local function finish()\n dumpReturnAlias('final')\n")]:
        if pet.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('return capture anchor')
        pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=pet.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());data=json.loads((out/'final_return_alias.json').read_text())
    scope='DIAGNOSTIC native script1 offset read alias to2. Requested script1 remains in active label. No direct ROM/RAM writes; not actual Navi reselection or flag acquisition proof.'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    passed=rc==0 and r['complete'] and data['read_aliases']==1
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf8')
    (out/'return_environment.json').write_text(json.dumps(dict(passed=passed,scope=scope,rom_sha256=m['output_sha256'],tool_sha256=sha(Path(__file__).read_bytes()),observer_sha256=sha(Path(pet.__file__).read_bytes()),**data),indent=2),encoding='utf8')
    print('return renderer alias',passed)
    return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
