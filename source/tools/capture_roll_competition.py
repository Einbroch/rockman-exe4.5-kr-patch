"""Quarantined ROM-read aliases to Roll competition dialogue; never progress proof."""
import json,struct,sys
from pathlib import Path
import capture_roll_pet as pet
from capture_roll_return import PROBE
from build_visibility_poc import ROOT,sha,require_hash
from archive_scripts import script_spans

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    script=int(value('--competition-script'));i=sys.argv.index('--competition-script');del sys.argv[i:i+2]
    if script not in [1,2,10,20,21,22,23]:raise ValueError('unregistered competition entry')
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);original=source.read_bytes()
    for a,b in [(0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB4C,0x4FC20)]:
        if rom[a:b]!=original[a:b]:raise ValueError('native caller drift')
    ar=next((x for x in m['archives'] if x['archive']=='6615A8'),None);pool=0x08000000+(ar['rom_offset'] if ar else 0x6615A8);size=ar['compiled_bytes'] if ar else 426
    payload=rom[pool-0x08000000:pool-0x08000000+size];spans=script_spans(payload,25)
    if not spans[script].startswith(bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')):raise ValueError('window prefix drift')
    old=struct.unpack_from('<I',rom,0x3810C)[0];offset0=struct.unpack_from('<H',payload,0)[0];target=struct.unpack_from('<H',payload,script*2)[0]
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE+PROBE.replace('RETURN_POOL',str(pool)).replace('dumpReturn','dumpCompetitionRam').replace('_return_ram.json','_talk_ram.json')
    for key,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+size)]:code=code.replace(key,str(v))
    code+=f'''
local rootAliases=0;local entryAliases=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if rootAliases==0 and address==0x0803810C and value=={old} and s['cpu.pipeline.execute.address']==0x08037F20 and s['cpu.r1']==0 then
  rootAliases=rootAliases+1;return {pool}
 end
end,emu.callbackType.read,0x0803810C,0x0803810F)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if rootAliases==1 and entryAliases==0 and address=={pool} and value=={offset0} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==0 and s['cpu.r5']==0x0200FA20 then
  entryAliases=entryAliases+1;return {target}
 end
end,emu.callbackType.read,{pool},{pool+1})
local function dumpCompetition(name)
 write(name..'_competition_alias.json','{{"root_aliases":'..rootAliases..',"entry_aliases":'..entryAliases..',"script":{script}}}')
end
'''
    marker='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('capture anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpRollPet(name)\n dumpCompetitionRam(name)\n dumpCompetition(name)\n',1)
    anchor='local function finish()\n';pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,anchor+" dumpCompetition('final')\n",1)
    rc=pet.runner.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_competition_alias.json').read_text());passed=rc==0 and r['complete'] and d['root_aliases']==d['entry_aliases']==1
    r.update(scope='DIAGNOSTIC pointer/table read aliases to Roll competition entry. Not native tournament result/entry/flag progression evidence.',normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    (out/'competition_environment.json').write_text(json.dumps({'passed':passed,'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'pet_probe_sha256':sha(Path(pet.__file__).read_bytes()),'ram_probe_sha256':sha((ROOT/'tools/capture_roll_return.py').read_bytes()),'old_root':old,'pool':pool,'size':size,'target_offset':target,**d},indent=2),encoding='utf-8')
    print('competition diagnostic',passed,d);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
