"""Prove032 no changed prior-appended inputs; controlled new scope refusals."""
from copy import deepcopy
from importlib import import_module
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from layout500_inputs_032 import load_inputs
from layout500_product_032 import guard_unaffected_appended


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);inputs,summary=load_inputs(sp.read_bytes());priors=[]
    for version in ('027','028','030'):
        module=import_module('layout500_inputs_'+version);p=module.MANIFEST;require_hash(ROOT/p,module.MANIFEST_SHA)
        m=read(p);priors.append([(r,b'') for r in m['archives']])
    valid=guard_unaffected_appended(inputs,*priors);cases=[]
    for group,prior in zip(('027','028','030'),priors):
        record=next(r for r,_ in prior if r['storage']=='new-raw');bad=deepcopy(inputs);bad[0][0]['archive']=record['archive']
        try:guard_unaffected_appended(bad,*priors)
        except ValueError as ex:cases.append(dict(fixture='changed-prior'+group+'-appended',rejected=True,error=str(ex)))
        else:raise ValueError('032 prior appended scope silently admitted')
    bad=deepcopy(inputs);bad[0][0]['storage']='new-raw'
    try:guard_unaffected_appended(bad,*priors)
    except ValueError as ex:cases.append(dict(fixture='unimplemented-new032-RAW',rejected=True,error=str(ex)))
    else:raise ValueError('032 missing allocation path admitted')
    frozen_write(ROOT/'analysis/pending_insertion_500_032_append_guard_v1/result.json',dict(schema=1,passed=True,actual_current_summary=summary,unchanged_prior_route=valid,controlled_refusals=cases,rom_written=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in ('tools/test_layout500_appended_guard_032.py','tools/layout500_product_032.py','tools/layout500_inputs_032.py','tools/specs/primary032_version.json')}))
    print('032 guarded unchanged031 appended route PASS',valid,'refusals',len(cases))


if __name__=='__main__':main()
