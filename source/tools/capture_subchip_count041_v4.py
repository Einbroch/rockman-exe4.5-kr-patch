"""041 copy of v3 over the generic segment runner (v3 base asserts exact040). Same READ aliases only."""
import sys,json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read


def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes()
    for a,b in [(0x5CCC,0x5CF6),(0x302F8,0x3031E),(0x41A40,0x41A68),(0x41C4C,0x41C7A),(0x41C9C,0x41CC2),(0x41D84,0x41D98)]:
        if rom[a:b]!=source[a:b]:raise ValueError('041 subchip original qualification code applicability')
    code=r'''
local subchipCountAliases041={};local subchipAvailabilityAliases041={}
local function itemStackWord041(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local outer=itemStackWord041(s['cpu.r13'])
 if s['cpu.pipeline.execute.address']==0x08030314 and s['cpu.r0']==0x27 and s['cpu.r1']==0x020061CC and s['cpu.r2']==0 and s['cpu.r14']==0x08005CD7 and outer>=0x08041500 and outer<0x08042050 then
  if address~=0x020061F3 or value~=0 or #subchipCountAliases041>=200 then error('041 exact native empty MiniEnergy count prerequisites') end
  subchipCountAliases041[#subchipCountAliases041+1]=string.format('{"frame":%d,"address":%d,"original":%d,"returned":1,"pc":%d,"lr":%d,"item":%d,"base":%d,"navi_offset":%d,"outer":%d}',frame,address,value,s['cpu.pipeline.execute.address'],s['cpu.r14'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],outer)
  return 1
 end
end,emu.callbackType.read,0x020061F3,0x020061F3)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local outer=itemStackWord041(s['cpu.r13']+36)
 if s['cpu.pipeline.execute.address']==0x08005CEC and s['cpu.r0']==0x27 and s['cpu.r5']==0x02000500 and s['cpu.r7']==0x020091F8 and s['cpu.r1']==0x52 and outer>=0x08041500 and outer<0x08042050 then
  if address~=0x0200921F or value~=0x2F or #subchipAvailabilityAliases041>=200 then error('041 exact native unavailable MiniEnergy comparison prerequisites') end
  subchipAvailabilityAliases041[#subchipAvailabilityAliases041+1]=string.format('{"frame":%d,"address":%d,"original":%d,"returned":82,"pc":%d,"item":39,"outer":%d}',frame,address,value,s['cpu.pipeline.execute.address'],outer)
  return 0x52
 end
end,emu.callbackType.read,0x0200921F,0x0200921F)
local function dumpSubchipCount041()
 write('subchip_availability_alias041.json','{"aliases":['..table.concat(subchipAvailabilityAliases041,',')..']}')
 write('subchip_count_alias041.json','{"aliases":['..table.concat(subchipCountAliases041,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('041 qualified subchip observer anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,code+anchor,1).replace('local function finish()\n','local function finish()\n dumpSubchipCount041()\n',1)
    rc=runner.main();out=Path(arg('--out'));r=read(out/'result.json');a=read(out/'subchip_count_alias041.json')['aliases']
    r.update(scope='DIAGNOSTIC: MiniEnergy39 quantity read0->1 only at original30314, Navi0 inventory base020061CC, subchip UI saved outerLR range41500:42050 (native getter LR5CD7); original availability comparison read47->82 at5CEC for that item only. Original menu, HP-full check, loader, reader and return retained. No item acquisition/save/use-success claim.',state_intervention=True,normal_play_checkpoint_eligible=False,natural_acquisition_verified=False,release_eligible=False,subchip_count_read_aliases=len(a))
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if not a:raise ValueError('041 qualified item count alias not reached; no consumption claim')
    return rc


if __name__=='__main__':raise SystemExit(main())


