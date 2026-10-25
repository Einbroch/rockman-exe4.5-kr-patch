"""Read-only035 field-loader/reader observations; no aliases or RAM writes."""
import sys,json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    for a,b in [(0x4F712,0x4F7B6),(0x2E42C,0x2E438),(0xEC158,0xEC15C)]:
        if source[a:b]!=rom[a:b]:raise ValueError('035 native loader applicability')
    code=r'''
local fieldEvents={};local readers={};local count=0
local function field32(a)
 local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v
end
local function recordField(pc)
 local s=emu.getState();local scene=field32(s['cpu.r10']+64)
 fieldEvents[#fieldEvents+1]=string.format('{"pc":%d,"frame":%d,"r0":%d,"r1":%d,"r4":%d,"lr":%d,"scene":%d,"sub":%d,"selector":%d}',pc,frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r4'],s['cpu.r14'],emu.read(scene+4,emu.memType.gbaMemory),emu.read(scene+5,emu.memType.gbaMemory),emu.read(0x02003D57,emu.memType.gbaMemory))
end
for _,pc in ipairs({0x0804F712,0x0804F724,0x0804F730,0x0804F744}) do
 emu.addMemoryCallback(function() recordField(pc) end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 count=count+1;recordField(0x0804F748)
 for _,pair in ipairs({{0x02039800,0x3000},{0x0203C800,0x1000},{0x0203D800,0x2800}}) do
  local t={};for j=0,pair[2]-1 do t[#t+1]=string.char(emu.read(pair[1]+j,emu.memType.gbaMemory)) end
  write(string.format('load_%03d_%08X.bin',count,pair[1]),table.concat(t))
 end
end,emu.callbackType.exec,0x0804F748,0x0804F748)
for _,pc in ipairs({0x0804F76E,0x0804F780,0x0804F802}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();readers[#readers+1]=string.format('{"pc":%d,"frame":%d,"r0":%d,"r1":%d,"lr":%d}',pc,frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'])
 end,emu.callbackType.exec,pc,pc)
end
local function dumpField()
 write('field_loader.json','{"loads":'..count..',"events":['..table.concat(fieldEvents,',')..'],"readers":['..table.concat(readers,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('035 capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,code+anchor,1)
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function finish()\n','local function finish()\n dumpField()\n',1)
    rc=runner.main();out=Path(arg('--out'));r=read(out/'result.json')
    r.update(field_observation='Read-only native field loader and reader; no aliases, writes, injected state or control changes. Current035 artifact native loader observation; Korean selected NPC acquisition is not inferred from load completion.')
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
