"""Diagnostic real compiled descriptions1..30; controller page changes only."""
import json
import struct
from pathlib import Path
import capture_chip_folder_qa as normal
from build_visibility_poc import sha,require_hash


def main():
    fixed=normal.frozen.library.fixed;rom=Path(fixed.value('--rom')).resolve()
    m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256']);blob=rom.read_bytes()
    r=next(r for r in m['archives'] if r['archive']=='76937C')
    if r['translated_units']!=30: raise ValueError('mono batch needs protected30 descriptions')
    base=0x08000000+r['rom_offset'];offsets=[struct.unpack_from('<H',blob,r['rom_offset']+i*2)[0] for i in range(1,31)]
    code=f'''
local monoBatchReads=0
local monoBatchOffsets={{{','.join(map(str,offsets))}}}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x080554A8 or s['cpu.r6']~=0x08619EF8 then return end
 monoBatchReads=monoBatchReads+1
 return monoBatchOffsets[(monoBatchReads-1)%30+1]
end,emu.callbackType.read,{base},{base+511})
local function dumpMonoBatchReads(name)
 write(name..'_mono_batch_reads.json',string.format('{{"reads":%d}}',monoBatchReads))
end
'''
    fixed.PROBE+=code
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpMonoBatchReads(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpMonoBatchReads('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1: raise ValueError('mono batch capture anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=normal.main();out=Path(fixed.value('--out'));result=json.loads((out/'result.json').read_text())
    calls=json.loads((out/'final_fixedcells.json').read_text())['calls'];streams={base+off:i for i,off in zip(range(1,31),offsets)}
    covered={streams[c['stream']] for c in calls if c['font']==0x08619EF8 and c['stream'] in streams}
    d=json.loads((out/'final_mono_batch_reads.json').read_text())
    valid=rc==0 and result['complete'] and covered==set(range(1,31)) and d['reads']>=30
    scope='DIAGNOSTIC mono source-table CPU reads choose real compiled description scripts1..30; no text-byte/ROM/save-RAM injection; NOT 30 acquired normal-play claims'
    result.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
        result['artifacts']['diagnostic_checkpoint.mss']=result['artifacts'].pop('checkpoint.mss')
    if not valid: result['complete']=False
    (out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    for filename in ('folder_qa_environment.json','library_environment.json','probe_environment.json'):
        if (out/filename).exists():
            e=json.loads((out/filename).read_text());e['scope']=scope
            (out/filename).write_text(json.dumps(e,indent=2),encoding='utf-8')
    (out/'mono_batch_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],
        'tool_sha256':sha(Path(__file__).read_bytes()),'passed':valid,'scope':scope,'covered_scripts':sorted(covered),
        'lookup_reads':d['reads'],'pool':base,'script_offsets':offsets},indent=2),encoding='utf-8')
    print('actual mono batch:',valid,'scripts',len(covered),'lookup reads',d['reads'])
    return rc if valid else 1


if __name__=='__main__': raise SystemExit(main())
