"""Validate own036 normal checkpoint chain and actual selected source loads."""
import argparse,struct
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--folder',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();rp=ROOT/'poc/output/pending500_036_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();selected={int(p['source_archive'],16):p for p in m['keyitem_rom']['npc036']['placements']};origin=ROOT/a.folder/'result.json';seen=set();chain=[];loads=[];calls=[];entries=[]
    while origin:
        if origin in seen:raise ValueError('036 origin cycle')
        seen.add(origin);d=origin.parent;r=read(origin)
        if not r['complete'] or r['return_code']!=0 or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False or r['scope'].startswith('DIAGNOSTIC'):raise ValueError('036 normal receipt identity')
        for name,h in r['artifacts'].items():require_hash(d/name,h)
        chain.append(dict(path=str(origin.relative_to(ROOT)),sha256=sha(origin.read_bytes())))
        events=read(d/'field_loader.json');starts=[e for e in events['events'] if e['pc']==0x0804F724]
        if events['loads']!=len(starts):raise ValueError('036 loader event/snapshot indexing')
        for i,e in enumerate(starts,1):
            arc=e['r0']-0x08000000
            if arc not in selected:continue
            p=selected[arc];native=lz77_decompress(source,arc)[0];blob=(d/f'load_{i:03d}_02039800.bin').read_bytes()
            if e['scene']!=p['scene'] or blob[:len(native)]!=native:raise ValueError('036 actual selected source acquisition differs')
            loads.append(dict(receipt=str(origin.relative_to(ROOT)),archive=f'{arc:06X}',scene=e['scene'],sub=e['sub'],selector=e['selector'],frame=e['frame'],native_bytes=len(native),native_sha256=sha(native),root=0x02039800))
        calls.extend(dict(receipt=str(origin.relative_to(ROOT)),**c) for c in read(d/'native_selector.json')['selectors'])
        entries.extend(dict(receipt=str(origin.relative_to(ROOT)),**c) for c in read(d/'npc_entries.json')['entries'])
        if r['state_origin']:
            parent=Path(r['state_origin']);pr=read(parent)
            if r['state_sha256']!=pr['artifacts']['checkpoint.mss']:raise ValueError('036 exact parent state checksum')
            require_hash(d/'input.mss',r['state_sha256']);origin=parent
        else:origin=None
    if not loads or not any(x['archive']=='79CF04' for x in loads):raise ValueError('036 Sunday79CF04 native source not acquired')
    folder=ROOT/a.folder;ram=(folder/'final_gbaExtWorkRam.bin').read_bytes();native=lz77_decompress(source,0x79CF04)[0];retained=ram[0x39800:0x39800+len(native)]==native;scene_at=struct.unpack_from('<I',ram,0xF300)[0]-0x02000000;position=None
    if 0<=scene_at<=len(ram)-0x2C:
        at=struct.unpack_from('<I',ram,scene_at+0x28)[0]-0x02000000
        if 0<=at<=len(ram)-0x30:position=[x/65536 for x in struct.unpack_from('<3i',ram,at+0x24)]
    frozen_write(ROOT/a.out,dict(passed=True,rom_sha256=m['output_sha256'],scope='Normal own036 coldboot/controller checkpoint chain and exact selected compressed source acquisition; not NPC glyph/selector/timing approval',chain=chain,normal_segment_count=len(chain),selected_native_loads=loads,observed_selector_events_NOT_display_approval=calls,observed_actor_entries_NOT_display_approval=entries,natural036_selection_display_verified=False,final_source79CF04_retained=retained,final_position=position,latest_checkpoint=str((folder/'checkpoint.mss').relative_to(ROOT)),latest_origin=str((folder/'result.json').relative_to(ROOT)),release_eligible=False,limitations=['Earlier73-action normal recipe reached PET calendar rather than field; preserved as route observation, not translation-failure evidence or successful NPC trial.','No old-ROM states, read aliases, actor mode/flags/HP/RAM injection. Normal native source load does not by itself prove translated clone consumption.','Final source residency is explicitly measured; battle scratch cannot be called field residency.'],dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_normal_progress036_v1.py','tools/capture_field_loader_036_v1.py','tools/specs/field_capture036_v1_version.json']}))
    print('PASS036 normal chain',len(chain),'segments, selected native loads',len(loads),'selector events',len(calls),'retained',retained,'position',position)

if __name__=='__main__':main()
