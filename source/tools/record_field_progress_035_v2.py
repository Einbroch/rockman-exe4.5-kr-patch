"""Current corrected ROM normal field observations, explicitly not cached pass."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress

def main():
    rp=ROOT/'poc/output/pending500_035_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();rows=[];loads=[];cached=[];common=[]
    for d in sorted((ROOT/'poc/runtime').glob('pending500-035-fixed-daytime-v2-*')):
        r=read(d/'result.json')
        if not r['complete'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('current normal receipt incomplete or wrong ROM')
        for name,h in r['artifacts'].items():require_hash(d/name,h)
        rows.append({'directory':str(d.relative_to(ROOT)),'receipt_sha256':sha((d/'result.json').read_bytes()),'frames':r['total_frames'],'screenshots':r['steps_captured']})
        obs=read(d/'field_loader.json');starts=[e for e in obs['events'] if e['pc']==0x0804F724]
        for i,e in enumerate(starts,1):
            p,_=lz77_decompress(source,e['r0']-0x08000000)
            if (d/f'load_{i:03d}_02039800.bin').read_bytes()[:len(p)]!=p:raise ValueError('actual first native payload mismatch')
            loads.append({'directory':str(d.relative_to(ROOT)),'source_archive':f"{e['r0']-0x08000000:X}",'scene':e['scene'],'sub':e['sub'],'selector':e['selector'],'native_bytes':len(p),'native_sha256':sha(p)})
        cached += [dict(e,directory=str(d.relative_to(ROOT))) for e in obs['readers'] if e['pc']==0x0804F76E]
        common += [dict(e,directory=str(d.relative_to(ROOT))) for e in obs['readers'] if e['pc']==0x0804F780]
    if not any(e['source_archive']=='79D650' and e['scene']==0xA0 and e['selector']==2 for e in loads):raise ValueError('no own daytime selected native source acquisition')
    reviewed={'boot':18,'route':64,'approach':24,'program-v1':2,'program-v2':3,'npc-v1':4,'inner-v1':5,'inner-v2':4,'inner-v3':5,'inner-v4':13,'inner-v5':2,'inner-v6':3,'inner-v7':3}
    screens={}
    for suffix,step in reviewed.items():
        p=ROOT/f'poc/runtime/pending500-035-fixed-daytime-v2-{suffix}/step_{step:03}.png';screens[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    frozen_write(ROOT/'analysis/pending500_035_v2/normal_field_progress_v1.json',dict(rom_sha256=m['output_sha256'],normal_controller_only=True,read_aliases_or_state_injections=False,segments=rows,native_loads=loads,cached_NPC_reader_calls=cached,common_RAW_reader_calls=common,native_cached_clone_display_verified=False,agent_directly_viewed_screens=screens,human_approval=False,latest_checkpoint='poc/runtime/pending500-035-fixed-daytime-v2-inner-v7/checkpoint.mss',latest_origin='poc/runtime/pending500-035-fixed-daytime-v2-inner-v7/result.json',observed_untranslated_board=dict(source_archive='799314',native_root='0203C800',evidence='poc/runtime/pending500-035-fixed-daytime-v2-inner-v2/step_004.png',scope='Separate native board reader, not035 selected9NPC archives'),route_reference='https://www.therockmanexezone.com/game-guides/mmbn4-5-map-guides/',limits='Normal9AM source79D650 acquisition and existing field/common NPC/board paths only. Absence of cached hits is not proof the path is unused. Native cached NPC selection/font/pages/reentry/timing remain pending. Existing500 wording unchanged.'))
    print('Corrected035 normal segments',len(rows),'cached calls',len(cached),'common calls',len(common),'native cached display NOT VERIFIED')

if __name__=='__main__':main()
