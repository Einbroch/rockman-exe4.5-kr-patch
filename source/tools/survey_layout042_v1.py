"""Survey: which remaining canonical groups pass an established layout validator (no ROM, no writes except report)."""
import re,json,sys
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from tpl_literals import literals
from survey_aggregate_pet_033 import replace_exact
from survey_calendar_layout500_031_v2 import place
from survey_batch500_017_layout import protected_edges
from battle_bbs_geometry040_v1 import validate as bbs
from profile_quick_geometry039_v1 import validate as communication
from normal_timing_capacity_025 import validate as normal
from pet_quick_capacity import validate as quick
from pet_flag_page_capacity_024 import validate as quick_flags
from normal_choice_capacity_025_v3 import validate as horizontal
from normal_vertical_choice_capacity_026 import validate as vertical
from positioned_normal_geometry041_v1 import validate as positioned
from pet_nickname_capacity_025 import validate as pet_nickname
from pet_nickname_flags_capacity_025_v2 import validate as pet_nickname_flags
from pet_guard_capacity_027 import validate as pet_guard
from pet_profile_capacity_027_v2 import validate as pet_profile
from pet_array_capacity_029 import validate as pet_array
from pet_chip_capacity_030 import validate as pet_chip
from pet_extended_native_capacity_031 import validate as pet_extended
from normal_player_name_capacity_031 import validate as normal_name
from normal_battle_choice_capacity_026 import validate as battle_choice
from pet_choice_capacity_026 import validate as pet_choice
from pet_entry_profile_capacity_030 import validate as pet_entry
from cleared_normal_geometry041_v1 import validate as cleared_normal
from default_quick_geometry041_v1 import validate as default_quick
from guarded_default_quick_geometry041_v1 import validate as guarded_quick
P={'normal':lambda o,t,ss,ids:normal(o,t,ss,ids,99,88),'quick':quick,'quick-flags':quick_flags,'horizontal-choice':lambda o,t,ss,ids:horizontal(o,t,ss,ids,99,88),'vertical-choice':lambda o,t,ss,ids:vertical(o,t,ss,ids,99,88),'positioned-normal':positioned,'normal-player-name':lambda o,t,ss,ids:normal_name(o,t,ss,ids,99,88),'battle-choice':lambda o,t,ss,ids:battle_choice(o,t,ss,ids,99,88),'pet-choice':lambda o,t,ss,ids:pet_choice(o,t,ss,ids,99),'pet-entry':lambda o,t,ss,ids:pet_entry(o,t,ss,ids,99),'cleared-normal':cleared_normal,'default-quick':default_quick,'guarded-default-quick':guarded_quick}
for name,fn in [('pet-nickname',pet_nickname),('pet-nickname-flags',pet_nickname_flags),('pet-guard',pet_guard),('pet-profile',pet_profile),('pet-array',pet_array),('pet-chip',pet_chip),('pet-extended',pet_extended)]:
    P[name]=lambda o,t,ss,ids,fn=fn:fn(o,t,ss,ids,99)
COMMS='analysis/pending_insertion_500_039_communication_words_survey_v1/selection.json'


def classify(g,text,drafts,source):
    arc=g['archive'];script=g['script'];ids=set(g['ids']);sr=g['source_tpl']
    oldcomm=classify.oldcomm
    if (arc,script) in oldcomm:kind='communication-help';caps=(132,132,132)
    elif arc in {'7000AC','7011F0','701ED8','7028FC'}:kind='battle-BBS-trial';caps=(168,168,168)
    else:kind=None;caps=(132,132,132) if 'msgOpenQuick' in g['commands'] else (180,180,168)
    match=re.search(r'^script '+str(script)+r' mmbn45s? \{[\s\S]*?(?=^script|\Z)',text,re.M)
    one='@archive '+arc+'\n'+match[0];raw={u.key:u.text for u in literals(one)};values={};units=[]
    for d in g['drafts']:
        if d['path'] not in drafts:require_hash(ROOT/d['path'],d['sha256']);drafts[d['path']]=read(d['path'])
        a=drafts[d['path']];u=deepcopy(next(x for x in a['units'] if x['id']==d['id']))
        if u['source']!=raw.get(u['id']):return None,'source mismatch',None,None
        value=place(u['translation'],caps)
        if value is None or value.replace('\n',' ')!=u['translation'].replace('\n',' ') or not protected_edges(u['source'],value):return None,'word-only layout exceeds profile',None,None
        values[u['id']]=value;units.append(u)
    target=replace_exact(one,values)
    errs=[]
    try:
        if kind=='communication-help':return kind,communication(one,target,[script],ids),values,units
        if kind=='battle-BBS-trial':return kind,bbs(one,target,[script],ids),values,units
    except Exception as ex:return None,kind+': '+str(ex)[:80],None,None
    for name,fn in P.items():
        try:return name,fn(one,target,[script],ids),values,units
        except Exception as ex:errs.append(name+':'+str(ex)[:60])
    return None,'; '.join(errs[:3]),None,None


def main():
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();c=read('analysis/pending_insertion_500_041_inventory_v1/census.json');done=set(read('analysis/pending_insertion_500_041_source_v8/selection.json')['selected_ids'])
    classify.oldcomm={(g['archive'],g['script']) for g in read(COMMS)['candidate_groups']}
    templates={};drafts={};ok=Counter();bad=Counter();reasons=Counter()
    for g in c['groups']:
        if set(g['ids'])&done:continue
        sr=g['source_tpl']
        if g['archive'] not in templates:templates[g['archive']]=(ROOT/sr['path']).read_text(encoding='utf-8-sig')
        kind,geo,values,units=classify(g,templates[g['archive']],drafts,source)
        if kind:ok[kind]+=g['units']
        else:bad[(g['literal_language'],g['storage'])]+=g['units'];reasons[geo.split(':')[0][:50]]+=g['units']
    print('PASS',sum(ok.values()),ok.most_common());print('FAIL',sum(bad.values()),bad.most_common());print(reasons.most_common(25))


if __name__=='__main__':main()
