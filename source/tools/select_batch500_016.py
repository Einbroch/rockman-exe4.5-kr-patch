"""Freeze exact500 from untouched raw archives; investigation, not product code."""
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
SURVEY='analysis/pending_insertion_500_016_survey_v1/survey.json'
OUT='analysis/pending_insertion_500_016_selection_v1/selection.json'
def main():
    s=read(SURVEY);m=read(s['baseline_rom'].replace('.gba','.json'));require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    if m['output_sha256']!=s['baseline_sha256'] or s['pinned_changed_inputs']:raise ValueError('Survey/baseline/pinned corpus')
    applied={r['archive'] for r in layout_records(m)};registry=read('tools/specs/exe45_dialogue_archives_v1.json')['archives'];groups=defaultdict(list)
    for g in s['candidates']:
        if g['archive'] not in applied and g['archive'] not in registry:groups[g['archive']].append(g)
    items=[dict(archive=a,groups=sorted(gs,key=lambda g:g['script']),units=sum(g['units'] for g in gs)) for a,gs in sorted(groups.items())]
    states={0:[]}
    for item in items:
        for total,chosen in list(states.items()):
            n=total+item['units']
            if n<=500 and (n not in states or len(chosen)+1<len(states[n])):states[n]=chosen+[item]
    if 500 not in states:raise ValueError('No exact500 whole-archive eligible-script scope')
    chosen=states[500];ids=[key for item in chosen for g in item['groups'] for key in g['ids']]
    if len(ids)!=500 or len(set(ids))!=500:raise ValueError('500 distinct source IDs')
    frozen_write(ROOT/OUT,dict(schema=1,batch_id='pending-insertion-500-016-source-only',source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],survey=dict(path=SURVEY,sha256=sha((ROOT/SURVEY).read_bytes())),total_new_units=500,selected=chosen,rom_written=False,prose_changed=False,release_eligible=False,policy='development-draft; NON-DISTRIBUTION',limits='Untouched known-pointer raw normal-dialogue candidates only; preflight and exact-artifact integration/runtime remain required. No semantic or natural-route approval.'))
    print('Selected500 in',len(chosen),'untouched archives:',[i['archive'] for i in chosen])
if __name__=='__main__':main()
