"""Finite calendar-table fullquick menu geometries, analysis only.

Default52,110 is scoped to the calendar322A8 caller and declared roots.
No arbitrary quick-to-normal coercion or new choice/control semantics.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from nickname_capacity import advance,ARGS
from calendar_delete_capacity_031 import CALENDARS

VERTICAL=frozenset((2,5,7,8))
HORIZONTAL=frozenset((24,30,33,60,61,62))
SIMPLE=frozenset((3,4,6,20,23,25,31,32,63))


def select_args(default,last,separate,clear,targets=3):
    return ('\t\tdefault = '+str(default)+'\n\t\tlastCancelSFX = '+str(last).lower()+'\n\t\tnoDelay = false\n\t\tBSeparate = '+str(separate).lower()+'\n\t\tdisableB = false\n\t\tclear = '+str(clear).lower()+'\n\t\ttargets = [\n'+''.join('\t\t\tjump = continue'+(',' if i<targets-1 else '')+'\n' for i in range(targets))+'\t\t]\n')


def validate(original,target,scripts,selected_ids,nickname_bound=99):
    if skeleton(original)!=skeleton(target) or not selected_ids or not scripts or len(scripts)!=len(set(scripts)) or type(nickname_bound) is not int or not 0<=nickname_bound<=99:raise ValueError('032 calendar menu protected scope/name bound')
    arc=re.search(r'^@archive (\w+)',target,re.M)[1]
    if arc not in CALENDARS or any(s not in VERTICAL|HORIZONTAL|SIMPLE|{0,10} for s in scripts):raise ValueError('032 calendar menu caller/root/script')
    proofs=[];seen=set()
    for script in scripts:
        match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
        if not match:raise ValueError('032 calendar menu language')
        seq=events('@archive '+arc+'\n'+match[0]);at=0;rows=[0];parts=[];pages=[];here=set();slots=0
        def command(name,args=''):
            nonlocal at
            if at>=len(seq) or seq[at][1:]!=('command',(name,args)):raise ValueError('032 calendar menu exact '+name+' at '+str(at))
            at+=1
        def text():
            nonlocal at
            if at>=len(seq) or seq[at][1]!='literal':raise ValueError('032 calendar menu literal topology')
            value=seq[at][2];at+=1;here.add(value.key)
            for i,line in enumerate(value.text.split('\n')):
                if i:rows.append(0)
                rows[-1]+=advance(line)
            parts.append(dict(id=value.key,text=value.text));return value
        def finish():
            if not parts or len(rows)>3 or any(w>(168 if i==2 else 180) for i,w in enumerate(rows)) or slots>5:raise ValueError('032 calendar menu aggregate page '+str(rows))
            return dict(widths=rows[:],parts=parts[:],dynamic_slots=slots)
        def option(nav):
            command('option','\t\tbrackets = false\n'+''.join('\t\t'+k+' = '+str(v)+'\n' for k,v in zip(('left','right','up','down'),nav)));command('space','\t\tcount = 1\n')
        command('callSkipMugshotFadeIn');command('msgOpenQuick')
        if at>=len(seq) or seq[at][1]!='command' or seq[at][2][0]!='mugshotShow' or not re.fullmatch(r'\t\tmugshot = \w+\n',seq[at][2][1]):raise ValueError('032 calendar menu exact portrait')
        at+=1;command('textSpeed','\t\tdelay = 0\n')
        if script==0:
            text()
            for name in ('callBufferCurrentMonth','callBufferCurrentDay'):
                command(name);command('printBuffer','\t\tbuffer = 1\n\t\tminLength = 2\n\t\tpadZeros = false\n\t\tpadLeft = true\n');rows[-1]+=22;slots+=1;parts.append(dict(provider=name,bound=22,valid_native_domain_required=True));text()
            pages.append(finish());command('waitHold')
        elif script in VERTICAL:
            prompt=text()
            if len(rows)!=2 or rows[-1]!=0 or rows[0]>180:raise ValueError('032 vertical prompt plus empty option row')
            prompt_widths=rows[:];labels=[]
            for index,nav in enumerate(((0,0,1,1),(1,1,0,0))):
                command('positionOptionVertical','\t\twidth = 7\n');option(nav);label=text();labels.append(label)
                if label.text.count('\n')!=(1 if index==0 else 0) or index==0 and not label.text.endswith('\n') or 8+advance(label.text.rstrip('\n'))>85:raise ValueError('032 vertical label/85px source allocation')
            # Centering determines each option's own x; do not add it to the
            # preceding prompt width. Logical rows are fixed1/2 by exact LF.
            command('select',select_args(1 if script in (7,8) else 0,False,True,False));command('waitHold')
            pages.append(dict(kind='vertical-two-choice',prompt_id=prompt.key,prompt_widths=prompt_widths,option_ids=[x.key for x in labels],allocated_advance=85,target_advance=max(8+advance(x.text.rstrip('\n')) for x in labels),rows=[1,2],clear=False,BSeparate=True))
        elif script in HORIZONTAL:
            prompt=text();prompt_widths=rows[:]
            if len(rows)!=3 or rows[-1]!=0 or any(w>180 for w in rows[:-1]):raise ValueError('032 horizontal prompt plus empty third row')
            if script!=30:command('soundDisableChoiceSFX')
            native_width=7 if arc=='6762A8' and script==30 else 8;allocation=11*(native_width-1)+16
            command('positionOptionHorizontal','\t\twidth = '+str(native_width)+'\n');labels=[]
            for nav in ((1,1,0,0),(0,0,1,1)):
                option(nav);label=text();labels.append(label)
                if '\n' in label.text:raise ValueError('032 horizontal single-line label')
            extent=sum(8+advance(x.text) for x in labels)
            if extent>allocation:raise ValueError('032 horizontal original93px allocation')
            command('select',select_args(0,True,False,True));command('waitHold')
            pages.append(dict(kind='horizontal-two-choice',prompt_id=prompt.key,prompt_widths=prompt_widths,option_ids=[x.key for x in labels],native_width=native_width,allocated_advance=allocation,target_advance=extent,row=2,clear=True,BSeparate=False))
        elif script==10:
            command('soundDisableChoiceSFX');text();command('printPlayerNickname',ARGS);rows[-1]+=nickname_bound;slots+=1;parts.append(dict(provider='printPlayerNickname',bound=nickname_bound,conditional_native=True));text()
            if len(rows)!=3 or rows[-1]!=0:raise ValueError('032 single option requires empty third row')
            first=finish();option((0,0,0,0));rows[-1]+=8;label=text()
            if '\n' in label.text:raise ValueError('032 single option label rows')
            finish();command('select',select_args(0,False,True,False,2));command('waitHold')
            pages.append(dict(kind='single-inline-option',caption=first,option_id=label.key,row=2,option_advance=8+advance(label.text),row_limit=168,clear=False,BSeparate=True))
        else:
            if script==25 and arc=='65F11C':text()
            if script==25:command('printPlayerNickname',ARGS);rows[-1]+=nickname_bound;slots+=1;parts.append(dict(provider='printPlayerNickname',bound=nickname_bound,conditional_native=True))
            while at<len(seq):
                if seq[at][1]=='literal':text();continue
                name,args=seq[at][2]
                if name=='keyWait':
                    pages.append(finish());command('keyWait','\t\tany = false\n');command('clearMsg');rows=[0];parts=[];slots=0
                elif name=='waitHold':
                    if parts:pages.append(finish())
                    elif not pages:raise ValueError('032 empty terminal without a page')
                    command('waitHold');break
                else:raise ValueError('032 simple caption unmodeled command '+name)
        if at!=len(seq) or not here&set(selected_ids):raise ValueError('032 calendar menu terminal/selected scope')
        seen|=here&set(selected_ids);proofs.append(dict(script=script,origin=[52,110],row_limits=[180,180,168],calendar_table_required=True,initializer='native322A8/default52,110/unpositioned-quick',pages=pages,product_admitted=False,runtime_pending=True,external_menu_continuation_preserved_not_executed=True))
    if seen!=set(selected_ids):raise ValueError('032 calendar menu unbound ID')
    return proofs
