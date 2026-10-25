"""Analysis-only explicit normal/PET event pages; no choices or inherited box.

Conditional valid legacy event names only. Preserved conditionals are recorded,
not executed by this geometry model. This file does not admit product inputs.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton,literals
from nickname_capacity import advance,ARGS
from pet_quick_capacity import PREFIX


def validate(original,target,scripts,selected_ids,nickname_bound):
    if skeleton(original)!=skeleton(target) or len(scripts)!=len(set(scripts)) or not selected_ids:raise ValueError('Event protected identity')
    if type(nickname_bound) is not int or not 0<=nickname_bound<=99:raise ValueError('Event nickname contract')
    archive=re.search(r'^@archive (\w+)',target,re.M)[1];proof=[];seen=set()
    for script in scripts:
        m=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
        if not m:raise ValueError('Event source script')
        seq=events('@archive '+archive+'\n'+m[0]);quick=seq[:4] and all(e[1]=='command' for e in seq[:4]) and [e[2] for e in seq[:4]]==PREFIX
        if quick:start=4;caps=[132]*3;origin=[92,110]
        else:
            opens=[i for i,e in enumerate(seq) if e[1:] == ('command',('msgOpen',''))]
            if len(opens)!=1:raise ValueError('Event explicit supported initializer')
            start=opens[0]+1;caps=[180,180,168];origin=[52,110]
            for _,kind,data in seq[:start-1]:
                if kind!='command' or data[0]!='mugshotShow' or not re.fullmatch(r'\t\tmugshot = \w+\n',data[1]):raise ValueError('Event normal portrait preamble')
        rows=[0];parts=[];pages=[];waiting=closed=False;string=numeric=None;slots=0;has_event=False;guards=[];here=set()
        for _,kind,data in seq[start:]:
            if closed:raise ValueError('Event after terminal')
            if kind=='literal':
                if waiting:raise ValueError('Event text after wait')
                for i,line in enumerate(data.text.split('\n')):
                    if i:rows.append(0)
                    rows[-1]+=advance(line)
                parts.append(dict(id=data.key,text=data.text));here.add(data.key);continue
            name,args=data
            if name in ('callBufferEventName','callBufferEventAMPM','callBufferEventHour','callBufferEventMinutes'):
                if waiting or args:raise ValueError('Event producer arguments/state')
                if name in ('callBufferEventName','callBufferEventAMPM'):string='name' if name.endswith('Name') else 'AMPM'
                else:numeric='hour' if name.endswith('Hour') else 'minute'
                has_event=True
            elif name=='printScheduleBuffer':
                if waiting or args!=ARGS or string is None:raise ValueError('Event string producer/lifetime')
                bound=110 if string=='name' else 22;rows[-1]+=bound;slots+=1;parts.append(dict(kind=name,provider=string,bound=bound,conditional_valid_legacy_record=True))
            elif name=='printBuffer':
                expected='\t\tbuffer = 1\n\t\tminLength = 2\n\t\tpadZeros = '+('false' if numeric=='hour' else 'true')+'\n\t\tpadLeft = true\n'
                if waiting or numeric is None or args!=expected:raise ValueError('Event exact numeric formatting')
                rows[-1]+=22;slots+=1;parts.append(dict(kind=name,provider=numeric,bound=22,conditional_valid_native_time=True))
            elif name=='printPlayerNickname':
                if waiting or args!=ARGS:raise ValueError('Event nickname arguments')
                rows[-1]+=nickname_bound;slots+=1;parts.append(dict(kind=name,bound=nickname_bound))
            elif name=='keyWait':
                if waiting or args!='\t\tany = false\n' or not parts or len(rows)>3 or any(w>caps[i] for i,w in enumerate(rows)) or slots>4:raise ValueError('Event aggregate page/slot capacity '+str(rows))
                pages.append(dict(widths=rows[:],parts=parts[:],dynamic_slots=slots));waiting=True
            elif name=='clearMsg':
                if not waiting or args:raise ValueError('Event clear after wait only')
                rows=[0];parts=[];waiting=False;slots=0;string=numeric=None
            elif name in ('callCheckNowEvent','callFindTodayEvent'):
                if parts or waiting or not pages or not re.fullmatch(r'\t\tjumpIfExists = \d+\n\t\tjumpIfNone = (?:\d+|continue)\n',args):raise ValueError('Event conditional after cleared page')
                guards.append(dict(command=name,arguments=args,native_branch_execution_pending=True))
                if not args.endswith('= continue\n'):closed=True
            elif name in ('flagClear','flagSet'):
                if parts or waiting or not re.fullmatch(r'\t\tflag = \d+\n',args):raise ValueError('Event flag outside text only')
            elif name in ('mugshotShow','mugshotHide'):
                if quick or name=='mugshotShow' and not re.fullmatch(r'\t\tmugshot = \w+\n',args) or name=='mugshotHide' and args:raise ValueError('Event portrait arguments')
            elif name=='textSpeed':
                if waiting or args!='\t\tdelay = 0\n':raise ValueError('Event native zero text speed')
            elif name in ('wait','waitSkip'):
                if waiting or not re.fullmatch(r'\t\tframes = \d+\n',args):raise ValueError('Event finite wait')
            elif name in ('end','waitHold'):
                if args or not pages or parts and not waiting or name=='waitHold' and (parts or waiting):raise ValueError('Event terminal contract')
                closed=True
            else:raise ValueError('Event unmodeled command '+name)
        if not closed or not has_event or not here&set(selected_ids):raise ValueError('Event closed selected scope')
        seen|=here&set(selected_ids);proof.append(dict(script=script,origin=origin,row_limits=caps,pages=pages,source_conditionals=guards,conditional_event_name_bound=110,conditional_provider_lifetime=True,product_admitted=False,runtime_pending=True,numeric_formatter_CPU_pending=any(p.get('kind')=='printBuffer' for page in pages for p in page['parts'])))
    if seen!=set(selected_ids) or not selected_ids<={x.key for x in literals(target)}:raise ValueError('Event unbound selected IDs')
    return proof
