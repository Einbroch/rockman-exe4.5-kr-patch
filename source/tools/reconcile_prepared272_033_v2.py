"""Reconcile253+19 source/carry preparation. Not500, ROM application or release."""
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from compile_layout_candidates_024 import ref
from archive_scripts import verify_untouched_scripts, script_spans
from tpl_literals import literals, skeleton
from field_hint_capacity import events

OUT = 'analysis/pending_insertion_500_033_preflight272_v2/status.json'
SETS = [('analysis/pending_insertion_500_033_aggregate_selection_v1/selection.json',
         'analysis/pending_insertion_500_033_compile253_v1/verification.json',
         'analysis/pending_insertion_500_033_carry253_v1/preflight.json'),
        ('analysis/pending_insertion_500_033_supplement19_selection_v1/selection.json',
         'analysis/pending_insertion_500_033_compile19_v2/verification.json',
         'analysis/pending_insertion_500_033_carry19_v1/preflight.json')]


def main():
    cfg = read('project.json'); source_path = ROOT/cfg['source_profile']['filename']; require_hash(source_path, cfg['source_profile']['sha256'])
    base = 'poc/output/pending500_032_v1.gba'; m = read(base.replace('.gba', '.json')); require_hash(ROOT/base, m['output_sha256']); require_hash(ROOT/base.replace('.gba', '_repro.gba'), m['output_sha256'])
    baseline = (ROOT/base).read_bytes(); applied = {u['id'] for r in layout_records(m) for u in r['layout']}; parents = {r['archive']: r for r in m['archives']}
    decision_path = 'analysis/pending_insertion_500_033_batch_policy_v1/decision.json'; decision = read(decision_path)
    if decision['required_new_literal_units_per_cohort'] != 500 or decision['partial253_rom_application_approved']: raise ValueError('033 exact500 human decision')
    seen = set(); archive_set = set(); profiles = Counter(); old_count = 0; references = []
    for selection_path, compiled_path, carry_path in SETS:
        selection, compiled, carry = [read(p) for p in (selection_path, compiled_path, carry_path)]
        for path, report in zip((selection_path, compiled_path, carry_path), (selection, compiled, carry)):
            if report['baseline_sha256'] != m['output_sha256'] or report['rom_written']: raise ValueError('033 current source-only baseline')
            for p, h in report['dependencies'].items(): require_hash(ROOT/p, h)
            references.append(ref(ROOT/path))
        ids = set(selection['selected_ids'])
        if ids & (seen | applied) or len(ids) != compiled['units'] or len(ids) != carry['new_units'] or not compiled['passed'] or not carry['passed'] or compiled['selection']['sha256'] != sha((ROOT/selection_path).read_bytes()): raise ValueError('033 duplicate or inconsistent source-only identities')
        if ids != {u['id'] for r in compiled['archives'] for u in r['units']} or ids != {k for r in carry['archives'] for k in r['new_ids']}: raise ValueError('033 selected/compiled/carry union')
        for r in compiled['archives']:
            for field in ('compiled', 'target_tpl'): require_hash(ROOT/r[field]['path'], r[field]['sha256'])
            if not all(r[k] for k in ('native_roundtrip', 'semantic_roundtrip', 'binary_roundtrip')): raise ValueError('033 source compile roundtrip')
        for r in carry['archives']:
            arc = r['archive']
            if arc in archive_set: raise ValueError('033 prepared cohorts overlap archive; explicit pre-allocation composition required')
            archive_set.add(arc); parent = parents[arc]
            if r['old_record'] != parent: raise ValueError('033 carry parent metadata')
            for field in ('carry_compiled', 'compiled', 'merged_tpl', 'merged_asset'): require_hash(ROOT/r[field]['path'], r[field]['sha256'])
            old = (ROOT/r['carry_compiled']['path']).read_bytes(); target = (ROOT/r['compiled']['path']).read_bytes(); at = parent['rom_offset']
            if old != baseline[at:at+parent['compiled_bytes']] or sha(old) != parent['compiled_sha256']: raise ValueError('033 carry actual032 bytes')
            if verify_untouched_scripts(old, target, r['script_count'], set(r['new_scripts'])) != r['unselected_parent_scripts']: raise ValueError('033 unselected parent bytes')
            old_layout = {u['id']: u for u in parent['layout']}; after = {u['id']: u for u in r['layout']}
            if any(after.get(k) != v for k, v in old_layout.items()): raise ValueError('033 prior richer display metrics')
            old_count += r['carry_units']
        seen |= ids
        for g in selection['groups']: profiles[g['profile']] += g['units']
    # Explicitly inspect the compiled Aqua command prefix. The spatial view
    # normalized FD09, but the actual source and target retain early FD09.
    cc = read(SETS[1][1]); aqua = next(r for r in cc['archives'] if r['archive'] == '697B70')
    original = (ROOT/aqua['source_tpl']['path']).read_text(encoding='utf-8-sig'); target = (ROOT/aqua['target_tpl']['path']).read_text(encoding='utf-8-sig')
    if skeleton(original) != skeleton(target): raise ValueError('033 actual Aqua controls moved')
    native = (ROOT/'analysis/pending_insertion_500_033_compile19_v2/697B70/697B70_native.msg').read_bytes()
    compiled = (ROOT/aqua['compiled']['path']).read_bytes(); a = script_spans(native, aqua['script_count']); b = script_spans(compiled, aqua['script_count'])
    for script in (50, 51, 52):
        if a[script][:12] != bytes.fromhex('fc06e702f40028f00000fd09') or b[script][:12] != a[script][:12] or b[script].count(b'\xFD\x09') != 1:
            raise ValueError('033 actual compiled early FD09 bytes '+str(script))
    extra_reports = ['analysis/pending_insertion_500_033_choice_sfx_cpu_v1/cpu.json', 'analysis/pending_insertion_500_033_aqua_models_v1/result.json']
    for p in extra_reports:
        report = read(p)
        if not report['passed']: raise ValueError('033 supplemental native/model evidence')
        for dep, h in report['dependencies'].items(): require_hash(ROOT/dep, h)
        references.append(ref(ROOT/p))
    previous = read('analysis/pending500_032_v1/batch_status.json')
    for p, h in previous['protected_artifacts'].items(): require_hash(ROOT/p, h)
    for name, h in m['build_tools_sha256'].items(): require_hash(ROOT/'tools'/name, h)
    if len(seen) != 272 or (ROOT/'poc/output/pending500_033_v1.gba').exists(): raise ValueError('033 partial272 cannot supersede a033ROM')
    frozen_write(ROOT/OUT, dict(schema=1, status='PARTIAL272_SOURCE_COMPILED_CUMULATIVE032_CARRY_VERIFIED_NOT500_OR_ROM',
                  baseline_rom=base, baseline_sha256=m['output_sha256'], actual_applied_total=m['translated_units'], new_units_applied=0,
                  source_compiled_candidates=len(seen), source_compiled_archives=len(archive_set), source_compiled_whole_scripts=sum(len(read(p)['groups']) for p, _, _ in SETS),
                  carry_units_in_changed_archives=old_count, requested_next_cohort=500, additional_safe_units_needed=500-len(seen),
                  selected_ids=sorted(seen), profiles=dict(profiles), user_decision=ref(ROOT/decision_path), reports=references,
                  checker=ref(ROOT/'tools/reconcile_prepared272_033_v2.py'),
                  source_and_previous_artifacts_preserved=True, new_distribution_packages_created=False,
                  rom_written=False, runtime_tested=False, release_eligible=False,
                  limits=['272 prepared source-only units, NOT500 or an applied033ROM. Actual current ROM remains032/17122.',
                          'Aqua actual original/compiled FD09 remains in its early position; CPU/model evidence is not GBA sound/choice approval.',
                          'Calendar13is now source-prepared, but still Japanese in actual032 until exact500 product integration.',
                          'Native provider/title/date/cache conditions, all current input/primary gates/preallocation/exactwrites/repro/new-ROM runtime and semantic review remain open.',
                          'The earlier partial253 primary module was never adopted or executed and is not authorized by the exact500 decision.'],
                  next_action='Find228additional safe units, freeze exact500, combine source-bound gates including Aqua FD09 and general pages, preserve20 prior-appended composition, then immutable-source primary/repro/static/CPU/new-ROM render/clear/exit/reentry. No packages until requested.'))
    print('PASS033 prepared', len(seen), 'units;', old_count, 'prior units preserved;', len(archive_set), 'archives; need', 500-len(seen), '; actual032 +0;NO ROM')


if __name__ == '__main__': main()
