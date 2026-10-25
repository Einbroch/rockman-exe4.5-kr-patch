"""SearchMan40 source integrity, renderer11 pages and native NumberMan3."""
import json,struct
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_numberman_return import pages
from capture_save_qa import inventory
from run_searchman_seasonal_diagnostic import STEM,PREFIX

def main():
    m,rom,e,s,checks=static(STEM,'675440')
    if (m['translated_units'],len(m['archives']),m['unchanged_archives'])!=(1547,32,700):raise ValueError('cumulative population')
    asset=read(ROOT/'translations/searchman_seasonal_ko.json');suffix=next(u for u in asset['units'] if u['id']=='675440:3:1')
    if suffix['source'].split('\n')[0]!='の' or suffix['translation'].split('\n')[0]!='、':raise ValueError('pinned invariant nickname suffix')
    old=ROOT/'poc/output/exe45_ko_development_windman_seasonal_v1.gba';om=read(old.with_suffix('.json'));before=old.read_bytes()
    if sha(before)!=om['output_sha256']:raise ValueError('previous identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if n['compiled_sha256']!=a['compiled_sha256'] or rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]!=before[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]:raise ValueError('retained31 payload drift')
    for a in om['translation_assets']:
        if not any(x['path']==a['path'] and x['sha256']==a['sha256'] for x in m['translation_assets']):raise ValueError('prior selected asset changed')
    graphics=[]
    pairs=[(k,m[k],om[k]) for k in ['calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics']]
    pairs.append(('equipment_title',m['folder_labels']['title'],om['folder_labels']['title']))
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
    lookup=rt/(PREFIX+'lookup');r=verify_route(lookup,m['output_sha256'],seen);parent=rt/(PREFIX+'normal-reload-select')/'result.json'
    if Path(r['state_origin']).resolve()!=parent.resolve():raise ValueError('lookup pre-load parent')
    pool=0x8000000+next(x for x in m['archives'] if x['archive']=='675440')['rom_offset'];groups={}
    for script,name,total in [(1,'diagnostic-new-year',3),(7,'diagnostic-weather',4),(8,'diagnostic-christmas-eve',4)]:
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen);d=read(p/'search_environment.json')
        if Path(r['state_origin']).resolve()!=parent.resolve():raise ValueError('diagnostic pre-load parent')
        if not d['passed'] or d['pool']!=pool or d['root_aliases']!=1 or d['entry_aliases']!=int(script!=1) or d['requested_script']!=1 or d['target_script']!=script or d['rom_sha256']!=m['output_sha256'] or d['tool_sha256']!=sha((ROOT/'tools/capture_searchman_seasonal_diagnostic.py').read_bytes()) or d['observer_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()) or d['lookup_sha256']!=sha((lookup/'final_seasonal_lookup.json').read_bytes()) or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('diagnostic identity/quarantine')
        groups[str(script)]=pages(p,script,1,m,rom,e,s,pool)
        if len(groups[str(script)])!=total:raise ValueError('diagnostic page population')
    _,_,ne,ns,nc=static(STEM,'68BBB4');np=0x8000000+next(x for x in m['archives'] if x['archive']=='68BBB4')['rom_offset'];regression=pages(rt/(PREFIX+'normal-return'),1,1,m,rom,ne,ns,np)
    if len(regression)!=3:raise ValueError('normal NumberMan3')
    out=ROOT/'analysis/searchman_seasonal_v1';out.mkdir(parents=True,exist_ok=True);diagnostic=[q for v in groups.values() for q in v];sheet=Image.new('RGB',(960,480))
    for row,qs in enumerate(groups.values()):
        for i,q in enumerate(qs):sheet.paste(Image.open(rt/q['route']/f"step_{q['step']:03}.png"),(240*i,160*row))
    sheet.save(out/'diagnostic_pages.png');summary=read(ROOT/'analysis/full_scope_searchman_v1/inventory.json')['summary']
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=40,new_translated_prose=38,source_identical_quotes=2,selected_text_units=1547,static=checks,retained31_archive_payloads_identical=True,prior_selected_asset_hashes_identical=True,nickname_suffix_source='の',nickname_suffix_target='、',diagnostic_searchman_pages=groups,normal_searchman_pages=[],normal_numberman_regression_pages=regression,native_save_sha256=saved['sha256'],native_save_success_script=58,cold_continue_has_no_loaded_checkpoint=True,remaining_catalog=summary['counts'],limits=['SearchMan11 pages renderer-only: root alias to SearchMan, scripts7/8 entry table alias; NumberMan caller/portrait remain. Not SearchMan normal unlock,portrait,date or likelihood calculation proof. Other27 prose incl gender/nickname60% consumer and event-name variable are static-only.','All40 literals mechanically checked, but culture/voice/WeatherSearch expression remain needs_review. No release claim.','Full requested translation incomplete; remaining catalog is not a complete-ROM translation denominator. Graphics/inline/fixed/name populations unresolved.','Hangul name editing/committed records/all redisplay/persistence/old-save compatibility and previous native wait-arrow53pixel difference remain open.'])
    result['retained_graphics_payloads']=graphics
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('SearchMan40 static / diagnostic11 / normal NumberMan3: PASS');return result

if __name__=='__main__':main()
