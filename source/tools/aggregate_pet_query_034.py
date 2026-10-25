"""Same-word LF search with fixed native choices; validation owns admission."""
import re
from functools import lru_cache
from field_hint_capacity import events
from pet_choice_capacity_026 import PREFIX
from nickname_capacity import ARGS,advance
from survey_aggregate_pet_033 import variants


def aggregate(original,units,bound):
    seq=events(original)
    if len(seq)<4 or any(k!='command' for _,k,_ in seq[:4]) or [d for _,_,d in seq[:4]]!=PREFIX:raise ValueError('034 query initializer')
    pool={u['id']:u for u in units};labels=set();choice=False
    for _,kind,data in seq[4:]:
        if kind=='command' and data[0]=='spacePx':choice=True
        elif kind=='command' and data[0]=='select':choice=False
        elif kind=='literal' and choice:labels.add(data.key)
    @lru_cache(None)
    def solve(at,rows):
        if at==len(seq):return ()
        _,kind,data=seq[at]
        if kind=='literal':
            values=((pool[data.key]['translation'],) if data.key in labels else variants(pool[data.key]['source'],pool[data.key]['translation'])) if data.key in pool else (data.text,)
            for value in values:
                if data.key in labels and '\n' in value:continue
                next_rows=list(rows)
                for i,line in enumerate(value.split('\n')):
                    if i:next_rows.append(0)
                    next_rows[-1]+=advance(line)
                if len(next_rows)>3 or max(next_rows)>132:continue
                tail=solve(at+1,tuple(next_rows))
                if tail is not None:return ((data.key,value),)+tail
            return None
        name,args=data;delta=0
        if name=='printPlayerNickname':
            if args!=ARGS:return None
            delta=bound
        elif name=='spacePx':
            m=re.fullmatch(r'\t\tcount = (8|16|24)\n',args)
            if m is None:return None
            delta=int(m[1])
        elif name=='space':
            if args!='\t\tcount = 1\n':return None
            delta=8
        elif name.startswith('print') or name.startswith('callBuffer'):return None
        if delta:
            if rows[-1]+delta>132:return None
            return solve(at+1,rows[:-1]+(rows[-1]+delta,))
        if name=='select' and '\t\tclear = true\n' not in args:return None
        return solve(at+1,(0,) if name in ('clearMsg','select') else rows)
    found=solve(4,(0,))
    if found is None:raise ValueError('034 no same-word query aggregate layout')
    values=dict(found)
    if not set(pool)<=set(values):raise ValueError('034 query missing literal identity')
    return {k:values[k] for k in pool}
