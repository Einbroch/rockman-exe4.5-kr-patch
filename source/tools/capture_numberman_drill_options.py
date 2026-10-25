"""Quarantined native script0 table-read alias to13/15, renderer-only proof."""
import argparse,json,struct,sys
from pathlib import Path
import capture_numberman_drill as drill
from build_visibility_poc import ROOT,sha,require_hash

def main():
    ap=argparse.ArgumentParser(add_help=False);ap.add_argument('--script',type=int,choices=(13,15),required=True);a,rest=ap.parse_known_args();sys.argv=[sys.argv[0]]+rest
    def value(k):return rest[rest.index(k)+1]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    original=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()
    require_hash(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'],'588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8')
    if rom[0x4FB4C:0x4FC20]!=original[0x4FB4C:0x4FC20]:raise ValueError('native init modified')
    ar=next(x for x in m['archives'] if x['archive']=='715064');pool=0x08000000+ar['rom_offset'];offset=struct.unpack_from('<H',rom,ar['rom_offset']+a.script*2)[0]
    drill.pet.PROBE+=f'''
local optionAliasReads=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if optionAliasReads==0 and address=={pool} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==0 and s['cpu.r5']==0x0200FA20 then optionAliasReads=1;return {offset} end
end,emu.callbackType.read,{pool},{pool+1})
local function dumpOptionAlias(name)
 write(name..'_options_alias.json','{{"target_script":{a.script},"requested_script":0,"read_aliases":'..optionAliasReads..'}}')
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpOptionAlias(name)\n'),('local function finish()\n',"local function finish()\n dumpOptionAlias('final')\n")]:
        if drill.pet.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('options capture anchor')
        drill.pet.runner.LUA_TEMPLATE=drill.pet.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=drill.main();out=Path(value('--out'));receipt=json.loads((out/'result.json').read_text());data=json.loads((out/'final_options_alias.json').read_text())
    scope='DIAGNOSTIC native script0 halfword table-read alias to13/15; no ROM/RAM direct writes. Initial active script label remains0; current target stream/offset proves renderer only. Not academic flags/acquisition, level invocation or gameplay selection effect proof.'
    receipt.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');receipt['artifacts']['diagnostic_checkpoint.mss']=receipt['artifacts'].pop('checkpoint.mss')
    passed=rc==0 and receipt['complete'] and data['read_aliases']==1
    if not passed:receipt['complete']=False
    (out/'result.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    (out/'options_environment.json').write_text(json.dumps({'passed':passed,'scope':scope,'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'observer_sha256':sha(Path(drill.__file__).read_bytes()),**data},indent=2),encoding='utf-8')
    print('options diagnostic',a.script,'passed',passed)
    return rc if passed else 1

if __name__=='__main__':raise SystemExit(main())
