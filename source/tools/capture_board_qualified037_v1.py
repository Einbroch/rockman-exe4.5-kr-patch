"""DIAGNOSTIC: alias only environmental tile-read to F3 twice.

Preserves original event table, original event-script initialization, board
provider, native RAM, caller LR, selector and display. NOT natural tree access.
"""
import sys,json,struct
from pathlib import Path
import capture_board_event037_v2 as event
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    for a,b in [(0x2DC68,0x2DCC4),(0x6A4DC,0x6A510)]:
        if rom[a:b]!=source[a:b]:raise ValueError('Original board event contract changed')
    word=lambda at:struct.unpack_from('<I',source,at)[0]-0x08000000
    table=word(word(0x2D568+0x20*4))
    if table!=0x56944 or source[table+3]!=3:raise ValueError('A0sub0 F3 original event selection')
    code=r'''
local tileAliases={}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']==0x0802DC6E and (frame==0 or frame==300) then
  if address~=0x02004ADE or value~=0 or emu.read(0x02004AD4,emu.memType.gbaMemory)~=0xA0 or emu.read(0x02004AD5,emu.memType.gbaMemory)~=0 then error('Qualified board dispatch prerequisites') end
  tileAliases[#tileAliases+1]=string.format('{"frame":%d,"address":%d,"original":%d,"returned":243}',frame,address,value)
  return 0xF3
 end
end,emu.callbackType.read,0x02004ADE,0x02004ADE)
local function dumpTileAlias()
 write('board_tile_alias.json','{"reads":['..table.concat(tileAliases,',')..']}')
end
'''
    runner=event.board.native.runner
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function capture(name)\n',code+'local function capture(name)\n',1)
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function finish()\n','local function finish()\n dumpTileAlias()\n',1)
    rc=event.main();out=Path(arg('--out'));r=read(out/'result.json')
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r.update(scope='DIAGNOSTIC original environmental dispatch tile-read alias0->F3 at frames0,300; original table->event script->provider->board BL->selector->display. NOT natural tree acquisition.',normal_play_checkpoint_eligible=False,natural_acquisition_verified=False,release_eligible=False)
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
