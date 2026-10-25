"""Freeze65 corrected-script units plus435 strict full-box units for development."""
import json,re
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from tpl_literals import replace_literals
from fullbox_capacity import validate

SELECTION='analysis/pending_insertion_500_020_selection_v1/selection.json'
SURVEY='analysis/pending_insertion_500_020_fullbox_survey_v1/survey.json'
LAYOUT='translations/pending_insertion_500_020_layout_v1.json'

def main():
    s=read('analysis/pending_insertion_500_020_survey_v1/survey.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);c=read('analysis/pending_insertion_500_020_wording_v1/report.json');pool=defaultdict(list)
    cov=read(s['pinned_coverage']['path']);require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256'])
    for path,h in cov['draft_asset_hashes'].items():
        require_hash(ROOT/path,h);a=read(path)
        for u in a['units']:pool[u['id']].append((path,h,u,a))
    corrections=[];excluded={a['archive'] for a in c['assets']}
    for a in c['assets']:
        require_hash(ROOT/a['path'],a['sha256']);asset=read(a['path'])
        for script in a['scripts']:
            ids=[k for k in a['selected_ids'] if int(k.split(':')[1])==script];p=next(p for p in a['nickname_capacity_profiles'] if p['script']==script)
            corrections.append(dict(archive=a['archive'],script=script,units=len(ids),ids=ids,drafts=[dict(id=k,path=a['path'],sha256=a['sha256']) for k in ids],source_tpl=asset['source_tpl'],template=p))
    candidates=[]
    for g in s['unresolved_groups']:
        if g['reasons']!=['adopted_normal_geometry'] or g['archive'] in excluded:continue
        units=[];refs=[]
        for k in g['ids']:
            options=pool[k]
            if len({(u['source'],u['translation'],u['state']) for _,_,u,_ in options})!=1:raise ValueError('Conflicting wording')
            p,h,u,a=options[0];units.append(u);refs.append(dict(id=k,path=p,sha256=h))
        ref=a['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);tpl=(ROOT/ref['path']).read_text(encoding='utf-8-sig');profile=dict(script=g['script'],ids=g['ids'])
        try:proof=validate(tpl,replace_literals(tpl,units),[profile],set(g['ids']))
        except ValueError:continue
        candidates.append(dict(archive=g['archive'],script=g['script'],units=len(g['ids']),ids=g['ids'],drafts=refs,source_tpl=ref,fullbox_profile=profile,development_geometry=proof))
    needed=500-sum(g['units'] for g in corrections);states={0:[]}
    for g in sorted(candidates,key=lambda g:(g['archive'],g['script'])):
        for n,chosen in list(states.items()):
            if n+g['units']<=needed and n+g['units'] not in states:states[n+g['units']]=chosen+[g]
    if needed not in states:raise ValueError('No distinct500 strict scope')
    groups=corrections+states[needed];ids=[k for g in groups for k in g['ids']]
    if len(ids)!=500 or len(set(ids))!=500:raise ValueError('Exact500')
    by=defaultdict(list)
    for g in groups:by[g['archive']].append(g)
    frozen_write(ROOT/SURVEY,dict(schema=1,baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],source_sha256=s['source_sha256'],candidates=candidates,conditional_units=sum(g['units'] for g in candidates),rom_written=False,release_eligible=False,limits='Development full-box180/180/168 range hypothesis, not quick-window expansion. Actual integrated long-page runtime required before verification/release.'))
    frozen_write(ROOT/LAYOUT,dict(schema=1,release_eligible=False,layouts={}))
    frozen_write(ROOT/SELECTION,dict(schema=1,batch_id='pending-insertion-500-020-source-only',source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],survey=dict(path=SURVEY,sha256=sha((ROOT/SURVEY).read_bytes())),individual_layout=dict(path=LAYOUT,sha256=sha((ROOT/LAYOUT).read_bytes())),total_new_units=500,selected=[dict(archive=a,groups=sorted(gs,key=lambda g:g['script']),units=sum(g['units'] for g in gs)) for a,gs in sorted(by.items())],rom_written=False,prose_changed=True,release_eligible=False,policy='development-draft; NON-DISTRIBUTION',limits='20 individual corrections in65 whole-script units plus435 unchanged-wording full-box units. New full-box extent runtime pending; not full localization or release.'))
    print('Selected500',len(by),'archives;',len(groups),'scripts; corrected65 + strictfullbox435')

if __name__=='__main__':main()
