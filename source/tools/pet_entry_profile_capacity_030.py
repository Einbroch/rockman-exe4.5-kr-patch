"""Analysis-only source-preserved entry guards followed by adopted PET body.

No guard executes here. All taken branches/call effects remain unadmitted
until native CPU and final-ROM GBA evidence bind their applicability.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from pet_array_capacity_029 import validate as arrays
from pet_profile_capacity_027_v2 import validate as direct
from pet_nickname_capacity_025 import validate as quick
from pet_guard_capacity_027 import PATTERNS

CALLS={'callCheckDefinedSchool':2,'callBufferRandomOlderBro':3,'callBufferRandomYoungerBro':4,'callBufferRandomOlderSis':5,'callBufferRandomYoungerSis':6,'callBufferRandomFriend':7,'callCheckDefinedFavFood':8,'callBufferRandomHobby':9,'callCheckDefinedDream':10,'callCheckDefinedCrush':11,'callCheckDefinedIdol':12,'callCheckDefinedPlayerEnemy':13,'callBufferRandomFavShow':14,'callCheckDefinedBestSubject':15,'callCheckDefinedWorstSubject':16,'callBufferRandomWish':17}
CALL_ARGS=r'\t\tjumpIfUndefined = (\d+|continue)\n\t\tjumpIfDefined = (\d+|continue)\n'

def project(tpl):
    guards=[];spans=[]
    for pos,kind,data in events(tpl):
        if kind!='command':raise ValueError('030 entry guard before initializer only')
        name,args=data
        if name=='positionBox':break
        if len(guards)>=8:raise ValueError('030 finite entry guard count')
        pattern=CALL_ARGS if name in CALLS else PATTERNS.get(name)
        if pattern is None or not re.fullmatch(pattern,args):raise ValueError('030 unknown entry guard '+name)
        for value in re.findall(r'jump\w+ = (\w+)',args):
            if value!='continue' and not 0<=int(value)<=254:raise ValueError('030 branch script index')
        if name=='checkFlag' and not 0<=int(re.search(r'flag = (\d+)',args)[1])<=65535:raise ValueError('030 flag bound')
        if name=='checkGlobal' and any(int(v)>255 for v in re.findall(r'(?:variable|value) = (\d+)',args)):raise ValueError('030 global bound')
        raw='\t'+name+'\n'+args
        if tpl[pos:pos+len(raw)]!=raw:raise ValueError('030 exact guard span')
        spans.append((pos,pos+len(raw)));guards.append(dict(command=name,arguments=args,native_FC0F_index=CALLS.get(name)))
    if not guards:raise ValueError('030 nonempty entry guard scope')
    out=tpl
    for a,b in reversed(spans):out=out[:a]+out[b:]
    return out,guards

def validate(original,target,scripts,selected_ids,nickname_bound):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('030 protected source controls')
    header=re.search(r'^@archive \w+',original,re.M)[0]+'\n';pattern=r'^script '+str(scripts[0])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)'
    src,dst=(re.search(pattern,t,re.M) for t in (original,target))
    if not src or not dst:raise ValueError('030 source script identity')
    so,sg=project(header+src[0]);st,tg=project(header+dst[0])
    if sg!=tg:raise ValueError('030 guard changed')
    errors=[]
    for core in (arrays,direct,quick):
        try:proof=core(so,st,scripts,selected_ids,nickname_bound);break
        except ValueError as ex:errors.append(str(ex))
    else:raise ValueError('030 body '+' | '.join(errors))
    proof[0].update(preserved_entry_guards=sg,conditional_taken_branch_and_caller_unproven=True,product_admitted=False)
    return proof
