"""Bound frozen pixel/clear/regression checks to cumulative758-unit build."""
from pathlib import Path
import report_megaman_escape_runtime as previous

def prepare():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    changes={
        'from korean_codec import encode_character':'from korean_codec import encode_character,EXTRA_CHARACTER_METRICS',
        "if '\\uac00'<=c<='\\ud7a3'":"if '\\uac00'<=c<='\\ud7a3' or c in EXTRA_CHARACTER_METRICS",
        "glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],wanted)":"glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],wanted,{c:v['vertical_shift'] for c,v in EXTRA_CHARACTER_METRICS.items() if c in wanted})",
        "index=ord(c)-0xAC00+bias if c in wanted else data[0]":"index=(EXTRA_CHARACTER_METRICS[c]['index'] if c in EXTRA_CHARACTER_METRICS else ord(c)-0xAC00)+bias if c in wanted else data[0]",
        'from prepare_megaman_escape import prepare as prepare_asset':'from prepare_roll_tactics import prepare as prepare_asset',
        'from archive_scripts import script_spans,verify_untouched_scripts':'from archive_scripts import script_spans,verify_untouched_scripts\nfrom verify_roll_tactics_dialogue_clear import verify_background_mask',
        "require(mask==background_mask,'closed dialogue background mask differs from pre-dialogue scene')":"clear_mask=verify_background_mask(p,step,mask,background_mask)",
        "'background_mask_matches_pre_dialogue_scene':True":"'background_mask_matches_pre_dialogue_scene':clear_mask['full_mask_match'],'native_obj_animation_delta':clear_mask",
        "STEM='exe45_ko_development_megaman_escape_v1'":"STEM='exe45_ko_development_roll_tactics_v1'",
        "PREFIX='poc/runtime/megaman-escape-v1-'":"PREFIX='poc/runtime/roll-tactics-v1-'",
        '==750':'==758',"'translated_units':750":"'translated_units':758",'cumulative750 scope':'cumulative758 scope',
        'translations/megaman_tactics_escape_ko.json':'translations/rockman_roll_tactics_escape_ko.json',
        "ar['translated_units']==8":"ar['translated_units']==16",'set(range(6))':'set(range(12))',
        '==138':'==132',"'preserved_other_navi_scripts':138":"'preserved_other_navi_scripts':132",
        "('failure-sample',4,[2,3],True)]":"('failure-sample',4,[2,3],True),('roll-confirm-sample',8,[2,3,4,5,6],True),('roll-success-sample',9,[2,3],True),('roll-failure-sample',10,[2,3],True),('roll-forbidden-sample',11,[2,3],True)]",
        "require_hash(ROOT/'tools/capture_megaman_escape_samples.py',a['tool_sha256'])":"require_hash(ROOT/('tools/capture_roll_escape_samples.py' if script>=8 else 'tools/capture_megaman_escape_samples.py'),a['tool_sha256']);require_hash(ROOT/'tools/capture_megaman_escape_samples.py',a['sampler_source_sha256']) if script>=8 else None",
        'if script==2 else':'if script in (2,8) else',
        'analysis/exe45_escape_tactics_':'analysis/exe45_roll_tactics758_',
        "('forbidden-clear',[2,3])]":"('forbidden-clear',[2,3]),('roll-confirm-sample',[7,8]),('roll-success-sample',[4,5]),('roll-failure-sample',[4,5]),('roll-forbidden-sample',[4,5])]",
        'PASS bounded750-unit development escape display and folder regression':'PASS bounded758-unit development Rockman/Roll escape display and folder regression',
        "'new_escape_literals':6":"'new_roll_tactics_literals':2",
        'Other Navi prompts/escape dialogue and most dialogue/UI/graphics remain untranslated.':'Roll8..11 are diagnostic lookup samples only, not actual Roll selection or escape outcomes. Roll mono6/7 also use diagnostic lookup aliases; other Navi dialogue, most UI/graphics remain untranslated.'
    }
    for old,new in changes.items():
        if code.count(old)!=1:raise ValueError('runtime binding drift:'+old+' count='+str(code.count(old)))
        code=code.replace(old,new)
    if code.count('units[2:]')!=2:raise ValueError('normal dialogue literal slice drift')
    code=code.replace('units[2:]','units[2:14]')
    ns={'__name__':'roll_tactics758_report_bound'}
    exec(compile(code,previous.__file__+' [exact758/normal and Roll diagnostics]','exec'),ns)
    result=ns['prepare']()
    result['verifier_source_sha256']=previous.sha(Path(previous.__file__).read_bytes())
    result['verifier_binding_sha256']=previous.sha(Path(__file__).read_bytes())
    result['clear_verifier_sha256']=previous.sha((previous.ROOT/'tools/verify_roll_tactics_dialogue_clear.py').read_bytes())
    from report_fixedcell_runtime import verify_route
    from report_chip_library_runtime import read,require
    from tpl_literals import resolve_units
    p=previous.ROOT/'poc/runtime/roll-tactics-v1-roll-tactics-sample'
    route=verify_route(p,result['rom_sha256'],set());env=read(p/'roll_prompt_alias_environment.json')
    require(route['normal_play_checkpoint_eligible'] is False and env['passed'] and env['rom_sha256']==result['rom_sha256'],'Roll prompt diagnostic binding')
    previous.require_hash(previous.ROOT/'tools/capture_roll_tactics_samples.py',env['tool_sha256'])
    previous.require_hash(previous.ROOT/'tools/capture_tactics_prompts.py',env['observer_sha256'])
    saves=read(p/'probe_environment.json');stem='exe45_ko_development_roll_tactics_v1'
    require(all(saves['files_after'].get(k)==v for k,v in saves['files_before'].items() if k not in (stem+'.sav',stem+'.rtc')),'Roll prompt diagnostic foreign save drift')
    require([(c['native_script'],c['displayed_script']) for c in env['calls']]==[(1,7),(0,6)],'native question/diagnostic aliases')
    reports={}
    for label,script in [('target',6),('distance',7)]:
        path=previous.ROOT/f'analysis/exe45_roll_tactics758_sample_{label}_v1.json';r=read(path)
        require(r['rom_sha256']==result['rom_sha256'] and r['status'].startswith('PASS') and len(r['screens'])==2 and all(s['script']==script and s['pixels_verified'] for s in r['screens']),'Roll prompt pixels/denominator')
        require(r['result_sha256']==previous.sha((p/'result.json').read_bytes()),'Roll prompt receipt')
        reports[label]={'path':str(path.relative_to(previous.ROOT)),'sha256':previous.sha(path.read_bytes()),'screens':r['screens']}
    asset=read(previous.ROOT/'translations/rockman_roll_tactics_escape_ko.json')
    result['roll_prompt_diagnostic']={'receipt_sha256':previous.sha((p/'result.json').read_bytes()),'scope':env['scope'],'aliases':env['calls'],'reports':reports,'other_save_files_preserved':True,
        'wording_links':[u for u in asset['units'] if int(u['id'].split(':')[1]) in (0,1,6,7)]}
    return result

if __name__=='__main__':
    import json
    print(json.dumps(prepare(),ensure_ascii=False,indent=2))
