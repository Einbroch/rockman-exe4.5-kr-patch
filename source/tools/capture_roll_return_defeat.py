"""Quarantined native return table read alias1->2; not actual defeat evidence."""
import json,struct,sys
from pathlib import Path
import capture_roll_return as normal
from build_visibility_poc import ROOT,sha,require_hash

def main():
    args=sys.argv
    def value(k):return args[args.index(k)+1]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes();source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);original=source.read_bytes();guards=[]
    for a,b in [(0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB4C,0x4FC20)]:
        if rom[a:b]!=original[a:b]:raise ValueError('native return caller/initializer changed')
        guards.append({'start':a,'end':b,'sha256':sha(original[a:b])})
    ar=next(x for x in m['archives'] if x['archive']=='65FEC0');pool=0x08000000+ar['rom_offset'];old=struct.unpack_from('<H',rom,ar['rom_offset']+2)[0];target=struct.unpack_from('<H',rom,ar['rom_offset']+4)[0]
    normal.PROBE+=f'''
local defeatAliases=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if defeatAliases==0 and address=={pool+2} and value=={old} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==2 and s['cpu.r5']==0x0200FA20 then
  defeatAliases=defeatAliases+1;return {target}
 end
end,emu.callbackType.read,{pool+2},{pool+3})
local function dumpDefeat(name)
 write(name..'_defeat_alias.json','{{"aliases":'..defeatAliases..',"native_script":1,"displayed_entry":2,"source_offset":{old},"target_offset":{target}}}')
end
'''
    for anchor,new in [('local function capture(name)\n','local function capture(name)\n dumpDefeat(name)\n'),('local function finish()\n',"local function finish()\n dumpDefeat('final')\n")]:
        if normal.pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('defeat capture anchor')
        normal.pet.runner.LUA_TEMPLATE=normal.pet.runner.LUA_TEMPLATE.replace(anchor,new,1)
    rc=normal.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_defeat_alias.json').read_text());passed=rc==0 and r['complete'] and d['aliases']==1
    scope='DIAGNOSTIC native table read alias1->2 only. No observer ROM/RAM writes. NOT actual defeat or normal loss selection evidence.'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    (out/'defeat_environment.json').write_text(json.dumps({'passed':passed,'rom_sha256':m['output_sha256'],'scope':scope,'tool_sha256':sha(Path(__file__).read_bytes()),'observer_sha256':sha(Path(normal.__file__).read_bytes()),'probe_sha256':sha(Path(normal.pet.__file__).read_bytes()),'native_guards':guards,**d},indent=2),encoding='utf-8');print('defeat diagnostic',passed,d);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
