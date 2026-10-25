"""Read-only source hint provider/caller trace on own037 state, not038 proof."""
import sys,json
from pathlib import Path
import capture_field_loader_037_v1 as native
from build_visibility_poc import sha
from cumulative_batch500 import read

def main():
    code=r'''
local hintEntries={}
for _,pc in ipairs({0x0806A818,0x0806C9A4,0x0804F7FC}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local scene=0;local registers={}
  for j=0,3 do scene=scene+emu.read(s['cpu.r10']+64+j,emu.memType.gbaMemory)*2^(8*j) end
  for j=0,14 do registers[#registers+1]=string.format('"%d":%d',j,s['cpu.r'..j]) end
  hintEntries[#hintEntries+1]=string.format('{"frame":%d,"pc":%d,"scene":%d,"script_provider":%d,"Navi":%d,"registers":{%s}}',frame,pc,scene,emu.read(scene+17,emu.memType.gbaMemory),emu.read(scene+1,emu.memType.gbaMemory),table.concat(registers,','))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpHints()
 write('hint_entries.json','{"entries":['..table.concat(hintEntries,',')..']}')
end
'''
    runner=native.runner;runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function capture(name)\n',code+'local function capture(name)\n',1);runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function finish()\n','local function finish()\n dumpHints()\n',1)
    rc=native.main();out=Path(sys.argv[sys.argv.index('--out')+1]);r=read(out/'result.json');r['hint_observation']='Read-only original source provider/caller, no aliases, writes, forced PC or arguments.037 observation is NOT038 runtime.';r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return rc

if __name__=='__main__':raise SystemExit(main())
