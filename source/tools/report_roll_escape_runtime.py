"""Bound frozen pixel/clear/regression checks to cumulative756-unit build."""
from pathlib import Path
import report_megaman_escape_runtime as previous

def prepare():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    changes={
        'from korean_codec import encode_character':'from korean_codec import encode_character,EXTRA_CHARACTER_METRICS',
        "if '\\uac00'<=c<='\\ud7a3'":"if '\\uac00'<=c<='\\ud7a3' or c in EXTRA_CHARACTER_METRICS",
        "glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],wanted)":"glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],wanted,{c:v['vertical_shift'] for c,v in EXTRA_CHARACTER_METRICS.items() if c in wanted})",
        "index=ord(c)-0xAC00+bias if c in wanted else data[0]":"index=(EXTRA_CHARACTER_METRICS[c]['index'] if c in EXTRA_CHARACTER_METRICS else ord(c)-0xAC00)+bias if c in wanted else data[0]",
        'from prepare_megaman_escape import prepare as prepare_asset':'from prepare_roll_escape import prepare as prepare_asset',
        'from archive_scripts import script_spans,verify_untouched_scripts':'from archive_scripts import script_spans,verify_untouched_scripts\nfrom verify_roll_dialogue_clear import verify_background_mask',
        "require(mask==background_mask,'closed dialogue background mask differs from pre-dialogue scene')":"clear_mask=verify_background_mask(p,step,mask,background_mask)",
        "'background_mask_matches_pre_dialogue_scene':True":"'background_mask_matches_pre_dialogue_scene':clear_mask['full_mask_match'],'native_obj_animation_delta':clear_mask",
        "STEM='exe45_ko_development_megaman_escape_v1'":"STEM='exe45_ko_development_roll_escape_v1'",
        "PREFIX='poc/runtime/megaman-escape-v1-'":"PREFIX='poc/runtime/roll-escape-v1-'",
        '==750':'==756',"'translated_units':750":"'translated_units':756",'cumulative750 scope':'cumulative756 scope',
        'translations/megaman_tactics_escape_ko.json':'translations/rockman_roll_escape_ko.json',
        "ar['translated_units']==8":"ar['translated_units']==14",'set(range(6))':'{0,1,2,3,4,5,8,9,10,11}',
        '==138':'==134',"'preserved_other_navi_scripts':138":"'preserved_other_navi_scripts':134",
        "('failure-sample',4,[2,3],True)]":"('failure-sample',4,[2,3],True),('roll-confirm-sample',8,[2,3,4,5,6],True),('roll-success-sample',9,[2,3],True),('roll-failure-sample',10,[2,3],True),('roll-forbidden-sample',11,[2,3],True)]",
        "require_hash(ROOT/'tools/capture_megaman_escape_samples.py',a['tool_sha256'])":"require_hash(ROOT/('tools/capture_roll_escape_samples.py' if script>=8 else 'tools/capture_megaman_escape_samples.py'),a['tool_sha256']);require_hash(ROOT/'tools/capture_megaman_escape_samples.py',a['sampler_source_sha256']) if script>=8 else None",
        'if script==2 else':'if script in (2,8) else',
        'analysis/exe45_escape_tactics_':'analysis/exe45_roll_tactics_',
        "('forbidden-clear',[2,3])]":"('forbidden-clear',[2,3]),('roll-confirm-sample',[7,8]),('roll-success-sample',[4,5]),('roll-failure-sample',[4,5]),('roll-forbidden-sample',[4,5])]",
        'PASS bounded750-unit development escape display and folder regression':'PASS bounded756-unit development Rockman/Roll escape display and folder regression',
        "'new_escape_literals':6":"'new_roll_escape_literals':6",
        'Other Navi prompts/escape dialogue and most dialogue/UI/graphics remain untranslated.':'Roll8..11 are diagnostic lookup samples only, not actual Roll selection or escape outcomes. Roll mono6/7 and other Navi dialogue, most UI/graphics remain untranslated.'
    }
    for old,new in changes.items():
        if code.count(old)!=1:raise ValueError('runtime binding drift:'+old+' count='+str(code.count(old)))
        code=code.replace(old,new)
    ns={'__name__':'roll_escape_report_bound'}
    exec(compile(code,previous.__file__+' [exact756/4 Roll diagnostics]','exec'),ns)
    result=ns['prepare']()
    result['verifier_source_sha256']=previous.sha(Path(previous.__file__).read_bytes())
    result['verifier_binding_sha256']=previous.sha(Path(__file__).read_bytes())
    result['clear_verifier_sha256']=previous.sha((previous.ROOT/'tools/verify_roll_dialogue_clear.py').read_bytes())
    return result

if __name__=='__main__':
    import json
    print(json.dumps(prepare(),ensure_ascii=False,indent=2))
