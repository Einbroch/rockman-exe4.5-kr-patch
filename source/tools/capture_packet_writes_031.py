"""Read-only packet-name ownership probe on own030 normal controller routes."""
import sys
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

PROBE=r'''
local packetWrites={};local packetCalls={}
emu.addMemoryCallback(function(address,value)
 if #packetWrites>=30000 then error('031 bounded packet write log overflow') end
 local s=emu.getState()
 packetWrites[#packetWrites+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"r5":%d,"lr":%d}',frame,address,value,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r5'],s['cpu.r14'])
end,emu.callbackType.write,0x0200F560,0x0200F59F)
for _,pc in ipairs({0x080090FC,0x0800910E,0x08009122,0x08009134,0x08038584}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();packetCalls[#packetCalls+1]=string.format('{"frame":%d,"pc":%d,"r0":%d,"r1":%d,"r5":%d,"r10":%d,"lr":%d}',frame,pc,s['cpu.r0'],s['cpu.r1'],s['cpu.r5'],s['cpu.r10'],s['cpu.r14'])
 end,emu.callbackType.exec,pc,pc)
end
local function dumpPacketWrites(name)
 write(name..'_packet_writes.json','{"writes":['..table.concat(packetWrites,',')..'],"calls":['..table.concat(packetCalls,',')..']}')
end
'''

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(value('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    if m['output_sha256']!='203fd306a7c9c713e3c6f4e7af3dd24d5f21eab0c000f210a061295d31083491':raise ValueError('031 exact030 read-only baseline')
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('031 packet capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,PROBE+marker+' dumpPacketWrites(name)\n',1)
    return runner.main()

if __name__=='__main__':raise SystemExit(main())
