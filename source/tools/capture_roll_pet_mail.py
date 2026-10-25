"""Quarantined table read alias for Roll license text; not progress evidence."""
import json,struct,sys
from pathlib import Path
import capture_roll_pet_talk as normal
from build_visibility_poc import ROOT,sha,require_hash
from archive_scripts import script_spans

SCRIPTS=[32,33]
FLAG_PREFIX={32:"ee00d62421ff",33:""}
def main():
    args=sys.argv
    def value(k):return args[args.index(k)+1]
    target_script=int(value('--talk-script'));i=args.index('--talk-script');del args[i:i+2]
    if target_script not in SCRIPTS:raise ValueError('unregistered license diagnostic')
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes();source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);original=source.read_bytes();guards=[]
    for a,b in [(0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB4C,0x4FC20)]:
        if rom[a:b]!=original[a:b]:raise ValueError('native PET caller/initializer changed')
        guards.append({'start':a,'end':b,'sha256':sha(original[a:b])})
    ar=next(x for x in m['archives'] if x['archive']=='664E28');pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];spans=script_spans(payload,255)
    flag_prefix=bytes.fromhex(FLAG_PREFIX[target_script]);prefix=flag_prefix+bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')+(bytes.fromhex('f90c01') if target_script==33 else b'')
    original_spans=script_spans(original[0x664E28:0x664E28+2158],255)
    if not original_spans[target_script].startswith(prefix):raise ValueError('original event flag/window prefix')
    if spans[0]!=bytes.fromhex('ef000a') or not spans[target_script].startswith(prefix):raise ValueError('source-pinned PET diagnostic entry commands')
    old=struct.unpack_from('<H',payload,0)[0];target=struct.unpack_from('<H',payload,target_script*2)[0]
    normal.pet.PROBE+=f'''
local licenseAliases=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if licenseAliases==0 and address=={pool} and value=={old} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==0 and s['cpu.r5']==0x0200FA20 then
  licenseAliases=licenseAliases+1;return {target}
 end
end,emu.callbackType.read,{pool},{pool+1})
local function dumpLicense(name)
 write(name..'_license_alias.json','{{"aliases":'..licenseAliases..',"native_script":0,"displayed_entry":{target_script},"source_offset":{old},"target_offset":{target}}}')
end
'''
    for anchor,new in [('local function capture(name)\n','local function capture(name)\n dumpLicense(name)\n'),('local function finish()\n',"local function finish()\n dumpLicense('final')\n")]:
        if normal.pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('license capture anchor')
        normal.pet.runner.LUA_TEMPLATE=normal.pet.runner.LUA_TEMPLATE.replace(anchor,new,1)
    rc=normal.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_license_alias.json').read_text());passed=rc==0 and r['complete'] and d['aliases']==1
    scope='DIAGNOSTIC PET table alias0 to32/33; original flag9430 or nickname instruction retained. No flag/nickname/ROM/RAM writes; not native progression/mail receipt evidence.'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    (out/'license_environment.json').write_text(json.dumps({'passed':passed,'rom_sha256':m['output_sha256'],'scope':scope,'entry_tool':'capture_roll_pet_mail.py','entry_flag_prefix_hex':flag_prefix.hex(),'tool_sha256':sha(Path(__file__).read_bytes()),'observer_sha256':sha(Path(normal.__file__).read_bytes()),'probe_sha256':sha(Path(normal.pet.__file__).read_bytes()),'native_guards':guards,**d},indent=2),encoding='utf-8');print('license diagnostic',passed,d);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
