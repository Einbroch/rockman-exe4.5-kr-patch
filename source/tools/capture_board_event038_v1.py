"""Read-only038 environmental-event dispatch and board initialization trace."""
import sys,json
from pathlib import Path
import capture_board038_v1 as board
from build_visibility_poc import sha
from cumulative_batch500 import read

def main():
    code=r'''
local eventRows={}
for _,pc in ipairs({0x0802DC68,0x0802DCAA,0x0806A4DC}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local scene=0
  for j=0,3 do scene=scene+emu.read(s['cpu.r10']+64+j,emu.memType.gbaMemory)*2^(8*j) end
  eventRows[#eventRows+1]=string.format('{"pc":%d,"frame":%d,"lr":%d,"r0":%d,"r1":%d,"r4":%d,"r5":%d,"scene":%d,"tile":%d,"parameter":%d}',pc,frame,s['cpu.r14'],s['cpu.r0'],s['cpu.r1'],s['cpu.r4'],s['cpu.r5'],scene,emu.read(scene+14,emu.memType.gbaMemory),emu.read(0x02010731,emu.memType.gbaMemory))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpEvent()
 write('board_dispatch.json','{"events":['..table.concat(eventRows,',')..']}')
end
'''
    runner=board.native.runner
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function capture(name)\n',code+'local function capture(name)\n',1)
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function finish()\n','local function finish()\n dumpEvent()\n',1)
    rc=board.main();out=Path(sys.argv[sys.argv.index('--out')+1]);r=read(out/'result.json')
    r['event_dispatch_observation']='Read-only original2DC68 tile dispatch /2DCAA native script setup /6A4DC provider setup. No aliases or writes.'
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
