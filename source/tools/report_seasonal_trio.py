"""Finite129-literal integrity and actual native New Year page evidence."""
import json,struct
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_numberman_return import pages
from capture_save_qa import inventory

STEM='exe45_ko_development_seasonal_trio_v1'
PREFIX='seasonal-trio-v1-'

def main():
    proof={};data={}
    for ar in ['65E438','6648D0','68BBB4']:
        m,rom,e,s,c=static(STEM,ar);proof[ar]=c;data[ar]=(e,s)
    if m['translated_units']!=1412 or len(m['archives'])!=29 or m['unchanged_archives']!=703:raise ValueError('cumulative population')
    old=ROOT/'poc/output/exe45_ko_development_numberman_return_v1.gba';om=read(old.with_suffix('.json'));previous=old.read_bytes()
    if sha(previous)!=om['output_sha256']:raise ValueError('old identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['compiled_sha256']!=n['compiled_sha256'] or previous[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('retained26 payload drift')
    for a in om['translation_assets']:
        if not any(n['path']==a['path'] and n['sha256']==a['sha256'] for n in m['translation_assets']):raise ValueError('retained selected asset drift')
    rt=ROOT/'poc/runtime';seen=set();chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','save-enter','save-commit','normal-reload-menu','normal-reload-navi','normal-reload-select','normal-return']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        expected=None if i in [0,8] else str(rt/(PREFIX+chain[i-1])/'result.json')
        if r['state_origin']!=expected or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('fresh native lineage')
        lua=(rt/(PREFIX+name)/'segment.lua').read_text(encoding='utf8')
        if 'emu.write' in lua or 'setState' in lua or 'AliasReads' in lua:raise ValueError('normal observer intervention')
    commit=rt/(PREFIX+'save-commit');env=read(commit/'save_environment.json');sav=STEM+'.sav';saved=env['files_after'][sav]
    if not env['observer_only'] or env['build_sha256']!=m['output_sha256'] or saved['bytes']!=65536 or saved['sha256']==sha(bytes([255])*65536):raise ValueError('native commit')
    if sha((commit/'persistent_files_after'/sav).read_bytes())!=saved['sha256'] or inventory(Path(env['save_directory']))[sav]!=saved:raise ValueError('current isolated persisted save identity')
    for fn in set(env['files_before'])|set(env['files_after']):
        if fn not in (sav,STEM+'.rtc') and env['files_before'].get(fn)!=env['files_after'].get(fn):raise ValueError('unrelated saves changed')
    ar='68BBB4';p=rt/(PREFIX+'normal-return');e,s=data[ar];pool=0x8000000+next(x for x in m['archives'] if x['archive']==ar)['rom_offset']
    normal=pages(p,1,1,m,rom,e,s,pool)
    for ar,name in [('65E438','rockman-select'),('6648D0','roll-new-year')]:
        q=rt/(PREFIX+name);rr=verify_route(q,m['output_sha256'],seen)
        parent='normal-reload-select' if ar=='65E438' else 'roll-save-enter'
        if Path(rr['state_origin']).resolve()!=(rt/(PREFIX+parent)/'result.json').resolve():raise ValueError('companion normal parent')
        lua=(q/'segment.lua').read_text(encoding='utf8')
        if 'emu.write' in lua or 'setState' in lua or 'AliasReads' in lua:raise ValueError('companion normal intervention')
        e,s=data[ar];pool=0x8000000+next(x for x in m['archives'] if x['archive']==ar)['rom_offset']
        normal.extend(pages(q,1,1,m,rom,e,s,pool))
    if len(normal)!=9:raise ValueError('all nine New Year pages')
    # The Roll route was initially labelled a save attempt but actually
    # reached the holiday greeting; its disk save did not change.
    re=read(rt/(PREFIX+'roll-save-commit')/'save_environment.json')
    if not re['observer_only'] or re['files_before'][sav]!=saved or re['files_after'][sav]!=saved:raise ValueError('Roll save attempt identity')
    rr=verify_route(rt/(PREFIX+'roll-save-commit'),m['output_sha256'],seen)
    roll_ram=(rt/(PREFIX+'roll-save-commit')/'step_013_gbaExtWorkRam.bin').read_bytes()
    roll_pool=0x8000000+next(x for x in m['archives'] if x['archive']=='6648D0')['rom_offset']
    if struct.unpack_from('<I',roll_ram,0xFA50)[0]!=roll_pool or roll_ram[0xFA21]!=1:raise ValueError('Roll attempt was seasonal greeting, not save success')
    out=ROOT/'analysis/seasonal_trio_v1';out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(720,480))
    for i,q in enumerate(normal):sheet.paste(Image.open(rt/q['route']/f"step_{q['step']:03}.png"),(240*(i%3),160*(i//3)))
    sheet.save(out/'new_year_pages.png')
    summary=read(ROOT/'analysis/full_scope_trio_v1/inventory.json')['summary']
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=129,new_translated_prose=123,source_identical_quote_units=6,selected_text_units=1412,static=proof,retained26_archive_payloads_identical=True,prior_selected_assets_hashes_identical=True,normal_new_year_pages=normal,native_save_sha256=saved['sha256'],cold_continue_has_no_loaded_checkpoint=True,roll_save_attempt=dict(native_save_success=False,observed='Normal input reached Roll seasonal script1, unchanged disk save; not Roll committed-save/persistence proof.'),remaining_catalog=summary['counts'],limits=['Full requested translation incomplete:28578 unselected Japanese-containing literals plus1917 other unselected literals require context/translation or evidenced protection. Not a completed percentage.','New Year9 pages (NumberMan3/Rockman4/Roll2) proved normal runtime; other seasonal branches and event-name buffers remain static-only.','Cultural/wordplay wording needs human review; separate approved4649 decision does not approve these drafts.','Graphics population outside732 catalog, prior arrow53pixel discrepancy, Hangul name editing/committed records/redisplay/persistence/old-save support remain open.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('seasonal trio static129 / native New Year9: PASS');return result

if __name__=='__main__':main()
