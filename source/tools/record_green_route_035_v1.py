"""Close the bounded green-route investigation without inventing NPC proof."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress


def main():
    m=read('poc/output/pending500_035_v2.json');require_hash(ROOT/'poc/output/pending500_035_v2.gba',m['output_sha256'])
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    native=lz77_decompress(source,0x79D650)[0];records=[]
    for i in range(1,15):
        f=ROOT/f'poc/runtime/pending500-035-fixed-green-route-v{i}';r=read(f/'result.json')
        if not r['complete'] or r['return_code']!=0 or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible',True) is False:raise ValueError('Normal route binding')
        for n,h in r['artifacts'].items():require_hash(f/n,h)
        parent=read(r['state_origin']);require_hash(f/'input.mss',r['state_sha256'])
        if not parent['complete'] or parent['rom_sha256']!=r['rom_sha256'] or parent['artifacts']['checkpoint.mss']!=r['state_sha256'] or parent.get('normal_play_checkpoint_eligible',True) is False:raise ValueError('Normal parent edge')
        ram=(f/'final_gbaExtWorkRam.bin').read_bytes();obs=read(f/'field_loader.json');events=read(f/'npc_entries.json')['entries']
        if ram[0x39800:0x39800+len(native)]!=native or events or any(x['pc']==0x0804F76E for x in obs['readers']):raise ValueError('Unexpected NPC evidence requires independent review')
        positions=[]
        for step in r['capture_steps']:
            rr=(f/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
            positions.append(dict(step=step,position=[v/65536 for v in struct.unpack_from('<3i',rr,0xFB54)]))
        records.append(dict(receipt=str((f/'result.json').relative_to(ROOT)),receipt_sha256=sha((f/'result.json').read_bytes()),checkpoint_sha256=r['artifacts']['checkpoint.mss'],positions=positions,source_retained_bytes=len(native)))
    f=ROOT/'poc/runtime/pending500-035-fixed-green-route-v14';ram=(f/'step_001_gbaExtWorkRam.bin').read_bytes();board=lz77_decompress(source,0x799314)[0]
    if struct.unpack_from('<I',ram,0xFA50)[0]!=0x0203C800 or ram[0xFA21]!=8 or ram[0x3C800:0x3C800+len(board)]!=board:raise ValueError('Actual board source/script binding')
    tpl=ROOT/'analysis/full_scope_v1/source_tpl/799314.tpl'
    frozen_write(ROOT/'analysis/pending500_035_v2/normal_green_progress_v1.json',dict(passed=True,scope='14 additional normal navigation segments; no cached NPC display reached',rom_sha256=m['output_sha256'],segments=records,cached_NPC_reader_hits=0,natural_cached_selection_verified=False,source_board=dict(archive='799314',source_tpl_sha256=sha(tpl.read_bytes()),observed_script=8,root=0x0203C800,source_script0='checkItem item0 amount1, missing->8; success sets Navi flag1368',observed_message='Exam Ticket required to enter exam-center administration area',gate_not_bypassed=True,scope_limit='Explains this exam-center entrance only, not all NPC route collisions.'),latest_checkpoint=records[-1]['receipt'].replace('result.json','checkpoint.mss'),dialogue_closed_visually=True,directly_viewed_final_captures=14,tool_sha256=sha((ROOT/'tools/record_green_route_035_v1.py').read_bytes()),release_eligible=False))
    print('PASS14 normal routes, source799314/script8 exam entrance identified, no cached NPC claim')


if __name__=='__main__':main()
