"""Freeze500 disjoint, complete Japanese-script populations from017 survey."""
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
SURVEY='analysis/pending_insertion_500_017_layout_survey_v1/survey.json'
OUT='analysis/pending_insertion_500_017_selection_v1/selection.json'
LAYOUT='translations/pending_insertion_500_017_layout.json'
def main(batch_id='pending-insertion-500-017-source-only'):
    s=read(SURVEY);require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    m=read(s['baseline_rom'].replace('.gba','.json'));records=list(layout_records(m));applied={u['id'] for r in records for u in r['layout']}
    if m['output_sha256']!=s['baseline_sha256'] or s['prose_changed'] or s['release_eligible']:raise ValueError('Survey policy')
    groups=defaultdict(list)
    for g in s['candidates']:
        if set(g['ids'])&applied:raise ValueError('Already applied ID')
        groups[g['archive']].append(g)
    items=[dict(archive=a,groups=sorted(gs,key=lambda g:g['script']),units=sum(g['units'] for g in gs)) for a,gs in sorted(groups.items())]
    states={0:[]}
    for item in items:
        for total,chosen in list(states.items()):
            n=total+item['units']
            if n<=500 and (n not in states or len(chosen)+1<len(states[n])):states[n]=chosen+[item]
    if 500 not in states:raise ValueError('No exact500 admitted complete-script subset')
    selected=states[500];ids=[key for i in selected for g in i['groups'] for key in g['ids']]
    if len(ids)!=500 or len(set(ids))!=500:raise ValueError('Distinct500')
    layouts={k:v for i in selected for g in i['groups'] for k,v in g.get('explicit_layouts',{}).items()}
    frozen_write(ROOT/LAYOUT,dict(schema=1,release_eligible=False,layouts=layouts))
    frozen_write(ROOT/OUT,dict(schema=1,batch_id=batch_id,source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],survey=dict(path=SURVEY,sha256=sha((ROOT/SURVEY).read_bytes())),individual_layout=dict(path=LAYOUT,sha256=sha((ROOT/LAYOUT).read_bytes())),total_new_units=500,selected=selected,rom_written=False,prose_changed=False,release_eligible=False,policy='development-draft; NON-DISTRIBUTION',limits='Frozen same-wording complete-script technical scope; cumulative single-writer carry admission, preflight and artifact/runtime verification remain required. Not semantic or presentation approval.'))
    print('Selected500',[(i['archive'],i['units']) for i in selected],'explicit layouts',len(layouts))
if __name__=='__main__':main()
