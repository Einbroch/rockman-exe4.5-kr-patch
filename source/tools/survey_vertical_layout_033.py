"""Same canonical wording on finite224 vertical-menu scripts, analysis only."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from survey_aggregate_pet_033 import replace_exact
from survey_calendar_layout500_031_v2 import place
from survey_batch500_017_layout import protected_edges
from normal_vertical_choices_033 import validate

INVENTORY = 'analysis/pending_insertion_500_033_vertical_inventory_v1/census.json'
OUT = 'analysis/pending_insertion_500_033_vertical_layout_v1/survey.json'


def main():
    census = read(INVENTORY); require_hash(ROOT/census['baseline_rom'], census['baseline_sha256'])
    for p, h in census['dependencies'].items(): require_hash(ROOT/p, h)
    good = []; bad = []
    for g in census['groups']:
        values = {}; layouts = {}; failed = None
        for link in g['drafts']:
            require_hash(ROOT/link['path'], link['sha256']); a = read(link['path']); u = next(u for u in a['units'] if u['id'] == link['id'])
            if a['source_tpl'] != g['source_tpl'] or a['source_archive_sha256'] != g['source_archive_sha256'] or u['state'] != 'needs_review': raise ValueError('033 vertical canonical source/state')
            value = place(u['translation'], (180, 180, 168))
            if value is None or not protected_edges(u['source'], value) or value.replace('\n', ' ') != u['translation'].replace('\n', ' '):
                failed = 'canonical same-word protected-edge placement'; break
            values[u['id']] = value
            if value != u['translation']: layouts[u['id']] = value
        if failed:
            bad.append(dict(archive=g['archive'], script=g['script'], ids=g['ids'], reason=failed)); continue
        require_hash(ROOT/g['source_tpl']['path'], g['source_tpl']['sha256']); original = (ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig')
        try: geometry = validate(original, replace_exact(original, values), [g['script']], set(g['ids']), 99, 88)
        except ValueError as ex:
            bad.append(dict(archive=g['archive'], script=g['script'], ids=g['ids'], reason=str(ex))); continue
        row = deepcopy(g); row.update(profile='normal-vertical-2or3', explicit_layouts=layouts, geometry=geometry, storage='raw-known-pointer', product_admitted=False); good.append(row)
    deps = [INVENTORY, 'tools/survey_vertical_layout_033.py', 'tools/normal_vertical_choices_033.py',
            'tools/survey_calendar_layout500_031_v2.py', 'tools/survey_aggregate_pet_033.py',
            'analysis/pending_insertion_500_033_vertical_wide_cpu_v1/cpu.json']
    frozen_write(ROOT/OUT, dict(schema=1, status='FINITE_VERTICAL_SAME_WORD_LAYOUT_PROPOSALS_NOT_ROM_ADMISSION',
                  baseline_rom=census['baseline_rom'], baseline_sha256=census['baseline_sha256'], source_sha256=census['source_sha256'],
                  native_nickname_bound=99, candidate_units=sum(g['units'] for g in good), candidate_groups=good,
                  rejections=bad, rejection_counts=dict(Counter(g['reason'] for g in bad)), dependencies={p: sha((ROOT/p).read_bytes()) for p in deps},
                  rom_written=False, new_units_applied=0, release_eligible=False,
                  limits='Spatial proposals on declared224population only. Not EA/EC execution/outcomes, caller/state, source compilation/carry, exact500 product gates or GBA runtime/semantic approval.'))
    print('033 vertical fitting candidates', sum(g['units'] for g in good), 'units', len(good), 'scripts;', Counter(g['reason'] for g in bad), flush=True)


if __name__ == '__main__': main()
