"""Geometry-only projection of source Navi branches after a cleared page.

Original branch controls are kept in compiled output. Native branching and
continuation initialization are explicitly NOT admitted by this model.
"""
import re
from tpl_literals import skeleton
from field_hint_capacity import events
from normal_timing_capacity_025 import validate as core

def validate(original,target,scripts,ids,bound,chip_bound=88):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('038 Navi-tail protected scope')
    arc=re.search(r'^@archive (\w+)',original,re.M)[1];script=scripts[0];projected=[];branches=None
    for tpl in (original,target):
        m=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)
        if m is None:raise ValueError('038 Navi-tail script language')
        text='@archive '+arc+'\n'+m[0];seq=events(text);indices=[i for i,e in enumerate(seq) if e[1]=='command' and e[2][0]=='checkNavi']
        if not indices:raise ValueError('038 no Navi tail')
        first=indices[0]
        if first<2 or seq[first-1][1:]!=('command',('clearMsg','')) or seq[first-2][1:]!=('command',('keyWait','\t\tany = false\n')):raise ValueError('038 Navi tail only after waited cleared page')
        rows=[]
        for _,kind,data in seq[first:]:
            if kind!='command':raise ValueError('038 text after Navi-tail branch')
            name,args=data
            if name=='checkNavi':
                a=re.fullmatch(r'\t\tnavi = (\d+)\n\t\tjumpIfTrue = (\d+)\n\t\tjumpIfFalse = continue\n',args)
                if a is None or not 0<=int(a[1])<23 or not 0<=int(a[2])<255:raise ValueError('038 finite Navi-tail operands')
                rows.append(dict(navi=int(a[1]),target=int(a[2])))
            elif name!='end' or args:raise ValueError('038 branch tail outside checkNavi/end')
        if branches is not None and branches!=rows:raise ValueError('038 protected Navi branch changed')
        branches=rows
        text=re.sub(r'^\tcheckNavi\n\t\tnavi = \d+\n\t\tjumpIfTrue = \d+\n\t\tjumpIfFalse = continue\n','',text,flags=re.M)
        projected.append(text)
    proof=core(*projected,scripts,ids,bound,chip_bound)
    proof[0].update(geometry_projection_only=True,source_navi_branch_tail_retained=branches,native_branch_and_continuation_runtime_pending=True)
    return proof
