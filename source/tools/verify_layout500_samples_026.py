"""Exact026 native vertical/PET input and font->OBJ->screen sample evidence."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_026_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json')
    selection=read('analysis/pending_insertion_500_026_selection_v1/selection.json');manifest=read('analysis/pending_insertion_500_026_carry_v1/preflight.json');pages=[];outcomes=[];artifacts={}
    for case,arc,script,origin,select_steps,chosen in [
        ('vertical-choice','716DE4',8,(52,110),range(5,16),{5:0,6:0,7:0,8:0,9:0,10:1,11:1,12:1,13:1,14:0,15:1}),
        ('pet-choice','683054',1,(92,110),range(7,17),{7:0,8:0,9:0,10:1,11:1,12:1,13:0,14:1,15:0,16:1})]:
        folder=ROOT/'poc/runtime'/('pending500-026-v1-raw-'+case);receipt=read(folder/'result.json');record=next(r for r in manifest['archives'] if r['archive']==arc);asset=read(record['merged_asset']['path'])
        pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,record['script_count'],asset=asset)
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] or receipt['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('026 diagnostic identity')
        if (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists():raise ValueError('026 diagnostic quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        artifacts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        group=next(g for g in selection['groups'] if g['archive']==arc and g['script']==script)
        choice=next(p for p in group['geometry'][0]['pages'] if p.get('kind') in ('vertical-two-choice','pet-fixed16-horizontal-choice'))
        by={u['id']:u for u in units};labels=[by[o['label']['id']] for o in choice['options']]
        page_specs=[(3,[units[0]],'prompt')]+[(s,labels,'choice') for s in select_steps]
        if case=='pet-choice':page_specs.append((5,[by[arc+':1:1']],'nickname'))
        for step,selected,kind in page_specs:
            cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'));ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or tuple(ram[0xFA38:0xFA3A])!=origin:raise ValueError('026 native root/origin')
            e={s:expected[s] for u in selected for s in streams[u['id']]};draws={d['stream']:d for d in trace['draws'] if d['stream'] in e};offsets={};provider_start=None
            if set(draws)!=set(e):raise ValueError('026 all current page glyph streams')
            def append(u,row,width):
                it=iter(streams[u['id']])
                for ch in u['translation']:
                    if ch=='\n':row+=1;width=0;continue
                    s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0]
                return row,width
            if kind=='choice':
                if ptr!=ends[labels[-1]['id']] or rom[ptr-0x08000000]!=0xEC or ram[0xFA24]!=1 or ram[0xFA33]!=chosen[step]:raise ValueError('026 native waiting choice/navigation')
                if case=='vertical-choice':
                    flags=struct.unpack_from('<H',ram,0xFA5E)[0];mode=struct.unpack_from('<I',ram,0x159F8)[0]&1
                    area=(166 if mode else 176) if flags&2 else (230 if mode else 240)
                    relative=(area-choice['allocated_advance'])//2-(0 if flags&2 else origin[0])
                    for row,u in enumerate(labels):append(u,row,relative+8)
                else:
                    width=16
                    for u in labels:
                        _,width=append(u,0,width+8)
            else:
                u=selected[0];width=0
                if kind=='nickname':
                    first=draws[streams[u['id']][0]]['offset']
                    if first%4 or not 0<=first//4<=99:raise ValueError('026 observed native nickname extent')
                    provider_start=width=first//4
                append(u,0,width)
                if ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('026 exact waited literal')
            if any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=e[s]['index'] for s,d in draws.items()):raise ValueError('026 glyph indices/aggregate row offsets')
            counts=Counter(g['index'] for g in e.values());reads={r['index']:r['reads'] for r in trace['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('026 font CPU coverage')
            proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=origin,cursor_screen_background=kind=='choice')
            if kind=='choice':
                im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set();cursors=[];oam=(folder/(cp+'_gbaSpriteRam.bin')).read_bytes()
                for index in range(128):
                    aa,bb,kk=struct.unpack_from('<HHH',oam,index*8)
                    if not aa&0x2300 and kk&1023==1020 and kk>>12==14:cursors.append((bb&511,aa&255))
                for s,glyph in e.items():
                    rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+glyph['index']*4)[0]
                    occupied.update((x,y) for y in range(origin[1]+rr*14,origin[1]+rr*14+12) for x in range(origin[0]+xx//4,origin[0]+xx//4+w))
                vacant={(x,y) for y in range(110,150) for x in range(origin[0],234) if not(x>=224 and y>=138) and not any(cx<=x<cx+16 and cy<=y<cy+16 for cx,cy in cursors)}-occupied
                if any(im.getpixel(pt)!=im.getpixel((233,110)) for pt in vacant):raise ValueError('026 choice clear/background residue')
                proof['vacant_pixels_cleared']=len(vacant)
            pages.append(dict(case=case,step=step,kind=kind,ids=[u['id'] for u in selected],observed_native_provider_start=provider_start,provider_start_is_observed_not_independently_recomputed=provider_start is not None,selected_option=chosen.get(step),**proof))
        last=17 if case=='vertical-choice' else 20;ram=(folder/f'step_{last:03}_gbaExtWorkRam.bin').read_bytes();own=next(r for r in m['archives'] if r['archive']=='65A608')
        if struct.unpack_from('<I',ram,0xFA50)[0]!=0x08000000+own['rom_offset']:raise ValueError('026 return to normal PET')
        events=read(folder/f'step_{last:03}_choice_trace.json')['events'];returned=[e for e in events if e['op']==0x4EC]
        if len(returned)!=1 or bytes.fromhex(returned[0]['hex'])[0x13]!=1 or not any(e['op']==0x1EA for e in events):raise ValueError('026 real native choice continuation/result')
        if case=='pet-choice':
            # Native BSeparate=false returns the last option, whose preserved
            # target is script2, not the separate third target.
            _,branch,be,bs,bend=model(rom,m,cfg,arc,2,record['script_count'],asset=asset)
            for step in (17,18):
                cp=f'step_{step:03}';bram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();tr=read(folder/(cp+'_roll_pet.json'));ee={s:be[s] for u in branch for s in bs[u['id']]};dd={d['stream']:d for d in tr['draws'] if d['stream'] in ee}
                if bram[0xFA21]!=2 or struct.unpack_from('<I',bram,0xFA4C)[0]!=bend[branch[-1]['id']] or set(dd)!=set(ee):raise ValueError('026 PET cancel target2 exact wait')
                proof=pixels(folder,step,list(dd.values()),ee,rom,m,origin=origin)
                pages.append(dict(case=case,step=step,kind='retained-cancel-branch',ids=[u['id'] for u in branch],**proof))
            if not any(e['op']==0x3EC for e in events):raise ValueError('026 actual native B path')
        outcomes.append(dict(case=case,native_result=1,original_pet_return=True,all_two_node_direction_edges_sampled=True,disable_b_ignored_at_step6=case=='vertical-choice',confirm=case=='vertical-choice',cancel=case=='pet-choice',actual_natural_event_or_battle_effects_verified=False))
    frozen_write(ROOT/'analysis/pending500_026_v1/raw_samples.json',dict(schema=1,passed=True,rom_sha256=sha(rom),pages=pages,outcomes=outcomes,receipts=artifacts,checker=dict(path='tools/verify_layout500_samples_026.py',sha256=sha((ROOT/'tools/verify_layout500_samples_026.py').read_bytes())),runtime_tested=True,release_eligible=False,limits='Quarantined PET root/table read aliases, actual native initializer/width pass/navigation/vertical B-disable/confirm and PET cancel->retained script2->PET return. Font CPU/OBJ/screen and choice cleared-background samples only. Nickname prefix offset is observed and bounded, not independently recomputed or worst-case/Hangul-name persistence proof. No natural mission/battle acquisition or flag effect, whole500 semantic approval, hardware/audio completion.'))
    print('PASS026',len(pages),'sample pages; vertical B-disable/A confirm; PET B cancel script2; both PET return; CPU/OBJ/pixels')

if __name__=='__main__':main()
