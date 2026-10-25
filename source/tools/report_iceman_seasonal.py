"""IceMan34 finite static scope, quarantined7 and normal NumberMan3 pages."""
import json,struct
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_numberman_return import pages
from capture_save_qa import inventory
from run_iceman_seasonal_diagnostic import STEM,PREFIX

def main():
    m,rom,e,s,checks=static(STEM,'6C5A88')
    if (m['translated_units'],len(m['archives']),m['unchanged_archives'])!=(2024,44,688):raise ValueError('cumulative population')
    asset=read(ROOT/'translations/iceman_seasonal_ko.json');units={u['id']:u for u in asset['units']}
    from build_development_patch import validate_nickname_suffix
    scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6C5A88'];validate_nickname_suffix(asset['units'],'6C5A88',scope)
    if (ROOT/'analysis/full_scope_v1/source_tpl/6C5A88.tpl').read_text(encoding='utf-8-sig').count('printPlayerNickname')!=2:raise ValueError('nickname consumer population')
    old=ROOT/'poc/output/exe45_ko_development_napalmman_seasonal_v1.gba';om=read(old.with_suffix('.json'));before=old.read_bytes()
    if sha(before)!=om['output_sha256']:raise ValueError('previous identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if n['compiled_sha256']!=a['compiled_sha256'] or rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]!=before[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]:raise ValueError('retained43 payload drift')
    for a in om['translation_assets']:
        if not any(x['path']==a['path'] and x['sha256']==a['sha256'] for x in m['translation_assets']):raise ValueError('prior selected asset changed')
    graphics=[];pairs=[(k,m[k],om[k]) for k in ['calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics']];pairs.append(('equipment_title',m['folder_labels']['title'],om['folder_labels']['title']))
    for name,n,a in pairs:
        offset=n['source_offset'];size=n.get('stored_bytes',n.get('bytes'));key='final_stored_sha256' if 'stored_bytes' in n else 'final_block_sha256'
        if (offset,size,n[key])!=(a['source_offset'],a.get('stored_bytes',a.get('bytes')),a[key]) or rom[offset:offset+size]!=before[offset:offset+size] or sha(rom[offset:offset+size])!=n[key]:raise ValueError('retained graphic payload drift')
        graphics.append(dict(scope=name,offset=offset,bytes=size,sha256=n[key],prior_identical=True))
    rt=ROOT/'poc/runtime';seen=set();chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','save-enter','save-commit','normal-reload-menu','normal-reload-navi','normal-reload-select','normal-return']
    verify_route(rt/'numberman-intro-v1-select-numberman-full',read(ROOT/'poc/output/exe45_ko_development_numberman_intro_v1.json')['output_sha256'],set())
    for i,name in enumerate(chain):
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen);expected=None if i in [0,8] else str(rt/(PREFIX+chain[i-1])/'result.json')
        if r['state_origin']!=expected or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('own normal ancestry')
        lua=(p/'segment.lua').read_text(encoding='utf8')
        if 'emu.write' in lua or 'setState' in lua or 'AliasReads' in lua:raise ValueError('normal intervention')
    commit=rt/(PREFIX+'save-commit');env=read(commit/'save_environment.json');sav=STEM+'.sav';saved=env['files_after'][sav]
    if (not env['observer_only'] or env['build_sha256']!=m['output_sha256'] or env['files_before'][sav]!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or saved['bytes']!=65536 or saved['sha256']==sha(bytes([255])*65536) or sha((commit/'persistent_files_after'/sav).read_bytes())!=saved['sha256'] or inventory(Path(env['save_directory']))[sav]!=saved):raise ValueError('native own save identity')
    for fn in set(env['files_before'])|set(env['files_after']):
        if fn not in (sav,STEM+'.rtc') and env['files_before'].get(fn)!=env['files_after'].get(fn):raise ValueError('unrelated save drift')
    ram=(commit/'step_013_gbaExtWorkRam.bin').read_bytes();savepool=0x8000000+next(x for x in m['archives'] if x['archive']=='6DA21C')['rom_offset']
    if ram[0xFA21]!=58 or struct.unpack_from('<I',ram,0xFA50)[0]!=savepool:raise ValueError('native save success58')
    lookup=rt/(PREFIX+'lookup');parent=rt/(PREFIX+'normal-reload-select')/'result.json'
    lr=verify_route(lookup,m['output_sha256'],seen)
    if Path(lr['state_origin']).resolve()!=parent.resolve():raise ValueError('own lookup parent')
    pool=0x8000000+next(x for x in m['archives'] if x['archive']=='6C5A88')['rom_offset'];diagnostic=[];groups={}
    for suffix,target in [('christmas-eve',8),('new-years-eve',10)]:
        p=rt/(PREFIX+'diagnostic-'+suffix);r=verify_route(p,m['output_sha256'],seen);d=read(p/'ice_environment.json')
        if Path(r['state_origin']).resolve()!=parent.resolve():raise ValueError('own pre-load parent')
        if not d['passed'] or d['pool']!=pool or d['root_aliases']!=1 or d['entry_aliases']!=int(target!=1) or d['requested_script']!=1 or d['target_script']!=target or d['rom_sha256']!=m['output_sha256'] or d['tool_sha256']!=sha((ROOT/'tools/capture_iceman_seasonal_diagnostic.py').read_bytes()) or d['observer_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()) or d['lookup_sha256']!=sha((lookup/'final_seasonal_lookup.json').read_bytes()) or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('diagnostic identity/quarantine')
        groups[suffix]=pages(p,target,1,m,rom,e,s,pool);diagnostic+=groups[suffix]
    if len(groups['christmas-eve'])!=3 or len(groups['new-years-eve'])!=4:raise ValueError('diagnostic groups')
    _,_,ne,ns,nc=static(STEM,'68BBB4');np=0x8000000+next(x for x in m['archives'] if x['archive']=='68BBB4')['rom_offset'];regression=pages(rt/(PREFIX+'normal-return'),1,1,m,rom,ne,ns,np)
    if len(diagnostic)!=7 or len(regression)!=3:raise ValueError('page population')
    out=ROOT/'analysis/iceman_seasonal_v1';out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,480))
    for i,q in enumerate(diagnostic):sheet.paste(Image.open(rt/q['route']/f"step_{q['step']:03}.png"),(240*(i%3),160*(i//3)))
    sheet.save(out/'diagnostic_seasonal_pages.png');summary=read(ROOT/'analysis/full_scope_iceman_v1/inventory.json')['summary']
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=34,new_translated_prose=32,source_identical_quotes=2,selected_text_units=2024,static=checks,retained43_archive_payloads_identical=True,prior_selected_asset_hashes_identical=True,retained_graphics_payloads=graphics,diagnostic_iceman_pages=diagnostic,diagnostic_groups=groups,normal_iceman_pages=[],normal_numberman_regression_pages=regression,native_save_sha256=saved['sha256'],native_save_success_script=58,cold_continue_has_no_loaded_checkpoint=True,remaining_catalog=summary['counts'],limits=['IceMan ChristmasEve3/NewYearsEve4 renderer-only: guarded root/conditional script-offset aliases, NumberMan caller/portrait remain. Not IceMan normal unlock,portrait,date proof. Other25 prose including gender and dynamic event consumer static-only.','All34 literals mechanically checked; culture/voice/terminology await human review. No release claim.','Full requested translation incomplete; catalog not a complete-ROM translation denominator. Graphics/inline/fixed/name populations unresolved.','Hangul name editing/committed records/all redisplay/persistence/old-save compatibility and previous native wait-arrow53pixel difference remain open.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('IceMan34 static / diagnostic7 / normal NumberMan3: PASS');return result

if __name__=='__main__':main()
