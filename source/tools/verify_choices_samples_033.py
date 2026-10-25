"""Exact033 quarantined native choices; not natural operator/profile-save QA."""
import struct
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels


def main():
    rp=ROOT/'poc/output/pending500_033_v1.gba'; m=read(rp.with_suffix('.json'))
    require_hash(rp,m['output_sha256']); rom=rp.read_bytes(); cfg=read('project.json')
    manifest=read('analysis/pending_insertion_500_033_carry500_v1/preflight.json')
    selection=read('analysis/pending_insertion_500_033_exact500_selection_v1/selection.json')
    specs=[
        ('vertical-three-cancel','766134',6,{5:0,6:1,7:2,8:1,9:0,10:0,11:0,12:1,13:2},15,3),
        ('vertical-three-a0','766134',6,{5:0},7,0),
        ('vertical-three-a1','766134',6,{5:0,6:1},8,1),
        ('vertical-three-a2','766134',6,{5:0,6:1,7:2},9,2),
        ('manager-cancel','7CC6A0',0,{7:0,8:1,9:0,10:1},14,1)]
    pages=[]; outcomes=[]; receipts={}
    for case,arc,script,steps,last,result in specs:
        folder=ROOT/('poc/runtime/pending500-033-v1-raw-'+case)
        receipt=read(folder/'result.json'); rec=next(r for r in manifest['archives'] if r['archive']==arc)
        asset=read(rec['merged_asset']['path'])
        pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,rec['script_count'],asset=asset)
        d=receipt['display_diagnostic']
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] is not False or d!=dict(roots=1,entries=1,navi=0,root=pool,script=script):
            raise ValueError('033 diagnostic identity '+case)
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('033 quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        receipts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        group=next(g for g in selection['groups'] if g['archive']==arc and g['script']==script)
        choice=next(p for p in group['geometry'][0]['pages'] if 'choice' in p.get('kind',''))
        by={u['id']:u for u in units}
        labels=([by[o['label']['id']] for o in choice['options']] if arc=='766134' else units[-2:])
        selected=([units[0]]+labels if script==5 and arc=='766134' else [units[-3]]+labels if arc=='7CC6A0' else labels)
        for step,chosen in steps.items():
            cp=f'step_{step:03}'; ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes(); tr=read(folder/(cp+'_roll_pet.json'))
            ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or tuple(ram[0xFA38:0xFA3A])!=(52,110) or ptr!=ends[labels[-1]['id']] or rom[ptr-0x08000000]!=0xEC or ram[0xFA24]!=1 or ram[0xFA33]!=chosen:
                raise ValueError('033 native choice wait/navigation '+case+':'+str(step))
            ee={s:expected[s] for u in selected for s in streams[u['id']]}
            dd={d['stream']:d for d in tr['draws'] if d['stream'] in ee}; offsets={}
            if set(dd)!=set(ee):raise ValueError('033 current choice glyph population')
            def append(u,row,width):
                it=iter(streams[u['id']])
                for ch in u['translation']:
                    if ch=='\n':row+=1;width=0;continue
                    s=next(it); offsets[s]=row*10752+width*4
                    width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0]
                return row,width
            if arc=='766134':
                flags=struct.unpack_from('<H',ram,0xFA5E)[0]; mode=struct.unpack_from('<I',ram,0x159F8)[0]&1
                area=(166 if mode else 176) if flags&2 else (230 if mode else 240)
                relative=(area-choice['allocated_advance'])//2-(0 if flags&2 else 52)
                if script==5:append(units[0],0,0)
                for row,u in zip(choice['rows'],labels):append(u,row,relative+8)
            else:
                append(units[-3],0,0)
                flags=struct.unpack_from('<H',ram,0xFA5E)[0]; mode=struct.unpack_from('<I',ram,0x159F8)[0]&1
                area=(166 if mode else 176) if flags&2 else (230 if mode else 240)
                relative=(area-choice['allocated_advance'])//2-(0 if flags&2 else 52)
                width=relative&~1
                for u in labels:_,width=append(u,2,width+8)
            if any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=ee[s]['index'] for s,d in dd.items()):raise ValueError('033 independently computed native positions')
            counts=Counter(g['index'] for g in ee.values()); reads={r['index']:r['reads'] for r in tr['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('033 font CPU reads')
            oam=(folder/(cp+'_gbaSpriteRam.bin')).read_bytes(); cursors=[]
            for i in range(128):
                aa,bb,kk=struct.unpack_from('<HHH',oam,i*8)
                if not aa&0x2300 and kk&1023==1020 and kk>>12==14:cursors.append(i)
            if len(cursors)!=1:raise ValueError('033 unique live choice cursor')
            proof=pixels(folder,step,list(dd.values()),ee,rom,m,origin=(52,110),cursor_screen_background=True,cursor_indices=tuple(cursors))
            pages.append(dict(case=case,step=step,ids=[u['id'] for u in selected],selected_option=chosen,cursor_oam_indices=cursors,**proof))
        ram=(folder/f'step_{last:03}_gbaExtWorkRam.bin').read_bytes()
        own=next(r for r in m['archives'] if r['archive']=='65A608')
        if struct.unpack_from('<I',ram,0xFA50)[0]!=0x08000000+own['rom_offset']:raise ValueError('033 native PET return '+case)
        events=read(folder/f'step_{last:03}_choice_trace.json')['events']; returned=[e for e in events if e['op']==0x4EC]
        if len(returned)!=1 or bytes.fromhex(returned[0]['hex'])[0x13]!=result or not any(e['op']==0x1EA for e in events):raise ValueError('033 native EA/EC outcome '+case)
        if ('cancel' in case) and not any(e['op']==0x3EC for e in events):raise ValueError('033 native B path')
        if arc=='7CC6A0':
            branch=(folder/'step_012_gbaExtWorkRam.bin').read_bytes()
            if branch[0xFA21]!=95 or struct.unpack_from('<I',branch,0xFA50)[0]!=pool:raise ValueError('033 retained cancel target95')
        outcomes.append(dict(case=case,native_result=result,normal_pet_return=True,natural_event_or_save_verified=False))
    frozen_write(ROOT/'analysis/pending500_033_v1/choice_samples.json',dict(schema=1,passed=True,rom_sha256=sha(rom),pages=pages,outcomes=outcomes,receipts=receipts,
        checker=dict(path='tools/verify_choices_samples_033.py',sha256=sha((ROOT/'tools/verify_choices_samples_033.py').read_bytes())),
        runtime_tested=True,visual_review_pending=True,release_eligible=False,
        limits='Read-alias diagnostic checkpoints only. Native EA/EC directions, B-disable, separate cancel and A outcomes, manager B target95, current choice glyph CPU/OBJ/pixels. No natural operator/battle event, manager Yes/editor, name provider worst case, Hangul commit/save, audio or whole-batch semantic approval.'))
    print('PASS033',len(pages),'native choice sample pages;',len(outcomes),'outcomes; font CPU/OBJ/pixels')


if __name__=='__main__':main()
