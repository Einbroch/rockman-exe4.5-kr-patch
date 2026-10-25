"""441 retained +58 mission captions +1 trader caption = exact500 source IDs."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from inspect_remaining_034 import BASE,BASE_SHA

OUT='analysis/pending_insertion_500_034_exact500_selection_v1/selection.json'


def main():
    paths=['analysis/pending_insertion_500_034_partial441_selection_v1/selection.json','analysis/pending_insertion_500_034_jump_layout_v1/survey.json','analysis/pending_insertion_500_034_leading_clear_layout_v1/survey.json','analysis/pending_insertion_500_034_normal_models_v1/result.json','analysis/pending_insertion_500_034_jump_cpu_v1/cpu.json','analysis/pending_insertion_500_034_leading_clear_cpu_v1/cpu.json','analysis/pending_insertion_500_034_preflight441_v1/verification.json']
    previous,jumps,clears,*checks=reports=[read(p) for p in paths]
    require_hash(ROOT/BASE,BASE_SHA);meta=read(BASE.replace('.gba','.json'))
    if previous['planned_new_units']!=441 or jumps['candidate_units']!=58 or clears['candidate_units']!=2 or any(not r['passed'] for r in checks):raise ValueError('034 exact500 source prerequisites')
    for report in reports:
        if 'baseline_sha256' in report and report['baseline_sha256']!=BASE_SHA:raise ValueError('034 exact500 current baseline')
        for p,h in report.get('dependencies',{}).items():require_hash(ROOT/p,h)
    one=next(g for g in clears['candidate_groups'] if g['archive']=='6FE8D4' and g['script']==21)
    if one['units']!=1:raise ValueError('034 final one whole script identity')
    groups=deepcopy(previous['groups'])+deepcopy(jumps['candidate_groups'])+[deepcopy(one)]
    applied={u['id'] for r in layout_records(meta) for u in r['layout']};ids=[];scripts=set();profiles=Counter()
    for g in groups:
        pair=(g['archive'],g['script'])
        if pair in scripts or g['storage']!='raw-existing' or g['product_admitted']:raise ValueError('034 exact500 scope/storage')
        scripts.add(pair);ids+=g['ids'];profiles[g['profile']]+=g['units']
        for link in g['drafts']:require_hash(ROOT/link['path'],link['sha256'])
    if len(ids)!=500 or len(set(ids))!=500 or set(ids)&applied or not set(previous['selected_ids'])<=set(ids):raise ValueError('034 exact500 new-ID delta/retained441')
    paths+=['tools/prepare_exact500_034.py','tools/normal_jump_tail_034.py','tools/normal_leading_clear_034.py']
    frozen_write(ROOT/OUT,dict(schema=1,status='EXACT500_SOURCE_LAYOUT_SELECTION_NOT_ROM_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=meta['source_sha256'],native_nickname_bound=99,planned_new_units=500,requested_rom_cohort=500,additional_units_needed=0,selected_ids=sorted(ids),groups=groups,profiles=dict(profiles),deferred_safe_source_proposals=[g['ids'] for g in clears['candidate_groups'] if g['script']!=21],dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,limits='All441 retained +58 whole-script mission captions +one whole-script trader caption.501st safe source proposal6FE8D4:23 retained/deferred to next cohort, not dropped. Includes18 punctuation IDs. Source/carry compilation, input gates/wholewrite/repro and own-ROM runtime still required.'))
    print('034 exact500 selected',len(groups),'scripts',len({g['archive'] for g in groups}),'archives;NO ROM yet')


if __name__=='__main__':main()
