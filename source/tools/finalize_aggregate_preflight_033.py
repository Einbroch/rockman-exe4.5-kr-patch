"""Close partial253 preparation, keeping actual032 ROM authority explicit."""
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from compile_layout_candidates_024 import ref
from survey_aggregate_pet_033 import BASE, BASE_SHA, OUT as SURVEY
from prepare_aggregate_pet_033 import OUT as SELECTION
from compile_aggregate_pet_033 import OUT as COMPILE
from merge_aggregate_pet_carry_033 import OUT as CARRY
from archive_scripts import verify_untouched_scripts

OUT = 'analysis/pending_insertion_500_033_preflight_v1/status.json'


def main():
    m = read(BASE.replace('.gba', '.json')); cfg = read('project.json')
    require_hash(ROOT/BASE, BASE_SHA); require_hash(ROOT/BASE.replace('.gba', '_repro.gba'), BASE_SHA)
    require_hash(ROOT/cfg['source_profile']['filename'], cfg['source_profile']['sha256'])
    previous = read('analysis/pending500_032_v1/batch_status.json')
    protected = dict(previous['protected_artifacts'])
    for p, h in protected.items():
        require_hash(ROOT/p, h)
    for name, h in m['build_tools_sha256'].items():
        require_hash(ROOT/'tools'/name, h)
    paths = [SURVEY, SELECTION, COMPILE+'/verification.json', CARRY+'/preflight.json',
             'analysis/pending_insertion_500_033_aggregate_models_v1/result.json']
    reports = [read(p) for p in paths]
    for report in reports:
        for p, h in report.get('dependencies', {}).items():
            require_hash(ROOT/p, h)
        if report.get('baseline_sha256', BASE_SHA) != BASE_SHA or report['rom_written']:
            raise ValueError('033 source-only baseline changed')
    survey, selection, compiled, carry, tests = reports
    if not compiled['passed'] or not carry['passed'] or not tests['passed']:
        raise ValueError('033 incomplete partial preflight')
    if compiled['selection']['sha256'] != sha((ROOT/SELECTION).read_bytes()):
        raise ValueError('033 source compilation selection binding')
    ids = set(selection['selected_ids']); applied = {u['id'] for r in layout_records(m) for u in r['layout']}
    if len(ids) != 253 or ids & applied or compiled['units'] != len(ids) or carry['new_units'] != len(ids):
        raise ValueError('033 actual/new disjoint literal denominator')
    if ids != {u['id'] for r in compiled['archives'] for u in r['units']} or ids != {k for r in carry['archives'] for k in r['new_ids']}:
        raise ValueError('033 selected/compiled/carry identity mismatch')
    for r in compiled['archives']:
        for key in ('compiled', 'target_tpl'):
            require_hash(ROOT/r[key]['path'], r[key]['sha256'])
        if not all(r[k] for k in ('native_roundtrip', 'semantic_roundtrip', 'binary_roundtrip')):
            raise ValueError('033 source-only archive roundtrip')
    primary = {r['archive']: r for r in m['archives']}; base = (ROOT/BASE).read_bytes()
    for r in carry['archives']:
        for key in ('carry_compiled', 'compiled', 'merged_tpl', 'merged_asset'):
            require_hash(ROOT/r[key]['path'], r[key]['sha256'])
        old = primary.get(r['archive'])
        if old is None or old != r['old_record']:
            raise ValueError('033 finite selected current032 primary consumer')
        parent = (ROOT/r['carry_compiled']['path']).read_bytes(); target = (ROOT/r['compiled']['path']).read_bytes()
        at = old['rom_offset']
        if parent != base[at:at+old['compiled_bytes']] or sha(parent) != old['compiled_sha256']:
            raise ValueError('033 cumulative032 source reconstruction mismatch')
        kept = verify_untouched_scripts(parent, target, r['script_count'], set(r['new_scripts']))
        if kept != r['unselected_parent_scripts']:
            raise ValueError('033 unselected-parent byte proof mismatch')
        old_layout = {u['id']: u for u in old['layout']}; after = {u['id']: u for u in r['layout']}
        if any(after.get(k) != v for k, v in old_layout.items()):
            raise ValueError('033 richer prior consumer layout changed')
        merged = read(r['merged_asset']['path'])
        if {u['id'] for u in merged['units']} != set(after) or not r['carry_reconstructed_from_source_and_assets']:
            raise ValueError('033 merged asset/layout or provenance')
    prior_appended = set()
    for path in ('analysis/pending_insertion_500_027_carry_v2/preflight.json',
                 'analysis/pending_insertion_500_028_carry_v1/preflight.json',
                 'analysis/pending_insertion_500_030_carry_v1/preflight.json'):
        prior_appended.update(r['archive'] for r in read(path)['archives'] if r['storage'] == 'new-raw')
    affected = sorted(prior_appended & {g['archive'] for g in selection['groups']})
    if (ROOT/'poc/output/pending500_033_v1.gba').exists():
        raise ValueError('033 partial source-only status cannot supersede actual033 ROM')
    frozen_write(ROOT/OUT, dict(schema=1, status='PARTIAL253_SOURCE_COMPILED_CUMULATIVE032_CARRY_VERIFIED_NOT500_OR_ROM',
                  baseline_rom=BASE, baseline_sha256=BASE_SHA, actual_applied_total=m['translated_units'],
                  new_units_applied=0, source_compiled_candidates=len(ids), source_compiled_archives=len(compiled['archives']),
                  source_compiled_whole_scripts=len(selection['groups']), lf_layout_changes=len(compiled['within_page_lf_edits']),
                  font_glyphs_verified=compiled['extended_glyphs_checked'], carry_units_in_changed_archives=carry['carry_units_in_changed_archives'],
                  requested_next_cohort=500, additional_safe_units_needed=500-len(ids), selected_ids=sorted(ids),
                  affected_prior_appended_archives=affected, reports=[ref(ROOT/p) for p in paths],
                  checker=ref(ROOT/'tools/finalize_aggregate_preflight_033.py'),
                  source_and_previous_artifacts_preserved=True, pinned032_build_tools_unchanged=True,
                  new_distribution_packages_created=False, rom_written=False, runtime_tested=False,
                  release_eligible=False, complete_integrated_request=False,
                  limits=['253 source-only candidates, NOT an applied500cohort. Actual current ROM remains032/17122units.',
                          'Canonical needs_review wording unchanged, only103 explicit LF placements. Geometry/compilation are not semantic or runtime approval.',
                          'Do not inject source-only full archives: cumulative carry output is separate and still needs primary ownership/gates.',
                          'Twenty prior-appended RAW archives require composition before their one allocation; frozen032 guard must remain enabled.',
                          'Conditional native name/profile/cache bounds remain prerequisites; no automatic Hangul commit/save/fresh redisplay or full-game completion.'],
                  next_action='Find247additional safe literal units (calendar13is a separate possible subset, not whole-game remainder). Freeze exact500, integrate source-bound page/provider gates and033 pre-allocation composition across027/028/030 roots, immutable-source primary/repro/whole diff/CPU and actual new-ROM render/clear/exit/reentry. No BPS/xdelta/ZIP until requested.'))
    print('PASS033 preflight', len(ids), 'compiled/carry units;', carry['carry_units_in_changed_archives'], 'prior preserved;',
          len(affected), 'prior-appended roots; actual032', m['translated_units'], '+0; NO ROM/package')


if __name__ == '__main__':
    main()
