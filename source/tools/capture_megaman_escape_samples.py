"""Quarantined native script-offset read alias, not actual escape outcomes."""
import argparse,json,struct,sys
from pathlib import Path
import capture_megaman_escape as normal
from build_visibility_poc import sha,require_hash

def main():
    ap=argparse.ArgumentParser(add_help=False);ap.add_argument('--script',type=int,choices=(2,3,4),required=True)
    args,rest=ap.parse_known_args();sys.argv=[sys.argv[0]]+rest
    fixed=normal.fixed;rom=Path(fixed.value('--rom'));m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256'])
    ar=next(a for a in m['archives'] if a['archive']=='76C944');blob=rom.read_bytes();base=0x08000000+ar['rom_offset']
    offset=struct.unpack_from('<H',blob,ar['rom_offset']+args.script*2)[0]
    fixed.PROBE+=f'''
local escapeAliasReads=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x0804FB76 or s['cpu.r0']~={base} or s['cpu.r1']~=10 then return end
 escapeAliasReads=escapeAliasReads+1
 return {offset}
end,emu.callbackType.read,{base+10},{base+11})
local function dumpEscapeAlias(name)
 write(name..'_escape_alias.json',string.format('{{"native_script":5,"displayed_script":{args.script},"offset":{offset},"reads":%d}}',escapeAliasReads))
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpEscapeAlias(name)\n'),
            ('local function finish()\n',"local function finish()\n dumpEscapeAlias('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('escape alias capture anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=normal.main();out=Path(fixed.value('--out'));route=json.loads((out/'result.json').read_text());d=json.loads((out/'final_escape_alias.json').read_text())
    scope=f'DIAGNOSTIC native forbidden-script5 table-offset CPU-read alias to compiled script{args.script}; no ROM/text/progress/save-RAM writes; NOT real escape result'
    route.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
        route['artifacts']['diagnostic_checkpoint.mss']=route['artifacts'].pop('checkpoint.mss')
    valid=rc==0 and route['complete'] and d['reads']>0
    if not valid:route['complete']=False
    (out/'result.json').write_text(json.dumps(route,indent=2),encoding='utf-8')
    (out/'escape_alias_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),
        'observer_sha256':sha(Path(normal.__file__).read_bytes()),'passed':valid,'scope':scope,**d},indent=2),encoding='utf-8')
    print('escape displayed script:',args.script,'alias reads:',d['reads'],'passed:',valid)
    return rc if valid else 1

if __name__=='__main__':raise SystemExit(main())
