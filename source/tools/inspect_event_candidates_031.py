"""Finite event-provider remainder within the existing031 frozen survey only."""
import re
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from field_hint_capacity import events
from pet_extended_native_capacity_031 import PREFIX

SURVEY='analysis/pending_insertion_500_031_layout_v1/survey.json'
OUT='analysis/pending_insertion_500_031_event_inventory_v1/census.json'


def main():
    survey=read(SURVEY);require_hash(ROOT/survey['baseline_rom'],survey['baseline_sha256'])
    if survey['baseline_sha256']!='203fd306a7c9c713e3c6f4e7af3dd24d5f21eab0c000f210a061295d31083491':raise ValueError('031 exact baseline')
    rows=[];deps={SURVEY:sha((ROOT/SURVEY).read_bytes()),'tools/inspect_event_candidates_031.py':sha((ROOT/'tools/inspect_event_candidates_031.py').read_bytes())}
    for g in survey['rejections']:
        path='analysis/full_scope_v1/source_tpl/'+g['archive']+'.tpl';text=(ROOT/path).read_text(encoding='utf-8-sig')
        match=re.search(r'^script '+str(g['script'])+r' \w+ \{[\s\S]*?(?=^script\s|\Z)',text,re.M)
        if match is None:raise ValueError('031 source script absent')
        seq=events('@archive '+g['archive']+'\n'+match[0]);commands=[data for _,kind,data in seq if kind=='command'];names=[v[0] for v in commands]
        if not set(names)&{'callBufferEventName','callBufferEventHour','callBufferEventMinutes','callBufferEventAMPM'}:continue
        deps[path]=sha((ROOT/path).read_bytes());quick='msgOpenQuick' in names
        rows.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],units=len(g['ids']),quick=quick,exact_PET_initializer=quick and commands[:4]==PREFIX,provider_calls=dict(Counter(n for n in names if n.startswith('callBufferEvent'))),commands=dict(Counter(names)),original_rejection=g['reason'],product_admitted=False))
    ids=[i for g in rows for i in g['ids']]
    if len(ids)!=len(set(ids)):raise ValueError('031 event candidate duplicate IDs')
    frozen_write(ROOT/OUT,dict(schema=1,status='FINITE_ANALYSIS_INVENTORY_NOT_ADMISSION',baseline_rom=survey['baseline_rom'],baseline_sha256=survey['baseline_sha256'],groups=len(rows),literal_units=len(ids),by_initializer=dict(Counter(('exact-PET' if g['exact_PET_initializer'] else 'other-quick' if g['quick'] else 'normal-or-inherited') for g in rows)),units_by_initializer=dict(Counter({k:sum(g['units'] for g in rows if ('exact-PET' if g['exact_PET_initializer'] else 'other-quick' if g['quick'] else 'normal-or-inherited')==k) for k in ['exact-PET','other-quick','normal-or-inherited']})),candidate_groups=rows,dependencies=deps,rom_written=False,release_eligible=False,limits=['Only rejected groups in031 existing frozen layout survey, not whole-game Japanese remainder.','No generated-title universal bounds, caller-inherited geometry, schedule loops or numeric display admission.','3024CPU fixtures and one actual030 meal route are separate bounded evidence, not blanket admission of this inventory.']))
    print('031 finite event inventory',len(rows),'scripts',len(ids),'literal units',flush=True)


if __name__=='__main__':main()
