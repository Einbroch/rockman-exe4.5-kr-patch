"""Actual032 RAW normal-window same-word LF candidates, not ROM admission."""
import re
from itertools import combinations
from functools import lru_cache
from collections import defaultdict, Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from field_hint_capacity import events, validate as fullbox
from tpl_literals import literals
from nickname_capacity import advance, ARGS
from survey_batch500_017_layout import protected_edges
from survey_aggregate_pet_033 import replace_exact, BASE, BASE_SHA, SURVEY
from normal_timing_capacity_025 import validate as normal
from normal_player_name_capacity_031 import validate as player

OUT = 'analysis/pending_insertion_500_033_normal_aggregate_v1/survey.json'
VALIDATORS = [('normal-player-name', player), ('normal-pages', normal), ('fullbox', fullbox)]


@lru_cache(None)
def variants(source, canonical):
    flat = canonical.replace('\n', ' '); cuts = [i for i, c in enumerate(flat) if c == ' ' and 0 < i < len(flat)-1]
    found = {canonical}
    for n in range(3):
        for selected in combinations(cuts, n):
            value = ''.join('\n' if i in selected else c for i, c in enumerate(flat))
            if protected_edges(source, value):
                found.add(value)
    return tuple(sorted((v for v in found if protected_edges(source, v) and len(v.split('\n')) <= 3
                         and max(map(advance, v.split('\n'))) <= 180),
                        key=lambda v: (v != canonical, abs(v.count('\n')-canonical.count('\n')), v)))


def aggregate(original, units, bound):
    seq = events(original); start = next((i for i, (_, k, d) in enumerate(seq) if k == 'command' and d == ('msgOpen', '')), None)
    if start is None:
        raise ValueError('033 normal explicit initializer required')
    if any(k == 'command' and (d[0].startswith('position') or d[0] in ('option', 'select', 'msgOpenQuick', 'space', 'spacePx')) for _, k, d in seq):
        raise ValueError('033 normal different geometry/control')
    pool = {u['id']: u for u in units}
    @lru_cache(None)
    def solve(at, rows):
        if at == len(seq):
            return ()
        _, kind, data = seq[at]
        if kind == 'literal':
            choices = variants(pool[data.key]['source'], pool[data.key]['translation']) if data.key in pool else (data.text,)
            for value in choices:
                next_rows = list(rows)
                for i, line in enumerate(value.split('\n')):
                    if i: next_rows.append(0)
                    next_rows[-1] += advance(line)
                if len(next_rows) > 3 or any(w > (168 if i == 2 else 180) for i, w in enumerate(next_rows)):
                    continue
                tail = solve(at+1, tuple(next_rows))
                if tail is not None: return ((data.key, value),)+tail
            return None
        name, args = data; width = 0
        if name in ('printPlayerNickname', 'printPlayerName'):
            if args != ARGS: return None
            width = bound if name == 'printPlayerNickname' else 66
        elif name == 'printChip':
            if args != '\t\tbuffer = 0\n\t\tchip = 104\n': return None
            width = 88
        elif name.startswith('print') or name.startswith('callBuffer'):
            return None
        if width:
            limit = 168 if len(rows) == 3 else 180
            if rows[-1]+width > limit: return None
            return solve(at+1, rows[:-1]+(rows[-1]+width,))
        return solve(at+1, (0,) if name == 'clearMsg' else rows)
    found = solve(start+1, (0,))
    if found is None: raise ValueError('033 no same-word normal aggregate placement')
    values = dict(found)
    if not pool.keys() <= values.keys(): raise ValueError('033 normal missing identity')
    return {k: values[k] for k in pool}


def main():
    s = read(SURVEY); cfg = read('project.json'); require_hash(ROOT/BASE, BASE_SHA)
    if s['baseline_sha256'] != BASE_SHA or s['pinned_changed_inputs']: raise ValueError('033 exact survey baseline')
    sp = ROOT/cfg['source_profile']['filename']; require_hash(sp, cfg['source_profile']['sha256']); source = sp.read_bytes(); source_sha = sha(source)
    m = read(BASE.replace('.gba', '.json')); applied = {u['id'] for r in layout_records(m) for u in r['layout']}
    bound = read('analysis/pending_insertion_500_033_aggregate_selection_v1/selection.json')['native_nickname_bound']
    require_hash(ROOT/cfg['text_catalog']['path'], cfg['text_catalog']['sha256'])
    catalog = {f"{r['offset']:X}": r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    require_hash(ROOT/s['pinned_coverage']['path'], s['pinned_coverage']['sha256']); pool = defaultdict(list)
    for p, h in read(s['pinned_coverage']['path'])['draft_asset_hashes'].items():
        require_hash(ROOT/p, h); a = read(p)
        for u in a['units']: pool[u['id']].append((p, h, u, a))
    good = []; bad = []; cache = {}; payloads = {}
    for g in s['unresolved_groups']+s['candidates']:
        arc = g['archive']; row = catalog[arc]
        if not g['ids'] or set(g['ids']) & applied or row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers'] == [0] or 'different_renderer' in g.get('reasons', []): continue
        units = []; refs = []; src = None
        for key in g['ids']:
            choices = pool[key]
            if not choices or len({(u['source'], u['translation'], u['state']) for _, _, u, _ in choices}) != 1: raise ValueError('033 conflicting wording')
            p, h, u, a = choices[0]; src = a['source_tpl']; units.append(u); refs.append(dict(id=key, path=p, sha256=h))
            if arc not in payloads: payloads[arc] = sha(payload_of(source, row))
            if a['source_archive_sha256'] != payloads[arc] or a['source_sha256'] != source_sha or u['state'] != 'needs_review': raise ValueError('033 normal source/policy')
        if arc not in cache:
            require_hash(ROOT/src['path'], src['sha256']); text = (ROOT/src['path']).read_text(encoding='utf-8-sig')
            cache[arc] = {int(x[1]): x[0] for x in re.finditer(r'^script (\d+) \w+ \{[\s\S]*?(?=^script\s|\Z)', text, re.M)}
        original = '@archive '+arc+'\n'+cache[arc][g['script']]; old = {u.key: u.text for u in literals(original)}
        if any(old[u['id']] != u['source'] for u in units): raise ValueError('033 normal source literal mismatch')
        try: values = aggregate(original, units, bound); target = replace_exact(original, values)
        except ValueError as ex:
            bad.append(dict(archive=arc, script=g['script'], ids=g['ids'], reason=str(ex))); continue
        geometry = None; errors = []
        for name, validator in VALIDATORS:
            try: geometry = validator(original, target, [g['script']], set(g['ids']), bound, 88); profile = name; break
            except ValueError as ex: errors.append(str(ex))
        if geometry is None:
            bad.append(dict(archive=arc, script=g['script'], ids=g['ids'], reason=' | '.join(errors))); continue
        good.append(dict(archive=arc, script=g['script'], ids=g['ids'], units=len(units), profile=profile, drafts=refs, source_tpl=src,
                         source_row=row, source_archive_sha256=payloads[arc], explicit_layouts={u['id']: values[u['id']] for u in units if values[u['id']] != u['translation']},
                         geometry=geometry, storage='raw-known-pointer', product_admitted=False))
    frozen_write(ROOT/OUT, dict(schema=1, status='ACTUAL032_NORMAL_AGGREGATE_ANALYSIS_NOT_ROM_ADMISSION', baseline_rom=BASE, baseline_sha256=BASE_SHA,
                  source_sha256=source_sha, native_nickname_bound=bound, candidate_units=sum(g['units'] for g in good), candidate_groups=good,
                  rejections=bad, rejection_counts=dict(Counter(g['reason'] for g in bad)),
                  dependencies={p: sha((ROOT/p).read_bytes()) for p in (SURVEY, 'tools/survey_aggregate_normal_033.py', 'tools/survey_aggregate_pet_033.py',
                    'tools/normal_timing_capacity_025.py', 'tools/normal_player_name_capacity_031.py', 'tools/field_hint_capacity.py')},
                  rom_written=False, new_units_applied=0, release_eligible=False,
                  limits='Analysis only: same canonical words/word spaces/protected edges/controls, existing validators, explicit normal RAW whole scripts. Not source compile/carry/product or runtime approval.'))
    print('033 normal candidates', sum(g['units'] for g in good), 'units', len(good), 'scripts;', Counter(g['profile'] for g in good), flush=True)


if __name__ == '__main__': main()
