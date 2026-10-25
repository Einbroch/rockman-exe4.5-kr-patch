"""Generic page-extent gate for one script: source and target simulated by the SAME rules.

Rows advance on LF inside literals; pages reset on msgOpen/msgOpenQuick/clearMsg/msgClose.
print* commands add a fixed bound to the current row in both simulations. Commands are
otherwise neutral, and they are identical in source and target (skeleton equality).
A target page passes if every row fits max(box cap for that row, source width of the same
row) and it has no more rows than max(source rows, box rows) where the box is known, or
the source rows where it is not. Reflow only exchanges LF and spaces (no wording change).
"""
import re
from functools import lru_cache
from field_hint_capacity import events
from tpl_literals import literals,skeleton
from nickname_capacity import advance

PRINT_BOUND=99
RESET=('msgOpen','msgOpenQuick','clearMsg','msgClose')
QUICK=132


def script_text(text,script):
    m=re.search(r'^script '+str(script)+r' (mmbn45s?) \{[\s\S]*?(?=^script\s|\Z)',text,re.M)
    if m is None:raise ValueError('script missing')
    return '@archive '+re.search(r'^@archive (\w+)',text,re.M)[1]+'\n'+m[0],m[1]


def arg(args,name,default=None):
    m=re.search(r'\t\t'+name+r' = (\w+)',args)
    return int(m[1]) if m and m[1].isdigit() else default


def simulate(one):
    """Pages as (caps, row_limit_known, rows, inherited). caps from origin x L and arrow x A:
    rows1-2 = 232-L, row3 = A-5-L (L=52,A=225 gives the verified 180/180/168);
    quick or unknown window additionally capped at 132."""
    seq=events(one);pages=[];rows=[0];box=None;L=52;A=225;top=110;has=False;inherited=True;explicit=False
    def caps():
        c=[232-L,232-L,A-2-L]
        if box=='quick' or (box is None and not explicit):c=[min(x,QUICK) for x in c]
        return c
    def close():
        if has:pages.append(dict(caps=caps(),rows=list(rows),inherited=inherited,standard=(top==110)))
    for _,kind,data in seq:
        if kind=='literal':
            for n,line in enumerate(data.text.split('\n')):
                if n:rows.append(0)
                rows[-1]+=advance(line)
            has=True;continue
        name,args=data
        if name in RESET:
            close();rows=[0];has=False;inherited=False
            if name=='msgOpen':box='normal';L,A,top=52,225,110
            elif name=='msgOpenQuick':box='quick';L,A,top=52,225,110
            elif name=='msgClose':box=None
        elif name=='positionText':L=arg(args,'left',L);top=arg(args,'top',top);explicit=True
        elif name=='positionArrow':A=arg(args,'left',A)
        elif name.startswith('print'):rows[-1]+=PRINT_BOUND;has=True
        elif name=='space':rows[-1]+=8*arg(args,'count',1)
        elif name=='spacePx':rows[-1]+=arg(args,'count',0)
    close()
    return pages


def check(src_one,tgt_one):
    if skeleton(src_one)!=skeleton(tgt_one):raise ValueError('controls changed')
    s=simulate(src_one);t=simulate(tgt_one)
    if len(s)!=len(t):raise ValueError('page structure differs')
    out=[]
    for a,b in zip(s,t):
        sr,tr,caps=a['rows'],b['rows'],a['caps']
        limit=len(sr) if a['inherited'] or not a['standard'] else max(len(sr),3)
        if len(tr)>limit:raise ValueError(f'rows {len(tr)}>{limit}')
        for i,w in enumerate(tr):
            cap=caps[min(i,2)]
            if i<len(sr) and sr[i]>cap:cap=sr[i]+12
            if w>cap:raise ValueError(f'row{i} {w}>{cap}')
        out.append(dict(caps=caps,source_rows=sr,target_rows=tr))
    return out


CAPS={'normal':(180,180,168),'quick':(132,132,132)}


def reflow(text,caps,first_offset=0):
    """Fewest rows by exchanging LF/space only; keeps leading/trailing LFs/spaces."""
    lead=len(text)-len(text.lstrip('\n '));trail=len(text)-len(text.rstrip('\n '))
    core=text[lead:len(text)-trail] if trail else text[lead:]
    words=re.split(r'[ \n]',core)
    @lru_cache(None)
    def best(i,row):
        if i==len(words):return ()
        cap=caps[min(row,len(caps)-1)];off=first_offset if row==0 else 0;w=off;res=None
        for j in range(i,len(words)):
            w+=advance(words[j])+(8 if j>i else 0)
            if w>cap:break
            rest=best(j+1,row+1) if j+1<len(words) else ()
            if rest is not None:
                cand=((i,j+1),)+rest
                if res is None or len(cand)<len(res):res=cand
        return res
    plan=best(0,0)
    if plan is None:return None
    return text[:lead]+'\n'.join(' '.join(words[a:b]) for a,b in plan)+(text[len(text)-trail:] if trail else '')


def fit(one,values):
    """Re-lay selected literals in order, each from its actual row/offset in the target page.
    Only LF<->space exchanges; returns new values (may equal input) or None."""
    out=dict(values)
    for _ in range(2):
        from survey_aggregate_pet_033 import replace_exact
        tgt=replace_exact(one,out);seq=events(tgt);rows=[0];box=None;L=52;A=225;explicit=False;changed=False
        def caps():
            c=[232-L,232-L,A-2-L]
            if box=='quick' or (box is None and not explicit):c=[min(x,QUICK) for x in c]
            return c
        for _,kind,data in seq:
            if kind=='literal':
                if data.key in out and data.text==out[data.key]:
                    c=caps();r=len(rows)-1
                    if r<3:
                        text=out[data.key];alt=reflow_from(text,c[r:]+[c[-1]]*0,rows[-1])
                        if alt is not None and alt!=text and alt.replace('\n',' ')==text.replace('\n',' '):out[data.key]=alt;changed=True;data_text=alt
                        else:data_text=text
                    else:data_text=out[data.key]
                else:data_text=data.text
                for n,line in enumerate(data_text.split('\n')):
                    if n:rows.append(0)
                    rows[-1]+=advance(line)
                continue
            name,args=data
            if name in RESET:
                rows=[0]
                if name=='msgOpen':box='normal';L,A=52,225
                elif name=='msgOpenQuick':box='quick';L,A=52,225
                elif name=='msgClose':box=None
            elif name=='positionText':L=arg(args,'left',L);explicit=True
            elif name=='positionArrow':A=arg(args,'left',A)
            elif name.startswith('print'):rows[-1]+=PRINT_BOUND
            elif name=='space':rows[-1]+=8*arg(args,'count',1)
            elif name=='spacePx':rows[-1]+=arg(args,'count',0)
        if not changed:break
    return out


def reflow_from(text,caps,offset):
    """Like reflow but the first row already holds `offset` px and rows are limited to len(caps).
    A leading space after variable text may become LF (still only a space<->LF exchange)."""
    if not caps:return None
    first=_reflow_from(text,caps,offset)
    if first is None and text.startswith(' ') and not text.startswith('  ') and len(caps)>1:
        alt=_reflow_from(text[1:],caps[1:],0)
        if alt is not None:return '\n'+alt
    return first


def _reflow_from(text,caps,offset):
    if not caps:return None
    lead=len(text)-len(text.lstrip('\n '));trail=len(text)-len(text.rstrip('\n '))
    if '\n' in text[:lead]:return None
    core=text[lead:len(text)-trail] if trail else text[lead:]
    if not core:return None
    words=re.split(r'[ \n]',core);start=offset+advance(text[:lead])
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
    plan=best(0,0)
    if plan is None:return None
    return text[:lead]+'\n'.join(' '.join(words[a:b]) for a,b in plan)+(text[len(text)-trail:] if trail else '')
