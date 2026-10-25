"""Remaining RAW scripts with exact prior wording locked; analysis only.

No script-splitting or established consumer validator is weakened. The new
cohort must additionally prove compiled parent-script identity before use.
"""
import re
from copy import deepcopy
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from tpl_literals import literals,resolve_units
from inspect_remaining_034 import OUT as CENSUS,BASE,BASE_SHA
from survey_aggregate_pet_033 import replace_exact,aggregate as pet_place,VALIDATORS as PET
from survey_aggregate_normal_033 import aggregate as normal_place
from survey_calendar_layout500_031_v2 import place
from survey_batch500_017_layout import protected_edges
from compile_exact500_033 import VALIDATORS as BASE_VALIDATORS
from normal_player_name_capacity_031 import validate as player
from field_hint_capacity import validate as fullbox
from normal_battle_choice_capacity_026 import validate as horizontal
from pet_choice_capacity_026 import validate as pet_choice
from event_dialogue_capacity_031 import validate as event
from calendar_delete_capacity_031 import validate as calendar
from calendar_menu_capacity_032_v2 import validate as menu

OUT='analysis/pending_insertion_500_034_locked_carry_layout_v1/survey.json'

def player_adapter(a,b,c,d,e):return player(a,b,c,d,e,88)
def full_adapter(a,b,c,d,e):return fullbox(a,b,c,d,e,88)
def horizontal_adapter(a,b,c,d,e):return horizontal(a,b,c,d,e,88)
VALIDATORS=BASE_VALIDATORS+[('normal-player-name',player_adapter),('fullbox',full_adapter),('normal-horizontal',horizontal_adapter),('pet-two-choice',pet_choice),('event-pages',event),('calendar-delete',calendar)]


def main():
    c=read(CENSUS);require_hash(ROOT/BASE,BASE_SHA)
    if c['baseline_sha256']!=BASE_SHA:raise ValueError('034 census product')
    m=read(BASE.replace('.gba','.json'));primary={r['archive']:r for r in m['archives']};owners={}
    for arc in primary:
        links=[x for x in m['translation_assets'] if x.get('archive')==arc and not x.get('scope','').startswith('read-only inherited')]
        if len(links)==1:owners[arc]=links[0]
    templates={};assets={};drafts={};good=[];bad=[];skipped=Counter()
    for g in c['groups']:
        if g['storage']!='raw-existing':skipped[g['storage']]+=g['units'];continue
        arc=g['archive'];script=g['script']
        if arc not in owners:skipped['ambiguous_owner']+=g['units'];continue
        if arc not in templates:
            ref=g['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);templates[arc]=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
            link=owners[arc];require_hash(ROOT/link['path'],link['sha256']);assets[arc]=resolve_units(read(link['path']))
        oldunits=[u for u in assets[arc] if int(u['id'].split(':')[1])==script]
        if {u['id'] for u in oldunits}!=set(g['already_applied_ids_in_script']):
            skipped['old_script_population_not_exact']+=g['units'];continue
        src=templates[arc];section=re.search(r'^script '+str(script)+r' \w+ \{[\s\S]*?(?=^script\s|\Z)',src,re.M)
        if section is None:raise ValueError('034 script source')
        original='@archive '+arc+'\n'+section[0]
        original_literals={u.key:u.text for u in literals(original)}
        if any(original_literals[u['id']]!=u['source'] for u in oldunits):raise ValueError('034 old literal source')
        locked={u['id']:u['translation'] for u in oldunits};base=replace_exact(original,locked);units=[]
        for link in g['drafts']:
            p=link['path']
            if p not in drafts:require_hash(ROOT/p,link['sha256']);drafts[p]=read(p)
            unit=next(u for u in drafts[p]['units'] if u['id']==link['id'])
            if unit['source']!=original_literals[unit['id']] or unit['state']!='needs_review':raise ValueError('034 new canonical binding')
            units.append(unit)
        profiles=[];candidates=[('canonical',{u['id']:u['translation'] for u in units})]
        for label,derive in [('pet-aggregate',pet_place),('normal-aggregate',normal_place)]:
            try:candidates.append((label,derive(base,units,99)))
            except ValueError:pass
        for cap in (132,180):
            values={u['id']:place(u['translation'],(cap,cap,min(cap,168))) for u in units}
            if all(v is not None for v in values.values()):candidates.append(('individual'+str(cap),values))
        last=[];accepted=None;allids=set(g['ids'])|set(locked)
        for label,values in candidates:
            if any(v.replace('\n',' ')!=next(u['translation'] for u in units if u['id']==k).replace('\n',' ') or not protected_edges(original_literals[k],v) for k,v in values.items()):continue
            target=replace_exact(base,values)
            if any(u.text!=locked[u.key] for u in literals(target) if u.key in locked):raise ValueError('034 prior wording/layout changed')
            for name,validate in VALIDATORS:
                try:geometry=validate(original,target,[script],allids,99)
                except ValueError as ex:last.append(str(ex));continue
                accepted=dict(deepcopy(g),profile=name,explicit_layouts={u['id']:values[u['id']] for u in units if values[u['id']]!=u['translation']},geometry=geometry,geometry_ids=sorted(allids),
                              locked_parent_units=[dict(id=u['id'],source=u['source'],translation=u['translation'],state=u['state']) for u in oldunits],parent_asset=owners[arc],layout_method=label,
                              parent_compiled_script_identity_pending=True,product_admitted=False)
                break
            if accepted:break
        if accepted:good.append(accepted)
        else:bad.append(dict(archive=arc,script=script,ids=g['ids'],units=g['units'],reason=' | '.join(sorted(set(last))) or 'No protected-edge same-word layout'))
    counts=Counter()
    for g in good:counts[g['profile']]+=g['units']
    deps=[CENSUS,'tools/survey_locked_carry_034.py','tools/compile_exact500_033.py','tools/survey_aggregate_pet_033.py','tools/survey_aggregate_normal_033.py']
    deps+=['tools/'+fn.__module__+'.py' for _,fn in VALIDATORS if fn.__module__!='__main__']
    frozen_write(ROOT/OUT,dict(schema=1,status='LOCKED_PARENT_SAME_WORD_LAYOUT_ANALYSIS_NOT_COMPILED_OR_ADMITTED',baseline_rom=BASE,baseline_sha256=BASE_SHA,
        candidate_units=sum(g['units'] for g in good),candidate_groups=good,profile_units=dict(counts),rejections=bad,skipped_units=dict(skipped),
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,release_eligible=False,
        limits='Current033 canonical drafts; prior selected literal wording/layout locked. Existing independent validators only. Parent script compilation/actual033 equality, source/carry roundtrip/metrics/scopes, exact500 build gates and own-ROM runtime still required.'))
    print('034 locked-parent candidates',sum(g['units'] for g in good),'units',len(good),'scripts',dict(counts));print('rejects',len(bad),'skipped',dict(skipped))


if __name__=='__main__':main()
