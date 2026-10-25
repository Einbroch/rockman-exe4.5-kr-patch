"""Qualified F3 event with its observed disabled flag read cleared, not RAM."""
import sys,json
from pathlib import Path
import capture_board_qualified037_v1 as previous
from build_visibility_poc import sha
from cumulative_batch500 import read

def main():
    code=r'''
local flagAliases={}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']==0x080287C4 and address==s['cpu.r3'] and (frame==0 or frame==300) then
  if value~=0x30 or s['cpu.r1']~=0x10 then error('F3 disabled-flag observation applicability') end
  flagAliases[#flagAliases+1]=string.format('{"frame":%d,"address":%d,"original":%d,"returned":32}',frame,address,value)
  return 0x20
 end
end,emu.callbackType.read,0x02004FA4,0x02004FA4)
local function dumpFlagAliases()
 write('board_flag_alias.json','{"reads":['..table.concat(flagAliases,',')..']}')
end
'''
    runner=previous.event.board.native.runner
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function capture(name)\n',code+'local function capture(name)\n',1)
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function finish()\n','local function finish()\n dumpFlagAliases()\n',1)
    rc=previous.main();out=Path(sys.argv[sys.argv.index('--out')+1]);r=read(out/'result.json')
    r['scope']='DIAGNOSTIC tile0->F3 plus disabled-flag read0x30->0x20 at original287C4, frames0,300 only; original event table/setup/provider/board caller/selector/display. NOT natural tree acquisition or progression.'
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
