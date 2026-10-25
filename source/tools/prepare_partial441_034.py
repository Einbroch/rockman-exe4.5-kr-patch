"""Combine275 prepared and166 conditional native list caption proposals."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from inspect_remaining_034 import BASE,BASE_SHA

OUT='analysis/pending_insertion_500_034_partial441_selection_v1/selection.json'


def main():
    paths=['analysis/pending_insertion_500_034_partial275_selection_v1/selection.json','analysis/pending_insertion_500_034_list_layout_v2/survey.json','analysis/pending_insertion_500_034_list_models_v1/result.json','analysis/pending_insertion_500_034_list_formatter_cpu_v1/cpu.json','analysis/pending_insertion_500_034_list_consumers_cpu_v1/cpu.json']
    previous,lists,tests,formatter,consumer=reports=[read(p) for p in paths]
    require_hash(ROOT/BASE,BASE_SHA);meta=read(BASE.replace('.gba','.json'))
    if previous['planned_new_units']!=275 or lists['candidate_units']!=166 or any(not r['passed'] for r in (tests,formatter,consumer)):raise ValueError('Partial441 prerequisites')
    for report in reports:
        if 'baseline_sha256' in report and report['baseline_sha256']!=BASE_SHA:raise ValueError('Partial441 baseline')
        for p,h in report.get('dependencies',{}).items():require_hash(ROOT/p,h)
    applied={u['id'] for r in layout_records(meta) for u in r['layout']};groups=deepcopy(previous['groups'])+deepcopy(lists['candidate_groups']);ids=[];scripts=set();profiles=Counter()
    for g in groups:
        if (g['archive'],g['script']) in scripts or g['storage']!='raw-existing' or g['product_admitted']:raise ValueError('Partial441 scope/storage')
        scripts.add((g['archive'],g['script']));ids+=g['ids'];profiles[g['profile']]+=g['units']
        for link in g['drafts']:require_hash(ROOT/link['path'],link['sha256'])
    if len(ids)!=441 or len(set(ids))!=441 or set(ids)&applied:raise ValueError('Partial441 distinct pending IDs')
    paths+=['tools/prepare_partial441_034.py','tools/pet_list_capacity_034_v2.py','analysis/pending_insertion_500_034_preflight275_v1/verification.json']
    frozen_write(ROOT/OUT,dict(schema=1,status='PARTIAL441_SOURCE_LAYOUT_SELECTION_NOT500_NOT_ROM_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=meta['source_sha256'],native_nickname_bound=99,planned_new_units=441,requested_rom_cohort=500,additional_units_needed=59,selected_ids=sorted(ids),groups=groups,profiles=dict(profiles),dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,limits='275 previous+166 list-caption proposals; includes18 punctuation IDs. Conditional native legacy lists only; graphics/editor/page lifetime and GBA rendering remain pending. Source/parent/cumulative checks still required. No partial ROM application.'))
    print('034 partial441 selected',len(groups),'scripts;',len({g['archive'] for g in groups}),'archives;59 more;NO ROM')


if __name__=='__main__':main()
