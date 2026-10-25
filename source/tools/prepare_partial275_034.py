"""Combine verified59 and216 query proposals; no partial ROM authority."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from inspect_remaining_034 import BASE,BASE_SHA
from prepare_partial59_034 import OUT as PRIOR

OUT='analysis/pending_insertion_500_034_partial275_selection_v1/selection.json'


def main():
    query='analysis/pending_insertion_500_034_query_layout_v1/survey.json';proof='analysis/pending_insertion_500_034_query_controls_cpu_v1/cpu.json';tests='analysis/pending_insertion_500_034_query_models_v1/result.json'
    previous=read(PRIOR);s=read(query);cpu=read(proof);t=read(tests);require_hash(ROOT/BASE,BASE_SHA);meta=read(BASE.replace('.gba','.json'))
    if previous['planned_new_units']!=59 or s['candidate_units']!=216 or not cpu['passed'] or not t['passed'] or cpu['baseline_sha256']!=BASE_SHA:raise ValueError('034 partial275 source prerequisites')
    for report in (previous,s,cpu,t):
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
    rom=(ROOT/BASE).read_bytes()
    for r in cpu['native_ranges']:
        if sha(rom[r['offset']:r['offset']+r['bytes']])!=r['sha256']:raise ValueError('034 query native CPU applicability')
    actual_flags={int(f['arguments'].split('=')[1]) for g in s['candidate_groups'] for p in g['geometry'] for f in p['preserved_flags']}
    if actual_flags!=set(cpu['flag_values']):raise ValueError('034 finite query flag proof')
    applied={u['id'] for r in layout_records(meta) for u in r['layout']};groups=deepcopy(previous['groups'])+deepcopy(s['candidate_groups']);ids=[];counts=Counter();scripts=set()
    for g in groups:
        if (g['archive'],g['script']) in scripts:raise ValueError('034 source script overlap')
        scripts.add((g['archive'],g['script']));ids+=g['ids'];counts[g['profile']]+=g['units']
        if g['storage']!='raw-existing' or g['product_admitted']:raise ValueError('034 undeclared storage/admission')
        for link in g['drafts']:require_hash(ROOT/link['path'],link['sha256'])
    if len(ids)!=275 or len(set(ids))!=275 or set(ids)&applied:raise ValueError('034 exact275 unapplied IDs')
    deps=[PRIOR,query,proof,tests,'analysis/pending_insertion_500_034_preflight59_v1/verification.json','tools/prepare_partial275_034.py','tools/pet_query_choices_034.py','tools/aggregate_pet_query_034.py']
    frozen_write(ROOT/OUT,dict(schema=1,status='PARTIAL275_SOURCE_LAYOUT_SELECTION_NOT500_NOT_ROM_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,
        source_sha256=meta['source_sha256'],native_nickname_bound=99,planned_new_units=275,requested_rom_cohort=500,additional_units_needed=225,
        selected_ids=sorted(ids),groups=groups,profiles=dict(counts),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},
        rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,
        limits='59 previously prepared +216 same-word PET query proposals. Includes18 punctuation literals, not275 independent prose translations. Existing controls/old wording locked; source/parent/cumulative compilation still required for216. Exactly500 needed for ROM application.'))
    print('034 frozen partial275',len(groups),'scripts',len({g['archive'] for g in groups}),'archives;225 more needed;NO ROM')


if __name__=='__main__':main()
