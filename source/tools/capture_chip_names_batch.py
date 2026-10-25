"""Diagnostic acquisition/descriptor read substitution; consume real clone bytes."""
import json
from pathlib import Path
import capture_chip_late_wait_qa as normal
from build_visibility_poc import sha


def main():
    fixed = normal.variant.cache.word.base.library.fixed
    code = r'''
local batchDesc=nil
local batchEpoch=0
local batchActive=false
local batchReads=0
local batchAcquisitionReads=0
local batchRows=0
local batchOriginal={}
local function batchFail(s) write('batch_failed.txt',s);emu.stop(1);error(s) end
emu.addMemoryCallback(function()
 local s=emu.getState()
 batchDesc=s['cpu.r1']+s['cpu.r0']*4
 batchEpoch=batchEpoch+1;batchActive=true
 local key=tostring(batchDesc)
 if not batchOriginal[key] then batchOriginal[key]=hexAt(batchDesc,28) end
end,emu.callbackType.exec,0x08042E50,0x08042E50)
emu.addMemoryCallback(function(address,value)
 if not batchActive then return end
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 if pc==0x08005D20 then
  batchAcquisitionReads=batchAcquisitionReads+1
  return s['cpu.r1'] -- equal native comparison; bypass acquisition, no RAM edit
 end
 if address<batchDesc or address>=batchDesc+28 then return end
 local off=(address-batchDesc)%4
 if pc==0x08042E84 and off==0 then
  batchReads=batchReads+1
  return math.floor(((batchEpoch-1)*7+math.floor((address-batchDesc)/4))%30)+1
 elseif pc==0x08042EC8 and off==2 then
  batchReads=batchReads+1;return 1
 end
end,emu.callbackType.read,0x02000000,0x0203FFFF)
emu.addMemoryCallback(function()
 if not batchActive then batchFail('batch row without active descriptor') end
 batchRows=batchRows+1
 if batchRows%7==0 then batchActive=false end
end,emu.callbackType.exec,0x08042EE4,0x08042EE4)
local function dumpBatch(name)
 local records={}
 for address,before in pairs(batchOriginal) do
  local after=hexAt(tonumber(address),28)
  if before~=after then batchFail('underlying descriptor mutated') end
  records[#records+1]=string.format('{"address":%s,"before":"%s","after":"%s"}',address,before,after)
 end
 write(name..'_batch.json',string.format('{"epochs":%d,"rows":%d,"descriptor_reads":%d,"acquisition_reads":%d,"descriptors":[%s]}',batchEpoch,batchRows,batchReads,batchAcquisitionReads,table.concat(records,',')))
end
'''
    fixed.PROBE += code
    for old, new in [('local function capture(name)\n','local function capture(name)\n dumpBatch(name)\n'),
                     ('local function finish()\n',"local function finish()\n dumpBatch('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError('batch capture anchor drift')
        fixed.runner.LUA_TEMPLATE = fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc = normal.main()
    out = Path(fixed.value('--out'))
    m = json.loads(Path(fixed.value('--rom')).with_suffix('.json').read_text())
    selected = {u['script'] for u in m['chip_library_extension']['clone']['units']}
    if selected != set(range(1,31)):
        raise ValueError('batch requires exactly protected scripts 1..30')
    d = json.loads((out / 'final_batch.json').read_text())
    c = json.loads((out / 'final_chip_ko.json').read_text())
    covered = {r['script'] for r in c['rows'] if r['private']}
    valid = rc == 0 and d['epochs'] > 30 and d['rows'] == d['epochs']*7
    valid = valid and d['descriptor_reads'] == 2*d['rows'] and d['acquisition_reads'] == d['rows'] and covered == selected
    result = json.loads((out / 'result.json').read_text())
    scope = 'DIAGNOSTIC descriptor/acquisition CPU-read substitution; real compiled clone names 1..30; no ROM/name-byte/save-RAM injection; NOT acquired normal play'
    result['scope'], result['normal_play_checkpoint_eligible'] = scope, False
    if (out / 'checkpoint.mss').exists():
        (out / 'checkpoint.mss').rename(out / 'diagnostic_checkpoint.mss')
        result['artifacts']['diagnostic_checkpoint.mss'] = result['artifacts'].pop('checkpoint.mss')
    if not valid:
        result['complete'] = False
    (out / 'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (out / 'batch_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),
        'rom_sha256':m['output_sha256'],'passed':valid,'scope':scope,'covered_scripts':sorted(covered),'observed':d},indent=2),encoding='utf-8')
    print('real clone batch names:',valid,'scripts:',len(covered),'rows:',d['rows'])
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
