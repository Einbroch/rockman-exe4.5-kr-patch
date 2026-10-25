"""Read-only actual038 communication-menu loader/reader trace, not039 proof."""
import sys,json
from pathlib import Path
import capture_field_loader_038_v1 as native
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    s=read('analysis/pending_insertion_500_039_communication_source_v1/selection.json')
    if s['baseline_sha256']!=m['output_sha256']:raise ValueError('038 observation source applicability')
    lengths={int(x['archive'],16)+0x08000000:x['native_bytes'] for x in s['profile_source_owners']}
    code=r'''
local commEvents={};local commLoads=0;local commSource=nil;local commDraws={}
local commLengths=LENGTHS
local function c32(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
for _,pc in ipairs({0x080448C8,0x080448D6,0x080448BC,0x080448C2,0x080448C6}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local regs={}
  for j=0,14 do regs[#regs+1]=string.format('"%d":%d',j,s['cpu.r'..j]) end
  commEvents[#commEvents+1]=string.format('{"frame":%d,"pc":%d,"context":%d,"root":%d,"stream":%d,"registers":{%s}}',frame,pc,c32(s['cpu.r10']+44),c32(0x0200FA50),c32(0x0200FA4C),table.concat(regs,','))
  if pc==0x080448D6 then
   if s['cpu.r1']~=0x02024000 or not commLengths[s['cpu.r0']] then error('Original communication LZ source/root differs') end
   commSource=s['cpu.r0']
  end
 end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 if commSource then
  commLoads=commLoads+1;local t={}
  for j=0,commLengths[commSource]-1 do t[#t+1]=string.char(emu.read(0x02024000+j,emu.memType.gbaMemory)) end
  write(string.format('communication_native_%03d.bin',commLoads),table.concat(t));commSource=nil
 end
end,emu.callbackType.exec,0x080448DA,0x080448DA)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r4']>=0x02024000 and s['cpu.r4']<0x02026000 then
  commDraws[#commDraws+1]=string.format('{"frame":%d,"stream":%d,"index":%d,"offset":%d,"context":%d}',frame,s['cpu.r4'],s['cpu.r1'],s['cpu.r6'],s['cpu.r5'])
 end
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)

local commNested={};local commCommands={}
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']==0x02024000 then
  commNested[#commNested+1]=string.format('{"frame":%d,"root":%d,"script":%d,"lr":%d,"sp":%d,"saved_outer_lr":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'],s['cpu.r13'],c32(s['cpu.r13']+16))
 end
end,emu.callbackType.exec,0x0804FB4C,0x0804FB4C)
for _,pc in ipairs({0x08051098,0x08050754}) do
 emu.addMemoryCallback(function()
  local s=emu.getState()
  if s['cpu.r4']>=0x02024000 and s['cpu.r4']<0x02026000 then
   commCommands[#commCommands+1]=string.format('{"frame":%d,"pc":%d,"stream":%d,"context":%d,"op":%d,"arg":%d}',frame,pc,s['cpu.r4'],s['cpu.r5'],emu.read(s['cpu.r4'],emu.memType.gbaMemory),emu.read(s['cpu.r4']+1,emu.memType.gbaMemory))
  end
 end,emu.callbackType.exec,pc,pc)
end
local function dumpCommunication()
 write('communication_nested.json','{"calls":['..table.concat(commNested,',')..'],"commands":['..table.concat(commCommands,',')..']}')
 write('communication_trace.json','{"loads":'..commLoads..',"events":['..table.concat(commEvents,',')..'],"draws":['..table.concat(commDraws,',')..']}')
end
'''.replace('LENGTHS','{'+','.join('['+str(k)+']='+str(v) for k,v in sorted(lengths.items()))+'}')
    runner=native.runner;marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('Communication observation anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+marker,1).replace('local function finish()\n','local function finish()\n dumpCommunication()\n',1)
    rc=native.main();out=Path(arg('--out'));r=read(out/'result.json');r['communication_observation']='Read-only actual038 source communication menu trace; normal inputs only. No aliases, writes, forced calls or network test. Not039 Korean runtime.';r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return rc

if __name__=='__main__':raise SystemExit(main())
