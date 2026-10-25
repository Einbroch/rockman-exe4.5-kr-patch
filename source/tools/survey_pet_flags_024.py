"""Additional fixed-flag PET pages only; no272 duplicates, no ROM."""
from collections import defaultdict,Counter
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import parse_tpi
from survey_pet_quick_reflow_024 import place,replace_for_analysis
from pet_flag_page_capacity_024 import validate


def main():
    p='analysis/pending_insertion_500_024_survey_v1/survey.json';s=read(p)
    require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    prior=read('analysis/pending_insertion_500_024_compile_v2/verification.json');existing={u['id'] for r in prior['archives'] for u in r['units']}
    require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256'])
    pool=defaultdict(list)
    for path,h in read(s['pinned_coverage']['path'])['draft_asset_hashes'].items():
        require_hash(ROOT/path,h);a=read(path)
        for u in a['units']:pool[u['id']].append((path,h,u,a))
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};good=[];bad=[]
    for g in s['unresolved_groups']+s['candidates']:
        if existing & set(g['ids']) or not set(g.get('reasons',[]))<={'adopted_normal_geometry'}:continue
        row=rows[g['archive']]
        if row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers']==[0]:continue
        units=[];refs=[];layouts={}
        for key in g['ids']:
            opts=pool[key]
            if not opts or len({(u['source'],u['translation'],u['state']) for _,_,u,_ in opts})!=1:raise ValueError('Frozen wording identity')
            path,h,u,a=opts[0];u=deepcopy(u);v=place(u['translation'])
            if v is None:bad.append(dict(archive=g['archive'],script=g['script'],reason='within3rows wording'));break
            if v!=u['translation']:layouts[key]=dict(before=u['translation'],after=v,added_lf=v.count('\n')-u['translation'].count('\n'))
            u['translation']=v;units.append(u);refs.append(dict(id=key,path=path,sha256=h))
        else:
            ref=a['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);original=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
            try:proof=validate(original,replace_for_analysis(original,units),[g['script']],set(g['ids']))
            except ValueError as ex:bad.append(dict(archive=g['archive'],script=g['script'],reason=str(ex)));continue
            good.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],units=len(g['ids']),drafts=refs,source_tpl=ref,layouts=layouts,geometry=proof,source_row=row,storage='raw-known-pointer',product_admitted=False))
    deps=[p,'analysis/pending_insertion_500_024_compile_v2/verification.json','tools/pet_flag_page_capacity_024.py','tools/survey_pet_flags_024.py','tools/survey_pet_quick_reflow_024.py','tools/pet_quick_capacity.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_024_pet_flags_v2/survey.json',dict(schema=1,status='ADDITIONAL_PET_FLAG_SPATIAL_ANALYSIS_NOT_ADMISSION',source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},candidate_units=sum(g['units'] for g in good),candidate_groups=good,rejections=bad,rejection_counts=dict(Counter(g['reason'] for g in bad)),rom_written=False,release_eligible=False,limits='Fixed source flagSet/flagClear at empty-page boundaries only; words/commands preserved, within-page LF proposal. No dynamic insertion, choice or new window. Native flag effects/source-bound build gate/carry/actual-ROM runtime remain unverified.'))
    print('Additional PET fixed-flag candidates',sum(g['units'] for g in good),'groups',len(good))


if __name__=='__main__':main()
