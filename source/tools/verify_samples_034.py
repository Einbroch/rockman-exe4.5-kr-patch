"""034 actual new Korean sample glyph/OBJ/pixel and wait/cursor evidence."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels


def main():
    rp=ROOT/'poc/output/pending500_034_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json')
    manifest=read('analysis/pending_insertion_500_034_carry500_v1/preflight.json');selection=read('analysis/pending_insertion_500_034_exact500_selection_v1/selection.json');selected=set(selection['selected_ids'])
    specs=[('list-caption','65B9E8',40,[(5,[0])],(92,110)),('query-choice','65B9E8',41,[(5,[0,1,2]),(6,[0,1,2]),(7,[0,1,2])],(92,110)),('mission-caption','716DE4',100,[(5,[0]),(7,[1])],(52,110)),('trader-caption','6FE8D4',21,[(5,[0])],(52,110))]
    pages=[];receipts={};covered=set()
    for case,arc,script,steps,origin in specs:
        folder=ROOT/('poc/runtime/pending500-034-v1-sample-'+case);receipt=read(folder/'result.json');rec=next(r for r in manifest['archives'] if r['archive']==arc);asset=read(rec['merged_asset']['path']);pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,rec['script_count'],asset=asset)
        d=receipt['display_diagnostic']
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] is not False or d!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('034 exact diagnostic identity '+case)
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('034 alias checkpoint not quarantined')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        receipts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        for step,ordinals in steps:
            chosen=[units[n] for n in ordinals];keys={u['id'] for u in chosen}
            if not keys<=selected:raise ValueError('034 sample not newly inserted')
            cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'));ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or tuple(ram[0xFA38:0xFA3A])!=origin:raise ValueError('034 own initialized root/origin '+case)
            ee={s:expected[s] for u in chosen for s in streams[u['id']]};draws={d['stream']:d for d in trace['draws'] if d['stream'] in ee}
            if set(draws)!=set(ee) or any(d['context']!=0x0200FA20 or d['glyph_index']!=ee[s]['index'] for s,d in draws.items()):raise ValueError('034 new literal native glyph stream '+case)
            for d in draws.values():
                row,off=divmod(d['offset'],10752);width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0]
                if not 0<=row<3 or off%4 or off//4+width>(132 if origin[0]==92 else 168 if row==2 else 180):raise ValueError('034 actual sample draw outside adopted row extent')
            counts=Counter(g['index'] for g in ee.values());reads={r['index']:r['reads'] for r in trace['font_reads']}
            if any(reads.get(index,0)<24*n for index,n in counts.items()):raise ValueError('034 actual font CPU reads')
            kwargs={};cursor_indices=[]
            if case=='query-choice':
                if ptr!=ends[units[2]['id']] or rom[ptr-0x08000000]!=0xEC or ram[0xFA24]!=1 or ram[0xFA33]!=(1 if step==6 else 0):raise ValueError('034 native choice boundary/left-right selection')
                oam=(folder/(cp+'_gbaSpriteRam.bin')).read_bytes()
                for i in range(128):
                    aa,bb,kk=struct.unpack_from('<HHH',oam,i*8)
                    if not aa&0x2300 and kk&1023==1020 and kk>>12==14:cursor_indices.append(i)
                if len(cursor_indices)!=1:raise ValueError('034 live horizontal cursor')
                kwargs['cursor_indices']=tuple(cursor_indices)
            elif ptr!=ends[chosen[-1]['id']] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('034 exact source native waited-page boundary '+case)
            proof=pixels(folder,step,list(draws.values()),ee,rom,m,origin=origin,cursor_screen_background=True,**kwargs)
            covered|=keys;pages.append(dict(case=case,step=step,ids=sorted(keys),origin=list(origin),current_pointer=ptr,cursor_oam_indices=cursor_indices,**proof))
    deps=['tools/verify_samples_034.py','tools/capture_samples_034.py','tools/verify_pending500_005_displays.py','tools/report_roll_pet.py','analysis/pending_insertion_500_034_exact500_selection_v1/selection.json']
    frozen_write(ROOT/'analysis/pending500_034_v1/samples.json',dict(schema=1,passed=True,rom_sha256=sha(rom),new_rendered_ids=sorted(covered),pages=pages,receipts=receipts,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},runtime_tested=True,visual_review_pending=True,release_eligible=False,limits='Guarded read-alias samples: list caption BEFORE buffer read, horizontal query cursor only, mission first two pages, trader shortage caption. Actual new glyph CPU reads/OBJ/pixels/wait or selector boundary. No list production/page lifetime, native menu acquisition, query confirm/editor/save, full mission outcome or whole500 semantics.'))
    print('034 new sample glyph/OBJ/pixel PASS',len(pages),'pages',len(covered),'literal IDs; visual review pending')


if __name__=='__main__':main()
