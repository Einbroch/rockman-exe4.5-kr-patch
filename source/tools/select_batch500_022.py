"""Current021 source-bound remaining full-box candidates and exact500 selection."""
import re
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from fullbox_layout import place
from fullbox_capacity import validate
from tpl_literals import replace_literals
from survey_batch500_017_layout import protected_edges
from prepare_repartition500 import layout_records
from verify_tpi_index import parse_tpi

SELECTION='analysis/pending_insertion_500_022_selection_v1/selection.json'
SURVEY='analysis/pending_insertion_500_022_fullbox_survey_v2/survey.json'
LAYOUT='translations/pending_insertion_500_022_layout_v1.json'

def main():
    s=read('analysis/pending_insertion_500_022_survey_v1/survey.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);m=read(s['baseline_rom'].replace('.gba','.json'));applied={u['id'] for r in layout_records(m) for u in r['layout']};cov=read(s['pinned_coverage']['path']);require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256']);pool=defaultdict(list)
    for path,h in cov['draft_asset_hashes'].items():
        require_hash(ROOT/path,h);a=read(path)
        for u in a['units']:pool[u['id']].append((path,h,u,a))
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    groups=[]
    for g in s['unresolved_groups']:
        row=rows[g['archive']]
        compressed_hint=(row['compressed'] and not row['size_header'] and len(row['pointers'])==1 and row['pointers'][0] in range(0x54180,0x541D4,4))
        if g['reasons']!=['adopted_normal_geometry'] and not (compressed_hint and set(g['reasons'])<={'different_storage_adapter','adopted_normal_geometry'}):continue
        units=[];refs=[];layouts={}
        for key in g['ids']:
            options=pool[key]
            if len({(u['source'],u['translation'],u['state']) for _,_,u,_ in options})!=1:raise ValueError('Conflicting wording')
            path,h,old,a=options[0];u=deepcopy(old);value=place(u['translation'])
            if value is None or not protected_edges(u['source'],value):break
            if value!=u['translation']:layouts[key]=value
            u['translation']=value;units.append(u);refs.append(dict(id=key,path=path,sha256=h))
        else:
            ref=a['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);tpl=(ROOT/ref['path']).read_text(encoding='utf-8-sig');profile=dict(script=g['script'],ids=g['ids'])
            target=replace_literals(tpl,units)
            try:proof=validate(tpl,target,[profile],set(g['ids']))
            except ValueError:
                section=re.search(r'^script '+str(g['script'])+r'\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',tpl,re.M).group()
                guards=re.findall(r'^\t(\w+)\b',section.split('\tmugshotShow')[0],re.M)
                if guards:profile['entry_guards']=guards
                if len(re.findall(r'^\tmugshotShow\s*$',section,re.M))>1:profile['portrait_changes']=True
                try:proof=validate(tpl,target,[profile],set(g['ids']))
                except ValueError:continue
            if set(g['ids'])&applied:raise ValueError('Already applied IDs')
            groups.append(dict(archive=g['archive'],script=g['script'],units=len(g['ids']),ids=g['ids'],drafts=refs,source_tpl=ref,fullbox_profile=profile,explicit_layouts=layouts,geometry=proof,storage_candidate=dict(compressed=row['compressed'],size_header=row['size_header'],pointers=row['pointers'],product_admitted=False,ram_capacity_verified=False if compressed_hint else None)))
    frozen_write(ROOT/SURVEY,dict(schema=1,baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],source_sha256=s['source_sha256'],candidates=groups,candidate_units=sum(g['units'] for g in groups),rom_written=False,prose_changed=False,release_eligible=False,limits='Same-wording full-box180/180/168 candidates only; no quick/variable/choice/storage relaxation or product admission.'))
    states={0:[]}
    for g in sorted(groups,key=lambda g:(g['archive'],g['script'])):
        for n,chosen in list(states.items()):
            k=n+g['units']
            if k<=500 and k not in states:states[k]=chosen+[g]
    if 500 not in states:raise ValueError('No exact500 strict full-box subset; preserve survey')
    chosen=states[500];ids=[k for g in chosen for k in g['ids']]
    if len(ids)!=len(set(ids)) or len(ids)!=500:raise ValueError('Distinct500')
    by=defaultdict(list)
    for g in chosen:by[g['archive']].append(g)
    layouts={k:v for g in chosen for k,v in g['explicit_layouts'].items()};frozen_write(ROOT/LAYOUT,dict(schema=1,release_eligible=False,layouts=layouts))
    frozen_write(ROOT/SELECTION,dict(schema=1,batch_id='pending-insertion-500-022-source-only',source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],survey=dict(path=SURVEY,sha256=sha((ROOT/SURVEY).read_bytes())),individual_layout=dict(path=LAYOUT,sha256=sha((ROOT/LAYOUT).read_bytes())),total_new_units=500,selected=[dict(archive=a,groups=sorted(gs,key=lambda g:g['script']),units=sum(g['units'] for g in gs)) for a,gs in sorted(by.items())],rom_written=False,prose_changed=False,release_eligible=False,policy='development-draft; NON-DISTRIBUTION',limits='500 frozen full-box units. Same wording/row counts; source-only compile/cumulative writer/product/runtime/review pending.'))
    print('Candidates',sum(g['units'] for g in groups),'selected500',len(by),'archives',len(chosen),'scripts; line placements',len(layouts))
if __name__=='__main__':main()
