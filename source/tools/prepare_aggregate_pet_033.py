"""Freeze all253 current conditional PET proposals, NOT a500 ROM cohort."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from survey_aggregate_pet_033 import OUT as SURVEY, BASE, BASE_SHA, replace_exact, VALIDATORS
from survey_batch500_017_layout import protected_edges

OUT = 'analysis/pending_insertion_500_033_aggregate_selection_v1/selection.json'


def main():
    s = read(SURVEY); require_hash(ROOT/BASE, BASE_SHA)
    for p, h in s['dependencies'].items():
        require_hash(ROOT/p, h)
    m = read(BASE.replace('.gba', '.json')); applied = {u['id'] for r in layout_records(m) for u in r['layout']}
    seen = set(); groups = deepcopy(s['candidate_groups']); validators = dict(VALIDATORS)
    for g in groups:
        if set(g['ids']) & (seen | applied) or g['storage'] != 'raw-known-pointer' or g['product_admitted']:
            raise ValueError('033 distinct source-only population')
        seen.update(g['ids']); values = {}
        for link in g['drafts']:
            require_hash(ROOT/link['path'], link['sha256']); a = read(link['path'])
            u = next(u for u in a['units'] if u['id'] == link['id'])
            value = g['explicit_layouts'].get(u['id'], u['translation'])
            if value.replace('\n', ' ') != u['translation'].replace('\n', ' ') or not protected_edges(u['source'], value):
                raise ValueError('033 canonical wording/padding changed')
            values[u['id']] = value
        require_hash(ROOT/g['source_tpl']['path'], g['source_tpl']['sha256'])
        old = (ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig')
        proof = validators[g['profile']](old, replace_exact(old, values), [g['script']], set(g['ids']), s['native_nickname_bound'])
        if proof != g['geometry']:
            raise ValueError('033 frozen geometry mismatch')
    if len(seen) != 253 or len(seen) != sum(g['units'] for g in groups):
        raise ValueError('033 finite partial denominator')
    tests = 'analysis/pending_insertion_500_033_aggregate_models_v1/result.json'; t = read(tests)
    if not t['passed']:
        raise ValueError('033 controlled contracts failed')
    for p, h in t['dependencies'].items():
        require_hash(ROOT/p, h)
    counts = Counter()
    for g in groups:
        counts[g['profile']] += g['units']
    deps = [SURVEY, tests, 'tools/prepare_aggregate_pet_033.py']
    frozen_write(ROOT/OUT, dict(schema=1, status='PARTIAL253_CONDITIONAL_SOURCE_ONLY_SELECTION_NOT_ROM_ADMISSION',
                               baseline_rom=BASE, baseline_sha256=BASE_SHA, source_sha256=s['source_sha256'],
                               native_nickname_bound=s['native_nickname_bound'], planned_new_units=len(seen),
                               requested_rom_cohort=500, additional_units_needed=500-len(seen),
                               selected_ids=sorted(seen), groups=groups, profiles=dict(counts),
                               dependencies={p: sha((ROOT/p).read_bytes()) for p in deps},
                               rom_written=False, new_units_applied=0, insertion_ready=False, release_eligible=False,
                               limits='253 conditional unchanged-wording source-only proposals, not500 or a playable033 ROM. Native record/cache/provider applicability, cumulative032 preservation, primary gating, exactwrites/repro/runtime and semantic review remain required.'))
    print('PASS033 frozen partial', len(seen), 'units', len(groups), 'scripts', len({g['archive'] for g in groups}), 'archives;NO ROM')


if __name__ == '__main__':
    main()
