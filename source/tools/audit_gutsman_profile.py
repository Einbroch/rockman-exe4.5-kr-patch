"""Immutable source, cumulative assets/bytes, exact ROM QA and final tool identity."""
import json,struct
from report_roll_pet import ROOT,read,sha,require_hash,static
from keyitem_rom_data import verify_final
from run_gutsman_profile import STEM,PREFIX

OLD='exe45_ko_development_gutsman_plugout_v1'
OUT=ROOT/'analysis/gutsman_profile_v1'

def main(stem=STEM,prefix=PREFIX,oldstem=OLD,outdir=OUT,questions=False,family=False,runtime_stem=None,answers=False,tools_manifest_stem=None,wishlist=False):
    STEM,PREFIX,OLD,OUT=stem,prefix,oldstem,ROOT/outdir
    questions=questions or family or answers or wishlist
    added,carried,retained_scripts=(3,150,96) if wishlist else (40,110,73) if answers else (29,81,89) if family else (41,40,87)
    m,rom,_,_,checks=static(STEM,'667044');old=read(ROOT/f'poc/output/{OLD}.json');prior=(ROOT/f'poc/output/{OLD}.gba').read_bytes();require_hash(ROOT/f'poc/output/{OLD}.gba',old['output_sha256'])
    source_path=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source_path,m['source_sha256']);source=source_path.read_bytes();reconstructed=bytearray(source);occupied=set()
    for w in m['expected_writes']:
        at=w['offset'];n=w['bytes'];value=bytes.fromhex(w['final_hex'])
        if len(value)!=n or source[at:at+n]!=bytes.fromhex(w['expected_hex']) or occupied.intersection(range(at,at+n)):raise ValueError('profile source ledger/overlap')
        occupied.update(range(at,at+n));reconstructed[at:at+n]=value
    if bytes(reconstructed)!=rom[:len(source)] or rom[:192]!=source[:192] or len(rom)!=len(source)+m['append_bytes'] or sha(rom[len(source):])!=m['append_sha256']:raise ValueError('profile header/ledger/append')
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    before={a['archive']:a for a in old['archives']};after={a['archive']:a for a in m['archives']}
    if set(after)!=(set(before) if questions else set(before)|{'667044'}):raise ValueError('unexpected profile archive scope')
    for name,a in before.items():
        b=after[name]
        if questions and name=='667044':
            from archive_scripts import script_spans
            oldsp=script_spans(prior[a['rom_offset']:a['rom_offset']+a['compiled_bytes']],97);newsp=script_spans(rom[b['rom_offset']:b['rom_offset']+b['compiled_bytes']],97)
            changed={31} if wishlist else set(range(40,64)) if answers else set(range(1,9)) if family else {9,11,13,15,17,19,21,23,25,88}
            if any(oldsp[i]!=newsp[i] for i in range(97) if i not in changed):raise ValueError('retained profile script bytes drift')
            continue
        if prior[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[b['rom_offset']:b['rom_offset']+b['compiled_bytes']]:raise ValueError('prior payload drift '+name)
    old_assets={a['path'].replace('\\','/'):a['sha256'] for a in old['translation_assets']};new_assets={a['path'].replace('\\','/'):a['sha256'] for a in m['translation_assets']}
    if questions:
        parent='translations/gutsman_profile_ko.json';child='translations/gutsman_profile_questions_ko.json'
        if family:parent,child=child,'translations/gutsman_profile_family_checked_ko.json'
        if answers:parent,child='translations/gutsman_profile_family_checked_ko.json','translations/gutsman_profile_answers_ko.json'
        if wishlist:parent,child='translations/gutsman_profile_answers_ko.json','translations/gutsman_profile_wishlist_ko.json'
        if set(new_assets)!=(set(old_assets)-{parent}|{child}) or any(new_assets[k]!=v for k,v in old_assets.items() if k!=parent) or m['translated_units']!=old['translated_units']+added:raise ValueError('question inherited inputs/denominator')
        indexed={u['id']:u for u in read(ROOT/child)['units']}
        if any(indexed.get(u['id'])!=u for u in read(ROOT/parent)['units']):raise ValueError('retained profile40 changed')
    elif set(new_assets)!=set(old_assets)|{'translations/gutsman_profile_ko.json'} or any(new_assets[k]!=v for k,v in old_assets.items()) or m['translated_units']!=old['translated_units']+40:raise ValueError('profile inherited inputs/denominator')
    font=m['extension']['normal_font_offset'];end=m['extension']['advance_offset'];oldfont=old['extension']['normal_font_offset'];oldend=old['extension']['advance_offset'];count=m['extension']['legacy_index_view']+m['extension']['hangul_syllables']+m['extension']['extra_glyph_count'];oldcount=old['extension']['legacy_index_view']+old['extension']['hangul_syllables']+old['extension']['extra_glyph_count']
    if rom[font:end]!=prior[oldfont:oldend] or count!=oldcount or rom[end:end+count*4]!=prior[oldend:oldend+count*4]:raise ValueError('profile font provider/advances changed')
    graphics=[]
    for key in ('calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics'):
        a,b=old[key],m[key];at=b['source_offset'];n=b.get('stored_bytes',b.get('bytes'))
        if a!=b or prior[at:at+n]!=rom[at:at+n]:raise ValueError('prior graphics drift '+key)
        graphics.append(key)
    verify_final(source,rom,m['keyitem_rom']);a,b=old['keyitem_rom'],m['keyitem_rom']
    if prior[a['rom_offset']:a['rom_offset']+a['rom_bytes']]!=rom[b['rom_offset']:b['rom_offset']+b['rom_bytes']]:raise ValueError('full39 keyitem clone drift')
    cpu=read(OUT/'cpu/report.json');runtime=read(OUT/('wishlist_runtime.json' if wishlist else 'answer_runtime.json' if answers else 'family_runtime.json' if family else 'question_runtime.json' if questions else 'profile_runtime.json'));plugout=read(OUT/'plugout_regression/plugout_runtime.json');pet=read(OUT/'pet_regression/runtime.json')
    if questions:
        runtime=dict(runtime,full_selected40_renderer_coverage=len(runtime['new_units_diagnostic_renderer_verified'])==added and runtime['all_diagnostics_stopped_before_input_init'],normal_runtime_units=runtime['new_units_normal_runtime_verified'],diagnostic_renderer_units=runtime['new_units_diagnostic_renderer_verified'])
    if not(cpu['passed'] and cpu['integrated_artifact_final_bytes_checked'] and cpu['baseline_rom_sha256']==m['output_sha256'] and runtime['passed'] and runtime['full_selected40_renderer_coverage'] and runtime['rom_sha256']==m['output_sha256'] and plugout['passed'] and plugout['rom_sha256']==m['output_sha256']):raise ValueError('exact profile CPU/runtime/regression identity')
    if not pet['passed'] or pet['rom_sha256']!=m['output_sha256'] or len(pet['runtime_observed_units'])!=22:raise ValueError('exact profile PET regression identity')
    runtime_stem=runtime_stem or STEM
    require_hash(ROOT/f'poc/output/{runtime_stem}.gba',m['output_sha256'])
    if (ROOT/f'poc/output/{runtime_stem}.gba').read_bytes()!=rom:raise ValueError('runtime transfer requires complete ROM byte identity')
    rt=ROOT/'poc/runtime';commit=rt/(PREFIX+'save-commit');env=read(commit/'save_environment.json');sav=runtime_stem+'.sav';saved=env['files_after'][sav]
    if not env['observer_only'] or env['build_sha256']!=m['output_sha256'] or env['files_before'][sav]!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or saved['bytes']!=65536 or saved['sha256']==sha(bytes([255])*65536) or sha((commit/'persistent_files_after'/sav).read_bytes())!=saved['sha256']:raise ValueError('profile fresh native save')
    state=(commit/'step_013_gbaExtWorkRam.bin').read_bytes();savepool=0x08000000+after['6DA21C']['rom_offset']
    if state[0xFA21]!=58 or struct.unpack_from('<I',state,0xFA50)[0]!=savepool:raise ValueError('native save success58')
    reload=read(rt/(PREFIX+'normal-reload-menu')/'result.json')
    if reload['state_origin'] is not None or reload['rom_sha256']!=m['output_sha256']:raise ValueError('cold continue imported checkpoint')
    tools={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in sorted((ROOT/'tools').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    tool_audit=None
    if tools_manifest_stem:
        tm=read(ROOT/f'poc/output/{tools_manifest_stem}.json');require_hash(ROOT/f'poc/output/{tools_manifest_stem}.gba',m['output_sha256'])
        if (ROOT/f'poc/output/{tools_manifest_stem}.gba').read_bytes()!=rom:raise ValueError('tool manifest requires complete ROM identity')
        actual={p.name:sha(p.read_bytes()) for p in sorted((ROOT/'tools').glob('*.py'))};pinned=tm['build_tools_sha256'];drift=sorted(k for k in set(actual)|set(pinned) if actual.get(k)!=pinned.get(k))
        if drift:raise ValueError('current build tool pins drift '+str(drift))
        tool_audit=dict(manifest_stem=tools_manifest_stem,python_tool_count=len(actual),tool_drift=drift,complete_rom_byte_identity=True)
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],source_sha256=sha(source),repro_sha256=sha((ROOT/f'poc/output/{STEM}_repro.gba').read_bytes()),selected_literal_units=m['translated_units'],added_literal_units=40,source_header_append_and_write_ledger_verified=True,unchanged_prior_archive_payloads=sorted(before),all_prior_input_hashes_unchanged=True,font_provider_and_advance_bytes_unchanged=True,unchanged_graphics=graphics,keyitem_full39_clone_unchanged=True,keyitem_final_machine_code_verified=True,profile_static=checks,native_save_sha256=saved['sha256'],native_save_success_script=58,cold_continue_without_imported_checkpoint=True,new_units_normal_runtime_verified=runtime['normal_runtime_units'],new_units_diagnostic_renderer_verified=runtime['diagnostic_renderer_units'],plugout_normal_regression_verified=True,tool_pins=tools,limits=runtime['limits']+['Other02031000 shop consumer normal execution remains unresolved. Whole catalog contains remaining Japanese.'])
    if questions:
        result.update(added_literal_units=added,unchanged_prior_archive_payloads=sorted(set(before)-{'667044'}),retained_profile_units=carried,unchanged_prior_profile_scripts=retained_scripts,all_prior_input_hashes_unchanged=False,all_other_prior_input_hashes_unchanged=True,profile_parent_asset_verified=True)
    result.update(runtime_baseline_stem=runtime_stem,runtime_transfer_by_complete_rom_byte_identity=runtime_stem!=STEM)
    if tool_audit:result['current_build_tool_audit']=tool_audit
    (OUT/'final_identity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({k:result[k] for k in ('passed','rom_sha256','selected_literal_units','added_literal_units')},indent=2))

if __name__=='__main__':main()
