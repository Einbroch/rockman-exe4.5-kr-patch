"""Read-only actual038 board object/caller observation; no script substitution."""
import sys,json
from pathlib import Path
import capture_field_loader_038_v1 as native
from cumulative_batch500 import read
from build_visibility_poc import sha


def main():
    code=r'''
local boardEntries={};local boardArgs={}
emu.addMemoryCallback(function()
 local s=emu.getState();local t={}
 for i=0,15 do t[#t+1]=emu.read(s['cpu.r5']+i,emu.memType.gbaMemory) end
 boardEntries[#boardEntries+1]=string.format('{"frame":%d,"object":%d,"caller_lr":%d,"source_bytes":[%s]}',frame,s['cpu.r5'],s['cpu.r14'],table.concat(t,','))
end,emu.callbackType.exec,0x0806A4FC,0x0806A4FC)
emu.addMemoryCallback(function()
 local s=emu.getState()
 boardArgs[#boardArgs+1]=string.format('{"frame":%d,"root":%d,"script":%d,"object":%d,"caller_lr_before_BL":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r5'],s['cpu.r14'])
end,emu.callbackType.exec,0x0806A502,0x0806A502)
local function dumpBoards()
 write('board_entries.json','{"entries":['..table.concat(boardEntries,',')..'],"BL_arguments":['..table.concat(boardArgs,',')..']}')
end
'''
    marker='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('Board observation insertion anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(marker,code+marker,1)
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace('local function finish()\n','local function finish()\n dumpBoards()\n',1)
    rc=native.main();out=Path(sys.argv[sys.argv.index('--out')+1]);r=read(out/'result.json');r['board_observation']='Read-only actual original6A4FC object and6A502 BL arguments; no script/root/LR/actor/ROM/RAM writes';r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return rc


if __name__=='__main__':raise SystemExit(main())
