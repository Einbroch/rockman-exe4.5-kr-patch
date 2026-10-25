"""036 native A0 Sunday actor/timebranch, close/reentry and return to movement."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress

def main():
    rp=ROOT/'poc/output/pending500_036_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();native=lz77_decompress(source,0x79CF04)[0];pool=0x08000000+next(x for x in m['keyitem_rom']['npc036']['archives'] if x['archive']=='79CF04')['rom_offset'];reports=[]
    for name in ['natural_first_display_v1.json','natural_reentry_display_v1.json']:
        path='analysis/pending500_036_v1/'+name;r=read(path)
        if not r['passed'] or r['rom_sha256']!=m['output_sha256'] or r['id']!='79CF04:3:0' or r['actual_render_script']!=3 or not r['native_loads']:raise ValueError('036 normal page/source prerequisite')
        for link in r['checkpoint_chain']:require_hash(ROOT/link['path'],link['sha256'])
        reports.append(dict(path=path,sha256=sha((ROOT/path).read_bytes())))
    folders=[ROOT/('poc/runtime/pending500-036-sunday-natural-npc-v'+str(i)) for i in (1,2)];receipts=[read(d/'result.json') for d in folders];calls=[]
    if receipts[1]['state_origin']!=str(folders[0]/'result.json') or receipts[1]['state_sha256']!=receipts[0]['artifacts']['checkpoint.mss']:raise ValueError('036 direct natural reentry edge')
    for d,r in zip(folders,receipts):
        if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False or r['scope'].startswith('DIAGNOSTIC'):raise ValueError('036 normal receipt')
        for name,h in r['artifacts'].items():require_hash(d/name,h)
        entries=read(d/'npc_entries.json')['entries'];readers=read(d/'field_loader.json')['readers'];selectors=read(d/'native_selector.json')['selectors']
        if len(entries)!=len(readers) or len(entries)!=len(selectors) or len(entries)!=1:raise ValueError('036 one natural actor open per segment')
        e=entries[0];rr=readers[0];s=selectors[0];g=e['registers']
        if (g['0'],g['1'],g['5'],g['14'])!=(0,0,0x0200ABB8,0x0806EDF1) or (rr['pc'],rr['r0'],rr['r1'],rr['lr'])!=(0x0804F76E,0x02039800,0,0x0806EDF1):raise ValueError('036 actual original caller/actor ABI')
        if (s['script'],s['root'],s['caller_lr'])!=(0,pool,0x0804F773) or s['cycles']<=0 or e['frame']!=rr['frame'] or e['frame']!=s['frame']:raise ValueError('036 actor/caller/selector linkage')
        ram=(d/'final_gbaExtWorkRam.bin').read_bytes()
        if ram[0x39800:0x39800+len(native)]!=native or struct.unpack_from('<I',ram,0xABB8+0x9C)[0]!=0:raise ValueError('036 native resident bytes/actor mode retained')
        calls.append(dict(receipt=str((d/'result.json').relative_to(ROOT)),**s))
    d=folders[1]
    for step in [1,3,4]:
        o=(d/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();active=[i for i in range(128) for a,b,k in [struct.unpack_from('<3H',o,8*i)] if not a&0x2300 and k>>12==14]
        if active:raise ValueError('036 text OBJs not disabled after closure')
    before=(d/'step_003_gbaExtWorkRam.bin').read_bytes();after=(d/'step_004_gbaExtWorkRam.bin').read_bytes();p0=struct.unpack_from('<3i',before,0xFB54);p1=struct.unpack_from('<3i',after,0xFB54)
    if p0==p1:raise ValueError('036 no actual post-close movement')
    pics=[('poc/runtime/pending500-036-sunday-natural-npc-v1/step_001.png')]+[f'poc/runtime/pending500-036-sunday-natural-npc-v2/step_{s:03}.png' for s in [1,2,3,4]]
    frozen_write(ROOT/'analysis/pending500_036_v1/natural_cached_display_v1.json',dict(passed=True,rom_sha256=m['output_sha256'],scope='Normal036 coldboot/controller/source79CF04 acquisition, actor0/time branch3, actual source caller ->036 clone -> font/OBJ/screen, closure/reentry/movement',natural_actor_selection_verified=True,natural_A0_representative_verified=True,scene_A1_A3_natural_paths_verified=False,first_and_reentry_display_reports=reports,native_calls=calls,actual_native_source_retained_bytes=len(native),rendered_unique_ids=['79CF04:3:0'],complete_page_displays=2,source_time_branch='Unchanged script0 checkNetTime09:00..10:30 ->script3; observed Sunday09:13/09:14',actor=0x0200ABB8,actor_mode=0,alias_or_state_injection_used=False,close_reentry_post_close_movement=True,post_close_positions=[[v/65536 for v in p0],[v/65536 for v in p1]],screens_directly_viewed=[dict(path=p,sha256=sha((ROOT/p).read_bytes())) for p in pics],latest_checkpoint=str((d/'checkpoint.mss').relative_to(ROOT)),latest_origin=str((d/'result.json').relative_to(ROOT)),timing_scope='Observed036 selector32360/32361 Mesen emulated CPU cycles only; not worst-case/hardware/audio guarantee',release_eligible=False,all500_runtime_or_semantic_review=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_natural_npc036_v1.py','tools/verify_native_npc_display_036_v1.py','tools/specs/native_display036_v1_version.json','tools/capture_field_loader_036_v1.py']}))
    print('PASS036 NATURAL A0 actor/timebranch/clone/font/pixels, close/reentry/actual movement; A1/A3 natural paths pending')

if __name__=='__main__':main()
