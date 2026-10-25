"""v059: unknown windows capped by the narrowest source text origin (140/140/131) instead of 132.
v054: player name/nickname and player-typed profile strings and opponent names bound 48px (4 Hangul) by user policy
(2026-10-24); long entries may overflow the window. Chips88, buffer/item99.
v043 generic page-extent gate: source and target simulated by the SAME rules.

Rows advance on LF inside literals; pages reset on msgOpen/msgOpenQuick/clearMsg/msgClose.
print* commands add print_bound(name) to the current row in both simulations; space/spacePx add their pixels.
Window: origin x L (positionText left, default52) and arrow x A (positionArrow left, default225):
rows1-2 cap 232-L, row3 cap A-2-L. msgOpenQuick uses the same window as msgOpen (041 runtime drew
quick text at52,110). Only an unknown window without explicit positionText is clamped to132.
A target page passes if it has no more rows than max(source rows,3) (standard top110 window, not
inherited) or the source rows otherwise, and each row fits its cap (or source+12 where the source
itself already exceeds the modelled cap). Re-layout only exchanges LF and spaces (no wording change),
page by page, keeping the translator's layout wherever it already fits.
"""
import re
from functools import lru_cache
from field_hint_capacity import events
from tpl_literals import skeleton
from nickname_capacity import advance
from survey_aggregate_pet_033 import replace_exact

PRINT_BOUND=99


NAME_BOUND=48


def print_bound(name):
    """v054 policy (user decision 2026-10-24): player name/nickname, player-typed profile strings and opponent/Navi
    names assumed <=4 Hangul (48px), NOT the native worst case (6 glyphs+suffix=99px). Longer entries may overflow
    the window. Chips88; numeric buffers/items/other strings keep99."""
    if name in ('printBuffer','printItem','printShortString') or name.startswith('printStringBuffer'):return PRINT_BOUND
    if 'Chip' in name:return 88
    return NAME_BOUND
RESET=('msgOpen','msgOpenQuick','clearMsg','msgClose')
QUICK=132
# v059: an unknown window (no msgOpen/positionText in the script) is capped by the narrowest text origin the
# source ever uses: positionText left 92 with arrow 225 -> 232-92=140 and 225-2-92=131 (all other source
# origins 10..80 are wider). Replaces the unsupported 132 clamp.
UNKNOWN=(140,140,131)
CAPS={'normal':(180,180,168),'quick':(132,132,132)}


def script_text(text,script):
    m=re.search(r'^script '+str(script)+r' (mmbn45s?) \{[\s\S]*?(?=^script\s|\Z)',text,re.M)
    if m is None:raise ValueError('script missing')
    return '@archive '+re.search(r'^@archive (\w+)',text,re.M)[1]+'\n'+m[0],m[1]


def arg(args,name,default=None):
    m=re.search(r'\t\t'+name+r' = (\w+)',args)
    return int(m[1]) if m and m[1].isdigit() else default


def simulate(one):
    """Pages: dict(caps,rows,inherited,standard,keys[(key,row,offset)])."""
    seq=events(one);pages=[];rows=[0];box=None;L=52;A=225;top=110;has=False;inherited=True;explicit=False;keys=[]
    def caps():
        c=[232-L,232-L,A-2-L]
        if box is None and not explicit:c=[min(x,u) for x,u in zip(c,UNKNOWN)]
        return c
    def close():
        if has:pages.append(dict(caps=caps(),rows=list(rows),inherited=inherited,standard=(top==110),keys=list(keys)))
    for _,kind,data in seq:
        if kind=='literal':
            keys.append((data.key,len(rows)-1,rows[-1]))
            for n,line in enumerate(data.text.split('\n')):
                if n:rows.append(0)
                rows[-1]+=advance(line)
            has=True;continue
        name,args=data
        if name in RESET:
            close();rows=[0];has=False;inherited=False;keys=[]
            if name in ('msgOpen','msgOpenQuick'):box='normal';L,A,top=52,225,110
            elif name=='msgClose':box=None
        elif name=='positionText':L=arg(args,'left',L);top=arg(args,'top',top);explicit=True
        elif name=='positionArrow':A=arg(args,'left',A)
        elif name.startswith('print'):rows[-1]+=print_bound(name);has=True
        elif name=='space':rows[-1]+=8*arg(args,'count',1)
        elif name=='spacePx':rows[-1]+=arg(args,'count',0)
    close()
    return pages


def page_errors(s,t):
    errs={}
    for i,(a,b) in enumerate(zip(s,t)):
        sr,tr,caps=a['rows'],b['rows'],a['caps']
        limit=len(sr) if a['inherited'] or not a['standard'] else max(len(sr),3)
        if len(tr)>limit:errs[i]=f'rows {len(tr)}>{limit}';continue
        for j,w in enumerate(tr):
            cap=caps[min(j,2)]
            if j<len(sr) and sr[j]>cap:cap=sr[j]+12
            if w>cap:errs[i]=f'row{j} {w}>{cap}';break
    return errs


def check(src_one,tgt_one):
    if skeleton(src_one)!=skeleton(tgt_one):raise ValueError('controls changed')
    s=simulate(src_one);t=simulate(tgt_one)
    if len(s)!=len(t):raise ValueError('page structure differs')
    e=page_errors(s,t)
    if e:raise ValueError(next(iter(e.values())))
    return [dict(caps=a['caps'],source_rows=a['rows'],target_rows=b['rows']) for a,b in zip(s,t)]


def _layout(words,caps,start):
    @lru_cache(None)
    def best(i,row):
        if i==len(words):return ()
        if row>=len(caps):return None
        cap=caps[row];w=start if row==0 else 0;res=None
        for j in range(i,len(words)):
            w+=advance(words[j])+(8 if j>i else 0)
            if w>cap:break
            rest=best(j+1,row+1)
            if rest is not None:
                cand=((i,j+1),)+rest
                if res is None or len(cand)<len(res):res=cand
        return res
    return best(0,0)


def variants(text,caps,row,offset,tail):
    """Alternative LF/space layouts for a literal starting at (row,offset); tail = px that follow on its last row."""
    out=[];lead=len(text)-len(text.lstrip('\n '));trail=len(text)-len(text.rstrip('\n '))
    core=text[lead:len(text)-trail] if trail else text[lead:]
    if not core or '\n' in text[:lead]:return out
    words=tuple(re.split(r'[ \n]',core));head=text[:lead];end=text[len(text)-trail:] if trail else ''
    rem=list(caps[row:]) or [caps[-1]]
    for c in (rem,rem[:-1]+[max(0,rem[-1]-tail)]):
        plan=_layout(words,tuple(c),offset+advance(head))
        if plan:out.append(head+'\n'.join(' '.join(words[a:b]) for a,b in plan)+end)
    if head==' ' and len(rem)>1:
        for c in (rem[1:],rem[1:-1]+[max(0,rem[-1]-tail)]):
            plan=_layout(words,tuple(c),0)
            if plan:out.append('\n'+'\n'.join(' '.join(words[a:b]) for a,b in plan)+end)
    return [v for v in dict.fromkeys(out) if v!=text and v.replace('\n',' ')==text.replace('\n',' ')]


def fit(one,values,rounds=4):
    """Page-local search: change a selected literal only if it reduces the failing pages."""
    vals=dict(values);s=simulate(one)
    def errs(v):
        t=simulate(replace_exact(one,v))
        return None if len(t)!=len(s) else page_errors(s,t)
    cur=errs(vals)
    if cur is None:return vals
    for _ in range(rounds):
        if not cur:break
        improved=False
        t=simulate(replace_exact(one,vals))
        for i in sorted(cur):
            for key,row,off in t[i]['keys']:
                if key not in vals:continue
                pg=t[i];idx=[k for k,_,_ in pg['keys']].index(key)
                last=len(vals[key].split('\n'))-1+row
                tail=0
                for v in variants(vals[key],s[i]['caps'],min(row,2),off,tail):
                    trial=dict(vals,**{key:v});e=errs(trial)
                    if e is not None and len(e)<len(cur) or (e is not None and i not in e and len(e)<=len(cur)):
                        vals,cur,improved=trial,e,True;break
                if i not in cur:break
        if not improved:break
    return vals


def reflow(text,caps,first_offset=0):
    """Fewest rows from row0 by exchanging LF/space only; keeps leading/trailing LFs/spaces."""
    v=variants(text,list(caps),0,first_offset,0)
    return v[0] if v else None


SEPARATOR='\n\tkeyWait\n\t\tany = false\n\tclearMsg\n\t'


def render(one,values,pages):
    """values: key->text; pages: key->[page texts] (split literals, joined by keyWait/clearMsg)."""
    out=replace_exact(one,values)
    from tpl_literals import literals as lits
    for item in reversed(lits(out)):
        if item.key in pages:
            ps=pages[item.key]
            if ' '.join(p.replace('\n',' ') for p in ps)!=values[item.key].replace('\n',' '):raise ValueError('split changes words')
            out=out[:item.start]+SEPARATOR.join('"'+p.replace('\n','\\n')+'"' for p in ps)+out[item.end:]
    return out


def _simple_ok(page):
    if not page['standard'] or page['inherited'] or len(page['rows'])>3:return False
    return all(w<=page['caps'][min(j,2)] for j,w in enumerate(page['rows']))


def split_fit(one,values,max_pages=4):
    """After fit(): split one selected literal per still-failing standard page into extra pages.
    Returns (values, pages) or None. Pages are only LF/space re-layouts of the same words."""
    s=simulate(one);t=simulate(replace_exact(one,values))
    if len(s)!=len(t):return None
    errs=page_errors(s,t);pages={}
    for i in sorted(errs):
        if not s[i]['standard'] or s[i]['inherited']:return None
        sel=[(k,r,o) for k,r,o in t[i]['keys'] if k in values]
        if not sel:return None
        done=False
        for key,row,off in reversed(sel):
            text=values[key];lead=len(text)-len(text.lstrip('\n '));trail=len(text)-len(text.rstrip('\n '))
            if '\n' in text[:lead] or '\n' in (text[len(text)-trail:] if trail else ''):continue
            core=text[lead:len(text)-trail] if trail else text[lead:]
            words=tuple(re.split(r'[ \n]',core));caps=s[i]['caps']
            if row>2:continue
            seq=[caps[j] for j in range(row,3)]+[caps[j%3] for j in range(3*(max_pages-1))]
            plan=_layout(words,tuple(seq),off+advance(text[:lead]))
            if not plan:continue
            first=3-row;lines=[' '.join(words[a:b]) for a,b in plan];chunks=[lines[:first]]+[lines[first+3*n:first+3*(n+1)] for n in range((len(lines)-first+2)//3)]
            chunks=[c for c in chunks if c]
            if len(chunks)<2:continue
            ps=['\n'.join(c) for c in chunks];ps[0]=text[:lead]+ps[0];ps[-1]=ps[-1]+(text[len(text)-trail:] if trail else '')
            trial=dict(pages,**{key:ps})
            try:tgt=render(one,values,trial)
            except ValueError:continue
            tt=simulate(tgt);extra=sum(len(v)-1 for v in trial.values());before=sum(len(v)-1 for k,v in trial.items() if k!=key)
            # pages of source page i in the split target start at i+before and span len(ps)
            span=tt[i+before:i+before+len(ps)]
            if len(tt)!=len(s)+extra or not span or not all(_simple_ok(p) for p in span):continue
            pages=trial;done=True;break
        if not done:return None
    return values,pages


def check_split(one,values,pages):
    """Non-split pages: check() rules against the source; split pages: standard window caps, <=3 rows."""
    if not pages:return check(one,replace_exact(one,values))
    s=simulate(one);u=simulate(replace_exact(one,values));tgt=render(one,values,pages);tt=simulate(tgt)
    if len(s)!=len(u):raise ValueError('page structure differs')
    errs=page_errors(s,u);split_pages=set()
    for i,p in enumerate(u):
        if any(k in pages for k,_,_ in p['keys']):split_pages.add(i)
    if set(errs)-split_pages:raise ValueError('unsplit page overflow')
    if len(tt)!=len(s)+sum(len(v)-1 for v in pages.values()):raise ValueError('split page count')
    at=0;out=[]
    for i in range(len(s)):
        n=1+sum(len(pages[k])-1 for k,_,_ in u[i]['keys'] if k in pages)
        span=tt[at:at+n];at+=n
        if i in split_pages and not all(_simple_ok(p) for p in span):raise ValueError('split page overflow')
        out.append(dict(caps=s[i]['caps'],source_rows=s[i]['rows'],target_pages=[p['rows'] for p in span]))
    return out
