"""Same-wording, same-row-count placement in the isolated full-box range."""
from functools import lru_cache
from nickname_capacity import advance

def place(text):
    rows=text.count('\n')+1
    if rows>3:return None
    caps=(180,180,168)
    if all(advance(s)<=caps[i] for i,s in enumerate(text.split('\n'))):return text
    flat=text.replace('\n',' ')
    @lru_cache(None)
    def solve(start,row):
        if row==rows-1:
            tail=flat[start:]
            return (tail,) if tail and advance(tail)<=caps[row] else None
        choices=[]
        for at in range(start+1,len(flat)):
            if flat[at]!=' ':continue
            head=flat[start:at]
            if advance(head)>caps[row]:break
            if not head or head.endswith(' '):continue
            rest=solve(at+1,row+1)
            if rest is not None:choices.append((head,)+rest)
        return min(choices,key=lambda xs:(max(map(advance,xs)),sum((caps[row+i]-advance(x))**2 for i,x in enumerate(xs)),xs)) if choices else None
    lines=solve(0,0)
    if lines is None:return None
    value='\n'.join(lines)
    if value.replace('\n',' ')!=flat or value.count('\n')!=text.count('\n'):raise ValueError('Full-box wording/topology changed')
    return value
