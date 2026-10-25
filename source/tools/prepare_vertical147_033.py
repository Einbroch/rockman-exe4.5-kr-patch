"""Freeze147 same-word vertical proposals, no ROM/product admission."""
from copy import deepcopy
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from survey_aggregate_pet_033 import replace_exact
from normal_vertical_choices_033 import validate

OUT = 'analysis/pending_insertion_500_033_vertical147_selection_v1/selection.json'


def main():
    survey_path = 'analysis/pending_insertion_500_033_vertical_layout_v1/survey.json'; s = read(survey_path)
    require_hash(ROOT/s['baseline_rom'], s['baseline_sha256']); m = read(s['baseline_rom'].replace('.gba', '.json'))
    applied = {u['id'] for r in layout_records(m) for u in r['layout']}; prepared = set(read('analysis/pending_insertion_500_033_preflight272_v2/status.json')['selected_ids'])
    for p, h in s['dependencies'].items(): require_hash(ROOT/p, h)
    groups = deepcopy(s['candidate_groups']); seen = set()
    for g in groups:
        if set(g['ids'])&(seen|applied|prepared): raise ValueError('033 vertical non-disjoint IDs')
        require_hash(ROOT/g['source_tpl']['path'], g['source_tpl']['sha256']); old = (ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig'); values = {}
        for link in g['drafts']:
            require_hash(ROOT/link['path'], link['sha256']); u = next(u for u in read(link['path'])['units'] if u['id'] == link['id']); values[u['id']] = g['explicit_layouts'].get(u['id'], u['translation'])
        if validate(old, replace_exact(old, values), [g['script']], set(g['ids']), 99, 88) != g['geometry']: raise ValueError('033 vertical changed current geometry')
        seen.update(g['ids'])
    tests = 'analysis/pending_insertion_500_033_vertical_models_v1/result.json'; t = read(tests)
    if not t['passed'] or len(seen) != 147: raise ValueError('033 vertical model/denominator')
    for p, h in t['dependencies'].items(): require_hash(ROOT/p, h)
    deps = [survey_path, tests, 'tools/prepare_vertical147_033.py', 'tools/normal_vertical_choices_033.py']
    frozen_write(ROOT/OUT, dict(schema=1, status='PARTIAL147_VERTICAL_SOURCE_ONLY_SELECTION_NOT500_OR_ROM',
                  baseline_rom=s['baseline_rom'], baseline_sha256=s['baseline_sha256'], source_sha256=s['source_sha256'], native_nickname_bound=99,
                  planned_new_units=len(seen), selected_ids=sorted(seen), groups=groups, profiles={'normal-vertical-2or3': len(seen)},
                  dependencies={p: sha((ROOT/p).read_bytes()) for p in deps}, rom_written=False, new_units_applied=0, release_eligible=False,
                  limits='147 source-only conditional spatial proposals in addition to272prepared. Native EA/EC input/branch/caller, source compile/carry, whole500 primary/repro/current-ROM runtime and semantic review remain open.'))
    print('PASS033 vertical selection147', len(groups), 'scripts;NO ROM')


if __name__ == '__main__': main()
