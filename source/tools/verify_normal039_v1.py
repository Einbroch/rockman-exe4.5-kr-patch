"""Own039 normal recipe chain, original NPC/board LZ residency and old dialogue.

Preserved038 board source acquisition is distinct from new039 communication
selector/Korean display. The observer measures038 wrapper only, not the
whole039->038->036 chain timing. This report does NOT verify new039 help.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from verify_pending500_005_displays import model


def main():
    rp=ROOT/'poc/output/pending500_039_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();recipe=read('analysis/pending500_039_v1/normal_recipe_receipts_v1.json');receipts=[];loads=[];calls=[];parent=None;selected={p['source_archive'] for p in m['keyitem_rom']['npc038']['placements']}
    for item in recipe['segments']:
        require_hash(ROOT/item['path'],item['sha256']);origin=ROOT/item['path'];d=origin.parent;r=read(origin)
        if not r['complete'] or r['return_code']!=0 or r['rom_sha256']!=sha(rom) or r.get('normal_play_checkpoint_eligible') is False or r['scope'].startswith('DIAGNOSTIC') or len(r['loaded_rom_guards'])!=6:raise ValueError('038 normal receipt/loaded sentinels')
        for name,h in r['artifacts'].items():require_hash(d/name,h)
        if parent:
            if r['state_origin']!=str(parent) or r['state_sha256']!=read(parent)['artifacts']['checkpoint.mss']:raise ValueError('038 exact own-state chain edge')
            require_hash(d/'input.mss',r['state_sha256'])
        elif r['state_origin'] is not None:raise ValueError('038 route must start coldboot')
        events=read(d/'field_loader.json')
        for pc,root,kind in [(0x0804F724,0x02039800,'native-NPC'),(0x0804F730,0x0203C800,'field-board')]:
            starts=[e for e in events['events'] if e['pc']==pc]
            if len(starts)!=events['loads']:raise ValueError('038 native load indexing')
            for i,e in enumerate(starts,1):
                archive=f"{e['r0']-0x08000000:X}"
                if archive not in selected and archive!='79CF04':continue
                payload=lz77_decompress(source,int(archive,16))[0];blob=(d/f'load_{i:03d}_{root:08X}.bin').read_bytes()
                if e['r1']!=root or blob[:len(payload)]!=payload:raise ValueError('038 actual source LZ/native RAM bytes')
                loads.append(dict(receipt=item['path'],archive=archive,source_class=kind,new038_source=archive in selected,scene=e['scene'],sub=e['sub'],root=root,native_bytes=len(payload),native_sha256=sha(payload)))
        calls.extend(dict(receipt=item['path'],**c) for c in read(d/'native_selector.json')['selectors']);receipts.append(dict(path=item['path'],sha256=item['sha256']));parent=origin
    if len(receipts)!=16 or not any(x['archive']=='799314' and x['new038_source'] for x in loads) or not any(x['archive']=='79CF04' for x in loads):raise ValueError('038 finite route/native source population')
    rec=next(x for x in m['keyitem_rom']['npc036']['archives'] if x['archive']=='79CF04');manifest=read('analysis/pending_insertion_500_036_npc_inputs_v1/manifest.json');assetref=next(x['asset'] for x in manifest['archives'] if x['archive']=='79CF04');require_hash(ROOT/assetref['path'],assetref['sha256']);asset=read(assetref['path']);pool,units,expected,streams,ends=model(rom,m,cfg,'79CF04',3,255,record=rec,asset=asset);key='79CF04:3:0'
    d=ROOT/'poc/runtime/pending500-039-normal-v1-16';page=(d/'step_002_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<2I',page,0xFA4C)!=(ends[key],pool):raise ValueError('038 prior036 timebranch3 context/stream root')
    before=(d/'step_003_gbaExtWorkRam.bin').read_bytes();after=(d/'step_004_gbaExtWorkRam.bin').read_bytes();p0=struct.unpack_from('<3i',before,0xFB54);p1=struct.unpack_from('<3i',after,0xFB54)
    if p0==p1:raise ValueError('038 post-close movement not observed')
    native=lz77_decompress(source,0x79CF04)[0]
    if after[0x39800:0x39800+len(native)]!=native or struct.unpack_from('<I',after,0xABB8+0x9C)[0]!=0:raise ValueError('038 resident source/actor mode changed')
    for step in [1,3,4]:
        o=(d/f'step_{step:03}_gbaSpriteRam.bin').read_bytes()
        if any(not a&0x2300 and k>>12==14 for i in range(128) for a,b,k in [struct.unpack_from('<3H',o,i*8)]):raise ValueError('038 dialogue OBJ not removed after close')
    frozen_write(ROOT/'analysis/pending500_039_v1/normal_path_v1.json',dict(passed=True,rom_sha256=sha(rom),scope=__doc__,own_coldboot_segments=receipts,native_loads=loads,new038_selector_observations=calls,prior036_rendered_ID=key,prior036_context_stream_verified=True,close_and_post_close_movement_verified=True,final_position=[v/65536 for v in p1],latest_checkpoint=str((d/'checkpoint.mss').relative_to(ROOT)),latest_origin=str((d/'result.json').relative_to(ROOT)),new038_board_selector_and_Korean_display_verified=False,new038_NPC_natural_scene_acquisition_verified=False,alias_or_game_state_injection_used=False,release_eligible=False,visual_review_pending=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_normal039_v1.py','tools/run_normal039_v1.py','tools/capture_field_loader_038_v1.py','analysis/pending500_039_v1/normal_recipe_receipts_v1.json']}))
    print('PASS038 own normal16, native selected/old loads',len(loads),'prior036 stream',key,'close/movement',list(p1),'NOT new board display approval')


if __name__=='__main__':main()
