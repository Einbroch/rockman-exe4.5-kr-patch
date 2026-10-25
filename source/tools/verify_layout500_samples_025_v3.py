"""025 actual GBA choice/nickname pages, native navigation and continuation."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_025_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json')
    selection=read('analysis/pending_insertion_500_025_selection_v1/selection.json');manifest=read('analysis/pending_insertion_500_025_carry_v1/preflight.json')
    pages=[];outcomes=[];images=[]
    for case,arc,script,steps,origin in [('choice-confirm','766134',4,(3,4,5,6,7,8),(52,110)),('choice-cancel','766134',4,(3,4),(52,110)),('choice-yes','766134',4,(3,4,5,6,7,8,9),(52,110)),('nickname','67D44C',2,(3,5),(92,110))]:
        folder=ROOT/'poc/runtime'/('pending500-025-v2-raw-'+case);receipt=read(folder/'result.json')
        ar=next(r for r in manifest['archives'] if r['archive']==arc);asset=read(ar['merged_asset']['path'])
        pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,ar['script_count'],asset=asset)
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] or receipt['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('025 own diagnostic identity')
        if (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists():raise ValueError('025 state quarantine')
        for n,h in receipt['artifacts'].items():require_hash(folder/n,h)
        group=next(g for g in selection['groups'] if g['archive']==arc and g['script']==script)
        for ordinal,step in enumerate(steps):
            cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'));ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or tuple(ram[0xFA38:0xFA3A])!=origin:raise ValueError('025 native current root/origin')
            selected=units if case.startswith('choice') else [units[ordinal]]
            e={s:expected[s] for u in selected for s in streams[u['id']]};offsets={};row=width=0
            if case.startswith('choice'):
                prompt,yes,no=selected
                it=iter(streams[prompt['id']])
                for ch in prompt['translation']:
                    if ch=='\n':row+=1;width=0;continue
                    s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0]
                choice=next(p for p in group['geometry'][0]['pages'] if p.get('kind')=='horizontal-two-choice')
                flags=struct.unpack_from('<H',ram,0xFA5E)[0];mode=(struct.unpack_from('<I',ram,0x159F8)[0]>>1)&1
                area=(166 if mode else 176) if flags&2 else 240
                rel=(area-choice['allocated_advance'])//2-(0 if flags&2 else origin[0]);width=rel&~1
                for u in (yes,no):
                    width+=8
                    for s in streams[u['id']]:offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0]
                if ptr!=ends[no['id']] or rom[ptr-0x08000000]!=0xEC or ram[0xFA24]!=1:raise ValueError('025 native waiting select state')
                chosen={'choice-confirm':{3:0,4:1,5:0,6:0,7:0,8:1},'choice-cancel':{3:0,4:1},'choice-yes':{3:0,4:1,5:1,6:1,7:1,8:0,9:0}}[case][step]
                if ram[0xFA33]!=chosen:raise ValueError('025 unchanged navigation graph/controller transition')
            else:
                u=selected[0];it=iter(streams[u['id']])
                for ch in u['translation']:
                    if ch=='\n':row+=1;width=0;continue
                    s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0]
                if rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600') or ordinal==1 and ptr!=ends[u['id']]:raise ValueError('025 nickname script exact wait')
            draws={d['stream']:d for d in trace['draws'] if d['stream'] in e}
            if set(draws)!=set(e) or any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=e[s]['index'] for s,d in draws.items()):raise ValueError('025 glyph stream/aggregate row offsets')
            counts=Counter(g['index'] for g in e.values());reads={r['index']:r['reads'] for r in trace['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('025 font CPU reads')
            proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=origin,cursor_screen_background=case.startswith('choice'))
            if case.startswith('choice') or ordinal==1:
                image=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set();cursors=[]
                oam=(folder/(cp+'_gbaSpriteRam.bin')).read_bytes()
                for index in range(128):
                    a,b,k=struct.unpack_from('<HHH',oam,index*8)
                    if not a&0x2300 and k&1023==1020 and k>>12==14:cursors.append((b&511,a&255))
                for s,glyph in e.items():
                    rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+glyph['index']*4)[0]
                    occupied.update((x,y) for y in range(origin[1]+rr*14,origin[1]+rr*14+12) for x in range(origin[0]+xx//4,origin[0]+xx//4+w))
                vacant={(x,y) for y in range(110,150) for x in range(origin[0],234) if not(x>=224 and y>=138) and not any(cx<=x<cx+16 and cy<=y<cy+16 for cx,cy in cursors)}-occupied
                if any(image.getpixel(pt)!=image.getpixel((233,110)) for pt in vacant):raise ValueError('025 static-page cleared background')
                proof['vacant_pixels_cleared']=len(vacant)
            pages.append(dict(case=case,step=step,ids=[u['id'] for u in selected],native_selected_option=ram[0xFA33] if case.startswith('choice') else None,**proof));images.append(Image.open(folder/(cp+'.png')).convert('RGB'))
        last=receipt['capture_steps'][-1];ram=(folder/f'step_{last:03}_gbaExtWorkRam.bin').read_bytes();own=next(r for r in m['archives'] if r['archive']=='65A608')
        if struct.unpack_from('<I',ram,0xFA50)[0]!=0x08000000+own['rom_offset']:raise ValueError('025 native return to original PET')
        trace=read(folder/f'step_{last:03}_choice_trace.json')['events']
        if case.startswith('choice'):
            select_at=ends[units[-1]['id']]-0x08000000
            command=rom[select_at:select_at+6]
            if command!=bytes.fromhex('ec0680ffffff'):raise ValueError('025 frozen source select flags/targets')
            # Native50662 loads option count;50732 uses r3-1 on B.
            # BSeparate(0x20) is false, so B shares the last real option.
            wanted=(0 if case=='choice-yes' else 1) if case!='choice-cancel' else len(choice['options'])-1+(1 if command[2]&0x20 else 0)
            returned=[e for e in trace if e['op']==0x4EC]
            if not returned or any(bytes.fromhex(e['hex'])[0x13]!=wanted for e in returned):raise ValueError('025 native confirm/cancel result')
            if not any(e['op']==0x1EA for e in trace):raise ValueError('025 native width/control option path not observed')
            if (case=='choice-cancel')!=any(e['op']==0x3EC for e in trace):raise ValueError('025 native cancel path identity')
            outcomes.append(dict(case=case,native_option_result=wanted,native_select_continuation_executed=True,original_pet_return=True,BSeparate=bool(command[2]&0x20),B_cancel_shares_last_option=not bool(command[2]&0x20)))
        images.append(Image.open(folder/f'step_{last:03}.png').convert('RGB'))
    out=ROOT/'analysis/pending500_025_v2/raw_samples_v3.json';sheet=out.with_suffix('.png')
    if sheet.exists():raise ValueError('Preserve025 sample sheet')
    im=Image.new('RGB',(960,((len(images)+3)//4)*160))
    for i,img in enumerate(images):im.paste(img,(i%4*240,i//4*160))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(sheet)
    frozen_write(out,dict(passed=True,rom_sha256=sha(rom),pages=pages,outcomes=outcomes,checker=dict(path='tools/verify_layout500_samples_025_v3.py',sha256=sha((ROOT/'tools/verify_layout500_samples_025_v3.py').read_bytes())),sampled_navigation_edges=[[0,'left',0],[0,'right',1],[0,'up',0],[0,'down',0],[1,'left',0],[1,'right',1],[1,'up',1],[1,'down',1]],contact_sheet=dict(path=str(sheet.relative_to(ROOT)),sha256=sha(sheet.read_bytes())),runtime_tested=True,release_eligible=False,limits='BSeparate=false: B cancel preserves native last-option outcome, not a separate third result. Quarantined PET root/table read aliases; actual native initialization/choice input/select result/return and glyph CPU/OBJ/pixels only. Battle decision/caller effects, natural speaker, native maximum nickname, all500 wording/branches and Hangul-name save integration are not established.'))
    print('PASS025 choice navigation/confirm/cancel/return and nickname two translated pages;glyph CPU/OBJ/pixels')

if __name__=='__main__':main()


