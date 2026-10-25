"""Diagnostic hint lookup->original LZ->native RAM, not natural acquisition.

Only loader Navi and hint-table scene read results are aliased. No source
pointer, decompressor, RAM, actor, progression, selector or ROM is written.
"""
import sys,json
from pathlib import Path
import capture_field_loader_038_v1 as native
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress
from prepare_source500_038_v3 import typed_lookup

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    audit=read('analysis/pending500_038_v2/integration.json')
    if not audit['passed'] or audit['rom_sha256']!=m['output_sha256']:raise ValueError('038 artifact prerequisite')
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    arc='78AE58';refs=typed_lookup(source)[arc]
    if not any(x['source_class']=='navi-hint' and x['scene']==0xA3 and x['navi']==21 for x in refs):raise ValueError('Original A3 ShadowMan hint reference')
    payload=lz77_decompress(source,int(arc,16))[0]
    if len(payload)>0x2800:raise ValueError('Hint native capacity')
    for lo,hi in [(0x4F712,0x4F7B6),(0xCEC,0xCF4),(0xEC158,0xEC15C)]:
        if rom[lo:hi]!=source[lo:hi]:raise ValueError('Hint loader source applicability')
    code=r'''
local qLoader=false;local qHint=false;local qLoads=0;local qNavis=0;local qScenes=0;local qSources={}
local function h32(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
emu.addMemoryCallback(function()
 local s=emu.getState();local scene=h32(s['cpu.r10']+64)
 if scene~=0x02004AD0 then error('Hint loader scene-context') end
 qLoader=emu.read(scene+4,emu.memType.gbaMemory)==0xA0
end,emu.callbackType.exec,0x0804F712,0x0804F712)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if qLoader and s['cpu.pipeline.execute.address']==0x08000CF0 and s['cpu.r14']==0x0804F739 then
  if value~=0 then error('Expected source MegaMan for diagnostic Navi read') end
  qNavis=qNavis+1;return 21
 end
end,emu.callbackType.read,0x02004AD1,0x02004AD1)
emu.addMemoryCallback(function()
 local s=emu.getState();qHint=qLoader and s['cpu.r0']==0x08053FA0 and s['cpu.r14']==0x0804F741
end,emu.callbackType.exec,0x0804F7A6,0x0804F7A6)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if qHint and s['cpu.pipeline.execute.address']==0x0804F7AC and address==s['cpu.r7']+4 then
  if value~=0xA0 then error('Expected original A0 loader scene read') end
  qScenes=qScenes+1;return 0xA3
 end
end,emu.callbackType.read,0x02004AD4,0x02004AD4)
emu.addMemoryCallback(function() qHint=false end,emu.callbackType.exec,0x0804F7B4,0x0804F7B4)
emu.addMemoryCallback(function()
 if qLoader then
  local s=emu.getState()
  if s['cpu.r0']~=0x0878AE58 or s['cpu.r1']~=0x0203D800 then error('Original hint lookup source/root differs') end
  qSources[#qSources+1]=s['cpu.r0']
 end
end,emu.callbackType.exec,0x0804F744,0x0804F744)
emu.addMemoryCallback(function()
 if qLoader then
  qLoads=qLoads+1;local t={}
  for j=0,LENGTH-1 do t[#t+1]=string.char(emu.read(0x0203D800+j,emu.memType.gbaMemory)) end
  write(string.format('qualified_hint_%03d.bin',qLoads),table.concat(t))
 end
 qLoader=false
end,emu.callbackType.exec,0x0804F748,0x0804F748)
local function dumpHintLoad()
 write('qualified_hint_load.json',string.format('{"loads":%d,"Navi_reads":%d,"scene_reads":%d,"sources":[%s]}',qLoads,qNavis,qScenes,table.concat(qSources,',')))
end
'''.replace('LENGTH',str(len(payload)))
    runner=native.runner;marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('038 hint probe anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+marker,1).replace('local function finish()\n','local function finish()\n dumpHintLoad()\n',1)
    rc=native.main();out=Path(arg('--out'));r=read(out/'result.json');q=read(out/'qualified_hint_load.json');count=q['loads']
    passed=rc==0 and r['complete'] and count>=1 and q['Navi_reads']==q['scene_reads']==count and q['sources']==[0x0878AE58]*count
    for j in range(1,count+1):
        if (out/f'qualified_hint_{j:03d}.bin').read_bytes()!=payload:passed=False
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r.update(complete=passed,scope='DIAGNOSTIC hint loader Navi0->21 and hint lookup sceneA0->A3 read aliases only. Original source lookup/LZ/native RAM proven; NOT natural ShadowMan/A3 acquisition or selector/display.',normal_play_checkpoint_eligible=False,target_archive=arc,target_scene=0xA3,target_Navi=21,qualified_load=q,native_bytes=len(payload),native_sha256=sha(payload),native_source_pointer_and_LZ_unmodified=True,natural_acquisition_verified=False,selector_display_verified=False,release_eligible=False)
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('038 qualified hint load',arc,passed,q);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
