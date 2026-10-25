"""Quarantined native TACTICS table-offset read aliases0/1 -> Roll6/7."""
import json,struct
from pathlib import Path
import capture_tactics_prompts as prompts
import capture_library_qa as library
from build_visibility_poc import ROOT,sha,require_hash

def main():
    fixed=library.fixed;rom=Path(fixed.value('--rom'));m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256'])
    ar=next(a for a in m['archives'] if a['archive']=='76C944');base=0x08000000+ar['rom_offset'];blob=rom.read_bytes()
    project=json.loads((ROOT/'project.json').read_text());source=ROOT/project['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    for start,end in [(0x20B48,0x20B70),(0x212C8,0x212E8),(0x554A4,0x554C4)]:
        if blob[start:end]!=native[start:end]:raise ValueError('native TACTICS lookup code changed')
    offsets=[struct.unpack_from('<H',blob,ar['rom_offset']+i*2)[0] for i in (6,7)]
    fixed.PROBE+=f'''
local rollPromptAliases={{}}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local index=s['cpu.r1']
 if s['cpu.pipeline.execute.address']~=0x080554A8 or s['cpu.r0']~={base} or s['cpu.r14']~=0x08020B5F or (index~=0 and index~=2) then return end
 local displayed=index==0 and 6 or 7;local offset=index==0 and {offsets[0]} or {offsets[1]}
 rollPromptAliases[#rollPromptAliases+1]=string.format('{{"native_script":%d,"displayed_script":%d,"offset":%d,"frame":%d}}',index/2,displayed,offset,frame)
 return offset
end,emu.callbackType.read,{base},{base+3})
local function dumpRollPromptAliases(name)
 write(name..'_roll_prompt_aliases.json','{{"calls":['..table.concat(rollPromptAliases,',')..']}}')
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpRollPromptAliases(name)\n'),
        ('local function finish()\n',"local function finish()\n dumpRollPromptAliases('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('prompt alias anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=prompts.main();out=Path(fixed.value('--out'));route=json.loads((out/'result.json').read_text());calls=json.loads((out/'final_roll_prompt_aliases.json').read_text())['calls']
    scope='DIAGNOSTIC native TACTICS0/1 table offset read aliases to compiled Roll6/7; native Rockman portrait/player unchanged, no ROM/text/progress/save-RAM writes; NOT normal Roll selection'
    route.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');route['artifacts']['diagnostic_checkpoint.mss']=route['artifacts'].pop('checkpoint.mss')
    valid=rc==0 and route['complete'] and {c['displayed_script'] for c in calls}=={6,7}
    if not valid:route['complete']=False
    (out/'result.json').write_text(json.dumps(route,indent=2),encoding='utf-8')
    (out/'roll_prompt_alias_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),
        'observer_sha256':sha(Path(prompts.__file__).read_bytes()),'passed':valid,'scope':scope,'calls':calls},indent=2),encoding='utf-8')
    return rc if valid else 1

if __name__=='__main__':raise SystemExit(main())
