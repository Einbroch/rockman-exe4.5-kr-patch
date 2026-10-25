"""Conditional geometry for calendar-table native script50 only, analysis.

Native322A8->4F7B6 resets defaults to52,110 before unpositioned quick open.
No generic quick-to-normal coercion, date pages51/52 or product admission.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from nickname_capacity import advance,ARGS

CALENDARS=frozenset('659CB8 65F11C 665698 66B0D4 670568 6762A8 67BCF4 6811F0 686A60 68CBFC 692874 697B70 69D8D4 6A2FBC 6A9970 6B525C 6BB2A4 6C0E38 6C6828 6CBFC0 6D1984'.split())
TOKENS=('callSkipMugshotFadeIn msgOpenQuick mugshotShow textSpeed callBufferEventHour printBuffer @literal callBufferEventMinutes printBuffer @literal callBufferEventAMPM printScheduleBuffer @literal callBufferEventFrequency printScheduleBuffer @literal callBufferEventName @literal printScheduleBuffer @literal keyWait clearMsg soundPlay @literal soundDisableChoiceSFX positionOptionHorizontal option space @literal option space @literal select flagClear wait mugshotHide msgCloseQuick end').split()


def validate(original,target,scripts,selected_ids,nickname_bound):
    if skeleton(original)!=skeleton(target) or list(scripts)!=[50] or not selected_ids:raise ValueError('Calendar delete exact protected script50')
    archive=re.search(r'^@archive (\w+)',target,re.M)[1]
    if archive not in CALENDARS:raise ValueError('Calendar delete native calendar-table scope')
    match=re.search(r'^script 50 mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
    if not match:raise ValueError('Calendar delete language/script')
    seq=events('@archive '+archive+'\n'+match[0])
    if [e[2][0] if e[1]=='command' else '@literal' for e in seq]!=TOKENS:raise ValueError('Calendar delete exact native event topology')
    args={i:e[2][1] for i,e in enumerate(seq) if e[1]=='command'}
    constants={0:'',1:'',3:'\t\tdelay = 0\n',4:'',7:'',10:'',13:'',16:'',20:'\t\tany = false\n',21:'',22:'\t\ttrack = 467\n',24:'',25:'\t\twidth = 8\n',27:'\t\tcount = 1\n',30:'\t\tcount = 1\n',34:'\t\tframes = 1\n',35:'',36:'',37:''}
    for i,value in constants.items():
        if args[i]!=value:raise ValueError('Calendar delete finite arguments '+str(i))
    if not re.fullmatch(r'\t\tmugshot = \w+\n',args[2]) or not re.fullmatch(r'\t\tflag = \d+\n',args[33]):raise ValueError('Calendar portrait/flag arguments')
    for i,zero in ((5,'false'),(8,'true')):
        if args[i]!='\t\tbuffer = 1\n\t\tminLength = 2\n\t\tpadZeros = '+zero+'\n\t\tpadLeft = true\n':raise ValueError('Calendar exact time formatter')
    if any(args[i]!=ARGS for i in (11,14,18)):raise ValueError('Calendar exact descriptor67 arguments')
    for i,nav in ((26,(1,1,0,0)),(29,(0,0,1,1))):
        want='\t\tbrackets = false\n'+''.join('\t\t'+key+' = '+str(value)+'\n' for key,value in zip(('left','right','up','down'),nav))
        if args[i]!=want:raise ValueError('Calendar exact two-node choice navigation')
    expected_select=('\t\tdefault = 0\n\t\tlastCancelSFX = true\n\t\tnoDelay = false\n\t\tBSeparate = false\n\t\tdisableB = false\n\t\tclear = true\n\t\ttargets = [\n\t\t\tjump = continue,\n\t\t\tjump = continue,\n\t\t\tjump = continue\n\t\t]\n')
    if args[32]!=expected_select:raise ValueError('Calendar exact select clear/cancel/continuations')
    rows=[0];parts=[];seen=set();bounds={5:22,8:22,11:22,14:35,18:110}
    for i,(_,kind,data) in enumerate(seq[:20]):
        if kind=='literal':
            for n,line in enumerate(data.text.split('\n')):
                if n:rows.append(0)
                rows[-1]+=advance(line)
            parts.append(dict(id=data.key,text=data.text));seen.add(data.key)
        elif i in bounds:rows[-1]+=bounds[i];parts.append(dict(kind=data[0],bound=bounds[i],native_slot=len([p for p in parts if 'bound' in p])))
    if len(rows)>3 or any(w>(168 if i==2 else 180) for i,w in enumerate(rows)):raise ValueError('Calendar delete aggregate first page '+str(rows))
    prompt=seq[23][2];prompt_rows=[advance(s) for s in prompt.text.split('\n')]
    if len(prompt_rows)!=3 or prompt_rows[-2:]!=[0,0] or prompt_rows[0]>180:raise ValueError('Calendar delete prompt must preserve choice row')
    labels=[seq[i][2] for i in (28,31)]
    if any('\n' in x.text for x in labels):raise ValueError('Calendar single-line option labels')
    extent=sum(8+advance(x.text) for x in labels);allocation=11*7+16
    if extent>allocation:raise ValueError('Calendar translated choices exceed native93px allocation')
    here=seen|{prompt.key}|{x.key for x in labels}
    if not set(selected_ids)<=here:raise ValueError('Calendar delete unbound IDs')
    return [dict(script=50,origin=[52,110],row_limits=[180,180,168],initializer='native-calendar322A8/default52,110/unpositioned-quick',calendar_table_required=True,pages=[dict(widths=rows,parts=parts,dynamic_slots=5),dict(kind='horizontal-two-choice',prompt_widths=prompt_rows,prompt_id=prompt.key,option_ids=[x.key for x in labels],target_advance=extent,allocated_advance=allocation,default=0,clear=True)],conditional_event_name_bound=110,frequency_bound=35,product_admitted=False,runtime_pending=True,source_choice_and_five_slot_runtime_binding_required=True)]
