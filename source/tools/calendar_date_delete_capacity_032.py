"""Conditional calendar-table51/52 geometry only; source commands unchanged."""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from nickname_capacity import advance,ARGS
from calendar_delete_capacity_031 import CALENDARS


def validate(original,target,scripts,selected_ids,nickname_bound=99):
    if skeleton(original)!=skeleton(target) or not selected_ids or not scripts or len(scripts)!=len(set(scripts)):raise ValueError('032 calendar date protected scope')
    arc=re.search(r'^@archive (\w+)',target,re.M)[1]
    if arc not in CALENDARS or any(s not in (51,52) for s in scripts):raise ValueError('032 calendar date declared table/scripts only')
    proof=[];seen=set()
    for script in scripts:
        match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
        if not match:raise ValueError('032 calendar date language')
        seq=events('@archive '+arc+'\n'+match[0]);at=0;rows=[0];parts=[];slots=0;here=set()
        def command(name,args=''):
            nonlocal at
            if at>=len(seq) or seq[at][1:]!=('command',(name,args)):raise ValueError('032 calendar date exact command '+name+' at '+str(at))
            at+=1
        def literal():
            nonlocal at
            if at>=len(seq) or seq[at][1]!='literal':raise ValueError('032 calendar date literal topology')
            value=seq[at][2];at+=1;here.add(value.key);return value
        def text():
            value=literal()
            for i,line in enumerate(value.text.split('\n')):
                if i:rows.append(0)
                rows[-1]+=advance(line)
            parts.append(dict(id=value.key,text=value.text));return value
        def numeric(name,zeros):
            nonlocal slots
            command(name);command('printBuffer','\t\tbuffer = 1\n\t\tminLength = 2\n\t\tpadZeros = '+zeros+'\n\t\tpadLeft = true\n');rows[-1]+=22;parts.append(dict(provider=name,bound=22));slots+=1
        command('callSkipMugshotFadeIn');command('msgOpenQuick')
        if seq[at][1]!='command' or seq[at][2][0]!='mugshotShow' or not re.fullmatch(r'\t\tmugshot = \w+\n',seq[at][2][1]):raise ValueError('032 calendar date portrait')
        at+=1;command('textSpeed','\t\tdelay = 0\n')
        if script==51:numeric('callBufferEventYear','true');text()
        numeric('callBufferEventMonth','false');text();numeric('callBufferEventDay','false');text()
        if script==51:
            command('callBufferEventDayName');text();command('printScheduleBuffer',ARGS);rows[-1]+=11;parts.append(dict(provider='weekday',bound=11));slots+=1;text()
        command('callBufferEventName');text();command('printScheduleBuffer',ARGS);rows[-1]+=110;parts.append(dict(provider='conditional-native-title',bound=110));slots+=1;text()
        if len(rows)>3 or any(w>(168 if i==2 else 180) for i,w in enumerate(rows)) or slots>5:raise ValueError('032 calendar date aggregate width/slots '+str(rows))
        command('keyWait','\t\tany = false\n');command('clearMsg');command('soundPlay','\t\ttrack = 467\n');prompt=literal();pw=[advance(x) for x in prompt.text.split('\n')]
        if len(pw)!=3 or pw[-2:]!=[0,0] or pw[0]>180:raise ValueError('032 calendar date prompt and empty choice row')
        command('soundDisableChoiceSFX');command('positionOptionHorizontal','\t\twidth = 8\n');labels=[]
        for nav in [(1,1,0,0),(0,0,1,1)]:
            command('option','\t\tbrackets = false\n'+''.join('\t\t'+k+' = '+str(v)+'\n' for k,v in zip(('left','right','up','down'),nav)));command('space','\t\tcount = 1\n');labels.append(literal())
        if any('\n' in x.text for x in labels) or sum(8+advance(x.text) for x in labels)>93:raise ValueError('032 calendar date original centered allocation')
        command('select','\t\tdefault = 0\n\t\tlastCancelSFX = true\n\t\tnoDelay = false\n\t\tBSeparate = false\n\t\tdisableB = false\n\t\tclear = true\n\t\ttargets = [\n\t\t\tjump = continue,\n\t\t\tjump = continue,\n\t\t\tjump = continue\n\t\t]\n')
        if at>=len(seq) or seq[at][1]!='command' or seq[at][2][0]!='flagClear' or not re.fullmatch(r'\t\tflag = \d+\n',seq[at][2][1]):raise ValueError('032 calendar date source flag')
        at+=1;command('wait','\t\tframes = 1\n');command('mugshotHide');command('msgCloseQuick');command('end')
        if at!=len(seq) or not here&set(selected_ids):raise ValueError('032 calendar date terminal/selected identity')
        seen|=here&set(selected_ids);proof.append(dict(script=script,origin=[52,110],row_limits=[180,180,168],calendar_table_required=True,pages=[dict(widths=rows,parts=parts,dynamic_slots=slots),dict(prompt_id=prompt.key,prompt_widths=pw,option_ids=[x.key for x in labels],kind='horizontal-two-choice',allocated_advance=93,target_advance=sum(8+advance(x.text) for x in labels))],conditional_title_bound=110,conditional_date_domains='year00..99/month1..12/day1..31/weekday0..6',product_admitted=False,runtime_pending=True))
    if seen!=set(selected_ids):raise ValueError('032 calendar date unbound selected ID')
    return proof
