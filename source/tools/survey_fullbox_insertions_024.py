"""Current023 frozen draft census under explicit full-box insertion model.

Analysis only: never admits a catalog row, changes prose or writes a ROM.
"""
import re
from collections import defaultdict,Counter
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import parse_tpi
from tpl_literals import replace_literals
from fullbox_layout import place
from field_hint_capacity import validate
from nickname_capacity import CPU
from survey_batch500_020_variables import applicability
from survey_batch500_017_layout import protected_edges


def main():
    s=read('analysis/pending_insertion_500_024_survey_v1/survey.json');rp=ROOT/s['baseline_rom'];require_hash(rp,s['baseline_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,s['source_sha256']);source=sp.read_bytes()
    require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256']);cov=read(s['pinned_coverage']['path']);pool=defaultdict(list)
    for path,h in cov['draft_asset_hashes'].items():
        require_hash(ROOT/path,h);a=read(path)
        for u in a['units']:pool[u['id']].append((path,h,u,a))
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);rows={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    bound=applicability(source,rom,read(CPU));candidates=[];rejected=[];skipped=Counter();tpls={}
    for g in s['unresolved_groups']+s['candidates']:
        reasons=set(g.get('reasons',[]));row=rows[g['archive']]
        if not reasons<={'adopted_normal_geometry','variable_insertion','different_storage_adapter'}:
            skipped.update(reasons);continue
        hint=(row['compressed'] and not row['size_header'] and len(row['pointers'])==1 and row['pointers'][0] in range(0x54180,0x541D4,4))
        if row['compressed'] and not hint:skipped['different_compressed_consumer']+=1;continue
        if row['size_header'] or not row['pointers'] or row['pointers']==[0]:skipped['unestablished_storage']+=1;continue
        units=[];refs=[];layouts={};a=None
        for key in g['ids']:
            opts=pool[key]
            if not opts or len({(u['source'],u['translation'],u['state']) for _,_,u,_ in opts})!=1:raise ValueError('Absent/conflicting frozen wording '+key)
            path,h,u,a=opts[0];u=deepcopy(u);value=place(u['translation'])
            if value is None or not protected_edges(u['source'],value):
                rejected.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],reason='same_wording_protected_line_placement'));break
            if value!=u['translation']:layouts[key]=value
            u['translation']=value;units.append(u);refs.append(dict(id=key,path=path,sha256=h))
        else:
            ref=a['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);tpl=tpls.setdefault(ref['path'],(ROOT/ref['path']).read_text(encoding='utf-8-sig'))
            try:proof=validate(tpl,replace_literals(tpl,units),[g['script']],set(g['ids']),bound,88)
            except ValueError as ex:
                rejected.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],reason=str(ex)));continue
            candidates.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],units=len(g['ids']),drafts=refs,source_tpl=ref,individual_layouts=layouts,geometry=proof,source_row=row,storage='existing-A3-clone-merge' if hint else 'raw-known-pointer',product_admitted=False))
    by=Counter();storage=Counter()
    for g in candidates:by['variable' if any(p['kind']!='literal' for page in g['geometry'][0]['pages'] for p in page['parts']) else 'plain']+=g['units'];storage[g['storage']]+=g['units']
    states={0:[]}
    for g in sorted(candidates,key=lambda g:(g['storage']!='raw-known-pointer',g['archive'],g['script'])):
        for n,groups in list(states.items()):
            if n+g['units']<=500 and n+g['units'] not in states:states[n+g['units']]=groups+[g]
    out='analysis/pending_insertion_500_024_fullbox_v1/survey.json'
    frozen_write(ROOT/out,dict(schema=1,status='ANALYSIS_NOT_PRODUCT_ADMISSION',source_sha256=sha(source),baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],dependencies={'analysis/pending_insertion_500_024_survey_v1/survey.json':sha((ROOT/'analysis/pending_insertion_500_024_survey_v1/survey.json').read_bytes()),'tools/field_hint_capacity.py':sha((ROOT/'tools/field_hint_capacity.py').read_bytes())},native_nickname_applicability_bound=bound,candidate_units=sum(g['units'] for g in candidates),candidate_units_by_type=dict(by),candidate_units_by_storage=dict(storage),candidate_groups=candidates,selected500=states.get(500),max_reachable_requested_subset=max(states),rejections=rejected,rejection_counts=dict(Counter(g['reason'] for g in rejected)),skipped_overlapping_reasons=dict(skipped),rom_written=False,release_eligible=False,limits='Same frozen wording, protected line topology and explicit normal mugshot/msgOpen command model. Source-storage/carry merge registration and source-bound gate outside B0, actual final layout/variables/runtime and human review remain separate. Duplicate B1/B0 decoded hints are not counted as new wording. Not a whole-game remaining count.'))
    print('Candidates',sum(g['units'] for g in candidates),dict(by),dict(storage),'exact500',500 in states)
    print('Rejections',Counter(g['reason'] for g in rejected))


if __name__=='__main__':main()
