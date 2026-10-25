"""Analysis projection of source-identical PET entry-only flag/global guards.

No guard executes in this model. The exact native PET initializer is still
required, and target controls are compared before projection. Taken branches,
natural caller state and flag effects require separate evidence.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from pet_nickname_capacity_025 import PREFIX,validate as quick
from pet_nickname_flags_capacity_025_v2 import validate as flags

PATTERNS={
    'checkFlag':r'\t\tflag = (\d+)\n\t\tjumpIfTrue = (\d+|continue)\n\t\tjumpIfFalse = (\d+|continue)\n',
    'checkGlobal':r'\t\tvariable = (\d+)\n\t\tvalue = (\d+)\n\t\tjumpIfEqual = (\d+|continue)\n\t\tjumpIfNotEqual = (\d+|continue)\n'
}

def project(tpl):
    seq=events(tpl);edits=[];guards=[]
    for pos,kind,data in seq:
        if kind!='command':raise ValueError('PET guard entry before literal only')
        name,args=data
        if name=='positionBox':break
        if name not in PATTERNS or not re.fullmatch(PATTERNS[name],args):raise ValueError('PET finite canonical entry guards')
        nums=[int(v) for v in re.findall(r' = (\d+)',args)]
        if name=='checkFlag' and not 0<=nums[0]<=65535 or name=='checkGlobal' and not(0<=nums[0]<=255 and 0<=nums[1]<=255):raise ValueError('PET entry guard storage bounds')
        raw='\t'+name+'\n'+args
        if tpl[pos:pos+len(raw)]!=raw:raise ValueError('PET entry guard canonical span')
        edits.append((pos,pos+len(raw)));guards.append(dict(command=name,arguments=args))
    if not guards:raise ValueError('PET guard nonempty scope')
    out=tpl
    for a,b in reversed(edits):out=out[:a]+out[b:]
    return out,guards

def validate(original,target,scripts,selected_ids,nickname_bound):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('PET guard protected scope')
    header=re.search(r'^@archive \w+',original,re.M)[0]+'\n';pattern=r'^script '+str(scripts[0])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)'
    src,dst=(re.search(pattern,t,re.M) for t in (original,target))
    if not src or not dst:raise ValueError('PET guard script identity')
    so,sg=project(header+src[0]);st,tg=project(header+dst[0])
    if sg!=tg:raise ValueError('PET guard source identity')
    errors=[]
    for core in (quick,flags):
        try:proof=core(so,st,scripts,selected_ids,nickname_bound);break
        except ValueError as ex:errors.append(str(ex))
    else:raise ValueError('PET guarded core '+' | '.join(errors))
    proof[0]['preserved_entry_guards']=sg;proof[0]['taken_guard_branch_and_natural_caller_pending']=True
    return proof
