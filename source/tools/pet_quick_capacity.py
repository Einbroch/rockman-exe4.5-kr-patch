"""Exact native PET quick-window topology, explicit132px aggregate pages."""
import re
from field_hint_capacity import events
from tpl_literals import skeleton,literals
from nickname_capacity import advance

PREFIX=[('positionBox','\t\tleft = 10\n\t\ttop = 12\n\t\ttype = 1\n'),('msgOpenQuick',''),('positionText','\t\tleft = 92\n\t\ttop = 110\n\t\tarrowDistance = 3\n'),('positionArrow','\t\tleft = 225\n\t\ttop = 141\n')]


def validate(original,target,scripts,selected_ids):
    if skeleton(original)!=skeleton(target) or len(scripts)!=len(set(scripts)) or not selected_ids:raise ValueError('Quick protected scope')
    archive=re.search(r'^@archive (\w+)',original,re.M).group(1);proof=[]
    for script in scripts:
        match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
        if match is None:raise ValueError('Quick source script')
        seq=events('@archive '+archive+'\n'+match.group())
        if [e[2] for e in seq[:4] if e[1]=='command']!=PREFIX or any(e[1]!='command' for e in seq[:4]):raise ValueError('Quick exact native initializer')
        widths=[0];parts=[];pages=[];waiting=False;closed=False;had_text=False;selected_here=set()
        def finish_page():
            if not parts or len(widths)>3 or max(widths)>132:raise ValueError('Quick aggregate page extent '+str(widths))
            pages.append(dict(widths=list(widths),parts=list(parts)))
        for _,kind,data in seq[4:]:
            if closed:raise ValueError('Quick event after terminal')
            if kind=='literal':
                if waiting:raise ValueError('Quick text after wait without clear')
                for i,line in enumerate(data.text.split('\n')):
                    if i:widths.append(0)
                    widths[-1]+=advance(line)
                parts.append(dict(id=data.key,text=data.text));had_text=True
                if data.key in selected_ids:selected_here.add(data.key)
                continue
            name,args=data
            if name=='keyWait':
                if waiting or args!='\t\tany = false\n':raise ValueError('Quick wait contract')
                finish_page();waiting=True
            elif name=='clearMsg':
                if not waiting or args:raise ValueError('Quick clear contract')
                widths=[0];parts=[];waiting=False
            elif name in ('flagSet','flagClear','flagSetNavi','flagClearNavi'):
                if had_text or not re.fullmatch(r'\t\tflag = \d+\n',args):raise ValueError('Quick pre-text flag only')
            elif name in ('wait','waitSkip'):
                if waiting or not re.fullmatch(r'\t\tframes = \d+\n',args):raise ValueError('Quick wait/timing arguments')
            elif name=='end':
                if not waiting or args:raise ValueError('Quick end without waited page')
                closed=True
            elif name=='jump':
                if parts or not pages or args=='\t\ttarget = continue\n' or not re.fullmatch(r'\t\ttarget = \d+\n',args):raise ValueError('Quick jump after cleared page only')
                closed=True
            elif name=='waitHold':
                # Analysis only: preserve the original terminal hold after a
                # waited and cleared page. No interpretation of its external
                # menu/event continuation is used to admit a ROM input.
                if parts or waiting or not pages or args:raise ValueError('Quick terminal hold after clear only')
                closed=True
            else:raise ValueError('Quick unmodeled command '+name)
        if not closed or not selected_here:raise ValueError('Quick terminal/selected identity')
        proof.append(dict(script=script,origin=[92,110],row_limits=[132,132,132],arrow=[225,141],pages=pages,runtime_pending=True))
    if set(selected_ids)-{i.key for i in literals(target) if int(i.key.split(':')[1]) in scripts}:raise ValueError('Quick unbound ID')
    return proof
