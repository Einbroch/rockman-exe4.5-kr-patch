"""Quarantined native table-read alias; NOT played/completed minigames."""
import argparse,json,struct,sys
from pathlib import Path
import capture_roll_pet as normal
from build_visibility_poc import ROOT,sha,require_hash

def main():
    ap=argparse.ArgumentParser(add_help=False);ap.add_argument('--script',type=int,choices=(50,60),required=True)
    args,rest=ap.parse_known_args();sys.argv=[sys.argv[0]]+rest
    def value(key):return rest[rest.index(key)+1]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256'])
    blob=rp.read_bytes();original=source.read_bytes();guards=[]
    for start,end in [(0x4F7B6,0x4F7D0),(0x4FB4C,0x4FC20)]:
        if blob[start:end]!=original[start:end]:raise ValueError('native initializer modified')
        guards.append({'start':start,'end':end,'sha256':sha(blob[start:end])})
    ar=next(a for a in m['archives'] if a['archive']=='65FF3C');pool=0x08000000+ar['rom_offset']
    offset=struct.unpack_from('<H',blob,ar['rom_offset']+args.script*2)[0];source_offset=struct.unpack_from('<H',blob,ar['rom_offset'])[0]
    normal.ARCHIVE='65FF3C'
    normal.PROBE+=f'''
local miniAliasReads=0;local miniAliasFrame=-1;local miniAliasLR=0;local miniAliasContext=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if miniAliasReads~=0 or address~={pool} or s['cpu.pipeline.execute.address']~=0x0804FB76 or s['cpu.r0']~={pool} or s['cpu.r1']~=0 then return end
 miniAliasReads=miniAliasReads+1;miniAliasFrame=frame;miniAliasLR=s['cpu.r14'];miniAliasContext=s['cpu.r5']
 return {offset}
end,emu.callbackType.read,{pool},{pool+1})
local function dumpMiniAlias(name)
 write(name..'_mini_alias.json',string.format('{{"native_script":0,"displayed_entry":{args.script},"source_offset":{source_offset},"offset":{offset},"reads":%d,"frame":%d,"lr":%d,"context":%d}}',miniAliasReads,miniAliasFrame,miniAliasLR,miniAliasContext))
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpMiniAlias(name)\n'),('local function finish()\n',"local function finish()\n dumpMiniAlias('final')\n")]:
        if normal.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('alias capture anchor')
        normal.runner.LUA_TEMPLATE=normal.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=normal.main();out=Path(value('--out'));route=json.loads((out/'result.json').read_text());d=json.loads((out/'final_mini_alias.json').read_text())
    scope='DIAGNOSTIC native fortune-script0 table-offset read alias; native minigame record/branch code executes, but no minigame played. No observer ROM/RAM writes. NOT real completion/reward evidence.'
    route.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');route['artifacts']['diagnostic_checkpoint.mss']=route['artifacts'].pop('checkpoint.mss')
    valid=rc==0 and route['complete'] and d['reads']==1 and d['context']==0x0200FA20
    if not valid:route['complete']=False
    (out/'result.json').write_text(json.dumps(route,indent=2),encoding='utf-8')
    (out/'mini_alias_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'observer_sha256':sha(Path(normal.__file__).read_bytes()),'native_code_guards':guards,'passed':valid,'scope':scope,**d},indent=2),encoding='utf-8')
    print('minigame diagnostic:',args.script,'reads:',d['reads'],'passed:',valid)
    return rc if valid else 1

if __name__=='__main__':raise SystemExit(main())
