"""Freeze026 exact500 raw script groups against actual025; no ROM writing."""
from collections import Counter
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from compare_archive_payloads import payload_of
from compile_layout_candidates_024 import ref

SURVEY='analysis/pending_insertion_500_026_layout_v5/survey.json'
CPU='analysis/pending_insertion_500_026_native_controls_v1/cpu.json'
TESTS='analysis/pending_insertion_500_026_models_test_v1/result.json'
OUT='analysis/pending_insertion_500_026_selection_v1/selection.json'

def verify_dependencies(record):
    for p,h in record['dependencies'].items():require_hash(ROOT/p,h)

def main():
    survey=read(SURVEY);cpu=read(CPU);tests=read(TESTS)
    for record in (survey,tests):verify_dependencies(record)
    require_hash(ROOT/'tools/bench_native_controls_026.py',cpu['tool_sha256'])
    rp=ROOT/survey['baseline_rom'];require_hash(rp,survey['baseline_sha256']);meta=read(rp.with_suffix('.json'))
    if (not cpu['passed'] or cpu['baseline_sha256']!=survey['baseline_sha256'] or cpu['case_count']!=3060
        or not tests['passed'] or tests['tests']!=38 or survey['rom_written']):raise ValueError('025 analysis evidence identity')
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,survey['source_sha256']);source=sp.read_bytes()
    applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    selected=deepcopy(survey['selected500']);seen=set();profiles=Counter();layouts={}
    if not selected or sum(g['units'] for g in selected)!=500:raise ValueError('025 pinned whole-group population')
    for g in selected:
        ids=set(g['ids'])
        if g['storage']!='raw-known-pointer' or g['product_admitted'] or g['units']!=len(ids) or ids&(seen|applied):raise ValueError('025 disjoint raw500')
        native=payload_of(source,g['source_row'])
        if sha(native)!=g['source_archive_sha256']:raise ValueError('025 original archive identity')
        require_hash(ROOT/g['source_tpl']['path'],g['source_tpl']['sha256'])
        for link in g['drafts']:
            require_hash(ROOT/link['path'],link['sha256']);a=read(link['path']);matches=[u for u in a['units'] if u['id']==link['id']]
            if len(matches)!=1 or a['source_tpl']!=g['source_tpl'] or a['source_archive_sha256']!=sha(native):raise ValueError('025 source/wording link')
            u=matches[0];value=g['explicit_layouts'].get(u['id'],u['translation'])
            if u['state']!='needs_review' or value.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('025 prose/review identity')
        if set(g['explicit_layouts'])-ids:raise ValueError('025 layout outside selection')
        layouts.update(g['explicit_layouts']);seen|=ids;profiles[g['profile']]+=g['units']
    if len(seen)!=500 or sum(profiles.values())!=500:raise ValueError('025 exact500 denominator')
    deps=[SURVEY,CPU,TESTS,'tools/prepare_layout500_026.py','analysis/translation_first_v1/coverage.json']
    frozen_write(ROOT/OUT,dict(schema=1,status='EXACT500_SOURCE_LAYOUT_SELECTION_NOT_ROM_ADMISSION',
        source_sha256=sha(source),baseline_rom=survey['baseline_rom'],baseline_sha256=sha(rp.read_bytes()),baseline_metadata=ref(rp.with_suffix('.json')),
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},native_nickname_bound=survey['native_nickname_bound'],
        planned_new_units=500,profiles=dict(profiles),groups=selected,selected_ids=sorted(seen),explicit_layout_changes=len(layouts),
        model_refusal_tests=38,native_control_cpu_cases=3060,rom_written=False,insertion_ready=False,release_eligible=False,
        limits='Frozen canonical needs_review wording; explicit within-page layouts; no prose substitutions. Source compile,025 carry reconstruction, product gate/write plan/repro, extended-glyph choice width pass and GBA cursor/input/outcome testing still required. Native six-glyph nickname only; not automatic Hangul-name commit/save/redisplay.'))
    print('PASS026 exact500 frozen;',len(selected),'groups;',len({g['archive'] for g in selected}),'archives;',len(layouts),'layouts;NO ROM written')

if __name__=='__main__':main()
