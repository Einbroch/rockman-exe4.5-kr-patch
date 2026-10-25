"""Finite profile-manager16scripts same-word proposals; not admission."""
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from compare_archive_payloads import payload_of
from verify_tpi_index import parse_tpi
from survey_aggregate_pet_033 import BASE, BASE_SHA, SURVEY, replace_exact
from survey_calendar_layout500_031_v2 import place
from survey_batch500_017_layout import protected_edges
from profile_manager_capacity_033 import validate

OUT = 'analysis/pending_insertion_500_033_manager_layout_v1/survey.json'


def main():
    s = read(SURVEY); cfg = read('project.json'); require_hash(ROOT/BASE, BASE_SHA); m = read(BASE.replace('.gba', '.json'))
    sp = ROOT/cfg['source_profile']['filename']; require_hash(sp, cfg['source_profile']['sha256']); source = sp.read_bytes()
    applied = {u['id'] for r in layout_records(m) for u in r['layout']}; coverage = read(s['pinned_coverage']['path']); require_hash(ROOT/s['pinned_coverage']['path'], s['pinned_coverage']['sha256'])
    pool = defaultdict(list)
    for p, h in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/p, h); a = read(p)
        if a['archive'] == '7CC6A0':
            for u in a['units']: pool[u['id']].append((p, h, u, a))
    require_hash(ROOT/cfg['text_catalog']['path'], cfg['text_catalog']['sha256']); row = next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset'] == int('7CC6A0', 16)); native_sha = sha(payload_of(source, row))
    good = []; bad = []
    for g in s['unresolved_groups']:
        if g['archive'] != '7CC6A0' or g['script'] not in range(16): continue
        if set(g['ids'])&applied or row['compressed'] or row['size_header']: raise ValueError('033 manager current pending raw population')
        values = {}; refs = []; layouts = {}; src = None; error = None
        for key in g['ids']:
            options = pool[key]
            if not options or len({(u['source'], u['translation'], u['state']) for _, _, u, _ in options}) != 1: raise ValueError('033 manager canonical conflict')
            p, h, u, a = options[0]; src = a['source_tpl']
            if a['source_archive_sha256'] != native_sha or u['state'] != 'needs_review': raise ValueError('033 manager source/policy')
            value = place(u['translation'], (180, 180, 168))
            if value is None or not protected_edges(u['source'], value): error = 'same-word protected-edge placement'; break
            values[key] = value; refs.append(dict(id=key, path=p, sha256=h))
            if value != u['translation']: layouts[key] = value
        if error:
            bad.append(dict(script=g['script'], ids=g['ids'], reason=error)); continue
        require_hash(ROOT/src['path'], src['sha256']); original = (ROOT/src['path']).read_text(encoding='utf-8-sig')
        try: geometry = validate(original, replace_exact(original, values), [g['script']], set(g['ids']), 99)
        except ValueError as ex:
            bad.append(dict(script=g['script'], ids=g['ids'], reason=str(ex))); continue
        good.append(dict(archive=g['archive'], script=g['script'], ids=g['ids'], units=len(values), profile='profile-manager-nonclear',
                         drafts=refs, source_tpl=src, source_row=row, source_archive_sha256=native_sha, explicit_layouts=layouts,
                         geometry=geometry, storage='raw-known-pointer', product_admitted=False))
    deps = [SURVEY, 'tools/survey_profile_manager_033.py', 'tools/profile_manager_capacity_033.py', 'tools/survey_calendar_layout500_031_v2.py', 'tools/survey_aggregate_pet_033.py']
    frozen_write(ROOT/OUT, dict(schema=1, status='FINITE_MANAGER_LAYOUT_PROPOSALS_NOT_SOURCE_COMPILED_OR_ADMITTED',
                  baseline_rom=BASE, baseline_sha256=BASE_SHA, source_sha256=cfg['source_profile']['sha256'], native_nickname_bound=99,
                  candidate_units=sum(g['units'] for g in good), candidate_groups=good, rejections=bad,
                  dependencies={p: sha((ROOT/p).read_bytes()) for p in deps}, rom_written=False, new_units_applied=0, release_eligible=False,
                  limits='Exact7CC6A0:0..15 existing native-name66 + nonclearing82px two-choice/jump20/95 spatial proposals only. Native input/branch/clear/redisplay, source compile/carry, primary exact500/repro/runtime and semantic review remain required.'))
    print('033 manager candidates', sum(g['units'] for g in good), 'units', len(good), 'scripts; rejects', bad)


if __name__ == '__main__': main()
