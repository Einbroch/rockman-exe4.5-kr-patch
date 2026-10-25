"""Qualified037 resident-byte + scene diagnostic through original NPC caller.

Requires full native LZ bytes captured on this exact037 artifact in a separate
qualified load run. Does not claim natural A1/A2/A3 actor/scene acquisition.
"""
import sys,json
from pathlib import Path
import capture_field_loader_037_v1 as native
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress


def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    archive=arg('--boundary-archive');origin=Path(arg('--native-load-origin'))
    for key in ['--boundary-archive','--native-load-origin']:
        i=sys.argv.index(key);del sys.argv[i:i+2]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();payload=lz77_decompress(source,int(archive,16))[0]
    load=read(origin);folder=origin.parent
    if not load['complete'] or load['rom_sha256']!=m['output_sha256'] or load['normal_play_checkpoint_eligible'] is not False or load['target_archive']!=archive or not load['native_source_pointer_and_LZ_unmodified'] or load['selector_display_verified'] is not False:raise ValueError('037 qualified native load prerequisite')
    for name,h in load['artifacts'].items():require_hash(folder/name,h)
    if (folder/'qualified_native_001.bin').read_bytes()!=payload or load['native_sha256']!=sha(payload):raise ValueError('037 full native source boundary mismatch')
    n=m['keyitem_rom']['npc037'];p=next(x for x in n['placements'] if x['source_archive']==archive)
    if p['source_class']!='native-NPC' or p['scene'] not in (0xA1,0xA2,0xA3) or rom[p['native_copy_offset']:p['native_copy_offset']+len(payload)]!=payload:raise ValueError('037 target source/class/scene')
    ins=n['wrapper']['proof']['instructions'];scene_pc=next(x['address'] for x in ins if x['mnemonic']=='ldrb' and x['operands']=='r3, [r2, #4]');compare_pc=next(x['address'] for x in ins if x['mnemonic']=='ldrb' and x['operands']=='r2, [r1]')
    code=r'''
local boundaryReads=0;local boundaryScenes=0;local boundaryMin=999999;local boundaryMax=-1
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']==SCENEPC and address==s['cpu.r2']+4 then
  if value~=0xA0 then error('Borrowed actor scene applicability') end
  boundaryScenes=boundaryScenes+1;return SCENE
 end
end,emu.callbackType.read,0x02004AD4,0x02004AD4)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']==COMPAREPC and address==s['cpu.r1'] then
  local offset=address-0x02039800;boundaryReads=boundaryReads+1
  boundaryMin=math.min(boundaryMin,offset);boundaryMax=math.max(boundaryMax,offset)
  return emu.read(NATIVE+offset,emu.memType.gbaMemory)
 end
end,emu.callbackType.read,0x02039800,0x02039800+LENGTH-1)
local function dumpBoundary(name)
 write(name..'_boundary.json',string.format('{"resident_reads":%d,"scene_reads":%d,"min_offset":%d,"max_offset":%d}',boundaryReads,boundaryScenes,boundaryMin,boundaryMax))
end
'''
    for k,v in [('SCENEPC',scene_pc),('COMPAREPC',compare_pc),('SCENE',p['scene']),('NATIVE',0x08000000+p['native_copy_offset']),('LENGTH',len(payload))]:code=code.replace(k,str(v))
    marker='local function capture(name)\n';native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpBoundary(name)\n',1);native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace('local function finish()\n',"local function finish()\n dumpBoundary('final')\n",1)
    rc=native.main();out=Path(arg('--out'));r=read(out/'result.json');b=read(out/'final_boundary.json');ss=read(out/'native_selector.json')['selectors']
    selected=[s for s in ss if s['native_root']==0x02039800 and s['caller_lr']==0x0804F773 and s['script']==0 and s['root']==0x08000000+p['rom_offset']]
    passed=rc==0 and r['complete'] and b['scene_reads']==1 and b['resident_reads']>=len(payload) and (b['min_offset'],b['max_offset'])==(0,len(payload)-1) and len(selected)==1
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r.update(complete=passed,scope='DIAGNOSTIC native A0 actor/caller, exact037 independently LZ-loaded source at resident-read boundary and selector scene alias; NOT natural target scene/actor acquisition',normal_play_checkpoint_eligible=False,target_archive=archive,target_scene=p['scene'],resident_boundary=b,native_selector_calls=selected,native_load_prerequisite=dict(path=str(origin.relative_to(ROOT)),sha256=sha(origin.read_bytes()),decompressed_sha256=sha(payload),bytes=len(payload)),natural_acquisition_verified=False,rendering_approval_pending=True,release_eligible=False,artifacts={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'})
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('037 qualified native boundary',archive,passed,b);return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
