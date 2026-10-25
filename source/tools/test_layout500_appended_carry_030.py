"""Real source-derived027->028->029 append composition before allocation."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from layout500_inputs_027 import load_inputs as load027
from layout500_inputs_028 import load_inputs as load028
from layout500_inputs_029 import load_inputs as load029
from layout500_product_030 import append_prior027,append_prior028,append_new_raw
from layout500_inputs_030 import load_inputs as load030

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    p27,_=load027(source);p28,_=load028(source);p29,_=load029(source);p30,summary=load030(source)
    plugins=ROOT/'analysis/pending_insertion_500_030_carry_v1/plugins'
    blob=bytearray();products={};records=[];selected={}
    append_prior027(source,blob,products,records,selected,p27,p28,p29,p30,plugins)
    append_prior028(source,blob,products,records,selected,p28,p29,p30,plugins)
    append_new_raw(source,blob,products,records,selected,p30,plugins)
    expected={r['archive']:(r,p) for r,p in p27}
    expected.update({r['archive']:(r,p) for r,p in p28})
    present=set(selected)
    expected.update({r['archive']:(r,p) for r,p in p29 if r['archive'] in present})
    expected.update({r['archive']:(r,p) for r,p in p30 if r['archive'] in present})
    if len(records)!=21 or len(products)!=21 or len(present)!=21:raise ValueError('029 append population')
    for record in records:
        r,p=expected[record['archive']];at,stored,payload=products[int(record['archive'],16)]
        if stored!=p or payload!=p or at&3 or blob[at-len(source):at-len(source)+len(p)]!=p:raise ValueError('029 append source-derived final payload')
        if r.get('new_ids') and record.get('cumulative030') and set(record['cumulative030']['new_ids'])!=set(r['new_ids']):raise ValueError('029 append selected IDs')
    refused=[]
    for label,call in [('027',lambda:append_prior027(source,bytearray(),{},[],{p27[0][0]['archive']:True},p27,p28,p29,p30,plugins)),('028',lambda:append_prior028(source,bytearray(),{},[],{r['archive']:True for r,_ in p28},p28,p29,p30,plugins))]:
        try:call()
        except ValueError as ex:refused.append(dict(stage=label,error=str(ex)))
        else:raise ValueError('029 duplicate writer accepted')
    changed=sorted(r['archive'] for r,_ in p30 if r['archive'] in present)
    deps=['tools/test_layout500_appended_carry_030.py','tools/layout500_product_030.py','analysis/pending_insertion_500_030_carry_v1/preflight.json']
    frozen_write(ROOT/'analysis/pending_insertion_500_030_append_tests_v1/result.json',dict(schema=1,passed=True,current_inputs=summary,appended_archives=21,current_changed_appended_archives=changed,cumulative_units=sum(r['translated_units'] for r in records),writer_overlap_refused=refused,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,limits='Isolated actual composition functions, no ROM/runtime or natural caller claim.'))
    print('PASS02920 prior appended archives;',len(changed),'changed before one allocation; duplicate writers refused')

if __name__=='__main__':main()
