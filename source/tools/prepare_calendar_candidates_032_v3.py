"""Normalize exact500 profile metadata and bind supplemental native evidence."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from calendar_menu_capacity_032_v2 import validate as menu_validate
from calendar_date_delete_capacity_032 import validate as date_validate
from survey_pet_quick_reflow_024 import replace_for_analysis

OUT='analysis/pending_insertion_500_032_calendar_selection_v3/selection.json'


def main():
    prior='analysis/pending_insertion_500_032_calendar_selection_v2/selection.json';old=read(prior);s=deepcopy(old)
    if not old['exact500'] or old['planned_new_units']!=500 or len(set(old['selected_ids']))!=500:raise ValueError('032 exact500 selection required')
    for p,h in old['dependencies'].items():require_hash(ROOT/p,h)
    require_hash(ROOT/old['baseline_rom'],old['baseline_sha256'])
    for g in s['groups']:
        require_hash(ROOT/g['source_tpl']['path'],g['source_tpl']['sha256']);original=(ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig');units=[]
        for link in g['drafts']:
            require_hash(ROOT/link['path'],link['sha256']);unit=deepcopy(next(x for x in read(link['path'])['units'] if x['id']==link['id']));unit['translation']=g['explicit_layouts'].get(unit['id'],unit['translation']);units.append(unit)
        proof=(date_validate if g['profile']=='calendar-date-delete' else menu_validate)(original,replace_for_analysis(original,units),[g['script']],set(g['ids']))
        if proof!=g['geometry']:raise ValueError('032 normalized current geometry')
    s['profiles']=dict(Counter({profile:sum(g['units'] for g in s['groups'] if g['profile']==profile) for profile in ('calendar-date-delete','calendar-menu')}))
    s['dependencies'][prior]=sha((ROOT/prior).read_bytes())
    paths=['tools/prepare_calendar_candidates_032_v3.py','analysis/pending_insertion_500_032_current_date_cpu_v1/cpu.json','analysis/pending_insertion_500_032_menu_models_v1/result.json','analysis/pending_insertion_500_032_date_models_v1/result.json','analysis/pending500_031_v1/frequency_cpu.json','analysis/pending500_031_v1/native_control_identity.json']
    for p in paths:
        if p.endswith('.json'):
            report=read(p)
            if not report['passed'] or report.get('baseline_sha256',report.get('rom_sha256',s['baseline_sha256']))!=s['baseline_sha256']:raise ValueError('032 normalized native/model evidence')
        s['dependencies'][p]=sha((ROOT/p).read_bytes())
    s['status']='EXACT500_SOURCE_ONLY_CALENDAR_SELECTION_NOT_ROM_ADMISSION';s['limits']='Exact500 conditional native date/menu consumers, canonical needs_review wording plus explicit LF-only layouts. Selection profile metadata normalized from groups; prior v2 date-only summary retained in provenance. No cumulative product, final Korean runtime, all500 semantic review or full Hangul/save approval.'
    frozen_write(ROOT/OUT,s);print('032 exact500 normalized profiles',s['profiles'],'scripts',len(s['groups']))


if __name__=='__main__':main()
