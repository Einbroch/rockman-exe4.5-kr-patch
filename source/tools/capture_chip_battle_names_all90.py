"""Name-only stack CPU-read aliases; held8frames, no chip acquisition/RAM edits."""
import json
from pathlib import Path
import capture_chip_battle_names as normal
from build_visibility_poc import sha


def main():
    fixed=normal.library.fixed
    fixed.PROBE+=r'''
local nameAliasReads=0
local nameAliasOriginals={}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x080166A6 then return end
 if address~=s['cpu.r13'] then error('battle-name stack read extent') end
 nameAliasReads=nameAliasReads+1
 nameAliasOriginals[tostring(value)]=true
 return (math.floor((nameAliasReads-1)/24)*3+(nameAliasReads-1)%3)%90+1
end,emu.callbackType.read,0x03000000,0x03007FFF)
local function dumpNameAliases(name)
 local values={};for k,v in pairs(nameAliasOriginals) do values[#values+1]=k end
 write(name..'_name_aliases.json',string.format('{"reads":%d,"original_values":[%s]}',nameAliasReads,table.concat(values,',')))
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpNameAliases(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpNameAliases('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1: raise ValueError('battle-name alias dump anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=normal.main();out=Path(fixed.value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_name_aliases.json').read_text())
    calls=json.loads((out/'final_fixedcells.json').read_text())['calls'];valid=rc==0 and r['complete'] and d['reads']==len(calls)==720
    scope='DIAGNOSTIC name-only stack CPU-read aliases at166A6 choose scripts1..90 held8frames; no ROM/text/descriptor/save-RAM edits; not90 acquired battle chips'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not valid: r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    (out/'battle_name_alias_environment.json').write_text(json.dumps({'rom_sha256':r['rom_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'passed':valid,'scope':scope,'observed':d,'parser_calls':len(calls)},indent=2),encoding='utf-8')
    print('battle-name aliases:',valid,'reads/calls',d['reads'],len(calls))
    return rc if valid else 1


if __name__=='__main__': raise SystemExit(main())
