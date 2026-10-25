"""Select exact500 geometry-only compressed proposals, NOT ROM admission."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from inspect_remaining_035 import BASE,BASE_SHA

SURVEY='analysis/pending_insertion_500_035_new_storage_layout_v1/survey.json'
OUT='analysis/pending_insertion_500_035_source500_selection_v1/selection.json'

def main():
    s=read(SURVEY);require_hash(ROOT/BASE,BASE_SHA)
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    meta=read(BASE.replace('.gba','.json'));applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    totals=Counter()
    for g in s['candidate_groups']:totals[g['archive']]+=g['units']
    groups=sorted(s['candidate_groups'],key=lambda g:(-totals[g['archive']],g['archive'],g['script']))
    states={0:[]}
    for g in groups:
        if g['storage']!='compressed' or g['already_applied_ids_in_script'] or g['locked_parent_units']:continue
        for n,path in list(states.items()):
            total=n+g['units']
            if total<=500 and total not in states:states[total]=path+[g]
        if 500 in states:break
    chosen=deepcopy(states[500]);ids=[k for g in chosen for k in g['ids']]
    if len(ids)!=500 or len(set(ids))!=500 or applied&set(ids):raise ValueError('035 exact500 disjoint IDs')
    profiles=Counter()
    for g in chosen:profiles[g['profile']]+=g['units']
    deps=[SURVEY,'analysis/pending500_034_v1/batch_status.json','tools/prepare_source500_035.py']
    frozen_write(ROOT/OUT,dict(schema=1,status='EXACT500_SOURCE_GEOMETRY_ONLY_STORAGE_UNPROVEN_NOT_ROM_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,
        source_sha256=meta['source_sha256'],native_nickname_bound=99,planned_new_units=500,selected_ids=sorted(ids),groups=chosen,profiles=dict(profiles),
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,
        limits='Exact500 source-only proposals, not product-ready500. All compressed loader/decompression destination/extent/residency and ownership gates remain unproven. No primary ROM or distribution package may be generated from this selection.'))
    print('035 exact500 source proposals',len(chosen),'scripts',len({g['archive'] for g in chosen}),'compressed archives;NO ROM')

if __name__=='__main__':main()
