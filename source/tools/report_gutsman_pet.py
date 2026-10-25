"""All44 finite static checks; genuine eight PET scenes and cursor/cancel QA."""
import json,struct
from collections import Counter
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_numberman_return import pages as dialogue_pages
from capture_save_qa import inventory
from run_gutsman_pet import STEM,PREFIX

def main(stem=STEM,prefix=PREFIX,expected_counts=(2188,49,683),oldstem='exe45_ko_development_gutsman_intro_v1',outdir='gutsman_pet_v1',inventory_outdir='full_scope_gutsman_pet_v1',added_literal_units=44,changed_archives=()):
    STEM,PREFIX=stem,prefix
    m,rom,e,streams,checks=static(STEM,'665F3C')
    if (m['translated_units'],len(m['archives']),m['unchanged_archives'])!=expected_counts:raise ValueError('population')
    old=ROOT/f'poc/output/{oldstem}.gba';om=read(old.with_suffix('.json'));before=old.read_bytes()
    if sha(before)!=om['output_sha256']:raise ValueError('prior identity')
    if changed_archives not in [(),('66A844',),('66651C',),('665698',),('6368E8',),('6368E8','665698'),('667044',)]:raise ValueError('unregistered prior archive delta')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['archive'] in changed_archives:
            from archive_scripts import script_spans
            count,oldcount,newcount,changed=(255,31,33,{13}) if a['archive']=='66A844' else (28,3,5,{1,2})
            if a['archive']=='667044':count,oldcount,newcount,changed=97,40,81,{9,11,13,15,17,19,21,23,25,88}
            if a['archive']=='667044' and a['translated_units']==81:count,oldcount,newcount,changed=97,81,110,set(range(1,9))
            if a['archive']=='667044' and a['translated_units']==110:count,oldcount,newcount,changed=97,110,150,set(range(40,64))
            if a['archive']=='667044' and a['translated_units']==150:count,oldcount,newcount,changed=97,150,153,{31}
            if a['archive']=='66651C' and a['translated_units']==5:count,oldcount,newcount,changed=28,5,6,{3}
            if a['archive']=='665698' and a['translated_units']==2:count,oldcount,newcount,changed=255,2,4,{22,23}
            if a['archive']=='665698' and a['translated_units']==4:count,oldcount,newcount,changed=255,4,7,{24}
            if a['archive']=='665698' and a['translated_units']==7:count,oldcount,newcount,changed=255,7,10,{0}
            if a['archive']=='665698' and a['translated_units']==10:count,oldcount,newcount,changed=255,10,14,{1,2}
            if a['archive']=='665698' and a['translated_units']==14:count,oldcount,newcount,changed=255,14,15,{31}
            if a['archive']=='665698' and a['translated_units']==15:count,oldcount,newcount,changed=255,15,18,{33}
            if a['archive']=='665698' and a['translated_units']==18:count,oldcount,newcount,changed=255,18,22,{6,7}
            if a['archive']=='665698' and a['translated_units']==22:
                from gutsman_calendar_management import CHANGED
                count,oldcount,newcount,changed=255,22,45,CHANGED
            if a['archive']=='665698' and a['translated_units']==45:count,oldcount,newcount,changed=255,45,54,{25,50,51}
            if a['archive']=='665698' and a['translated_units']==54:count,oldcount,newcount,changed=255,54,57,{10}
            if a['archive']=='6368E8':count,oldcount,newcount,changed=(255,5,7,{74,75}) if a['translated_units']==5 else (255,4,5,{73})
            if a['archive']=='6368E8' and a['translated_units']==7:count,oldcount,newcount,changed=255,7,12,{119,120,121,122,123}
            if a['archive']=='6368E8' and a['translated_units']==12:count,oldcount,newcount,changed=255,12,13,{80}
            if a['archive']=='6368E8' and a['translated_units']==13:count,oldcount,newcount,changed=255,13,16,{10}
            oldsp=script_spans(before[a['rom_offset']:a['rom_offset']+a['compiled_bytes']],count);newsp=script_spans(rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']],count)
            if a['translated_units']!=oldcount or n['translated_units']!=newcount or any(oldsp[i]!=newsp[i] for i in range(count) if i not in changed):raise ValueError('registered Guts literal delta only')
            continue
        if n['compiled_sha256']!=a['compiled_sha256'] or rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]!=before[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]:raise ValueError('retained48 payload drift')
    for a in om['translation_assets']:
        if changed_archives==('667044',) and Path(a['path']).as_posix() in ('translations/gutsman_profile_ko.json','translations/gutsman_profile_questions_ko.json','translations/gutsman_profile_family_checked_ko.json','translations/gutsman_profile_answers_ko.json'):
            from build_development_patch import selected_scope
            child=next(x for x in m['translation_assets'] if x.get('archive')=='667044');require=read(ROOT/child['path']);scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['667044'];selected_scope(scope,require)
            if require['parent_asset']['sha256']!=a['sha256']:raise ValueError('profile parent selected identity')
            continue
        if not any(Path(x['path'])==Path(a['path']) and x['sha256']==a['sha256'] for x in m['translation_assets']):raise ValueError('prior selected asset drift')
    graphics=[];pairs=[(k,m[k],om[k]) for k in ['calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics']];pairs.append(('equipment_title',m['folder_labels']['title'],om['folder_labels']['title']))
    for name,n,a in pairs:
        offset=n['source_offset'];size=n.get('stored_bytes',n.get('bytes'));key='final_stored_sha256' if 'stored_bytes' in n else 'final_block_sha256'
        if (offset,size,n[key])!=(a['source_offset'],a.get('stored_bytes',a.get('bytes')),a[key]) or rom[offset:offset+size]!=before[offset:offset+size] or sha(rom[offset:offset+size])!=n[key]:raise ValueError('graphic payload drift')
        graphics.append(dict(scope=name,offset=offset,bytes=size,sha256=n[key],prior_identical=True))
    bindings=[]
    for who,archive,root in [('GutsManIntro','665EB8',0x38110),('GutsManPET','665F3C',0x38114),('NumberMan','68BBB4',0x382AC),('Forte','6D5A9C',0x3857C)]:
        ar=next(x for x in m['archives'] if x['archive']==archive);actual=struct.unpack_from('<I',rom,root)[0];expected=0x08000000+ar['rom_offset']
        if actual!=expected:raise ValueError('native binding')
        bindings.append(dict(navi=who,archive=archive,root_offset=root,rom_pointer=actual,expected_pointer=expected))
    rt=ROOT/'poc/runtime';seen=set();chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','save-enter','save-commit','normal-reload-menu','normal-reload-navi','normal-reload-select','normal-return'];routes={}
    verify_route(rt/'numberman-intro-v1-select-numberman-full',read(ROOT/'poc/output/exe45_ko_development_numberman_intro_v1.json')['output_sha256'],set())
    parents={name:None if i in [0,8] else chain[i-1] for i,name in enumerate(chain)}
    parents.update({'intro-regression':'normal-reload-select','select-gutsman':'normal-reload-select','prompt-seed':'select-gutsman','prompts':'prompt-seed'})
    for name,parent in parents.items():
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen);routes[name]=r;expected=None if parent is None else str(rt/(PREFIX+parent)/'result.json')
        if r['state_origin']!=expected or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('normal ancestry')
        if any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('normal intervention')
    commit=rt/(PREFIX+'save-commit');env=read(commit/'save_environment.json');sav=STEM+'.sav';saved=env['files_after'][sav]
    if not env['observer_only'] or env['build_sha256']!=m['output_sha256'] or env['files_before'][sav]!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or saved['bytes']!=65536 or saved['sha256']==sha(bytes([255])*65536) or sha((commit/'persistent_files_after'/sav).read_bytes())!=saved['sha256'] or inventory(Path(env['save_directory']))[sav]!=saved:raise ValueError('own save')
    for fn in set(env['files_before'])|set(env['files_after']):
        if fn not in (sav,STEM+'.rtc') and env['files_before'].get(fn)!=env['files_after'].get(fn):raise ValueError('unrelated saves')
    ram=(commit/'step_013_gbaExtWorkRam.bin').read_bytes();savepool=0x8000000+next(x for x in m['archives'] if x['archive']=='6DA21C')['rom_offset']
    if ram[0xFA21]!=58 or struct.unpack_from('<I',ram,0xFA50)[0]!=savepool:raise ValueError('native success58')
    pool=0x8000000+next(x for x in m['archives'] if x['archive']=='665F3C')['rom_offset'];pages=[];observed=set()
    for name in ['select-gutsman','prompt-seed','prompts']:
        p=rt/(PREFIX+name)
        for step in routes[name]['capture_steps']:
            cp=f'step_{step:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes()
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool:continue
            script=ram[0xFA21];keys=[k for k in streams if int(k.split(':')[1])==script]
            if not keys:continue
            obs=read(p/(cp+'_roll_pet.json'));entry=max((c['frame'] for c in obs['calls']),default=0);wanted={s for k in keys for s in streams[k]};last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted and d['frame']>=entry}
            if set(last)!=wanted:continue
            draws=[last[s] for k in keys for s in streams[k]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('CPU glyph reads')
            proof=pixels(p,step,draws,e,rom,m,cursor_screen_background=True);im=Image.open(p/(cp+'.png')).convert('RGB');occupied=set()
            for d in draws:
                row,off=divmod(d['offset'],10752);x0=92+off//4;y0=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0];occupied.update((x,y) for y in range(y0,y0+12) for x in range(x0,x0+w))
            blank={(x,y) for y in range(110,122 if script==1 else 136) for x in range(92,234) if (x,y) not in occupied}
            if {im.getpixel(xy) for xy in blank}!={im.getpixel((231,112))}:raise ValueError('vacant prose clearing')
            observed.update(keys);pages.append(dict(route=p.name,step=step,script=script,units=keys,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((p/(cp+'.png')).read_bytes()),**proof))
    expectation={1:(2,108),2:(2,144),3:(1,220),4:(2,108),5:(1,220)}
    for script,base in zip(range(3,9),range(6,30,4)):expectation.update({base:(1,220),base+1:(script,108),base+2:(script,144),base+3:(1,220)})
    behavior=[];p=rt/(PREFIX+'prompts')
    for step,(script,cursor_x) in expectation.items():
        ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',(p/f'step_{step:03}_gbaSpriteRam.bin').read_bytes(),0)
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script or b&511!=cursor_x:raise ValueError(f'focus/cancel/return:{step}:{ram[0xFA21]}:{b&511}')
        if script!=1 and (a&255!=136 or k&1023!=1020 or k>>12!=14):raise ValueError('option cursor contract')
        behavior.append(dict(step=step,script=script,cursor_x=cursor_x,same_relocated_root=True))
    for script in range(1,9):
        if not any(q['script']==script for q in pages):raise ValueError('complete PET scene missing')
    if len(observed)!=22:raise ValueError('finite runtime unit population')
    _,_,ie,ins,ic=static(STEM,'665EB8');ip=0x8000000+next(x for x in m['archives'] if x['archive']=='665EB8')['rom_offset'];intro=dialogue_pages(rt/(PREFIX+'intro-regression'),1,1,m,rom,ie,ins,ip)
    _,_,ne,ns,nc=static(STEM,'68BBB4');np=0x8000000+next(x for x in m['archives'] if x['archive']=='68BBB4')['rom_offset'];regression=dialogue_pages(rt/(PREFIX+'normal-return'),1,1,m,rom,ne,ns,np)
    if len(intro)!=2 or len(regression)!=3:raise ValueError('regression population')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(960,320))
    for i,script in enumerate(range(1,9)):
        q=next(q for q in pages if q['script']==script);sheet.paste(Image.open(rt/q['route']/f"step_{q['step']:03}.png"),(240*(i%4),160*(i//4)))
    sheet.save(out/'normal_pet_prompts.png');summary=read(ROOT/'analysis'/inventory_outdir/'inventory.json')['summary']
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=added_literal_units,selected_text_units=m['translated_units'],static=checks,native_navi_bindings=bindings,**{f'retained{len(om["archives"])-len(changed_archives)}_archive_payloads_identical':True},changed_archive_contract=list(changed_archives),prior_selected_asset_hashes_identical=True,retained_graphics_payloads=graphics,pages=pages,choice_behavior=behavior,runtime_observed_units=sorted(observed),runtime_open_units=sorted(set(streams)-observed),normal_gutsman_intro_pages=intro,normal_numberman_regression_pages=regression,native_save_sha256=saved['sha256'],native_save_success_script=58,cold_continue_has_no_loaded_checkpoint=True,remaining_catalog=summary['counts'],limits=['Eight native GutsMan idle/initial PET scenes;22 literal units plus yes/no focus,No acceptance,B cancellation and return. Reentry10..16/interruption20 other22 units static-only. No accepted Yes navigation or live communication proved.','Native save/continue is NumberMan regression, not GutsMan save or Hangul name persistence/old-save compatibility.','Wording/voice human review pending; whole ROM/images/inline/fixed/name populations incomplete. Previous wait-arrow53pixel difference unresolved.'])
    if changed_archives==('667044',):
        result.update(prior_selected_asset_hashes_identical=False,all_other_prior_selected_asset_hashes_identical=True,retained_profile_units=81 if next(a for a in om['archives'] if a['archive']=='667044')['translated_units']==81 else 40)
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Guts PET44 static / normal8 scenes22 units / Guts intro2 / NumberMan3: PASS');return result

if __name__=='__main__':main()
