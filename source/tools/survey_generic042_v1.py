"""Survey remaining canonical groups through the generic page gate (no writes)."""
import sys,re,json
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT
from cumulative_batch500 import read
from tpl_literals import literals
from survey_aggregate_pet_033 import replace_exact
from generic_page_gate059_v1 import script_text,check,reflow,CAPS,simulate,fit,split_fit,check_split


def try_group(g,text,drafts):
    one,lang=script_text(text,g['script']);raw={u.key:u.text for u in literals(one)};values={}
    for d in g['drafts']:
        if d['path'] not in drafts:drafts[d['path']]=read(d['path'])
        u=next(x for x in drafts[d['path']]['units'] if x['id']==d['id'])
        if u['source']!=raw.get(u['id']):return None,'source mismatch',lang
        values[u['id']]=u['translation']
    try:return (values,check(one,replace_exact(one,values))),None,lang
    except ValueError as ex:pass
    values=fit(one,values)
    try:return (values,check(one,replace_exact(one,values))),None,lang
    except ValueError as ex:err=re.sub(r'\d+','N',str(ex))
    r=split_fit(one,values)
    if r is None:return None,err,lang
    try:return (r,check_split(one,*r)),None,'split-'+lang
    except ValueError as ex:return None,'split '+str(ex),lang


if __name__=='__main__':
    c=read('analysis/pending_insertion_500_041_inventory_v1/census.json');done=set(read('analysis/pending_insertion_500_041_source_v8/selection.json')['selected_ids'])
    t={};d={};ok=Counter();bad=Counter()
    for g in c['groups']:
        if set(g['ids'])&done:continue
        if g['archive'] not in t:t[g['archive']]=(ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig')
        r,why,lang=try_group(g,t[g['archive']],d)
        if r:ok[(lang,g['storage'])]+=g['units']
        else:bad[(lang,why)]+=g['units']
    print('PASS',sum(ok.values()),ok.most_common());print('FAIL',sum(bad.values()));[print(' ',n,k) for k,n in bad.most_common(15)]
