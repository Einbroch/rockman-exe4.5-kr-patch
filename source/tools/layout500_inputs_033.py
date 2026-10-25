"""Exact500 source-bound input gate against actual cumulative032.

Canonical wording/protected edges, all37parent bytes, current page/choice
models and native provider bounds verified before primary allocation.
No candidate search, ROM allocation, runtime or release approval here.
"""
import re
from collections import Counter, defaultdict
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from tpl_literals import literals, resolve_units, skeleton
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts
from prepare_repartition500 import layout_records
from survey_pet_quick_reflow_024 import replace_for_analysis
from survey_batch500_017_layout import protected_edges
from survey_aggregate_pet_033 import replace_exact
from pet_profile_capacity_027_v2 import validate as profile_validate
from profile_provider_bounds_027_v2 import bounds as profile_bounds
from pet_array_capacity_029 import validate as array_validate
from array_provider_bounds_029 import bounds as array_bounds
from pet_chip_capacity_030 import validate as chip_validate
from chip_profile_bounds_030 import bounds as chip_bounds
from pet_extended_native_capacity_031 import validate as extended_validate
from event_dialogue_capacity_031 import validate as event_validate
from calendar_delete_capacity_031 import validate as calendar_validate
from calendar_aqua_capacity_033 import validate as aqua_validate
from calendar_menu_capacity_032_v2 import validate as menu_validate
from normal_vertical_choices_033 import validate as multi_vertical_validate
from profile_manager_capacity_033 import validate as manager_validate
from field_hint_capacity import validate as full_validate
from pet_nickname_capacity_025 import validate as quick_validate
from normal_battle_choice_capacity_026 import validate as choice_validate
from normal_vertical_choice_capacity_026 import validate as vertical_validate
from pet_choice_capacity_026 import validate as pet_choice_validate
from normal_timing_capacity_025 import validate as normal_validate
from pet_nickname_flags_capacity_025_v2 import validate as flags_validate
from build_development_patch import literal_scope, validate_literal_numerals, translate_literal_scope

MANIFEST = 'analysis/pending_insertion_500_033_carry500_v1/preflight.json'
MANIFEST_SHA = '5369e2461f76ed30e93eb62c79eedabdcc9a3586e39d626c02f2af2c362fc2a8'
OUT = 'analysis/pending_insertion_500_033_input_gate500_v1/verification.json'


def checked_ref(ref):
    require_hash(ROOT/ref['path'], ref['sha256'])
    return ROOT/ref['path']


def literal_values(tpl):
    return [(i.key, i.language, i.text) for i in literals(tpl)]


def validate_group(original, target, group, units):
    """Exact selected wording/scope plus current consumer-specific geometry."""
    ids = [u['id'] for u in units]
    if len(ids) != len(set(ids)) or set(ids) != set(group['ids']):
        raise ValueError('025 group ID denominator')
    if any(int(key.split(':')[1]) != group['script'] for key in ids):
        raise ValueError('025 group script identity')
    # Standalone punctuation/provider delimiters stay byte-identical and are
    # included in page geometry, but are not Japanese translation units.
    source_ids = {i.key for i in literals(original)
                  if int(i.key.split(':')[1]) == group['script']
                  and re.search(r'[\u3040-\u30ff\u3400-\u9fff]',i.text)}
    if source_ids != set(ids):
        raise ValueError('025 whole-script population')
    expected = []
    for link in group['drafts']:
        asset = read(checked_ref(link))
        matches = [u for u in asset['units'] if u['id'] == link['id']]
        if len(matches) != 1 or asset['source_tpl'] != group['source_tpl']:
            raise ValueError('025 draft identity')
        unit = matches[0]
        value = group['explicit_layouts'].get(unit['id'], unit['translation'])
        if value.replace('\n', ' ') != unit['translation'].replace('\n', ' ') or not protected_edges(unit['source'],value):
            raise ValueError('025 prose changed')
        expected.append(dict(id=unit['id'], source=unit['source'],
                             translation=value, state=unit['state']))
    if sorted(units, key=lambda u:u['id']) != sorted(expected, key=lambda u:u['id']):
        raise ValueError('025 selected wording/state changed')
    validate_literal_numerals(units, dict(preserve_literal_numerals=True))
    proposed = replace_exact(original, {u['id']:u['translation'] for u in units})
    actual = {i.key:i.text for i in literals(target)}
    if any(actual.get(u['id']) != u['translation'] for u in units):
        raise ValueError('025 merged target differs from selected wording')
    args = (original, proposed, [group['script']], set(ids))
    profile = group['profile']
    if profile == 'calendar-aqua-early-sfx':
        proof = aqua_validate(*args, 99)
    elif profile == 'calendar-menu':
        proof = menu_validate(*args, 99)
    elif profile == 'normal-vertical-2or3':
        proof = multi_vertical_validate(*args, 99, 88)
    elif profile == 'profile-manager-nonclear':
        proof = manager_validate(*args, 99)
    elif profile == 'calendar-delete-quick':
        proof = calendar_validate(*args, 99)
    elif profile == 'event-pages':
        proof = event_validate(*args, 99)
    elif profile == 'pet-extended-native':
        proof = extended_validate(*args, 99)
    elif profile == 'pet-native-chip-profile':
        proof = chip_validate(*args, 99)
    elif profile == 'pet-array-conditional':
        proof = array_validate(*args, 99)
    elif profile == 'pet-direct-profile':
        proof = profile_validate(*args, 99)
    elif profile == 'fullbox':
        proof = full_validate(*args, 99, 88)
    elif profile == 'pet-native-nickname':
        proof = quick_validate(*args, 99)
    elif profile == 'pet-flags':
        proof = flags_validate(*args, 99)
    elif profile == 'normal-horizontal-choice':
        proof = choice_validate(*args, 99, 88)
    elif profile == 'normal-vertical-choice':
        proof = vertical_validate(*args, 99, 88)
    elif profile == 'pet-fixed-choice':
        proof = pet_choice_validate(*args, 99)
    elif profile in ('normal-pages', 'normal-within-page-lf-proposal'):
        proof = normal_validate(*args, 99, 88)
    else:
        raise ValueError('025 unknown consumer profile')
    if proof != group['geometry']:
        raise ValueError('025 current page geometry differs')
    return proof


def load_inputs(source):
    require_hash(ROOT/MANIFEST, MANIFEST_SHA)
    manifest = read(MANIFEST)
    if sha(source) != manifest['source_sha256'] or not manifest['passed']:
        raise ValueError('025 immutable source applicability')
    for p,h in manifest['dependencies'].items():
        require_hash(ROOT/p,h)
    selection = read('analysis/pending_insertion_500_033_exact500_selection_v1/selection.json')
    mechanical = read('analysis/pending_insertion_500_033_compile500_v1/verification.json')
    for record in (selection, mechanical):
        for p,h in record['dependencies'].items():
            require_hash(ROOT/p,h)
    CPU='analysis/pending_insertion_500_031_opponent_chip_cpu_v1/cpu.json'
    for path in selection['dependencies']:
        evidence=read(path) if path.endswith('.json') else None
        if isinstance(evidence,dict):
            if evidence.get('passed') is False:raise ValueError('031 source preparation evidence failed')
            for dep,h in evidence.get('dependencies',{}).items():require_hash(ROOT/dep,h)
    cfg = read('project.json')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    from verify_tpi_index import parse_tpi
    catalog = {format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    baseline_path = ROOT/manifest['baseline_rom']
    require_hash(baseline_path, manifest['baseline_sha256'])
    baseline = baseline_path.read_bytes()
    for evidence_path in (CPU,'analysis/pending_insertion_500_025_native_controls_v1/cpu.json'):
        evidence=read(evidence_path)
        if not evidence['passed']:raise ValueError('026 native control evidence failed')
        for region in evidence['native_ranges']:
            offset,n=region['offset'],region['bytes']
            if sha(source[offset:offset+n])!=region['sha256'] or baseline[offset:offset+n]!=source[offset:offset+n]:
                raise ValueError('026 native control applicability changed')
    profile_bounds(source,baseline)
    array_bounds(source,baseline)
    chip_bounds(source,baseline)
    meta = read(baseline_path.with_suffix('.json'))
    parents = {r['archive']:r for r in meta['archives']}
    parents.update({r['archive']:r for r in meta['keyitem_rom']['hint_archives']})
    # The legacy A3 input stage has one adopted explicit LF layout. Compare
    # its effective pinned input, not the earlier draft before that layout.
    from hint_rom_data import input_entries
    hint_assets = {a['archive']:a for _,_,a,_,_,_,_ in input_entries(source)}
    applied = {u['id'] for r in layout_records(meta) for u in r['layout']}
    groups = defaultdict(list)
    for group in selection['groups']:
        groups[group['archive']].append(group)
    if len(manifest['archives']) != 37 or len({r['archive'] for r in manifest['archives']}) != 37 or set(groups) != {r['archive'] for r in manifest['archives']}:
        raise ValueError('025 archive population')
    new_ids = set()
    counts = Counter()
    admitted = []
    for record in manifest['archives']:
        arc = record['archive']
        if record['source_row'] != catalog[arc]:
            raise ValueError('025 catalog row/reference applicability')
        native = payload_of(source, record['source_row'])
        if sha(native) != record['source_payload_sha256']:
            raise ValueError('025 native payload applicability')
        parent = parents.get(arc)
        if parent != record['old_record']:
            raise ValueError('025 actual024 parent identity')
        if record['storage']!=('raw-carry' if parent else 'new-raw'):raise ValueError('028 exact raw/new storage')
        carry = checked_ref(record['carry_compiled']).read_bytes()
        old_bytes = baseline[parent['rom_offset']:parent['rom_offset']+parent['compiled_bytes']] if parent else native
        if carry != old_bytes or sha(carry) != record['parent_compiled_sha256']:
            raise ValueError('025 source reconstructed carry mismatch')
        asset = read(checked_ref(record['merged_asset']))
        units = resolve_units(asset)
        if len(units) != record['carry_units']+record['new_units']:
            raise ValueError('025 merged unit population')
        ids = {u['id'] for u in units}
        selected = set(record['new_ids'])
        if len(ids) != len(units) or selected & (new_ids | applied) or not selected <= ids:
            raise ValueError('025 distinct actual new IDs')
        old_ids = ids-selected
        if old_ids != ({r['id'] for r in parent['layout']} if parent else set()):
            raise ValueError('025 carry ID population')
        if old_ids:
            parent_asset = read(checked_ref(record['parent']))
            old_units = resolve_units(hint_assets[arc] if record['storage']=='A3-clone-merge' else parent_asset)
            if {u['id']:u for u in units if u['id'] in old_ids} != {u['id']:u for u in old_units}:
                raise ValueError('025 prior wording/state changed')
        original = checked_ref(groups[arc][0]['source_tpl']).read_text(encoding='utf-8-sig')
        target = checked_ref(record['merged_tpl']).read_text(encoding='utf-8-sig')
        # Legacy assets retain their own adopted review/layout policy. Only
        # the new disjoint units use the narrow needs_review LF adapter.
        steps=[parent[k] for k in ('cumulative024','cumulative025','cumulative026','cumulative027','cumulative028','cumulative029','cumulative030','cumulative031','cumulative032') if parent and parent.get(k)]
        introduced=set().union(*(set(step['new_ids']) for step in steps)) if steps else set()
        base_units=[u for u in units if u['id'] in old_ids and u['id'] not in introduced]
        first_scope=steps[0]['parent_scope'] if steps else record['parent_scope']
        carry_target=translate_literal_scope(original,base_units,first_scope) if base_units else original
        for step in steps:
            step_ids=set(step['new_ids'])
            carry_target=replace_for_analysis(carry_target,[u for u in units if u['id'] in old_ids and u['id'] in step_ids])
        expected = replace_for_analysis(carry_target, [u for u in units if u['id'] in selected])
        if skeleton(target) != skeleton(original) or literal_values(target) != literal_values(expected):
            raise ValueError('025 source commands/merged literals changed')
        for group in groups[arc]:
            subset = [u for u in units if u['id'] in set(group['ids'])]
            validate_group(original, target, group, subset)
            counts[group['profile']] += len(subset)
        for key in old_ids:
            before,after = literal_scope(record['parent_scope'],key),literal_scope(record['scope'],key)
            if any(before.get(k) != after.get(k) for k in ('consumer','literal_language','max_literal_rows','max_line_advance')):
                raise ValueError('025 inherited consumer contract changed')
        payload = checked_ref(record['compiled']).read_bytes()
        if len(payload) != record['compiled_bytes'] or len(payload)>65535:
            raise ValueError('025 payload16bit capacity')
        preserved = verify_untouched_scripts(carry,payload,record['script_count'],set(record['new_scripts']))
        if preserved != record['unselected_parent_scripts']:
            raise ValueError('025 unselected prior bytes changed')
        if set(record['new_scripts']) != {int(i.split(':')[1]) for i in selected}:
            raise ValueError('025 selected script identity')
        new_ids |= selected
        admitted.append((record,payload))
    if len(new_ids) != 500 or new_ids != set(selection['selected_ids']) or counts != Counter(selection['profiles']):
        raise ValueError('025 exact500/profile denominator')
    return admitted, dict(new_units=len(new_ids), carry_units=sum(r['carry_units'] for r,_ in admitted),
                         archives=len(admitted), profiles=dict(counts),
                         storage=dict(Counter(r['storage'] for r,_ in admitted)))


def main():
    cfg = read('project.json')
    source_path = ROOT/cfg['source_profile']['filename']
    require_hash(source_path,cfg['source_profile']['sha256'])
    _, summary = load_inputs(source_path.read_bytes())
    deps = [MANIFEST, 'tools/layout500_inputs_033.py','tools/calendar_delete_capacity_031.py','tools/event_dialogue_capacity_031.py','tools/pet_extended_native_capacity_031.py', 'tools/field_hint_capacity.py',
            'tools/pet_nickname_capacity_025.py','tools/normal_battle_choice_capacity_026.py','tools/normal_vertical_choice_capacity_026.py','tools/pet_choice_capacity_026.py','tools/normal_timing_capacity_025.py',
            'tools/pet_nickname_flags_capacity_025_v2.py','tools/tpl_literals.py',
            'tools/archive_scripts.py','tools/build_development_patch.py']
    frozen_write(ROOT/OUT, dict(schema=1,status='CUMULATIVE_INPUT_GATE_PASS_NOT_PRIMARY_ROM_BUILD',
        passed=True,**summary,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},
        source_sha256=sha(source_path.read_bytes()),
        baseline_rom='poc/output/pending500_032_v1.gba',
        baseline_sha256='cc2d02d3fda6ab27601d1735015b24b11d869308dff3e08f0fd4f06f31518f64',
        rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,
        limits='Fresh source-bound input, wording, current geometry and actual025 carry verification. '
               'Primary raw/A3 allocation, inherited B0/other-clone verification, ExpectedWrites and '
               'independent product rebuild plus actual026 runtime remain pending. Fixed conditional/flag '
               'commands are source-preserved, not executed by the spatial models.'))
    print('PASS025 cumulative input gate',summary)


if __name__ == '__main__':
    main()
