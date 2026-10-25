"""Source-only battle BBS layout proposal.168px is conservative trial policy.

NOT a confirmed framebuffer/window capacity or runtime input/hold proof.
Original32/68 text and202/108 arrow anchors are preserved exactly.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton,literals
from nickname_capacity import advance

PREFIX=[('color','\t\tpalette = 9\n'),('positionText','\t\tleft = 32\n\t\ttop = 68\n\t\tarrowDistance = 3\n'),('positionArrow','\t\tleft = 202\n\t\ttop = 108\n')]


def validate(original,target,scripts,ids):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1 or not ids:raise ValueError('040 BBS protected scope')
    arc=re.search(r'^@archive (\w+)',target,re.M)[1];script=scripts[0];match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script|\Z)',target,re.M)
    if match is None:raise ValueError('040 BBS source language')
    seq=events('@archive '+arc+'\n'+match[0])
    if len(seq)<4 or any(k!='command' for _,k,_ in seq[:3]) or [x for _,_,x in seq[:3]]!=PREFIX:raise ValueError('040 BBS exact source prefix')
    widths=[0];parts=[];pages=[];waiting=closed=False;seen=set()
    for _,kind,data in seq[3:]:
        if closed:raise ValueError('040 BBS event after terminal')
        if kind=='literal':
            if waiting:raise ValueError('040 BBS literal after wait')
            for i,line in enumerate(data.text.split('\n')):
                if i:widths.append(0)
                widths[-1]+=advance(line)
            parts.append(dict(id=data.key,text=data.text));seen.add(data.key);continue
        name,args=data
        if name=='keyWait':
            if waiting or args!='\t\tany = false\n' or not parts or len(widths)>3 or max(widths)>168:raise ValueError('040 BBS trial page extent '+str(widths))
            pages.append(dict(widths=widths[:],parts=parts[:]));waiting=True
        elif name=='clearMsg':
            if args or not waiting:raise ValueError('040 BBS exact clear phase')
            widths=[0];parts=[];waiting=False
        elif name=='waitHold':
            if args or not waiting or not pages:raise ValueError('040 BBS waited visible hold')
            closed=True
        else:raise ValueError('040 BBS unmodeled command '+name)
    if not closed or set(ids)!=seen:raise ValueError('040 BBS exact selected literal population')
    return [dict(script=script,origin=[32,68],arrow=[202,108],trial_row_limits=[168,168,168],pages=pages,terminal='waitHold-after-keyWait-visible-page',confirmed_capacity=False,runtime_pending=True,product_admitted=False)]
