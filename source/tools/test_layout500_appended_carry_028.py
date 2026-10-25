"""Exercise real027->028 composition before one allocation, no ROM written."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from layout500_inputs_027 import load_inputs as load027
from layout500_inputs_028 import load_inputs as load028
from layout500_product_028 import append_prior027,append_new_raw


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    prior,_=load027(source);current,summary=load028(source);blob=bytearray();products={};records=[];selected={};plugins=ROOT/'analysis/pending_insertion_500_028_carry_v1/plugins'
    append_prior027(source,blob,products,records,selected,prior,current,plugins)
    if len(records)!=11 or len(products)!=11:raise ValueError('028 prior027 allocation population')
    changed={r['archive']:raw for r,raw in current if r['storage']=='raw-carry'}
    if len(changed)!=2:raise ValueError('028 bounded appended-carry population')
    for r,raw in prior:
        at,stored,payload=products[r['source_row']['offset']]
        expected=changed.get(r['archive'],raw)
        if stored!=expected or payload!=expected or blob[at-len(source):at-len(source)+len(expected)]!=expected:raise ValueError('028 merged before one prior027 allocation')
    append_new_raw(source,blob,products,records,selected,current,plugins)
    if len(records)!=20 or len(products)!=20:raise ValueError('028 cumulative raw allocation population')
    union={u['id'] for r in records for u in r['layout']}
    if len(union)!=1000 or sum(r['translated_units'] for r in records)!=1000:raise ValueError('028 exact027+028 populations')
    for r,raw in current:
        at,stored,payload=products[r['source_row']['offset']]
        if stored!=raw or payload!=raw or at&3:raise ValueError('028 final source-bound current payload')
    refused=[]
    try:append_prior027(source,bytearray(),{},{}, {prior[0][0]['archive']:True},prior,current,plugins)
    except ValueError as ex:refused.append(str(ex))
    else:raise ValueError('028 prior writer overlap accepted')
    deps=['tools/test_layout500_appended_carry_028.py','tools/layout500_product_028.py','tools/layout500_product_027.py','analysis/pending_insertion_500_028_carry_v1/preflight.json']
    frozen_write(ROOT/'analysis/pending_insertion_500_028_append_tests_v1/result.json',dict(schema=1,passed=True,current_inputs=summary,prior027_archives=11,current_new_archives=9,current_changed_appended_archives=2,cumulative_units=1000,writer_overlap_refused=refused,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,runtime_tested=False,limits='Real composition/allocation functions on isolated in-memory source-derived block; not whole ROM or GBA evidence.'))
    print('PASS028 appended carry2 preserved+merged, newRAW9, union1000, writer overlap refused; NO ROM')


if __name__=='__main__':main()
