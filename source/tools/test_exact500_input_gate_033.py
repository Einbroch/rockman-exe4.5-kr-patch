"""Exercise production025 group admission with frozen source and corrupt inputs."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from layout500_inputs_033 import load_inputs,validate_group
from survey_pet_quick_reflow_024 import replace_for_analysis
from tpl_literals import literals,serialize

def corrupt_selected(target,key):
    item=next(i for i in literals(target) if i.key==key)
    return target[:item.start]+serialize('가'+item.text)+target[item.end:]

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    admitted,summary=load_inputs(source)
    selection=read('analysis/pending_insertion_500_033_exact500_selection_v1/selection.json');cases=[]
    records={r['archive']:r for r,_ in admitted}
    for profile in sorted(selection['profiles']):
        g=next(g for g in selection['groups'] if g['profile']==profile);r=records[g['archive']]
        original=(ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig');asset=read(r['merged_asset']['path']);units=[u for u in asset['units'] if u['id'] in g['ids']]
        target=replace_for_analysis(original,units);validate_group(original,target,g,units)
        def reject(name,change):
            gg,uu=deepcopy(g),deepcopy(units);tt=change(gg,uu,target)
            try:validate_group(original,tt,gg,uu)
            except (ValueError,KeyError,IndexError) as ex:cases.append(dict(profile=profile,fixture=name,rejected=True,error=str(ex)));return
            raise ValueError('025 invalid production group accepted '+profile+'/'+name)
        reject('missing-unit',lambda gg,uu,t:(uu.pop(),t)[1])
        reject('duplicate-unit',lambda gg,uu,t:(uu.append(deepcopy(uu[0])),t)[1])
        reject('changed-wording',lambda gg,uu,t:(uu[0].update(translation=uu[0]['translation']+'가'),t)[1])
        reject('changed-review-state',lambda gg,uu,t:(uu[0].update(state='reviewed'),t)[1])
        reject('changed-geometry',lambda gg,uu,t:(gg.update(geometry=[]),t)[1])
        reject('unknown-profile',lambda gg,uu,t:(gg.update(profile='unbounded'),t)[1])
        reject('target-not-selected-wording',lambda gg,uu,t:corrupt_selected(t,uu[0]['id']))
    frozen_write(ROOT/'analysis/pending_insertion_500_033_gate_tests500_v1/result.json',dict(passed=True,positive_groups=len(selection['profiles']),valid_exact500_inputs=summary,rejected_fixture_count=len(cases),fixtures=cases,dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/test_exact500_input_gate_033.py','tools/layout500_inputs_033.py','analysis/pending_insertion_500_033_carry500_v1/preflight.json']},rom_written=False,limits='Real production group entry and frozen-source load_inputs, mutated in-memory inputs only. Not runtime or general malicious-input completeness.'))
    print('PASS025 production gate exact500 and',len(cases),'refusal fixtures')

if __name__=='__main__':main()
