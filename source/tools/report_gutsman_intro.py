"""Finite four-literal integrity; native GutsMan intro and NumberMan regression."""
import json,struct
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_numberman_return import pages
from capture_save_qa import inventory
from run_gutsman_intro import STEM,PREFIX

def main():
    m,rom,e,s,checks=static(STEM,'665EB8')
    if (m['translated_units'],len(m['archives']),m['unchanged_archives'])!=(2144,48,684):raise ValueError('cumulative population')
    old=ROOT/'poc/output/exe45_ko_development_forte_seasonal_v1.gba';om=read(old.with_suffix('.json'));before=old.read_bytes()
    if sha(before)!=om['output_sha256']:raise ValueError('prior identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if n['compiled_sha256']!=a['compiled_sha256'] or rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]!=before[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]:raise ValueError('retained47 payload drift')
    for a in om['translation_assets']:
        if not any(x['path']==a['path'] and x['sha256']==a['sha256'] for x in m['translation_assets']):raise ValueError('prior selected asset drift')
    graphics=[];pairs=[(k,m[k],om[k]) for k in ['calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics']];pairs.append(('equipment_title',m['folder_labels']['title'],om['folder_labels']['title']))
    for name,n,a in pairs:
        offset=n['source_offset'];size=n.get('stored_bytes',n.get('bytes'));key='final_stored_sha256' if 'stored_bytes' in n else 'final_block_sha256'
        if (offset,size,n[key])!=(a['source_offset'],a.get('stored_bytes',a.get('bytes')),a[key]) or rom[offset:offset+size]!=before[offset:offset+size] or sha(rom[offset:offset+size])!=n[key]:raise ValueError('graphic payload drift')
        graphics.append(dict(scope=name,offset=offset,bytes=size,sha256=n[key],prior_identical=True))
    bindings=[]
    for who,archive,root in [('GutsManIntro','665EB8',0x38110),('GutsManSeasonal','66A234',0x38144),('NumberMan','68BBB4',0x382AC),('Forte','6D5A9C',0x3857C)]:
        ar=next(x for x in m['archives'] if x['archive']==archive);actual=struct.unpack_from('<I',rom,root)[0];expected=0x08000000+ar['rom_offset']
        if actual!=expected:raise ValueError('native navi binding')
        bindings.append(dict(navi=who,archive=archive,root_offset=root,rom_pointer=actual,expected_pointer=expected))
    rt=ROOT/'poc/runtime';seen=set();chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','save-enter','save-commit','normal-reload-menu','normal-reload-navi','normal-reload-select','normal-return']
    verify_route(rt/'numberman-intro-v1-select-numberman-full',read(ROOT/'poc/output/exe45_ko_development_numberman_intro_v1.json')['output_sha256'],set())
    for i,name in enumerate(chain):
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen);expected=None if i in [0,8] else str(rt/(PREFIX+chain[i-1])/'result.json')
        if r['state_origin']!=expected or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('own normal ancestry')
        lua=(p/'segment.lua').read_text(encoding='utf8')
        if 'emu.write' in lua or 'setState' in lua or 'AliasReads' in lua:raise ValueError('normal intervention')
    commit=rt/(PREFIX+'save-commit');env=read(commit/'save_environment.json');sav=STEM+'.sav';saved=env['files_after'][sav]
    if (not env['observer_only'] or env['build_sha256']!=m['output_sha256'] or env['files_before'][sav]!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or saved['bytes']!=65536 or saved['sha256']==sha(bytes([255])*65536) or sha((commit/'persistent_files_after'/sav).read_bytes())!=saved['sha256'] or inventory(Path(env['save_directory']))[sav]!=saved):raise ValueError('own native save identity')
    for fn in set(env['files_before'])|set(env['files_after']):
        if fn not in (sav,STEM+'.rtc') and env['files_before'].get(fn)!=env['files_after'].get(fn):raise ValueError('unrelated save drift')
    ram=(commit/'step_013_gbaExtWorkRam.bin').read_bytes();savepool=0x8000000+next(x for x in m['archives'] if x['archive']=='6DA21C')['rom_offset']
    if ram[0xFA21]!=58 or struct.unpack_from('<I',ram,0xFA50)[0]!=savepool:raise ValueError('native save success58')
    p=rt/(PREFIX+'select-gutsman');r=verify_route(p,m['output_sha256'],seen)
    if Path(r['state_origin']).resolve()!=(rt/(PREFIX+'normal-reload-select')/'result.json').resolve() or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('native Guts parent')
    lua=(p/'segment.lua').read_text(encoding='utf8')
    if any(x in lua for x in ['emu.write','setState','AliasReads']):raise ValueError('Guts intervention')
    pool=0x8000000+next(x for x in m['archives'] if x['archive']=='665EB8')['rom_offset'];intro=pages(p,1,1,m,rom,e,s,pool)
    _,_,ne,ns,nc=static(STEM,'68BBB4');np=0x8000000+next(x for x in m['archives'] if x['archive']=='68BBB4')['rom_offset'];regression=pages(rt/(PREFIX+'normal-return'),1,1,m,rom,ne,ns,np)
    if len(intro)!=2 or len(regression)!=3:raise ValueError('page population')
    out=ROOT/'analysis/gutsman_intro_v1';out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,160))
    for i,q in enumerate(intro):sheet.paste(Image.open(p/f"step_{q['step']:03}.png"),(240*i,0))
    sheet.save(out/'normal_intro_pages.png');summary=read(ROOT/'analysis/full_scope_gutsman_intro_v1/inventory.json')['summary']
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=4,selected_text_units=2144,static=checks,native_navi_bindings=bindings,retained47_archive_payloads_identical=True,prior_selected_asset_hashes_identical=True,retained_graphics_payloads=graphics,normal_gutsman_intro_pages=intro,normal_gutsman_return_pages=[],normal_numberman_regression_pages=regression,native_save_sha256=saved['sha256'],native_save_success_script=58,cold_continue_has_no_loaded_checkpoint=True,remaining_catalog=summary['counts'],limits=['First meeting script1 two pages via genuine GutsMan selection. Reselection script2 two literals static-only; caller/flag prerequisites not verified. No alias used.','Wording/voice needs human review. Full translation incomplete; graphics/inline/fixed/name populations unresolved.','Hangul name editing/committed records/all redisplay/persistence/old-save compatibility and previous native wait-arrow53pixel difference remain open.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Guts intro4 static / normal Guts2 / NumberMan3: PASS');return result

if __name__=='__main__':main()
