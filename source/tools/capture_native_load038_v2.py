"""Qualified038 original NPC lookup/LZ boundary; no natural progression claim.

Only three original lookup read results (scene/sub/day) are aliased while the
loader executes. No source pointer/LZ routine/RAM/actor/progress is written.
Native caller/selector/display is deliberately NOT required or inferred here.
"""
import sys,json
from pathlib import Path
import capture_field_loader_038_v1 as native
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from field_native_rom_product_038_v2 import verify_final
from field_native_rom_selector_038_v1 import source_population
from prepare_native_inputs038_v1 import OUT,selected_from


def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    archive=arg('--qualified-archive');i=sys.argv.index('--qualified-archive');del sys.argv[i:i+2]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();verify_final(source,rom,m['keyitem_rom'])
    manifest=read(OUT+'/manifest.json');entry=next(r for r in manifest['archives'] if r['archive']==archive)
    if entry['source_class']!='native-NPC' or entry['scene']!=0xA4:raise ValueError('Qualified038 new native scene scope')
    row=next(r for r in source_population(source,selected_from(manifest['archives'])) if r['archive']==archive)
    if len(row['payload'])>0x3000:raise ValueError('Qualified038 native buffer bound')
    for lo,hi in [(0x4F712,0x4F7B6),(0x2E42C,0x2E438),(0xEC158,0xEC15C)]:
        if rom[lo:hi]!=source[lo:hi]:raise ValueError('Unmodified native loader applicability')
    code=r'''
local qLoader=false;local qLookup=false;local qLoads=0;local qScenes=0;local qSubs=0;local qDays=0;local qSources={}
local function q32(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=q32(s['cpu.r10']+64)
 if ctx~=0x02004AD0 then error('Qualified loader scene-context applicability') end
 qLoader=emu.read(ctx+4,emu.memType.gbaMemory)==0xA0
end,emu.callbackType.exec,0x0804F712,0x0804F712)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if qLoader and s['cpu.pipeline.execute.address']==0x0802E42E then qDays=qDays+1;return DAY end
end,emu.callbackType.read,0x02003D57,0x02003D57)
emu.addMemoryCallback(function()
 local s=emu.getState();qLookup=qLoader and s['cpu.r0']==0x08053700 and s['cpu.r14']==0x0804F721
end,emu.callbackType.exec,0x0804F790,0x0804F790)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 if qLookup and pc==0x0804F796 and address==s['cpu.r7']+4 then qScenes=qScenes+1;return SCENE end
 if qLookup and pc==0x0804F79A and address==s['cpu.r7']+5 then qSubs=qSubs+1;return SUB end
end,emu.callbackType.read,0x02004AD4,0x02004AD5)
emu.addMemoryCallback(function() qLookup=false end,emu.callbackType.exec,0x0804F7A4,0x0804F7A4)
emu.addMemoryCallback(function()
 if qLoader then
  local s=emu.getState();if s['cpu.r0']~=SOURCE or s['cpu.r1']~=0x02039800 then error('Qualified lookup selected wrong native source/root') end
  qSources[#qSources+1]=s['cpu.r0']
 end
end,emu.callbackType.exec,0x0804F724,0x0804F724)
emu.addMemoryCallback(function()
 if qLoader then
  qLoads=qLoads+1;local t={}
  for j=0,LENGTH-1 do t[#t+1]=string.char(emu.read(0x02039800+j,emu.memType.gbaMemory)) end
  write(string.format('qualified_native_%03d.bin',qLoads),table.concat(t))
 end
 qLoader=false
end,emu.callbackType.exec,0x0804F748,0x0804F748)
local function dumpQualifiedLoad()
 write('qualified_load.json',string.format('{"loads":%d,"scene_reads":%d,"sub_reads":%d,"day_reads":%d,"sources":[%s]}',qLoads,qScenes,qSubs,qDays,table.concat(qSources,',')))
end
'''
    for k,v in [('SOURCE',0x08000000+int(archive,16)),('SCENE',row['scene']),('SUB',row['sub']),('DAY',row['slot']),('LENGTH',len(row['payload']))]:code=code.replace(k,str(v))
    marker='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('038 load observation anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(marker,code+marker,1)
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace('local function finish()\n','local function finish()\n dumpQualifiedLoad()\n',1)
    rc=native.main();out=Path(arg('--out'));r=read(out/'result.json');q=read(out/'qualified_load.json');count=q['loads']
    passed=rc==0 and r['complete'] and count>=1 and q['scene_reads']==q['sub_reads']==q['day_reads']==count and q['sources']==[0x08000000+int(archive,16)]*count
    for j in range(1,count+1):
        if (out/f'qualified_native_{j:03d}.bin').read_bytes()!=row['payload']:passed=False
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r.update(complete=passed,scope='DIAGNOSTIC qualified scene/sub/day lookup -> original source LZ -> full native RAM bytes only; NOT natural acquisition or038 selector/display',normal_play_checkpoint_eligible=False,target_archive=archive,target_scene=row['scene'],qualified_load=q,native_bytes=len(row['payload']),native_sha256=sha(row['payload']),lookup_alias=dict(scene=row['scene'],sub=row['sub'],weekday=row['slot']),native_source_pointer_and_LZ_unmodified=True,natural_acquisition_verified=False,selector_display_verified=False,release_eligible=False,artifacts={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'})
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('038 qualified native load',archive,passed,q);return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
