"""Conditional geometry ONLY for native default-origin quick mail alerts.

No explicit position in these scripts: a caller must independently prove
fresh native default52,110 context before this can enter any product build.
Projection is analysis-only and never rewrites actual protected controls.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from normal_timing_capacity_025 import validate as core


def project(text,script):
    h=re.search(r'^@archive \w+',text,re.M)[0]+'\n';m=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',text,re.M)
    if not m:raise ValueError('Default quick source script')
    one=h+m[0];seq=events(one)
    prefix=[('callSkipMugshotFadeIn',''),('msgOpenQuick','')]
    if [e[2] for e in seq[:2] if e[1]=='command']!=prefix or any(e[1]!='command' for e in seq[:2]):raise ValueError('Default quick exact fade/quick prefix')
    if any(k=='command' and d[0].startswith(('position','print','callBuffer')) for _,k,d in seq):raise ValueError('Default quick no explicit layout/provider')
    raw='\tcallSkipMugshotFadeIn\n\tmsgOpenQuick\n'
    if one.count(raw)!=1:raise ValueError('Default quick canonical prefix span')
    return one.replace(raw,'\tmsgOpen\n',1)


def validate(original,target,scripts,selected_ids):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('Default quick protected scope')
    before=project(original,scripts[0]);after=project(target,scripts[0]);proof=core(before,after,scripts,selected_ids,99,88)
    for p in proof:p.update(initializer='native-default-context-required/msgOpenQuick',assumed_origin=[52,110],caller_default_origin_binding_required=True,fade_command_CPU_and_runtime_pending=True,geometry_projection_only=True,product_admitted=False)
    return proof
