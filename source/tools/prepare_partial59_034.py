"""Freeze59 same-word candidates; NOT a500 cohort and never a ROM applier."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from survey_locked_carry_034 import OUT as SURVEY
from inspect_remaining_034 import BASE,BASE_SHA

OUT='analysis/pending_insertion_500_034_partial59_selection_v1/selection.json'

def main():
    survey=read(SURVEY);require_hash(ROOT/BASE,BASE_SHA)
    for p,h in survey['dependencies'].items():require_hash(ROOT/p,h)
    meta=read(BASE.replace('.gba','.json'));applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    groups=deepcopy(survey['candidate_groups']);ids=[k for g in groups for k in g['ids']]
    if len(ids)!=59 or len(set(ids))!=59 or set(ids)&applied:raise ValueError('034 exact partial59 disjoint population')
    for g in groups:
        if set(g['ids'])&{u['id'] for u in g['locked_parent_units']} or set(g['geometry_ids'])!=set(g['ids'])|{u['id'] for u in g['locked_parent_units']}:raise ValueError('034 geometry/locked distinction')
    deps=[SURVEY,'tools/prepare_partial59_034.py','analysis/pending500_033_v1/batch_status.json']
    frozen_write(ROOT/OUT,dict(schema=1,status='PARTIAL59_LOCKED_PARENT_SELECTION_NOT500_NOT_ROM_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,
        source_sha256=meta['source_sha256'],native_nickname_bound=99,planned_new_units=59,requested_rom_cohort=500,additional_units_needed=441,
        selected_ids=sorted(ids),groups=groups,profiles=survey['profile_units'],dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},
        rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,limits='59 selected, not500. Seven partially translated scripts retain exact old wording/layout; parent script bytes must independently match actual033 before accepting source compilation. No partial ROM application authorized.'))
    print('034 frozen59 candidates',len(groups),'scripts',len({g['archive'] for g in groups}),'archives;441 more required;NO ROM')

if __name__=='__main__':main()
