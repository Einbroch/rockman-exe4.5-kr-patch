"""Source-profile window geometry ONLY; not external menu interaction proof.

Unlike ordinary quick dialogue these scripts use zero-speed text and EDFF
hold with the page still visible. That hold is not a keyWait/clear/end.
Do not broaden the ordinary quick validator or infer external menu space.
"""
import re
from tpl_literals import skeleton,literals
from field_hint_capacity import events
from pet_quick_capacity import PREFIX
from nickname_capacity import advance

def validate(original,target,scripts,selected_ids):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1 or not selected_ids:raise ValueError('Profile protected scope')
    arc=re.search(r'^@archive (\w+)',target,re.M)[1];script=scripts[0]
    s=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
    if s is None:raise ValueError('Profile script language')
    seq=events('@archive '+arc+'\n'+s[0])
    if len(seq)<4 or any(e[1]!='command' for e in seq[:4]) or [e[2] for e in seq[:4]]!=PREFIX:raise ValueError('Profile exact native initializer')
    widths=[0];parts=[];pages=[];waiting=closed=False;seen=set();speed=False;terminal=None
    def check():
        if not parts or len(widths)>3 or any(x>132 for x in widths):raise ValueError('Profile text-window extent '+str(widths))
        return dict(widths=widths[:],parts=parts[:])
    for _,kind,data in seq[4:]:
        if closed:raise ValueError('Profile events after terminal')
        if kind=='literal':
            if waiting or not speed:raise ValueError('Profile literal phase')
            for i,line in enumerate(data.text.split('\n')):
                if i:widths.append(0)
                widths[-1]+=advance(line)
            parts.append(dict(id=data.key,text=data.text))
            if data.key in selected_ids:seen.add(data.key)
            continue
        name,args=data
        if name=='textSpeed':
            if speed or parts or waiting or pages or args!='\t\tdelay = 0\n':raise ValueError('Profile original zero-speed pre-text only')
            speed=True
        elif name=='keyWait':
            if waiting or args!='\t\tany = false\n':raise ValueError('Profile page wait')
            p=check();p['ending']='keyWait';pages.append(p);waiting=True
        elif name=='clearMsg':
            if not waiting or args:raise ValueError('Profile clear only after actual wait')
            widths=[0];parts=[];waiting=False
        elif name=='waitHold':
            if args or not speed:raise ValueError('Profile source hold arguments')
            if parts and not waiting:
                p=check();p['ending']='EDFF-visible-page-hold';pages.append(p)
            elif not pages:raise ValueError('Profile empty hold')
            closed=True;terminal='waitHold'
        elif name=='end':
            if args or not waiting:raise ValueError('Profile end requires actual wait')
            closed=True;terminal='end'
        else:raise ValueError('Profile unmodeled command '+name)
    if not closed or seen!=set(selected_ids):raise ValueError('Profile terminal/selected IDs')
    return [dict(script=script,origin=[92,110],row_limits=[132,132,132],arrow=[225,141],initializer=PREFIX,pages=pages,terminal=terminal,source_text_speed=0,external_menu_overlap_verification_pending=True,native_hold_and_zero_speed_CPU_pending=True,runtime_pending=True,product_admitted=False)]
