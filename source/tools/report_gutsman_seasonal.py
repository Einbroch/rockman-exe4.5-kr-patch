"""GutsMan49 integrity, normal seasonal2 and exact-ROM regression evidence."""
import json,struct
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_numberman_return import pages
from run_gutsman_seasonal import STEM,PREFIX
from capture_save_qa import inventory

def main():
    m,rom,e,s,checks=static(STEM,'66A234')
    if m['translated_units']!=1461 or len(m['archives'])!=30 or m['unchanged_archives']!=702:raise ValueError('cumulative population')
    old=ROOT/'poc/output/exe45_ko_development_seasonal_trio_v1.gba';om=read(old.with_suffix('.json'));before=old.read_bytes()
    if sha(before)!=om['output_sha256']:raise ValueError('old identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if n['compiled_sha256']!=a['compiled_sha256'] or rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]!=before[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]:raise ValueError('retained29 payload drift')
    for a in om['translation_assets']:
        if not any(x['path']==a['path'] and x['sha256']==a['sha256'] for x in m['translation_assets']):raise ValueError('prior asset changed')
    rt=ROOT/'poc/runtime';seen=set();chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','save-enter','save-commit','normal-reload-menu','normal-reload-navi','normal-reload-select','normal-return']
    verify_route(rt/'numberman-intro-v1-select-numberman-full',read(ROOT/'poc/output/exe45_ko_development_numberman_intro_v1.json')['output_sha256'],set())
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        expected=None if i in [0,8] else str(rt/(PREFIX+chain[i-1])/'result.json')
        if r['state_origin']!=expected:raise ValueError('own cold/native continue ancestry')
    commit=rt/(PREFIX+'save-commit');env=read(commit/'save_environment.json');sav=STEM+'.sav';saved=env['files_after'][sav]
    if (not env['observer_only'] or env['build_sha256']!=m['output_sha256']
            or env['files_before'][sav]!={'bytes':65536,'sha256':sha(bytes([255])*65536)}
            or saved['bytes']!=65536 or saved['sha256']==sha(bytes([255])*65536)
            or sha((commit/'persistent_files_after'/sav).read_bytes())!=saved['sha256']
            or inventory(Path(env['save_directory']))[sav]!=saved):raise ValueError('native own save identity')
    for fn in set(env['files_before'])|set(env['files_after']):
        if fn not in (sav,STEM+'.rtc') and env['files_before'].get(fn)!=env['files_after'].get(fn):raise ValueError('unrelated test save drift')
    ram=(commit/'step_013_gbaExtWorkRam.bin').read_bytes();savepool=0x8000000+next(x for x in m['archives'] if x['archive']=='6DA21C')['rom_offset']
    if ram[0xFA21]!=58 or struct.unpack_from('<I',ram,0xFA50)[0]!=savepool:raise ValueError('native save success58 not observed')
    for name,parent in [('select-gutsman','normal-reload-select'),('gutsman-advance','select-gutsman')]:
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen)
        if Path(r['state_origin']).resolve()!=(rt/(PREFIX+parent)/'result.json').resolve():raise ValueError('Guts normal parent')
        lua=(p/'segment.lua').read_text(encoding='utf8')
        if 'emu.write' in lua or 'setState' in lua or 'AliasReads' in lua or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('normal intervention')
    pool=0x8000000+next(x for x in m['archives'] if x['archive']=='66A234')['rom_offset']
    found=[];attempts=[]
    for name in ['select-gutsman','gutsman-advance']:
        try:found=pages(rt/(PREFIX+name),1,1,m,rom,e,s,pool)
        except ValueError as exc:
            # Only an unobserved target may route to the next genuine input
            # segment; geometry, clearing/font failures must not be bypassed.
            if not str(exc).startswith('unobserved complete page'):raise
            attempts.append(dict(route=name,observation=str(exc)));continue
        break
    if len(found)!=2:raise ValueError('normal GutsMan New Year2 not observed')
    _,_,ne,ns,nc=static(STEM,'68BBB4');np=0x8000000+next(x for x in m['archives'] if x['archive']=='68BBB4')['rom_offset']
    regression=pages(rt/(PREFIX+'normal-return'),1,1,m,rom,ne,ns,np)
    out=ROOT/'analysis/gutsman_seasonal_v1';out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,160))
    for i,q in enumerate(found):sheet.paste(Image.open(rt/q['route']/f"step_{q['step']:03}.png"),(240*i,0))
    sheet.save(out/'new_year_pages.png')
    summary=read(ROOT/'analysis/full_scope_gutsman_v1/inventory.json')['summary']
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=49,new_translated_prose=47,source_identical_quotes=2,selected_text_units=1461,static=checks,retained29_archive_payloads_identical=True,prior_selected_asset_hashes_identical=True,normal_new_year_pages=found,normal_numberman_regression_pages=regression,native_save_sha256=saved['sha256'],native_save_success_script=58,cold_continue_has_no_loaded_checkpoint=True,pre_target_attempts=attempts,remaining_catalog=summary['counts'],limits=['Normal GutsMan New Year2 observed; other45 new prose/anniversary variable consumer and other holiday/gender branches not executed here.','Full requested translation incomplete;28531 unselected Japanese-containing and1915 other unselected literals remain in732 catalog; graphics/inline/name populations outside catalog unresolved.','Cultural wording/voice needs review, no release claim.','Hangul names/editing/committed records/all redisplay/persistence/old-save compatibility and prior native wait-arrow53pixel difference remain open.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('GutsMan49 static / normal New Year2 / NumberMan3 regression: PASS');return result

if __name__=='__main__':main()
