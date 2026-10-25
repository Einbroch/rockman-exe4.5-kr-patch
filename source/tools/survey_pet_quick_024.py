"""Frozen wording/line placements in exact native PET quick boxes; no ROM."""
from collections import defaultdict,Counter
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import parse_tpi
from survey_batch500_017_layout import place,protected_edges
from tpl_literals import replace_literals
from pet_quick_capacity import validate


def main():
    s=read('analysis/pending_insertion_500_024_survey_v1/survey.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256']);cov=read(s['pinned_coverage']['path']);pool=defaultdict(list)
    for path,h in cov['draft_asset_hashes'].items():
        require_hash(ROOT/path,h);a=read(path)
        for u in a['units']:pool[u['id']].append((path,h,u,a))
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);rows={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};good=[];bad=[]
    for g in s['unresolved_groups']+s['candidates']:
        if not set(g.get('reasons',[]))<={'adopted_normal_geometry'}:continue
        row=rows[g['archive']]
        if row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers']==[0]:continue
        units=[];refs=[];layouts={}
        for key in g['ids']:
            opts=pool[key]
            if len({(u['source'],u['translation'],u['state']) for _,_,u,_ in opts})!=1:raise ValueError('Conflicting wording '+key)
            path,h,u,a=opts[0];u=deepcopy(u);value=place(u['translation'])
            if value is None or not protected_edges(u['source'],value):bad.append(dict(archive=g['archive'],script=g['script'],reason='same-wording132px-placement'));break
            if value!=u['translation']:layouts[key]=value
            u['translation']=value;units.append(u);refs.append(dict(id=key,path=path,sha256=h))
        else:
            ref=a['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);tpl=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
            try:proof=validate(tpl,replace_literals(tpl,units),[g['script']],set(g['ids']))
            except ValueError as ex:bad.append(dict(archive=g['archive'],script=g['script'],reason=str(ex)));continue
            good.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],units=len(g['ids']),drafts=refs,source_tpl=ref,individual_layouts=layouts,geometry=proof,source_row=row,storage='raw-known-pointer',product_admitted=False))
    states={0:[]}
    for g in sorted(good,key=lambda g:(g['archive'],g['script'])):
        for n,groups in list(states.items()):
            if n+g['units']<=500 and n+g['units'] not in states:states[n+g['units']]=groups+[g]
    frozen_write(ROOT/'analysis/pending_insertion_500_024_quick_v1/survey.json',dict(schema=1,status='EXPLICIT_QUICK_GEOMETRY_ANALYSIS_NOT_PRODUCT_ADMISSION',baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],source_sha256=s['source_sha256'],source_survey_sha256=sha((ROOT/'analysis/pending_insertion_500_024_survey_v1/survey.json').read_bytes()),candidate_units=sum(g['units'] for g in good),candidate_groups=good,selected500=states.get(500),max_reachable_requested_subset=max(states),rejections=bad,rejection_counts=dict(Counter(g['reason'] for g in bad)),rom_written=False,release_eligible=False,limits='Exact source-positioned PET quick-window132px/3rows; wording/LF count preserved. Composite literal/timing pages modeled, no variable/choices/window changes. Consumer opcode/geometry applicability, source/carry/product/CPU/runtime/human review remain separate.'))
    print('Quick candidates',sum(g['units'] for g in good),'exact500',500 in states,'archives',len({g['archive'] for g in good}));print(Counter(g['reason'] for g in bad))


if __name__=='__main__':main()
