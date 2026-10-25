"""Actual source-derived prior append-route composition, no product ROM output."""
from importlib import import_module
from copy import deepcopy
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from layout500_inputs_033 import load_inputs
from layout500_product_033 import append_prior, guard_supported, compose
from layout500_product_032 import guard_unaffected_appended

OUT = 'analysis/pending_insertion_500_033_preallocation500_v1/verification.json'


def main():
    cfg = read('project.json'); sp = ROOT/cfg['source_profile']['filename']; require_hash(sp, cfg['source_profile']['sha256']); source = sp.read_bytes()
    current, summary = load_inputs(source); priors = {}; deps = {}
    for v in ('027', '028', '029', '030', '031', '032'):
        module = import_module('layout500_inputs_'+v); require_hash(ROOT/module.MANIFEST, module.MANIFEST_SHA)
        deps[module.MANIFEST] = module.MANIFEST_SHA
        manifest = read(module.MANIFEST); priors[v] = []
        for r in manifest['archives']:
            require_hash(ROOT/r['compiled']['path'], r['compiled']['sha256'])
            priors[v].append((r, (ROOT/r['compiled']['path']).read_bytes()))
    old_guard = guard_unaffected_appended(priors['032'], priors['027'], priors['028'], priors['030'])
    supported = guard_supported(current, priors['027'], priors['028'], priors['030'])
    bp = ROOT/'poc/output/pending500_032_v1.gba'; meta = read(bp.with_suffix('.json')); require_hash(bp, meta['output_sha256']); baseline = bp.read_bytes()
    parent = {r['archive']: r for r in meta['archives']}; changed = {r['archive']: (r, p) for r, p in current}
    blob = bytearray(); products = {}; records = []; selected = {}
    plugins = ROOT/'analysis/pending_insertion_500_033_carry500_v1/plugins'
    for v in ('027', '028', '030'):
        append_prior(source, blob, products, records, selected, v, priors[v],
                     priors['028'], priors['029'], priors['030'], priors['031'], priors['032'], current, plugins)
    ids = set(); ranges = []; seen = set(); checked = []
    for result in records:
        arc = result['archive']; before = parent[arc]; at = result['rom_offset']; n = result['compiled_bytes']
        actual = bytes(blob[at-len(source):at-len(source)+n])
        expected = changed[arc][1] if arc in changed else baseline[before['rom_offset']:before['rom_offset']+before['compiled_bytes']]
        expected_layout = changed[arc][0]['layout'] if arc in changed else before['layout']
        if arc in seen or actual != expected or result['layout'] != expected_layout or sha(actual) != result['compiled_sha256'] or at & 3:
            raise ValueError('033 preallocation source/current binding '+arc)
        if arc in changed:
            ids.update(changed[arc][0]['new_ids'])
            if not result.get('cumulative033'):
                raise ValueError('033 appended missing final composed scope')
        ranges.append((at, at+n)); seen.add(arc)
        checked.append(dict(archive=arc, changed=arc in changed, payload_sha256=sha(actual),
                            bytes=n, at=at, metadata_preserved=True))
    ranges.sort()
    if any(a[1] > b[0] for a, b in zip(ranges, ranges[1:])) or len(products) != len(records) or len(records) != supported['prior_appended']:
        raise ValueError('033 allocation overlap/population')
    if set(supported['affected_prior_appended']) != set(changed)&seen:
        raise ValueError('033 changed appended routes unaccounted')
    refused = []
    for label, modify in [('duplicate-archive', lambda x: x.append(deepcopy(x[0]))),
                           ('unsupported-new-RAW', lambda x: x[0][0].update(storage='new-raw')),
                           ('compressed-source', lambda x: x[0][0]['source_row'].update(compressed=True))]:
        test = deepcopy(current); modify(test)
        try: guard_supported(test, priors['027'], priors['028'], priors['030'])
        except ValueError as ex: refused.append(dict(label=label, error=str(ex)))
        else: raise ValueError('033 invalid allocation route admitted '+label)
    r, p = next((r, p) for r, p in current if r['archive'] in seen); old = parent[r['archive']]
    raw = baseline[old['rom_offset']:old['rom_offset']+old['compiled_bytes']]; bad = bytes([raw[0]^1])+raw[1:]
    try: compose(r, p, bad, old, plugins)
    except ValueError as ex: refused.append(dict(label='wrong-current-parent-payload', error=str(ex)))
    else: raise ValueError('033 corrupted parent admitted')
    deps.update({p: sha((ROOT/p).read_bytes()) for p in ('tools/verify_exact500_preallocation_033.py',
               'tools/layout500_product_033.py', 'tools/layout500_inputs_033.py',
               'tools/layout500_product_032.py', 'tools/specs/primary032_version.json')})
    frozen_write(ROOT/OUT, dict(schema=1, passed=True, baseline_sha256=meta['output_sha256'],
                  summary=summary, prior032_guard_unchanged=old_guard, new_route=supported,
                  appended_archives=len(records), changed_appended_archives=len(set(changed)&seen),
                  new_units_on_appended_routes=len(ids), products=checked, controlled_refusals=refused,
                  dependencies=deps, rom_written=False, release_eligible=False,
                  limits='In-memory preallocation composition from immutable source and pinned inputs only. No source-to-final-ROM ExpectedWrites, boot, runtime or product output. Does not authorize a500unit cohort or relax old032 guard.'))
    print('PASS033 preallocation', len(records), 'prior roots,', len(set(changed)&seen), 'changed;', len(ids), 'new IDs;', len(refused), 'refusals;NO ROM')


if __name__ == '__main__': main()
