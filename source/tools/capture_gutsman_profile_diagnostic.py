"""Quarantined native profile29 table-read alias; renderer evidence only."""
import json,struct,sys
from pathlib import Path
import capture_roll_family as normal
from archive_scripts import script_spans
from build_visibility_poc import ROOT,sha,require_hash
from keyitem_rom_data import verify_final

SCRIPTS=[27,32,33,34,80,81,82,83,84,85,86,87,89,90,91,92,93,94,95]
QUESTION_SCRIPTS=[9,11,13,15,17,19,21,23,25,88]
FAMILY_SCRIPTS=[1,3,5,7]
ANSWER_SCRIPTS=[40,41,43,44,46,47,49,50,52,53,55,56,58,59,61,62]
WISHLIST_SCRIPTS=[31]
HEADER=bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    target_script=int(value('--profile-script'));i=sys.argv.index('--profile-script');del sys.argv[i:i+2]
    if target_script not in SCRIPTS+QUESTION_SCRIPTS+FAMILY_SCRIPTS+ANSWER_SCRIPTS+WISHLIST_SCRIPTS:raise ValueError('unregistered profile diagnostic')
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    original_path=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(original_path,m['source_sha256']);source=original_path.read_bytes()
    verify_final(source,rom,m['keyitem_rom'])
    guards=[]
    for a,b in [(0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB58,0x4FC20)]:
        if rom[a:b]!=source[a:b]:raise ValueError('profile caller/initializer/native reader drift')
        guards.append(dict(start=a,end=b,sha256=sha(source[a:b])))
    ar=next(x for x in m['archives'] if x['archive']=='667044');pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    spans=script_spans(payload,97);native=script_spans(source[0x667044:0x667044+5225],97)
    skip=spans[target_script].find(HEADER)
    if not spans[29].startswith(HEADER) or skip<0 or native[target_script].find(HEADER)!=skip or spans[target_script].count(HEADER)!=1 or (skip and target_script not in (17,32)):raise ValueError('profile source-pinned UI entry')
    if spans[target_script][:skip]!=native[target_script][:skip]:raise ValueError('profile age dispatch changed')
    old=struct.unpack_from('<H',payload,29*2)[0];target=struct.unpack_from('<H',payload,target_script*2)[0]+skip;address=pool+29*2
    normal.ARCHIVE='667044'
    normal.pet.PROBE+=f'''
local profileAliases=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if profileAliases==0 and address=={address} and value=={old} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==58 and s['cpu.r5']==0x0200FA20 then
  profileAliases=profileAliases+1;return {target}
 end
end,emu.callbackType.read,{address},{address+1})
local function dumpProfileAlias(name)
 write(name..'_profile_alias.json','{{"aliases":'..profileAliases..',"requested_script":29,"displayed_script":{target_script},"source_offset":{old},"target_offset":{target},"age_dispatch_skipped_bytes":{skip if target_script==32 else 0},"gender_dispatch_skipped_bytes":{skip if target_script==17 else 0}}}')
end
'''
    for anchor,new in [('local function capture(name)\n','local function capture(name)\n dumpProfileAlias(name)\n'),('local function finish()\n',"local function finish()\n dumpProfileAlias('final')\n")]:
        if normal.pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('profile diagnostic anchor')
        normal.pet.runner.LUA_TEMPLATE=normal.pet.runner.LUA_TEMPLATE.replace(anchor,new,1)
    rc=normal.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_profile_alias.json').read_text());passed=rc==0 and r['complete'] and d['aliases']==1
    scope='DIAGNOSTIC guarded profile29 table read alias to source-pinned UI entry. No ROM/RAM writes. NOT native age/response selection, input, persistence or progression evidence.'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    (out/'profile_environment.json').write_text(json.dumps(dict(passed=passed,rom_sha256=m['output_sha256'],scope=scope,tool_sha256=sha(Path(__file__).read_bytes()),observer_sha256=sha(Path(normal.__file__).read_bytes()),probe_sha256=sha(Path(normal.pet.__file__).read_bytes()),native_guards=guards,**d),indent=2),encoding='utf-8')
    print('profile diagnostic',passed,d);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
