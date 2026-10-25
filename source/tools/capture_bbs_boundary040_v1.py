"""Qualified039 BBS diagnostic through original F4 event/script10/startBBS.

One environmental tile READ alias only; no game RAM/ROM/PC or caller writes.
This does not establish natural board acquisition; all output states quarantined.
"""
import sys,json,struct
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress
from capture_roll_pet import PROBE


def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    for a,b in [(0x2DC68,0x2DCC4),(0x6A4DC,0x6A510),(0x4B7FC,0x4B828),(0x4B59C,0x4B5AE)]:
        if rom[a:b]!=source[a:b]:raise ValueError('040 original BBS entry/loader/reader applicability')
    if source[0x56948]!=10 or struct.unpack_from('<III',source,0x4B81C)!=(0x0804B380,0x0202E000,0x02032000):raise ValueError('040 original F4/BBS0 loading metadata')
    lengths={}
    for i in range(6):
        for delta in (0,4):
            addr=struct.unpack_from('<I',source,0x4B380+i*8+delta)[0];lengths[addr]=len(lz77_decompress(source,addr-0x08000000)[0])
    code=r'''
local bbsAliases={};local bbsEvents={};local bbsCalls={};local pendingBBS=nil;local bbsLoads=0
local bbsLengths=LENGTHS
local function b32(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if frame==0 and s['cpu.pipeline.execute.address']==0x0802DC6E and #bbsAliases==0 then
  if address~=0x02004ADE or value~=0 or emu.read(0x02004AD4,emu.memType.gbaMemory)~=0xA0 or emu.read(0x02004AD5,emu.memType.gbaMemory)~=0 then error('040 BBS qualified event prerequisite') end
  bbsAliases[#bbsAliases+1]=string.format('{"frame":%d,"address":%d,"original":%d,"returned":244}',frame,address,value);return 0xF4
 end
end,emu.callbackType.read,0x02004ADE,0x02004ADE)
for _,pc in ipairs({0x0806A502,0x0804B7FC,0x0804B80C,0x0804B816,0x0804B59C,0x0804B5AA,0x0804B5AE}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local regs={};for j=0,14 do regs[#regs+1]=string.format('"%d":%d',j,s['cpu.r'..j]) end
  bbsEvents[#bbsEvents+1]=string.format('{"frame":%d,"pc":%d,"registers":{%s},"context_root":%d,"context_stream":%d}',frame,pc,table.concat(regs,','),b32(0x0200FA50),b32(0x0200FA4C))
  if pc==0x0804B80C or pc==0x0804B816 then
   if not bbsLengths[s['cpu.r0']] then error('040 BBS unknown source selection') end
   pendingBBS={source=s['cpu.r0'],dest=s['cpu.r1'],length=bbsLengths[s['cpu.r0']]}
  end
 end,emu.callbackType.exec,pc,pc)
end
for _,pc in ipairs({0x0804B810,0x0804B81A}) do
 emu.addMemoryCallback(function()
  if pendingBBS then bbsLoads=bbsLoads+1;local t={};for j=0,pendingBBS.length-1 do t[#t+1]=string.char(emu.read(pendingBBS.dest+j,emu.memType.gbaMemory)) end;write(string.format('bbs_native_%03d_%08X.bin',bbsLoads,pendingBBS.source),table.concat(t));pendingBBS=nil end
 end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']==0x02032000 then bbsCalls[#bbsCalls+1]=string.format('{"frame":%d,"root":%d,"script":%d,"lr":%d,"sp":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'],s['cpu.r13']) end
end,emu.callbackType.exec,0x0804FB4C,0x0804FB4C)
local function dumpBBS()
 write('bbs_boundary.json','{"tile_aliases":['..table.concat(bbsAliases,',')..'],"loads":'..bbsLoads..',"events":['..table.concat(bbsEvents,',')..'],"calls":['..table.concat(bbsCalls,',')..']}')
end
'''.replace('LENGTHS','{'+','.join('['+str(k)+']='+str(v) for k,v in sorted(lengths.items()))+'}')
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];glyph=PROBE
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',0x02032000),('PET_END',0x02039800)]:glyph=glyph.replace(k,str(v))
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('040 BBS observation anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+glyph+marker+' dumpRollPet(name)\n',1).replace('local function finish()\n',"local function finish()\n dumpBBS()\n dumpRollPet('final')\n",1)
    rc=runner.main();out=Path(arg('--out'));r=read(out/'result.json')
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r.update(scope='DIAGNOSTIC one original environment read0->F4 at frame0; source table->script10/startBBS->original loading/UI/reader. NOT natural board access.',normal_play_checkpoint_eligible=False,natural_acquisition_verified=False,release_eligible=False);r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return rc


if __name__=='__main__':raise SystemExit(main())
