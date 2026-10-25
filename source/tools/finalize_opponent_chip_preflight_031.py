"""Close031130source-only preflight. Does NOT apply a500cohort or build ROM."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from compile_layout_candidates_024 import ref

OUT='analysis/pending_insertion_500_031_preflight_v1/status.json'

def main():
    base='poc/output/pending500_030_v1.gba';m=read(base.replace('.gba','.json'));require_hash(ROOT/base,m['output_sha256']);old=read('analysis/pending500_030_v1/batch_status.json')
    if old['rom_sha256']!=m['output_sha256'] or old['total_units']!=16122:raise ValueError('031 authority remains030')
    for name,h in m['build_tools_sha256'].items():require_hash(ROOT/'tools'/name,h)
    for p,h in old['protected_artifacts'].items():require_hash(ROOT/p,h)
    reports={
        'cpu':'analysis/pending_insertion_500_031_opponent_chip_cpu_v1/cpu.json',
        'runtime':'analysis/pending_insertion_500_031_opponent_chip_runtime_v1/verification.json',
        'visual':'analysis/pending_insertion_500_031_opponent_chip_runtime_v1/visual_review.json',
        'compile':'analysis/pending_insertion_500_031_opponent_chip_compile130_v1/verification.json',
        'models':'analysis/pending_insertion_500_031_models_test_v1/result.json',
    };rs={k:read(p) for k,p in reports.items()}
    for k,r in rs.items():
        if not r['passed'] or r.get('baseline_sha256',m['output_sha256'])!=m['output_sha256']:raise ValueError('031 report identity '+k)
        for p,h in r.get('dependencies',{}).items():require_hash(ROOT/p,h)
    if rs['cpu']['case_count']!=1580 or rs['cpu']['native_helpers_substituted'] or len(rs['runtime']['pages'])!=2 or rs['models']['tests']!=20 or rs['compile']['units']!=130 or rs['compile']['archive_count']!=18 or rs['compile']['rom_written'] or rs['compile']['product_integrated']:raise ValueError('031 evidence denominator')
    require_hash(ROOT/'tools/bench_opponent_chips_031.py',rs['cpu']['tool_sha256'])
    for r in rs['runtime']['receipts']:
        require_hash(ROOT/r['path'],r['sha256']);receipt=read(r['path']);folder=(ROOT/r['path']).parent
        for p,h in receipt['artifacts'].items():require_hash(folder/p,h)
    v=rs['visual'];require_hash(ROOT/v['contact_path'],v['contact_sha256'])
    if v['screens_directly_viewed']!=6 or v['contact_sha256']!=rs['runtime']['contact']['sha256']:raise ValueError('031 direct visual identity')
    selection_path='analysis/pending_insertion_500_031_opponent_chip_selection_v1/selection.json';s=read(selection_path)
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    wanted=set(s['selected_ids']);applied={u['id'] for r in layout_records(m) for u in r['layout']};compiled={u['id'] for a in rs['compile']['archives'] for u in a['units']}
    if len(wanted)!=130 or wanted&applied or compiled!=wanted:raise ValueError('031 new-but-not-applied IDs')
    if list((ROOT/'poc/output').glob('pending500_031*.gba')):raise ValueError('031 unaccounted product ROM')
    survey_path='analysis/pending_insertion_500_031_layout_v1/survey.json';survey=read(survey_path)
    if survey['selected500'] is not None or survey['max_reachable_requested_subset']!=223:raise ValueError('031 no500 fact changed')
    frozen_write(ROOT/OUT,dict(schema=1,status='SOURCE_ONLY_130_CHIP_CANDIDATES_VERIFIED_NEXT500_NOT_READY',baseline_rom=base,baseline_sha256=m['output_sha256'],actual_applied_total=16122,new_units_applied=0,new_source_compile_candidates=130,candidate_whole_scripts=46,candidate_archives=18,selected_ids=sorted(wanted),candidate_layout_pool_units=223,whole_game_remaining_count_established=False,reports={k:ref(ROOT/p) for k,p in reports.items()},selection=ref(ROOT/selection_path),survey=ref(ROOT/survey_path),source_and_prior_product_tools_preserved=True,prior_protected_artifacts_verified=len(old['protected_artifacts']),new_rom_created=False,new_distribution_packages_created=False,product_admitted=False,release_eligible=False,semantic_human_approved=False,limits=['130canonical existing needs_review candidates compiled from source; not new prose drafting or ROM application.268existing glyphs checked.','Two source/030native opponent-chip producers/F90C1580cases, two native max8glyph GBA paths and6directly viewed captures. GBA text remains original Japanese, not new Korean130pages.','Only223units can currently form the next subset under the considered model set; no500subset. This is not a whole-game remainder count.','Player-name and multiplayer-name transport/terminator/history bounds remain unadmitted; Hangul composition/commit/save/redisplay and source-language chip-name values remain open.'],next_action='Continue from030 IDs. Analyze transport/store terminator ownership or another independently scoped consumer to establish a complete500subset; then version compiler/carry/product gates, source-only full/repro builds and actual-new-ROM GBA QA. Do not apply130alone or count them in16122.'))
    print('PASS031 source-only130 preflight; applied delta0; actual030 total16122 preserved; no500/ROM/package')

if __name__=='__main__':main()
