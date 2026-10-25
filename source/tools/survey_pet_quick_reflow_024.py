"""Analyze within-page LF expansion; never edits drafts, build gates or ROM.

This is a proposed layout policy, not permission to inject its output. Exact
native quick-box commands and aggregate pages are still checked separately.
"""
from functools import lru_cache
from collections import defaultdict, Counter
from copy import deepcopy
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from tpl_literals import literals, serialize, skeleton
from pet_quick_capacity import validate
from nickname_capacity import advance


def place(text):
    # No removal of protected leading/trailing rows, padding, or word spaces.
    # Keep this proposal narrow: only ordinary complete, unpadded paragraphs.
    if text != text.strip() or text.count('\n') > 2:
        return None
    flat = text.replace('\n', ' ')
    @lru_cache(None)
    def solve(at, rows):
        if rows == 1:
            tail = flat[at:]
            return (tail,) if tail and advance(tail) <= 132 else None
        choices = []
        for end in range(at + 1, len(flat)):
            if flat[end] != ' ':
                continue
            line = flat[at:end]
            if advance(line) > 132:
                break
            if line.endswith(' '):
                continue
            rest = solve(end + 1, rows - 1)
            if rest:
                choices.append((line,) + rest)
        return min(choices, key=lambda xs: (max(map(advance, xs)), xs)) if choices else None
    for rows in range(text.count('\n') + 1, 4):
        lines = solve(0, rows)
        if lines:
            result = '\n'.join(lines)
            if result.replace('\n', ' ') != flat:
                raise ValueError('Wording changed')
            return result
    return None


def replace_for_analysis(tpl, units):
    indexed = {u['id']: u for u in units}
    if len(indexed) != len(units):
        raise ValueError('Duplicate ID')
    edits = []
    for item in literals(tpl):
        if item.key not in indexed:
            continue
        u = indexed[item.key]
        if item.language != 'mmbn45' or u['source'] != item.text or u['state'] != 'needs_review':
            raise ValueError('Source/review identity')
        edits.append((item.start, item.end, serialize(u['translation'])))
    if len(edits) != len(units):
        raise ValueError('Missing ID')
    out = tpl
    for start, end, value in reversed(edits):
        out = out[:start] + value + out[end:]
    if skeleton(out) != skeleton(tpl):
        raise ValueError('Command topology changed')
    return out


def main(out='analysis/pending_insertion_500_024_quick_reflow_v2/survey.json'):
    survey_path = 'analysis/pending_insertion_500_024_survey_v1/survey.json'
    s = read(survey_path)
    require_hash(ROOT/s['baseline_rom'], s['baseline_sha256'])
    require_hash(ROOT/s['pinned_coverage']['path'], s['pinned_coverage']['sha256'])
    pool = defaultdict(list)
    for path, digest in read(s['pinned_coverage']['path'])['draft_asset_hashes'].items():
        require_hash(ROOT/path, digest)
        a = read(path)
        for u in a['units']:
            pool[u['id']].append((path, digest, u, a))
    good, bad = [], []
    from verify_tpi_index import parse_tpi
    cfg = read('project.json')
    require_hash(ROOT/cfg['text_catalog']['path'], cfg['text_catalog']['sha256'])
    rows = {format(r['offset'], 'X'): r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    for g in s['unresolved_groups'] + s['candidates']:
        if not set(g.get('reasons', [])) <= {'adopted_normal_geometry'}:
            continue
        row = rows[g['archive']]
        if row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers'] == [0]:
            continue
        units, refs, layouts = [], [], {}
        for key in g['ids']:
            opts = pool[key]
            if not opts or len({(u['source'], u['translation'], u['state']) for _, _, u, _ in opts}) != 1:
                raise ValueError('Absent/conflicting frozen wording')
            path, digest, u, a = opts[0]
            u = deepcopy(u)
            value = place(u['translation'])
            if value is None:
                bad.append(dict(archive=g['archive'], script=g['script'], reason='within-three-rows-wording-placement'))
                break
            if value != u['translation']:
                layouts[key] = dict(before=u['translation'], after=value, added_lf=value.count('\n')-u['translation'].count('\n'))
            u['translation'] = value
            units.append(u)
            refs.append(dict(id=key, path=path, sha256=digest))
        else:
            ref = a['source_tpl']
            require_hash(ROOT/ref['path'], ref['sha256'])
            tpl = (ROOT/ref['path']).read_text(encoding='utf-8-sig')
            try:
                proof = validate(tpl, replace_for_analysis(tpl, units), [g['script']], set(g['ids']))
            except ValueError as ex:
                bad.append(dict(archive=g['archive'], script=g['script'], reason=str(ex)))
                continue
            good.append(dict(archive=g['archive'], script=g['script'], ids=g['ids'], units=len(g['ids']), drafts=refs, source_tpl=ref, layouts=layouts, geometry=proof, source_row=row, product_admitted=False))
    states = {0: []}
    for g in sorted(good, key=lambda x: (x['archive'], x['script'])):
        for n, selected in list(states.items()):
            if n+g['units'] <= 500 and n+g['units'] not in states:
                states[n+g['units']] = selected+[g]
    deps = [survey_path, 'tools/survey_pet_quick_reflow_024.py', 'tools/pet_quick_capacity.py', 'tools/nickname_capacity.py', 'tools/tpl_literals.py']
    result = dict(schema=1, status='PROPOSED_WITHIN_PAGE_LF_POLICY_ANALYSIS_ONLY', baseline_rom=s['baseline_rom'], baseline_sha256=s['baseline_sha256'], source_sha256=s['source_sha256'], dependencies={p: sha((ROOT/p).read_bytes()) for p in deps}, candidate_units=sum(g['units'] for g in good), candidate_groups=good, selected500=states.get(500), max_reachable_requested_subset=max(states), rejections=bad, rejection_counts=dict(Counter(b['reason'] for b in bad)), prose_changed=False, rom_written=False, release_eligible=False, limits='Frozen wording, word spaces and command order preserved; proposed LF expansion inside existing waited pages only, at most3rows/132px each. No new page/wait/window or variable allowance. Not adopted production policy: source-bound compiler gate, LF opcode/clear lifetime/consumer applicability, binary roundtrips, carry, exact-ROM CPU/runtime checks remain required.')
    frozen_write(ROOT/out, result)
    print('Proposed quick units', result['candidate_units'], 'exact500', 500 in states)
    print(result['rejection_counts'])


if __name__ == '__main__':
    main()
