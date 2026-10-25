"""Controlled current034 consumer-gate acceptance and mutation refusals."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from layout500_inputs_034 import load_inputs,validate_group


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);inputs,summary=load_inputs(sp.read_bytes())
    selection=read('analysis/pending_insertion_500_034_exact500_selection_v1/selection.json');recs={r['archive']:r for r,_ in inputs};samples={}
    for g in selection['groups']:samples.setdefault(g['profile'],g)
    positives=[];refusals=[]
    for name,g in samples.items():
        rec=recs[g['archive']];original=(ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig');target=(ROOT/rec['merged_tpl']['path']).read_text(encoding='utf-8-sig');asset=read(rec['merged_asset']['path']);units=[u for u in asset['units'] if u['id'] in set(g['ids'])]
        validate_group(original,target,g,units);positives.append(name)
        changes=[('duplicate-unit',lambda a,b:b.append(deepcopy(b[0]))),('missing-unit',lambda a,b:b.pop()),('changed-source',lambda a,b:b[0].update(source=b[0]['source']+'x')),('changed-wording',lambda a,b:b[0].update(translation=b[0]['translation']+'가')),('changed-state',lambda a,b:b[0].update(state='distribution_eligible')),('unknown-profile',lambda a,b:a.update(profile='UNKNOWN')),('forged-geometry',lambda a,b:a.update(geometry=[])),('lost-geometry-ID',lambda a,b:a.update(geometry_ids=[]))]
        for kind,modify in changes:
            group=deepcopy(g);test=deepcopy(units);modify(group,test)
            try:validate_group(original,target,group,test)
            except ValueError as ex:refusals.append(dict(profile=name,kind=kind,error=str(ex)))
            else:raise ValueError('034 malformed group accepted '+name+':'+kind)
    mixed=next(g for g in selection['groups'] if g['locked_parent_units']);rec=recs[mixed['archive']];original=(ROOT/mixed['source_tpl']['path']).read_text(encoding='utf-8-sig');target=(ROOT/rec['merged_tpl']['path']).read_text(encoding='utf-8-sig');units=[u for u in read(rec['merged_asset']['path'])['units'] if u['id'] in set(mixed['ids'])]
    for kind,modify in [('locked-wording',lambda x:x['locked_parent_units'][0].update(translation='가')),('locked-source',lambda x:x['locked_parent_units'][0].update(source='가')),('locked-ID-loss',lambda x:x.update(locked_parent_units=[]))]:
        test=deepcopy(mixed);modify(test)
        try:validate_group(original,target,test,units)
        except ValueError as ex:refusals.append(dict(profile='mixed-parent',kind=kind,error=str(ex)))
        else:raise ValueError('034 malformed locked parent accepted '+kind)
    deps=['tools/test_inputs_034.py','tools/layout500_inputs_034.py','tools/specs/inputs034_version.json','analysis/pending_insertion_500_034_exact500_selection_v1/selection.json']
    frozen_write(ROOT/'analysis/pending_insertion_500_034_input_models_v1/result.json',dict(schema=1,passed=True,positive_count=len(positives),refusal_count=len(refusals),positive_profiles=positives,refusals=refusals,source_sha256=sha(sp.read_bytes()),summary=summary,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,runtime_tested=False,release_eligible=False,limits='Controlled current source-bound group-gate mutation fixtures, not independently reviewed translation meaning, final ROM or GBA runtime.'))
    print('034 input models',len(positives),'positive',len(refusals),'refusal PASS')


if __name__=='__main__':main()
