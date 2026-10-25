"""Current024 authority: source-only500 and023 shared-consumer evidence."""
import subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records


def main():
    paths=['analysis/pending_insertion_500_024_checkpoint_v2/checkpoint.json','analysis/pending_insertion_500_024_selection_v1/selection.json','analysis/pending_insertion_500_024_compile500_v1/verification.json','analysis/pending_insertion_500_024_shared_runtime_v1/verification.json']
    previous,selection,compiled,runtime=(read(p) for p in paths)
    for r in (selection,compiled,runtime):
        if r['baseline_sha256']!=previous['baseline_sha256']:raise ValueError('One exact023 baseline')
    if not compiled['passed'] or compiled['rom_written'] or compiled['insertion_ready'] or not runtime['passed'] or runtime['new500_rendered'] or not runtime['read_alias_diagnostic']:raise ValueError('Component scope/promotion')
    for r in (selection,compiled):
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
    for p,h in previous['preserved_artifacts'].items():require_hash(ROOT/p,h)
    ids=[u['id'] for r in compiled['archives'] for u in r['units']]
    meta=read(previous['baseline_rom'].replace('.gba','.json'));applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    if len(ids)!=500 or len(set(ids))!=500 or set(ids)!=set(selection['selected_ids']) or applied&set(ids):raise ValueError('Exact500 distinct not applied')
    for r in compiled['archives']:
        for k in ('source_tpl','compiled','target_tpl'):require_hash(ROOT/r[k]['path'],r[k]['sha256'])
        if not all(r[k] for k in ('native_roundtrip','semantic_roundtrip','binary_roundtrip')) or r['product_admitted']:raise ValueError('Source-only archive invariant')
    for k in ('receipt','source_asset','contact_sheet'):require_hash(ROOT/runtime[k]['path'],runtime[k]['sha256'])
    outputs=[]
    for pattern in ('test_normal_pages_024.py','test_pet_quick_capacity_024.py'):
        test=subprocess.run([sys.executable,'-X','utf8','-m','unittest','discover','-s','tools','-p',pattern,'-v'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        if test.returncode:raise ValueError(test.stdout+test.stderr)
        outputs.append(dict(pattern=pattern,passed=True,output=test.stderr))
    deps=paths+['tools/checkpoint_layout500_024.py','tools/test_normal_pages_024.py','tools/test_pet_quick_capacity_024.py','tools/capture_normal_window_024.py','tools/capture_normal_window_exit_024.py','tools/verify_normal_window_024.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_024_checkpoint_v3/checkpoint.json',dict(schema=1,status='EXACT500_SOURCE_ONLY_COMPILED_WITH_BASELINE_SHARED_RENDERER_EVIDENCE_NO_NEW_ROM',baseline_rom=previous['baseline_rom'],baseline_sha256=previous['baseline_sha256'],verified_rom_translated_units=12622,planned_new_units=500,source_only_archives=compiled['archive_count'],source_only_extended_glyphs=compiled['extended_glyphs_checked'],within_page_lf_edit_units=len(compiled['within_page_lf_edits']),profiles=selection['profiles'],raw_units=343,A3_clone_merge_units=157,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},preserved_artifacts=previous['preserved_artifacts'],tests=outputs,baseline_shared_renderer_pages=len(runtime['pages']),baseline_renderer_read_alias=True,new500_rom_runtime_tested=False,new_rom_units=0,rom_written=False,package_written=False,insertion_ready=False,release_eligible=False,next_action='Do NOT retranslate/reselect500. Reconstruct current023 carry translations for these69 archives, merge exact selected IDs, and preserve all previously translated script bytes/consumer contracts. Register explicit source-bound normal/PET-within-page-LF/conditional models in the immutable-source primary build and update A3 clone selection without changing B0/other consumers. Then exact500 delta, all-carry, ExpectedWrites, independent repro, final-ROM CPU and GBA pixel/clearing/exit/reentry checks. Never inject source-only complete archives over023 carry.',limits='Source-only500 and old023 shared-consumer sample are distinct claims. Native guarded events and new500 natural routes, source-bound product admission, cumulative ROM integration, automatic Hangul commit/save/redisplay, inherited UI defects and semantic review remain unresolved. Baseline sample proves1/3/1/2-row native msgOpen-before-portrait and first E5 closure followed by the original own PET reopening; not an empty idle exit or absence of legitimate PET text OBJ.'))
    print('PASS024 checkpointv3:exact500 source-only/69archives/496glyphs;023 shared4pages verified;ROM unchanged')


if __name__=='__main__':main()
