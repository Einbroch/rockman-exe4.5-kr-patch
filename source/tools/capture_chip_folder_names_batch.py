"""Diagnostic folder descriptor reads; actual clone names, 30-update pages."""
import json
from pathlib import Path
import capture_chip_folder_qa as normal
from build_visibility_poc import sha


def main():
    fixed=normal.frozen.library.fixed
    code=r'''
local folderBatchActive=false
local folderBatchEpoch=0
local folderBatchRows=0
local folderBatchReads=0
local folderBatchDesc=nil
local folderBatchFrames={}
local folderBatchBefore={}
local function folderBatchFail(s) write('folder_batch_failed.txt',s);emu.stop(1);error(s) end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r2']~=0x0202A680 or s['cpu.r5']~=7 then return end
 if folderBatchActive then folderBatchFail('nested folder batch') end
 folderBatchDesc=s['cpu.r1']+s['cpu.r0']*32
 folderBatchEpoch=folderBatchEpoch+1;folderBatchActive=true
 folderBatchFrames[#folderBatchFrames+1]=s['frameCount']
 local key=tostring(folderBatchDesc)
 if not folderBatchBefore[key] then folderBatchBefore[key]=hexAt(folderBatchDesc,224) end
end,emu.callbackType.exec,0x0803CB20,0x0803CB20)
emu.addMemoryCallback(function(address,value)
 if not folderBatchActive then return end
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x0803CB48 then return end
 if address<folderBatchDesc+8 or address>=folderBatchDesc+224 or (address-folderBatchDesc)%32~=8 then folderBatchFail('folder descriptor bounds') end
 folderBatchReads=folderBatchReads+1
 local row=math.floor((address-folderBatchDesc)/32)
 local id=(math.floor((folderBatchEpoch-1)/30)*7+row)%30+1
 return id*128
end,emu.callbackType.read,0x02000000,0x0203FFFF)
emu.addMemoryCallback(function()
 if not folderBatchActive then return end
 local s=emu.getState();folderBatchRows=folderBatchRows+1
 if s['cpu.r4']==6 then folderBatchActive=false end
end,emu.callbackType.exec,0x0803CB7A,0x0803CB7A)
local function dumpFolderBatch(name)
 local records={}
 for address,before in pairs(folderBatchBefore) do
  local after=hexAt(tonumber(address),224)
  if before~=after then folderBatchFail('underlying folder descriptor mutated') end
  records[#records+1]=string.format('{"address":%s,"before":"%s","after":"%s"}',address,before,after)
 end
 write(name..'_folder_batch.json',string.format('{"epochs":%d,"rows":%d,"descriptor_reads":%d,"descriptors":[%s]}',folderBatchEpoch,folderBatchRows,folderBatchReads,table.concat(records,',')))
end
'''
    fixed.PROBE+=code
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpFolderBatch(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpFolderBatch('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:
            raise ValueError('folder batch dump anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=normal.main();out=Path(fixed.value('--out'))
    m=json.loads(Path(fixed.value('--rom')).with_suffix('.json').read_text())
    selected={u['script'] for u in m['chip_folder_extension']['clone']['units']}
    if selected!=set(range(1,31)):
        raise ValueError('folder batch requires protected names 1..30')
    d=json.loads((out/'final_folder_batch.json').read_text())
    c=json.loads((out/'final_chip_ko.json').read_text())
    covered={r['script'] for r in c['rows'] if r['private']}
    valid=rc==0 and d['epochs']>150 and d['rows']==d['epochs']*7 and d['descriptor_reads']==d['rows'] and covered==selected
    scope='DIAGNOSTIC folder descriptor CPU-read substitution; real clone names 1..30; no ROM/name-byte/save-RAM injection; not acquired normal play; pages held 30 updates'
    result=json.loads((out/'result.json').read_text())
    result.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
        result['artifacts']['diagnostic_checkpoint.mss']=result['artifacts'].pop('checkpoint.mss')
    if not valid: result['complete']=False
    (out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (out/'folder_batch_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),
        'rom_sha256':m['output_sha256'],'passed':valid,'scope':scope,'covered_scripts':sorted(covered),'observed':d},indent=2),encoding='utf-8')
    print('folder actual clone names:',valid,'covered',len(covered),'rows',d['rows'])
    return rc if valid else 1


if __name__=='__main__':
    raise SystemExit(main())
