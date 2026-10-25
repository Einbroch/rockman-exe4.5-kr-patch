"""Exact500 source-only scope:272 prior+144 operator+84 profile-manager."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from survey_aggregate_pet_033 import BASE, BASE_SHA, replace_exact
from profile_manager_capacity_033 import validate as manager

OUT = 'analysis/pending_insertion_500_033_exact500_selection_v1/selection.json'


def main():
    require_hash(ROOT/BASE, BASE_SHA); m = read(BASE.replace('.gba', '.json')); applied = {u['id'] for r in layout_records(m) for u in r['layout']}
    prior_paths = ['analysis/pending_insertion_500_033_aggregate_selection_v1/selection.json',
                   'analysis/pending_insertion_500_033_supplement19_selection_v1/selection.json']
    groups = []; seen = set(); deps = []
    for path in prior_paths:
        s = read(path)
        for p, h in s['dependencies'].items(): require_hash(ROOT/p, h)
        groups += deepcopy(s['groups']); deps.append(path)
    vertical_path = 'analysis/pending_insertion_500_033_vertical147_selection_v1/selection.json'; vertical = read(vertical_path)
    for p, h in vertical['dependencies'].items(): require_hash(ROOT/p, h)
    selected_vertical = [deepcopy(g) for g in vertical['groups'] if g['archive'] == '766134']
    if sum(g['units'] for g in selected_vertical) != 144: raise ValueError('033 operator whole-family144')
    groups += selected_vertical; deps.append(vertical_path)
    manager_path = 'analysis/pending_insertion_500_033_manager_layout_v1/survey.json'; ms = read(manager_path)
    for p, h in ms['dependencies'].items(): require_hash(ROOT/p, h)
    selected_manager = sorted(ms['candidate_groups'], key=lambda g: g['script'])[:14]
    if len(selected_manager) != 14 or sum(g['units'] for g in selected_manager) != 84: raise ValueError('033 exact84 manager whole-script cohort')
    for g in selected_manager:
        values = {}
        for link in g['drafts']:
            require_hash(ROOT/link['path'], link['sha256']); u = next(u for u in read(link['path'])['units'] if u['id'] == link['id']); values[u['id']] = g['explicit_layouts'].get(u['id'], u['translation'])
        require_hash(ROOT/g['source_tpl']['path'], g['source_tpl']['sha256']); old = (ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig')
        if manager(old, replace_exact(old, values), [g['script']], set(g['ids']), 99) != g['geometry']: raise ValueError('033 manager current proposal mismatch')
    groups += deepcopy(selected_manager); deps.append(manager_path)
    counts = Counter()
    for g in groups:
        if set(g['ids'])&(seen|applied) or g['storage'] != 'raw-known-pointer' or g['product_admitted']: raise ValueError('033 exact500 disjoint source-only raw scope')
        seen.update(g['ids']); counts[g['profile']] += g['units']
    if len(seen) != 500 or sum(g['units'] for g in groups) != 500: raise ValueError('033 exact500 denominator')
    tests = 'analysis/pending_insertion_500_033_manager_models_v1/result.json'; t = read(tests)
    if not t['passed']: raise ValueError('033 manager contracts failed')
    for p, h in t['dependencies'].items(): require_hash(ROOT/p, h)
    policy = 'analysis/pending_insertion_500_033_batch_policy_v1/decision.json'
    if read(policy)['required_new_literal_units_per_cohort'] != 500: raise ValueError('033 exact500 human policy')
    deps += [tests, policy, 'tools/prepare_exact500_033.py']
    reserve = sorted({k for g in vertical['groups'] if g['archive'] != '766134' for k in g['ids']} | {k for g in ms['candidate_groups'] if g['script'] >= 14 for k in g['ids']})
    frozen_write(ROOT/OUT, dict(schema=1, status='EXACT500_SOURCE_ONLY_SELECTION_NOT_PRIMARY_OR_RUNTIME_ADMISSION',
                  baseline_rom=BASE, baseline_sha256=BASE_SHA, source_sha256=s['source_sha256'], native_nickname_bound=99,
                  planned_new_units=len(seen), selected_ids=sorted(seen), groups=groups, profiles=dict(counts),
                  reserved_not_selected_ids=reserve, dependencies={p: sha((ROOT/p).read_bytes()) for p in deps},
                  rom_written=False, new_units_applied=0, insertion_ready=False, release_eligible=False,
                  limits='272prior+144operator+84manager=500 whole-script source-only units.3vertical and12manager fitting proposals reserved, not applied. Exact500doesnot waive native EA/EC/manager continuation input/branch, current compiler/carry, product gates/preallocation/ExpectedWrites/repro/new-ROM runtime or semantic review.'))
    print('PASS033 exact500 source-only selection', len(groups), 'scripts', len({g['archive'] for g in groups}), 'archives;', len(reserve), 'reserved;NO ROM')


if __name__ == '__main__': main()
