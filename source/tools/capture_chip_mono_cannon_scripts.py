"""Diagnostic script-table read aliases for actual compiled Cannon scripts1..3."""
import json
import struct
from pathlib import Path
import capture_chip_folder_qa as normal
from build_visibility_poc import sha,require_hash


def main():
    fixed=normal.frozen.library.fixed;rom=Path(fixed.value('--rom')).resolve()
    m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256']);blob=rom.read_bytes()
    r=next(r for r in m['archives'] if r['archive']=='76937C');base=0x08000000+r['rom_offset']
    offsets=[struct.unpack_from('<H',blob,r['rom_offset']+i*2)[0] for i in (1,2,3)]
    code=f'''
local monoScriptReads=0
local monoOffsets={{{','.join(map(str,offsets))}}}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x080554A8 or s['cpu.r6']~=0x08619EF8 then return end
 monoScriptReads=monoScriptReads+1
 return monoOffsets[(monoScriptReads-1)%3+1]
end,emu.callbackType.read,{base+2},{base+3})
local function dumpMonoScriptReads(name)
 write(name..'_mono_script_reads.json',string.format('{{"reads":%d}}',monoScriptReads))
end
'''
    fixed.PROBE+=code
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpMonoScriptReads(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpMonoScriptReads('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1: raise ValueError('mono script dump anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=normal.main();out=Path(fixed.value('--out'));result=json.loads((out/'result.json').read_text())
    calls=json.loads((out/'final_fixedcells.json').read_text())['calls']
    streams={base+off:i for i,off in zip((1,2,3),offsets)}
    covered={streams[c['stream']] for c in calls if c['font']==0x08619EF8 and c['stream'] in streams}
    d=json.loads((out/'final_mono_script_reads.json').read_text())
    valid=rc==0 and result['complete'] and covered=={1,2,3} and d['reads']>=3
    scope='DIAGNOSTIC mono script1 lookup CPU-read returns real compiled script1/2/3 offsets; no text-byte/ROM/save-RAM injection; not HiCannon/MegaCannon acquired normal play'
    result.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
        result['artifacts']['diagnostic_checkpoint.mss']=result['artifacts'].pop('checkpoint.mss')
    if not valid: result['complete']=False
    (out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (out/'mono_script_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],
        'tool_sha256':sha(Path(__file__).read_bytes()),'passed':valid,'scope':scope,'covered_scripts':sorted(covered),
        'lookup_reads':d['reads'],'pool':base,'script_offsets':offsets},indent=2),encoding='utf-8')
    print('actual mono scripts:',valid,sorted(covered),'lookup reads',d['reads'])
    return rc if valid else 1


if __name__=='__main__': raise SystemExit(main())
