"""One table read alias on own relocated Guts talk; no root/state writes."""
import sys,json,struct
from pathlib import Path
import capture_gutsman_pet_talk as observer
import capture_roll_pet as pet
from archive_scripts import script_spans
from build_visibility_poc import ROOT,require_hash,sha
SCRIPTS=[11,12,17,25,27,33,34]
def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    script=int(value('--talk-script'));i=sys.argv.index('--talk-script');del sys.argv[i:i+2]
    if script not in SCRIPTS:raise ValueError('diagnostic scope')
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes();source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    guards=[]
    for a,b in [(0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB4C,0x4FC20)]:
        if rom[a:b]!=native[a:b]:raise ValueError('native consumer changed')
        guards.append(dict(start=a,end=b,sha256=sha(native[a:b])))
    ar=next(a for a in m['archives'] if a['archive']=='66A844');pool=0x8000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    if struct.unpack_from('<I',rom,0x38148)[0]!=pool or not script_spans(payload,255)[script].startswith(bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')):raise ValueError('own native root/window')
    offset0=struct.unpack_from('<H',payload,0)[0];target=struct.unpack_from('<H',payload,script*2)[0]
    code=f'''
local talkEntryAliases=0
emu.addMemoryCallback(function(a,v)
 local s=emu.getState()
 if talkEntryAliases==0 and a=={pool} and v=={offset0} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==0 and s['cpu.r5']==0x0200FA20 then talkEntryAliases=1;return {target} end
end,emu.callbackType.read,{pool},{pool+1})
local function dumpTalkAlias(name)
 write(name..'_talk_alias.json','{{"entry_aliases":'..talkEntryAliases..',"script":{script}}}')
end
'''
    anchor='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpTalkAlias(name)\n',1)
    anchor='local function finish()\n';pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,anchor+" dumpTalkAlias('final')\n",1)
    rc=observer.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_talk_alias.json').read_text());passed=rc==0 and r['complete'] and d['entry_aliases']==1
    r.update(scope='DIAGNOSTIC talk script0 offset alias only; native root/portrait preserved, no acquired flag/item/date claims.',normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf8')
    (out/'talk_environment.json').write_text(json.dumps(dict(passed=passed,rom_sha256=m['output_sha256'],tool_sha256=sha(Path(__file__).read_bytes()),observer_sha256=sha(Path(observer.__file__).read_bytes()),pet_probe_sha256=sha(Path(pet.__file__).read_bytes()),pool=pool,native_guards=guards,**d),indent=2),encoding='utf8')
    return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
