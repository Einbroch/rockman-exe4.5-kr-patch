"""Read-only source-read trace for native PET OBJ block; no data overrides."""
import json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha

EXTRA=r'''
local petReads={};local petReadCount=0
emu.addMemoryCallback(function(address,value)
 petReadCount=petReadCount+1
 if #petReads>=160 then return end
 local s=emu.getState()
 petReads[#petReads+1]=string.format('{"address":%d,"value":%d,"frame":%d,"pc":%d,"lr":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d}',address,value or -1,frame,s['cpu.pipeline.execute.address'],s['cpu.r14'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'])
end,emu.callbackType.read,0x086303B8,0x086315B7)
local function dumpPetReads(name)
 write(name..'_pet_source_reads.json',string.format('{"total":%d,"first_reads":[%s]}',petReadCount,table.concat(petReads,',')))
end
'''

def main():
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,EXTRA+marker+' dumpPetReads(name)\n',1)
    rc=runner.main()
    return rc

if __name__=='__main__':raise SystemExit(main())
