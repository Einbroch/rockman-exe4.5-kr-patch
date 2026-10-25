"""Whole catalog ledger + exact-ID reuse candidates; never builds a ROM.

Authored text remains in selected draft assets; the ledger is read-only derived.
Existing alternatives only aid human/model reading, never auto-select prose.
"""
import json,re
from collections import Counter,defaultdict
from pathlib import Path
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals,skeleton,serialize
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from korean_codec import encode_character,decode_character

PLAN='translations/full_translation_first_plan.json'

def read(p):return json.loads(p.read_text(encoding='utf8'))

def check_draft(asset,baseline,available,source_rom,rows):
    if asset.get('policy')!='development-draft; NON-DISTRIBUTION' or asset['review']['release_eligible'] is not False:raise ValueError('draft review/policy')
    if asset['source_sha256']!=sha(source_rom):raise ValueError('draft source revision')
    name=asset['archive'];row=rows[name]
    if asset['source_archive_sha256']!=sha(payload_of(source_rom,row)):raise ValueError('draft source payload')
    p=ROOT/asset['source_tpl']['path'];require_hash(p,asset['source_tpl']['sha256']);original=p.read_text(encoding='utf-8-sig')
    lookup={x.key:x for x in literals(original)};seen=set();target=original;details=[]
    for u in sorted(asset['units'],key=lambda u:lookup[u['id']].start,reverse=True):
        key=u['id'];text=u['translation'];x=lookup[key]
        if key in seen or key not in baseline or baseline[key]['status']!='unselected_japanese' or u['source']!=baseline[key]['source'] or u['source']!=x.text:raise ValueError('draft immutable ID/source/selection')
        seen.add(key)
        if u['state']!='needs_review' or not text or re.search(r'[\u3040-\u30ff\u3400-\u9fff]',text):raise ValueError('draft state/untranslated')
        if re.findall(r'-?\d+|\[[^\]]+\]',text)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('draft numbers/tokens')
        if re.findall(r'\d+[~〜～]\d+',text)!=re.findall(r'\d+[~〜～]\d+',x.text):raise ValueError('draft numeric ranges')
        if text.count('\n')!=x.text.count('\n') or text.endswith('\n')!=x.text.endswith('\n'):raise ValueError('draft line topology')
        for c in text:
            if '\uac00'<=c<='\ud7a3' and (ord(c) not in available or decode_character(encode_character(c))[0]!=c):raise ValueError('missing glyph/codec')
        target=target[:x.start]+serialize(text)+target[x.end:]
        widths=[sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line) for line in text.split('\n')]
        details.append(dict(id=key,proposed_advance_px=widths,needs_geometry_reassessment=max(widths,default=0)>132))
    if skeleton(original)!=skeleton(target):raise ValueError('draft command topology')
    before={x.key:x for x in literals(original)};after={x.key:x for x in literals(target)}
    if any(after[k].text!=x.text or after[k].language!=x.language for k,x in before.items() if k not in seen):raise ValueError('unselected source changed')
    return details

def main():
    plan=read(ROOT/PLAN);ref=plan['source_inventory'];require_hash(ROOT/ref['path'],ref['sha256'])
    bp=ROOT/plan['baseline_rom']['path'];require_hash(bp,plan['baseline_rom']['sha256'])
    data=read(ROOT/ref['path']);units=data['units'];base={u['id']:u for u in units}
    if len(base)!=len(units):raise ValueError('ledger population')
    if len(units)!=ref['units'] or data['baseline_rom_sha256']!=plan['baseline_rom']['sha256']:raise ValueError('ledger baseline')
    counts=Counter(u['status'] for u in units)
    if counts['unselected_japanese']!=ref['unselected_japanese'] or counts['unselected_non_japanese_review']!=ref['other_review']:raise ValueError('remaining denominator')
    cfg=read(ROOT/'project.json');src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);rom=src.read_bytes()
    cat=ROOT/cfg['text_catalog']['path'];require_hash(cat,cfg['text_catalog']['sha256']);rows={f"{r['offset']:X}":r for r in parse_tpi(cat)}
    if len(rows)!=ref['catalog_archives']:raise ValueError('catalog732')
    font=cfg['development_dependencies']['font'];require_hash(ROOT/font['path'],font['sha256'])
    available={int(line.split()[1]) for line in (ROOT/font['path']).read_text(encoding='utf8').splitlines() if line.startswith('ENCODING ')}
    drafts={};draft_hashes={};geometry=[]
    for name in plan['draft_assets']:
        path=ROOT/name;a=read(path);draft_hashes[name]=sha(path.read_bytes());geometry+=check_draft(a,base,available,rom,rows)
        for u in a['units']:
            if u['id'] in drafts:raise ValueError('conflicting authored draft units')
            drafts[u['id']]=dict(u,authority=name)
    candidates=defaultdict(list);stale=[];candidate_hashes={}
    for path in sorted((ROOT/'translations').glob('*.json')):
        a=read(path)
        for u in a.get('units',[]) if isinstance(a,dict) else []:
            if not isinstance(u,dict) or not all(k in u for k in ('id','source','translation')) or u['id'] not in base:continue
            if not isinstance(u['translation'],str) or not u['translation']:continue
            name=str(path.relative_to(ROOT)).replace('\\','/')
            candidate_hashes[name]=sha(path.read_bytes())
            if u['source']!=base[u['id']]['source']:
                stale.append(dict(id=u['id'],asset=name,reason='source mismatch; never reuse'));continue
            candidates[u['id']].append(dict(asset=name,translation=u['translation'],state=u.get('state','unknown'),automatic_selection=False))
    ledger=[];per_archive=defaultdict(Counter)
    for u in units:
        key=u['id'];existing=u['status']=='selected_in_current_rom';draft=drafts.get(key)
        stage='existing_rom_draft' if existing else 'authored_draft_not_in_rom' if draft else 'awaiting_context_and_translation' if u['status']=='unselected_japanese' else 'non_japanese_review_not_excluded'
        entry=dict(u,draft_stage=stage,authored_translation=draft['translation'] if draft else None,draft_authority=draft['authority'] if draft else None,reuse_candidates=candidates.get(key,[]),consumer_constraints='Source preservation established; actual consumer/layout remains as recorded in per-archive evidence. Draft-first is not insertion readiness.')
        ledger.append(entry);per_archive[u['archive']][stage]+=1
    drafted=len(drafts);remaining=counts['unselected_japanese']-drafted
    result=dict(passed=True,workflow=plan['workflow'],baseline_rom_sha256=plan['baseline_rom']['sha256'],source_sha256=cfg['source_profile']['sha256'],plan_sha256=sha((ROOT/PLAN).read_bytes()),source_inventory_sha256=ref['sha256'],catalog_archives=len(rows),catalog_literals=len(units),existing_rom_selected=counts['selected_in_current_rom'],rom_unselected_japanese=counts['unselected_japanese'],new_authored_drafts=drafted,japanese_still_without_selected_draft=remaining,other_review_not_excluded=counts['unselected_non_japanese_review'],draft_complete=False,rom_integration_started=False,release_eligible=False,font_sha256=font['sha256'],draft_asset_hashes=draft_hashes,reuse_candidate_asset_hashes=candidate_hashes,source_mismatch_candidates=stale,conflicting_reuse_candidate_ids=[k for k,v in candidates.items() if len({c['translation'] for c in v})>1],geometry_review_flags=[d for d in geometry if d['needs_geometry_reassessment']],per_archive={k:dict(v) for k,v in per_archive.items()},tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('prepare_translation_first.py','draft_remaining_navi_save.py')},limits=plan['limits'])
    result['tools'].update({n:sha((ROOT/'tools'/n).read_bytes()) for n in ('draft_tournament_dialogue.py','draft_protoman_missions.py','draft_story_mail.py','draft_starman_fortune.py','draft_gold_bbs.py','test_translation_first.py')})
    result['tools'].update({n:sha((ROOT/'tools'/n).read_bytes()) for n in ('draft_battle_bbs.py','draft_plaza_npcs.py')})
    result['tools'].update({n:sha((ROOT/'tools'/n).read_bytes()) for n in ('draft_mystery_data.py','draft_official_prelim.py')})
    result['tools'].update({n:sha((ROOT/'tools'/n).read_bytes()) for n in ('draft_blackworks_routes.py',)})
    result['tools'].update({n:sha((ROOT/'tools'/n).read_bytes()) for n in ('draft_official_entry.py',)})
    result['tools'].update({n:sha((ROOT/'tools'/n).read_bytes()) for n in ('draft_undernet_routes.py',)})
    result['tools'].update({n:sha((ROOT/'tools'/n).read_bytes()) for n in ('draft_hard_access_tests.py','draft_profile_editor.py','draft_everyday_venue.py','draft_appliance_routes.py','draft_golf_routes.py','draft_car_garden_routes.py','draft_background_venue.py','draft_factory_heel_routes.py','draft_napalm_media_market.py','draft_homepage_organ_routes.py','draft_fallen_dark_routes.py','draft_windman_field_routes.py','draft_navi_rewards_strengthening.py','draft_virus_practice_routes.py','draft_shademan_coffin.py','draft_shademan_victory.py','draft_laserman_encounter.py','draft_laserman_aftermath.py','draft_bass_encounter.py','draft_bass_victory.py','draft_profile_data_manager.py','draft_credits.py','draft_minigame_results.py','draft_schedule_reminders.py','draft_mail_alerts.py','draft_quick_box_routes.py','draft_progress_roll_menu.py','draft_remaining_roll_profile.py','draft_quick_results_guts_reminders.py','draft_windman_menu_remaining.py','draft_quick_wind_routes.py','draft_batch500_001.py','draft_batch500_002.py','draft_batch500_003.py','draft_batch500_004.py','draft_batch500_005.py','draft_batch500_006.py','draft_batch500_007.py','draft_batch500_008.py','draft_batch500_009.py','draft_batch500_010.py','draft_batch500_011.py','draft_batch500_012.py','draft_batch500_013.py','draft_batch500_014.py','draft_batch500_015.py','draft_batch500_016.py','draft_batch500_017.py','draft_batch500_018.py','draft_batch500_019.py','draft_batch500_020.py','draft_batch500_021.py','draft_batch500_022.py','draft_batch500_023.py','draft_batch500_024.py','draft_batch500_025.py','draft_batch500_026.py','draft_batch500_027.py','draft_batch500_028.py','draft_batch500_029.py','draft_batch500_030.py','draft_batch500_031.py','draft_batch500_032.py','draft_batch500_033.py','draft_batch500_034.py','draft_batch500_035.py','draft_batch500_036.py','draft_batch500_037.py','draft_batch500_038.py','draft_batch500_039.py','draft_batch500_040.py','draft_batch500_041.py','draft_batch500_042.py','draft_batch500_043.py','draft_batch500_044.py','draft_batch500_045.py','draft_batch500_046.py','draft_final_047.py')})
    out=ROOT/'analysis/translation_first_v1';out.mkdir(exist_ok=True)
    (out/'worklist.json').write_text(json.dumps(dict(summary=result,units=ledger),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (out/'coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    require_hash(bp,plan['baseline_rom']['sha256']);require_hash(src,cfg['source_profile']['sha256'])
    print(json.dumps({k:result[k] for k in ('passed','catalog_literals','existing_rom_selected','rom_unselected_japanese','new_authored_drafts','japanese_still_without_selected_draft','draft_complete','rom_integration_started')},ensure_ascii=False))

if __name__=='__main__':main()
