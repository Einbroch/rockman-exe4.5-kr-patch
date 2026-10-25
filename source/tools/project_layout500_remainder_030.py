"""Projection after frozen030 selection, NOT actual-ROM or whole-game count."""
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    path='analysis/pending_insertion_500_030_layout_v2/survey.json';selected_path='analysis/pending_insertion_500_030_selection_v1/selection.json'
    survey=read(path);selection=read(selected_path)
    for data in (survey,selection):
        for p,h in data['dependencies'].items():require_hash(ROOT/p,h)
    selected=set(selection['selected_ids']);remaining=[];counts=Counter()
    for g in survey['candidate_groups']:
        ids=set(g['ids'])
        if ids&selected:
            if not ids<=selected:raise ValueError('030 unexpected partial script selection')
            continue
        counts[g['profile']]+=len(ids);remaining.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],profile=g['profile']))
    frozen_write(ROOT/'analysis/pending_insertion_500_030_projected_remainder_v1/projection.json',dict(schema=1,status='PROJECTION_ONLY_AFTER_SELECTION_NOT_FINAL_ROM_COVERAGE',baseline_rom=selection['baseline_rom'],baseline_sha256=selection['baseline_sha256'],projected_selected_units=len(selected),projected_finite_model_remaining_units=sum(counts.values()),projected_profile_units=dict(counts),projected_groups=remaining,selected500_has_been_verified_in_actual030=False,whole_game_remaining_count_established=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in (path,selected_path,'tools/project_layout500_remainder_030.py')},next_investigation='After actual030 succeeds, recensus its applied IDs. Existing direct/conditional-array/native-chip profiles have fewer than500 candidates; do not force another500 by relaxing unproved variable providers, entry guards, renderer, storage or mixed-partial-script contracts. Analyze a source-bound next consumer or partial-script merge first.',limits='Logical subtraction from frozen029-based analysis and planned030 IDs. Not a playable030 check, release scope, or untranslated remainder census.'))
    print('Projected finite model remainder',dict(counts),'not whole-game count or current030 application proof')


if __name__=='__main__':main()
