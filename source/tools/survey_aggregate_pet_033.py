"""Actual032 remaining PET pages: finite same-word aggregate LF proposals.

Analysis only. No renderer/provider/storage expansion and no ROM writes.
Existing consumer validators independently own admission of each proposal.
"""
import re
from itertools import combinations
from collections import defaultdict, Counter
from functools import lru_cache
from copy import deepcopy
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from field_hint_capacity import events
from tpl_literals import literals, skeleton
from nickname_capacity import advance, ARGS, CPU
from survey_batch500_020_variables import applicability
from survey_batch500_017_layout import protected_edges
from canonical_literals_031 import canonical_literals
from pet_extended_native_capacity_031 import PREFIX, PROVIDER_BOUNDS, validate as extended
from pet_nickname_capacity_025 import validate as nickname
from pet_profile_capacity_027_v2 import validate as profile
from pet_array_capacity_029 import validate as array
from pet_chip_capacity_030 import validate as chip
from pet_entry_profile_capacity_030 import validate as entry
from pet_guard_capacity_027 import validate as guard
from pet_nickname_flags_capacity_025_v2 import validate as flags
from profile_provider_bounds_027_v2 import bounds as profile_bounds
from chip_profile_bounds_030 import bounds as chip_bounds

SURVEY = 'analysis/pending_insertion_500_033_survey_v1/survey.json'
OUT = 'analysis/pending_insertion_500_033_aggregate_v1/survey.json'
BASE = 'poc/output/pending500_032_v1.gba'
BASE_SHA = 'cc2d02d3fda6ab27601d1735015b24b11d869308dff3e08f0fd4f06f31518f64'
VALIDATORS = [('pet-extended-native', extended), ('pet-native-chip-profile', chip),
              ('pet-array-conditional', array), ('pet-direct-profile', profile),
              ('pet-entry-profile-conditional', entry), ('pet-entry-guards', guard),
              ('pet-flags', flags), ('pet-native-nickname', nickname)]


@lru_cache(None)
def variants(source, canonical):
    """Only interior LF/space interchange; preserve words, spaces and edges."""
    flat = canonical.replace('\n', ' ')
    cuts = [i for i, c in enumerate(flat) if c == ' ' and 0 < i < len(flat)-1]
    found = {canonical}
    for n in range(3):
        for selected in combinations(cuts, n):
            value = ''.join('\n' if i in selected else c for i, c in enumerate(flat))
            if protected_edges(source, value):
                found.add(value)
    return tuple(sorted((v for v in found if protected_edges(source, v)
                         and len(v.split('\n')) <= 3
                         and max(map(advance, v.split('\n'))) <= 132),
                        key=lambda v: (v != canonical, abs(v.count('\n')-canonical.count('\n')), v)))


def replace_exact(tpl, values):
    before = literals(tpl)
    out = canonical_literals(tpl)
    for item in reversed(literals(out)):
        if item.key in values:
            text = values[item.key]
            if any(c in text for c in ('"', '\\', '\r', '\t')):
                raise ValueError('033 unrepresentable translation')
            out = out[:item.start] + '"' + text.replace('\n', '\\n') + '"' + out[item.end:]
    if skeleton(tpl) != skeleton(out):
        raise ValueError('033 control mutation')
    if {u.key: u.text for u in literals(out)} != {u.key: values.get(u.key, u.text) for u in before}:
        raise ValueError('033 lossless replacement')
    return out


def aggregate(original, units, bound):
    seq = events(original)
    if [data for _, kind, data in seq[:4] if kind == 'command'] != PREFIX or any(k != 'command' for _, k, _ in seq[:4]):
        raise ValueError('033 exact PET initializer')
    pool = {u['id']: u for u in units}
    providers = dict(PROVIDER_BOUNDS, printPlayerNickname=bound)

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
                    if i:
                        next_rows.append(0)
                    next_rows[-1] += advance(line)
                if len(next_rows) > 3 or max(next_rows) > 132:
                    continue
                tail = solve(at+1, tuple(next_rows))
                if tail is not None:
                    return ((data.key, value),) + tail
            return None
        name, args = data
        if name in providers:
            if args != ARGS:
                return None
            if rows[-1]+providers[name] > 132:
                return None
            return solve(at+1, rows[:-1]+(rows[-1]+providers[name],))
        if name.startswith('print') or name.startswith('callBuffer') or name in {'option', 'select', 'space', 'spacePx', 'positionText', 'positionBox', 'positionArrow'}:
            return None
        # This search never certifies these controls. The existing strict
        # consumer validator below must accept their original sequence/args.
        return solve(at+1, (0,) if name == 'clearMsg' else rows)

    result = solve(4, (0,))
    if result is None:
        raise ValueError('033 no same-word aggregate placement')
    values = dict(result)
    if not pool.keys() <= values.keys():
        raise ValueError('033 incomplete layout identity')
    return {k: values[k] for k in pool}


def main():
    s = read(SURVEY); cfg = read('project.json'); require_hash(ROOT/BASE, BASE_SHA)
    if s['baseline_sha256'] != BASE_SHA or s['pinned_changed_inputs']:
        raise ValueError('033 exact completed032 survey')
    source_path = ROOT/cfg['source_profile']['filename']; require_hash(source_path, cfg['source_profile']['sha256'])
    source = source_path.read_bytes(); rom = (ROOT/BASE).read_bytes(); meta = read(BASE.replace('.gba', '.json'))
    applied = {u['id'] for r in layout_records(meta) for u in r['layout']}
    bound = applicability(source, rom, read(CPU)); profile_bounds(source, rom); chip_bounds(source, rom)
    require_hash(ROOT/cfg['text_catalog']['path'], cfg['text_catalog']['sha256'])
    rows = {f"{r['offset']:X}": r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    require_hash(ROOT/s['pinned_coverage']['path'], s['pinned_coverage']['sha256'])
    pool = defaultdict(list)
    for p, h in read(s['pinned_coverage']['path'])['draft_asset_hashes'].items():
        require_hash(ROOT/p, h); asset = read(p)
        for u in asset['units']:
            pool[u['id']].append((p, h, u, asset))
    good = []; bad = []; skipped = Counter(); sections = {}; hashes = {}
    for g in s['unresolved_groups'] + s['candidates']:
        if not g['ids'] or set(g['ids']) & applied:
            skipped['empty_or_contains_applied'] += 1; continue
        arc = g['archive']; row = rows[arc]
        if row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers'] == [0]:
            skipped['other_storage'] += 1; continue
        if 'different_renderer' in g.get('reasons', []):
            skipped['other_renderer'] += 1; continue
        units = []; refs = []; src = None
        for key in g['ids']:
            choices = pool[key]
            if not choices or len({(u['source'], u['translation'], u['state']) for _, _, u, _ in choices}) != 1:
                raise ValueError('033 missing/conflicting canonical draft '+key)
            p, h, u, a = choices[0]
            if src is not None and a['source_tpl'] != src:
                raise ValueError('033 inconsistent source reference')
            src = a['source_tpl']; refs.append(dict(id=key, path=p, sha256=h)); units.append(deepcopy(u))
            if arc not in hashes:
                hashes[arc] = sha(payload_of(source, row))
            if a['source_archive_sha256'] != hashes[arc] or a['source_sha256'] != sha(source) or u['state'] != 'needs_review':
                raise ValueError('033 canonical source/review policy')
        if arc not in sections:
            require_hash(ROOT/src['path'], src['sha256'])
            text = (ROOT/src['path']).read_text(encoding='utf-8-sig')
            sections[arc] = {int(x[1]): x[0] for x in re.finditer(r'^script (\d+) \w+ \{[\s\S]*?(?=^script\s|\Z)', text, re.M)}
        original = '@archive '+arc+'\n'+sections[arc][g['script']]
        source_literals = {u.key: u for u in literals(original)}
        if any(source_literals[u['id']].text != u['source'] for u in units):
            raise ValueError('033 current source literal mismatch')
        try:
            values = aggregate(original, units, bound)
            target = replace_exact(original, values)
        except ValueError as ex:
            bad.append(dict(archive=arc, script=g['script'], ids=g['ids'], reason=str(ex))); continue
        errors = []; geometry = None
        for name, validate in VALIDATORS:
            try:
                geometry = validate(original, target, [g['script']], set(g['ids']), bound)
                profile_name = name; break
            except ValueError as ex:
                errors.append(str(ex))
        if geometry is None:
            bad.append(dict(archive=arc, script=g['script'], ids=g['ids'], reason=' | '.join(errors))); continue
        explicit = {u['id']: values[u['id']] for u in units if values[u['id']] != u['translation']}
        good.append(dict(archive=arc, script=g['script'], ids=g['ids'], units=len(units), profile=profile_name,
                         drafts=refs, source_tpl=src, source_row=row, source_archive_sha256=hashes[arc],
                         explicit_layouts=explicit, geometry=geometry, storage='raw-known-pointer', product_admitted=False))
    states = {0: []}
    for g in sorted(good, key=lambda g: (g['archive'], g['script'])):
        for n, chosen in list(states.items()):
            total = n+g['units']
            if total <= 500 and total not in states:
                states[total] = chosen+[g]
    counts = Counter()
    for g in good:
        counts[g['profile']] += g['units']
    deps = [SURVEY, CPU, 'tools/survey_aggregate_pet_033.py', 'tools/canonical_literals_031.py',
            'tools/survey_batch500_017_layout.py', 'tools/profile_provider_bounds_027_v2.py', 'tools/chip_profile_bounds_030.py']
    deps += ['tools/'+v.__module__+'.py' for _, v in VALIDATORS]
    frozen_write(ROOT/OUT, dict(schema=1, status='ACTUAL032_AGGREGATE_SAME_WORD_LF_PROPOSALS_NOT_ROM_ADMISSION',
                               baseline_rom=BASE, baseline_sha256=BASE_SHA, source_sha256=sha(source), native_nickname_bound=bound,
                               dependencies={p: sha((ROOT/p).read_bytes()) for p in deps},
                               candidate_units=sum(g['units'] for g in good), candidate_groups=good, profile_units=dict(counts),
                               selected500=states.get(500), max_reachable_requested_subset=max(states), rejections=bad,
                               rejection_counts=dict(Counter(g['reason'] for g in bad)), skipped_groups=dict(skipped),
                               wording_changed=False, rom_written=False, new_units_applied=0, release_eligible=False,
                               limits=['Finite pinned-draft RAW whole-script PET population, not whole-game remainder.',
                                       'Existing validators independently reproduced; conditional providers retain their native-record/cache prerequisites.',
                                       'Only LF placement; canonical words, word spaces, protected LF/padding edges and controls remain unchanged.',
                                       'Source compile/carry, primary gates, exact writes/repro/runtime and semantic review still required.']))
    print('033 aggregate candidates', sum(g['units'] for g in good), dict(counts), 'exact500', 500 in states, 'max', max(states), flush=True)
    print('Top rejections', Counter(g['reason'] for g in bad).most_common(8), flush=True)


if __name__ == '__main__':
    main()
