"""Native caller/selector diagnostic with a qualified resident-byte boundary.

The native LZ77 load is verified independently from current-ROM GBA captures.
Only the selector's resident-source byte reads and scene read are aliased.
The native actor, mode, script number, original BL/LR, context initializer,
target root, parser and renderer run unchanged. Not natural A1/A3 acquisition.
"""
import sys,json
from pathlib import Path
import capture_field_loader_036_v1 as native
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    case=arg('--boundary-case');i=sys.argv.index('--boundary-case');del sys.argv[i:i+2]
    if case not in ('a1','a3'):raise ValueError('Declared boundary classes only')
    arc,scene={'a1':('7AAF94',0xA1),'a3':('7B469C',0xA3)}[case];rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();payload=lz77_decompress(source,int(arc,16))[0]
    folder=ROOT/('poc/runtime/pending500-036-qualified-native-'+case+('-v1' if case=='a1' else '-load-v1'));prior=read(folder/'result.json');q=prior['qualified_scene'];blob=(folder/'load_001_02039800.bin').read_bytes()
    if prior['rom_sha256']!=m['output_sha256'] or prior['return_code']!=0 or q['source']!=0x08000000+int(arc,16) or q['native_loads']!=1 or blob[:len(payload)]!=payload:raise ValueError('Actual current-ROM native decompression boundary prerequisite')
    for name,h in prior['artifacts'].items():require_hash(folder/name,h)
    n=m['keyitem_rom']['npc036'];p=next(x for x in n['placements'] if x['source_archive']==arc);ins=n['wrapper']['proof']['instructions'];scene_pc=next(x['address'] for x in ins if x['mnemonic']=='ldrb' and x['operands']=='r3, [r2, #4]');compare_pc=next(x['address'] for x in ins if x['mnemonic']=='ldrb' and x['operands']=='r2, [r1]')
    if rom[p['native_copy_offset']:p['native_copy_offset']+len(payload)]!=payload:raise ValueError('ROM reference differs from actual LZ result')
    code=r'''
local boundaryReads=0;local boundaryScenes=0;local boundaryMin=999999;local boundaryMax=-1
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']==SCENEPC and address==s['cpu.r2']+4 then
  if value~=0xA0 then error('Borrowed native actor scene applicability') end
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
    for k,v in [('SCENEPC',scene_pc),('COMPAREPC',compare_pc),('SCENE',scene),('NATIVE',0x08000000+p['native_copy_offset']),('LENGTH',len(payload))]:code=code.replace(k,str(v))
    marker='local function capture(name)\n';native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpBoundary(name)\n',1);native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace('local function finish()\n',"local function finish()\n dumpBoundary('final')\n",1)
    rc=native.main();out=Path(arg('--out'));r=read(out/'result.json');b=read(out/'final_boundary.json')
    passed=rc==0 and r['complete'] and b['scene_reads']==1 and b['resident_reads']>=len(payload) and (b['min_offset'],b['max_offset'])==(0,len(payload)-1)
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r.update(complete=passed,scope='DIAGNOSTIC native A0 actor/caller with byte-identical independently loaded A1/A3 resident-read boundary and selector scene alias; NOT natural A1/A3 acquisition',field_observation='No RAM/ROM/actor/mode/script/LR writes; native source4F764/4F76E ->036selector ->clone/initializer/parser/font executes',normal_play_checkpoint_eligible=False,boundary_case=case,target_archive=arc,target_scene=scene,resident_boundary=b,native_load_prerequisite=dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes()),decompressed_sha256=sha(payload),bytes=len(payload)),artifacts={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'})
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Native boundary',case,passed,b);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
