"""Geometry projection of protected battle-tail stores, NOT native admission.

Only stores after the final explicit page wait, before flags/end, are removed
from a geometry-only projection. No source or output bytecode is transformed.
Native store execution and event outcome require separate source/CPU evidence.
"""
import re
from tpl_literals import skeleton
from field_hint_capacity import events
from normal_timing_capacity_025 import validate as core

def validate(original,target,scripts,ids,bound,chip_bound=88):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('038 protected tail scope')
    arc=re.search(r'^@archive (\w+)',original,re.M)[1];script=scripts[0]
    projected=[];tail=None
    for tpl in (original,target):
        m=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)
        if m is None:raise ValueError('038 tail script language')
        text='@archive '+arc+'\n'+m[0];seq=events(text);stores=[i for i,e in enumerate(seq) if e[1]=='command' and e[2][0] in ('storeGlobal8','storeGlobal16')]
        if not stores:raise ValueError('038 no store tail')
        first=stores[0]
        if first==0 or seq[first-1][1:]!=('command',('keyWait','\t\tany = false\n')):raise ValueError('038 tail must follow final explicit wait')
        rows=[]
        for _,kind,data in seq[first:]:
            if kind!='command':raise ValueError('038 text after battle tail')
            name,args=data
            if name in ('storeGlobal8','storeGlobal16'):
                a=re.fullmatch(r'\t\tglobal = (\d+)\n\t\tvalue = (\d+)\n',args)
                if a is None:raise ValueError('038 noncanonical store')
                index,value=map(int,a.groups())
                if not (name=='storeGlobal8' and index in (24,25,26,28) and 0<=value<256 or name=='storeGlobal16' and index==27 and 0<=value<65536):raise ValueError('038 battle store domain')
                rows.append(dict(command=name,index=index,value=value))
            elif name in ('flagSet','flagClear'):
                if not re.fullmatch(r'\t\tflag = \d+\n',args):raise ValueError('038 tail flag arguments')
            elif name!='end' or args:raise ValueError('038 tail control outside stores/flags/end')
        if tail is not None and rows!=tail:raise ValueError('038 protected stores changed')
        tail=rows
        for name in ('storeGlobal8','storeGlobal16'):
            text=re.sub(r'^\t'+name+r'\n\t\tglobal = \d+\n\t\tvalue = \d+\n','',text,flags=re.M)
        projected.append(text)
    proof=core(*projected,scripts,ids,bound,chip_bound)
    proof[0].update(geometry_projection_only=True,source_store_tail_retained=tail,native_store_effects_CPU_pending=True,battle_outcome_runtime_pending=True)
    return proof
