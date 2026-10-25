"""Freeze source-only calendar51/52 Korean candidates, not an applied500."""
import re
from collections import Counter
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from survey_calendar_layout500_031_v2 import place
from survey_pet_quick_reflow_024 import replace_for_analysis
from survey_batch500_017_layout import protected_edges
from calendar_date_delete_capacity_032 import validate
from calendar_menu_capacity_032 import validate as menu_validate,VERTICAL,HORIZONTAL,SIMPLE

OUT='analysis/pending_insertion_500_032_calendar_selection_v1/selection.json'
INVENTORY='analysis/pending_insertion_500_032_calendar_inventory_v1/census.json'


def main():
    census=read(INVENTORY);require_hash(ROOT/census['baseline_rom'],census['baseline_sha256'])
    for p,h in census['dependencies'].items():require_hash(ROOT/p,h)
    groups=[];bad=[]
    for g in census['groups']:
        if g['script'] not in VERTICAL|HORIZONTAL|SIMPLE|{0,10,51,52}:continue
        if g['already_applied_ids'] or g['missing_or_conflicting']:raise ValueError('032 source-only date whole-script/wording')
        units=[];layouts={};ref=None
        for link in g['drafts']:
            require_hash(ROOT/link['path'],link['sha256']);asset=read(link['path']);u=deepcopy(next(x for x in asset['units'] if x['id']==link['id']))
            if u['state']!='needs_review' or u['source']!=link['source'] or u['translation']!=link['translation']:raise ValueError('032 date canonical identity')
            if ref is not None and ref!=asset['source_tpl']:raise ValueError('032 date source representation agreement')
            ref=asset['source_tpl'];value=place(u['translation'],(180,180,168))
            if value is None or not protected_edges(u['source'],value):break
            if value!=u['translation']:layouts[u['id']]=value
            u['translation']=value;units.append(u)
        if len(units)!=len(g['ids']):bad.append(dict(archive=g['archive'],script=g['script'],reason='No canonical within-page placement'));continue
        require_hash(ROOT/ref['path'],ref['sha256']);original=(ROOT/ref['path']).read_text(encoding='utf-8-sig');section=re.search(r'^script '+str(g['script'])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',original,re.M)[0];one='@archive '+g['archive']+'\n'+section;target=replace_for_analysis(one,units)
        try:geometry=(validate if g['script'] in (51,52) else menu_validate)(one,target,[g['script']],set(g['ids']))
        except ValueError as ex:bad.append(dict(archive=g['archive'],script=g['script'],reason=str(ex)));continue
        groups.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],units=len(units),profile='calendar-date-delete' if g['script'] in (51,52) else 'calendar-menu',drafts=[{k:r[k] for k in ('id','path','sha256')} for r in g['drafts']],source_tpl=ref,source_row=g['source_row'],source_archive_sha256=g['source_payload_sha256'],explicit_layouts=layouts,geometry=geometry,storage='raw-known-pointer',product_admitted=False))
    candidates=groups[:];dates=[g for g in candidates if g['profile']=='calendar-date-delete'];states={sum(g['units'] for g in dates):dates}
    for g in candidates:
        if g['profile']=='calendar-date-delete':continue
        for n,prior in list(states.items()):
            total=n+g['units']
            if total<=500 and total not in states:states[total]=prior+[g]
    selected=states.get(500);groups=selected if selected is not None else candidates
    ids=[i for g in groups for i in g['ids']]
    if len(ids)!=len(set(ids)):raise ValueError('032 duplicate dates')
    deps=[INVENTORY,'tools/prepare_calendar_candidates_032.py','tools/calendar_date_delete_capacity_032.py','tools/calendar_menu_capacity_032.py','tools/survey_calendar_layout500_031_v2.py','analysis/pending_insertion_500_032_date_cpu_v1/cpu.json','analysis/pending_insertion_500_032_anniversary_runtime_v1/verification.json']
    for p in deps[-2:]:
        r=read(p)
        if not r['passed'] or r['baseline_sha256']!=census['baseline_sha256']:raise ValueError('032 date native evidence applicability')
    frozen_write(ROOT/OUT,dict(schema=1,status='SOURCE_ONLY_CALENDAR_SELECTION_NOT_ROM_ADMISSION',source_sha256=census['source_sha256'],baseline_rom=census['baseline_rom'],baseline_sha256=census['baseline_sha256'],candidate_units=sum(g['units'] for g in candidates),candidate_groups=candidates,exact500=selected is not None,max_reachable=max(states),planned_new_units=len(ids),selected_ids=sorted(ids),groups=groups,profiles=dict(Counter({str(s):sum(g['units'] for g in groups if g['script']==s) for s in (51,52)})),rejections=bad,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},native_nickname_bound=99,rom_written=False,insertion_ready=False,release_eligible=False,limits='Conditional date/title/choice geometry only. Exact source commands and canonical wording with LF-only placement. Not a complete500, cumulative carry, semantic approval or finalKorean032runtime. Native51 max10 title gameplay only,52 remains conditional.'))
    print('032 calendar candidate units',sum(g['units'] for g in candidates),'exact500',selected is not None,'selected',len(ids),'scripts',len(groups),'max',max(states),'rejections',bad)


if __name__=='__main__':main()
