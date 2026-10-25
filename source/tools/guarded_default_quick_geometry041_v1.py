"""Conditional layout projection for preserved native mail entry guards."""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from default_quick_geometry041_v1 import validate as core


def project(text,script):
    h=re.search(r'^@archive \w+',text,re.M)[0]+'\n';m=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',text,re.M)
    if not m:raise ValueError('Guarded default quick source script')
    one=h+m[0];edits=[];guards=[]
    for at,kind,data in events(one):
        if kind!='command':raise ValueError('Guarded default quick literal before initializer')
        name,args=data
        if name=='callSkipMugshotFadeIn':break
        pattern=r'\t\tvariable = (\d+)\n\t\tvalue = (\d+)\n\t\tjumpIfEqual = continue\n\t\tjumpIfNotEqual = (\d+)\n'
        match=re.fullmatch(pattern,args)
        if name!='checkGlobal' or not match or len(guards)>=4 or any(int(x)>254 for x in match.groups()):raise ValueError('Guarded default quick finite read-only entry condition')
        raw='\t'+name+'\n'+args
        if one[at:at+len(raw)]!=raw:raise ValueError('Guarded default quick canonical span')
        edits.append((at,at+len(raw)));guards.append(dict(command=name,arguments=args,execution_and_taken_branch_pending=True))
    if not guards:raise ValueError('Guarded default quick nonempty guards')
    for a,b in reversed(edits):one=one[:a]+one[b:]
    return one,guards


def validate(original,target,scripts,selected_ids):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('Guarded default quick protected controls')
    so,sg=project(original,scripts[0]);to,tg=project(target,scripts[0])
    if sg!=tg:raise ValueError('Guarded default quick changed original condition')
    proof=core(so,to,scripts,selected_ids)
    for p in proof:p.update(preserved_entry_guards=sg,source_guard_CPU_and_runtime_pending=True,product_admitted=False)
    return proof
