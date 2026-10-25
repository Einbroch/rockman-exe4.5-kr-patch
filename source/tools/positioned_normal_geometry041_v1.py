"""Analysis-only explicit positioned normal pages; never product admission.

Project exact source positions into existing normal-page geometry, leaving
the real source/target scripts unchanged. Only finite explicit triplets below
are admitted for analysis. Caller/loading, actual clipping and clearing need
independent exact-ROM evidence before any product use.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from normal_timing_capacity_025 import validate as core

PROFILES={
    (34,0,14,4,45):'tournament-top',
    (130,12,110,3,141):'tournament-bottom',
    (50,2,30,3,61):'tutorial-top',
}


def project(text,script):
    header=re.search(r'^@archive \w+',text,re.M)[0]+'\n'
    match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',text,re.M)
    if match is None:raise ValueError('Positioned script language')
    one=header+match[0];seq=events(one);positions=[];edits=[];opened=False;seen_literal=False
    for at,kind,data in seq:
        if kind=='literal':seen_literal=True;continue
        name,args=data
        if name=='msgOpen':
            if opened or args:raise ValueError('Positioned single normal initializer')
            opened=True
        if name not in ('positionMugshot','positionBox','positionText','positionArrow'):continue
        if seen_literal:raise ValueError('Positioned geometry after first literal')
        patterns={'positionMugshot':r'\t\tleft = 27\n\t\ttop = (\d+)\n','positionBox':r'\t\tleft = 0\n\t\ttop = (\d+)\n\t\ttype = 0\n','positionText':r'\t\tleft = 52\n\t\ttop = (\d+)\n\t\tarrowDistance = (\d+)\n','positionArrow':r'\t\tleft = (?:225|221)\n\t\ttop = (\d+)\n'}
        m=re.fullmatch(patterns[name],args)
        if not m or opened!=(name in ('positionText','positionArrow')):raise ValueError('Positioned exact initializer ordering/arguments')
        positions.append((name,tuple(map(int,m.groups()))));raw='\t'+name+'\n'+args
        if one[at:at+len(raw)]!=raw:raise ValueError('Positioned canonical span')
        edits.append((at,at+len(raw)))
    if [x[0] for x in positions]!=['positionMugshot','positionBox','positionText','positionArrow']:raise ValueError('Positioned full explicit geometry')
    key=tuple(v for _,vs in positions for v in vs)
    if key not in PROFILES:raise ValueError('Positioned finite source geometry')
    arrow=221 if PROFILES[key]=='tutorial-top' else 225
    if '\tpositionArrow\n\t\tleft = '+str(arrow)+'\n' not in one:raise ValueError('Positioned exact arrow x')
    for a,b in reversed(edits):one=one[:a]+one[b:]
    return one,dict(profile=PROFILES[key],origin=[52,key[2]],box_top=key[1],portrait=[27,key[0]],arrow=[arrow,key[4]],arrow_distance=key[3])


def validate(original,target,scripts,selected_ids):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('Positioned protected structure')
    before,b=project(original,scripts[0]);after,a=project(target,scripts[0])
    if a!=b:raise ValueError('Positioned source geometry changed')
    proof=core(before,after,scripts,selected_ids,99,88)
    for p in proof:
        p.update(a,initializer='source-explicit-positioned-msgOpen',geometry_projection_only=True,actual_positioned_runtime_pending=True,product_admitted=False)
    return proof
