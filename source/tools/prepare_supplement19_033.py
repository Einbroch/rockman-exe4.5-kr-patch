"""Freeze remaining13 calendar and6 normal units; source-only, not500."""
import re
from copy import deepcopy
from collections import defaultdict, Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from compare_archive_payloads import payload_of
from verify_tpi_index import parse_tpi
from tpl_literals import literals
from survey_aggregate_pet_033 import BASE, BASE_SHA, replace_exact
from survey_calendar_layout500_031_v2 import place
from survey_batch500_017_layout import protected_edges
from calendar_aqua_capacity_033 import validate as aqua
from calendar_menu_capacity_032_v2 import validate as menu
from normal_timing_capacity_025 import validate as normal

OUT = 'analysis/pending_insertion_500_033_supplement19_selection_v1/selection.json'


def main():
    cfg = read('project.json'); sp = ROOT/cfg['source_profile']['filename']; require_hash(sp, cfg['source_profile']['sha256']); source = sp.read_bytes()
    require_hash(ROOT/BASE, BASE_SHA); m = read(BASE.replace('.gba', '.json')); applied = {u['id'] for r in layout_records(m) for u in r['layout']}
    prior = read('analysis/pending_insertion_500_033_aggregate_selection_v1/selection.json'); prepared = set(prior['selected_ids'])
    require_hash(ROOT/cfg['text_catalog']['path'], cfg['text_catalog']['sha256']); catalog = {f"{r['offset']:X}": r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    coverage_path = 'analysis/translation_first_v1/coverage.json'; coverage = read(coverage_path); pool = defaultdict(list)
    for p, h in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/p, h); a = read(p)
        for u in a['units']: pool[u['id']].append((p, h, u, a))
    remainder_path = 'analysis/pending500_032_v1/calendar_remainder.json'; remainder = read(remainder_path)
    if remainder['rom_sha256'] != BASE_SHA: raise ValueError('033 actual calendar remainder baseline')
    groups = []
    for pending in remainder['groups']:
        arc = pending['archive']; script = pending['script']; row = catalog[arc]; native_sha = sha(payload_of(source, row)); values = {}; refs = []; src = None; explicit = {}
        for key in pending['ids']:
            options = pool[key]
            if not options or len({(u['source'], u['translation'], u['state']) for _, _, u, _ in options}) != 1: raise ValueError('033 supplement missing/conflicting wording')
            p, h, u, a = options[0]
            if src is not None and src != a['source_tpl']: raise ValueError('033 supplement inconsistent source')
            src = a['source_tpl']
            if a['source_archive_sha256'] != native_sha or a['source_sha256'] != cfg['source_profile']['sha256'] or u['state'] != 'needs_review': raise ValueError('033 supplement canonical/source policy')
            value = place(u['translation'], (180, 180, 168))
            if value is None or not protected_edges(u['source'], value) or value.replace('\n', ' ') != u['translation'].replace('\n', ' '): raise ValueError('033 supplement canonical placement failed')
            values[key] = value; refs.append(dict(id=key, path=p, sha256=h))
            if value != u['translation']: explicit[key] = value
        require_hash(ROOT/src['path'], src['sha256']); original = (ROOT/src['path']).read_text(encoding='utf-8-sig'); target = replace_exact(original, values)
        source_ids = {u.key for u in literals(original) if int(u.key.split(':')[1]) == script and re.search(r'[\u3040-\u30ff\u3400-\u9fff]', u.text)}
        if source_ids != set(values): raise ValueError('033 supplement whole-script Japanese population')
        kind = 'calendar-aqua-early-sfx' if arc == '697B70' else 'calendar-menu'
        geometry = (aqua if arc == '697B70' else menu)(original, target, [script], set(values), 99)
        groups.append(dict(archive=arc, script=script, ids=pending['ids'], units=len(values), profile=kind, drafts=refs,
                           source_tpl=src, source_row=row, source_archive_sha256=native_sha, explicit_layouts=explicit,
                           geometry=geometry, storage='raw-known-pointer', product_admitted=False))
    normal_path = 'analysis/pending_insertion_500_033_normal_aggregate_v1/survey.json'; ns = read(normal_path)
    for p, h in ns['dependencies'].items(): require_hash(ROOT/p, h)
    if ns['baseline_sha256'] != BASE_SHA or ns['candidate_units'] != 6: raise ValueError('033 supplement normal baseline/denominator')
    for g in ns['candidate_groups']:
        gg = deepcopy(g); values = {}
        for link in gg['drafts']:
            require_hash(ROOT/link['path'], link['sha256']); u = next(u for u in read(link['path'])['units'] if u['id'] == link['id']); values[u['id']] = gg['explicit_layouts'].get(u['id'], u['translation'])
        require_hash(ROOT/gg['source_tpl']['path'], gg['source_tpl']['sha256']); old = (ROOT/gg['source_tpl']['path']).read_text(encoding='utf-8-sig')
        if normal(old, replace_exact(old, values), [gg['script']], set(values), 99, 88) != gg['geometry']: raise ValueError('033 supplement normal current geometry')
        groups.append(gg)
    ids = [k for g in groups for k in g['ids']]
    if len(ids) != 19 or len(set(ids)) != 19 or set(ids)&(applied|prepared): raise ValueError('033 supplement exact19 new disjoint IDs')
    cpu_path = 'analysis/pending_insertion_500_033_choice_sfx_cpu_v1/cpu.json'; cpu = read(cpu_path)
    if not cpu['passed'] or cpu['baseline_sha256'] != BASE_SHA: raise ValueError('033 supplement native FD09 evidence')
    for p, h in cpu['dependencies'].items(): require_hash(ROOT/p, h)
    counts = Counter()
    for g in groups: counts[g['profile']] += g['units']
    deps = [coverage_path, remainder_path, normal_path, cpu_path, 'tools/prepare_supplement19_033.py', 'tools/calendar_aqua_capacity_033.py',
            'tools/calendar_delete_capacity_031.py', 'tools/calendar_date_delete_capacity_032.py', 'tools/calendar_menu_capacity_032_v2.py',
            'tools/survey_calendar_layout500_031_v2.py', 'tools/normal_timing_capacity_025.py',
            'analysis/pending_insertion_500_033_aggregate_selection_v1/selection.json']
    frozen_write(ROOT/OUT, dict(schema=1, status='SUPPLEMENT19_SOURCE_ONLY_SELECTION_NOT500_OR_ROM', baseline_rom=BASE, baseline_sha256=BASE_SHA,
                  source_sha256=cfg['source_profile']['sha256'], native_nickname_bound=99, planned_new_units=19,
                  selected_ids=sorted(ids), groups=groups, profiles=dict(counts),
                  dependencies={p: sha((ROOT/p).read_bytes()) for p in deps},
                  rom_written=False, new_units_applied=0, release_eligible=False,
                  limits='13calendar+6normal source-only selection. Aqua actual FD09 position/control skeleton unchanged; only spatial model projected. Native title/date/name conditions, carry/primary gates/full500/current-ROM runtime and semantic review remain pending.'))
    print('PASS033 supplement19 selection', len(groups), 'scripts', len({g['archive'] for g in groups}), 'archives;NO ROM')


if __name__ == '__main__': main()
