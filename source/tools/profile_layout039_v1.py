"""Layout proposal only: preserve all wording through explicit break kinds.

An old LF is normalized to one space, as in the existing layout convention.
Space breaks consume that exact space; Hangul-syllable breaks consume none.
No shortening/substitution, page/wait changes, or product admission is done.
"""
from functools import lru_cache
from nickname_capacity import advance

def reconstruct(lines,kinds):
    if not lines or len(kinds)!=len(lines)-1 or any(k not in ('space','hangul-syllable') for k in kinds):
        raise ValueError('039 explicit line-break schema')
    return ''.join(line+(' ' if kinds[i]=='space' else '') if i<len(kinds) else line for i,line in enumerate(lines))

def propose(canonical,cap=132):
    if not canonical or canonical[0].isspace() or canonical[-1].isspace() or any(c in canonical for c in '\r\t'):
        raise ValueError('039 layout scope requires unpadded body literal')
    flat=canonical.replace('\n',' ')
    @lru_cache(None)
    def solve(start,left):
        tail=flat[start:]
        if tail and advance(tail)<=cap:return (0,0,[tail],[])
        if left<=1:return None
        best=None
        for at in range(start+1,len(flat)):
            line=flat[start:at]
            if advance(line)>cap:break
            if flat[at]==' ' and at+1<len(flat) and flat[at+1]!=' ':
                kind='space';nxt=at+1;soft=0
            elif '\uac00'<=flat[at-1]<='\ud7a3' and '\uac00'<=flat[at]<='\ud7a3':
                kind='hangul-syllable';nxt=at;soft=1
            else:continue
            rest=solve(nxt,left-1)
            if rest is None:continue
            score=(soft+rest[0],(cap-advance(line))**2+rest[1],[line]+rest[2],[kind]+rest[3])
            if best is None or score[:2]<best[:2]:best=score
        return best
    found=solve(0,3)
    if found is None:raise ValueError('039 wording exceeds three-row capacity')
    lines,kinds=found[2:];target='\n'.join(lines)
    if reconstruct(lines,kinds)!=flat or len(lines)>3 or any(advance(x)>cap for x in lines):raise ValueError('039 lossless layout invariant')
    return dict(canonical=canonical,flat_wording=flat,target=target,lines=lines,break_kinds=kinds,soft_breaks=found[0],widths=list(map(advance,lines)),wording_changed=False,proposal_only=True,presentation_approved=False)
