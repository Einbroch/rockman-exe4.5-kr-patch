"""026 analysis-only exact PET quick window and finite padded horizontal choices.

Source/target commands remain identical. The caller must establish native
six-glyph/suffix applicability; this is not automatic Hangul name support.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton,literals
from nickname_capacity import advance,ARGS

PREFIX=[('positionBox','\t\tleft = 10\n\t\ttop = 12\n\t\ttype = 1\n'),('msgOpenQuick',''),('positionText','\t\tleft = 92\n\t\ttop = 110\n\t\tarrowDistance = 3\n'),('positionArrow','\t\tleft = 225\n\t\ttop = 141\n')]


def validate(original,target,scripts,selected_ids,nickname_bound):
    if type(nickname_bound) is not int or not 0<=nickname_bound<=99:raise ValueError('Quick nickname applicability bound')
    if skeleton(original)!=skeleton(target) or len(scripts)!=len(set(scripts)) or not selected_ids:raise ValueError('Quick protected scope')
    archive=re.search(r'^@archive (\w+)',original,re.M).group(1);proof=[]
    for script in scripts:
        match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
        if match is None:raise ValueError('Quick source script')
        seq=events('@archive '+archive+'\n'+match.group())
        if [e[2] for e in seq[:4] if e[1]=='command']!=PREFIX or any(e[1]!='command' for e in seq[:4]):raise ValueError('Quick exact native initializer')
        widths=[0];parts=[];pages=[];waiting=False;closed=False;had_text=False;selected_here=set();choice=None;choice_count=0
        def finish_page():
            if not parts or len(widths)>3 or max(widths)>132:raise ValueError('Quick aggregate page extent '+str(widths))
            pages.append(dict(widths=list(widths),parts=list(parts)))
        for _,kind,data in seq[4:]:
            if closed:raise ValueError('Quick event after terminal')
            if kind=='literal':
                if choice is not None:
                    if not choice['options'] or choice['options'][-1]['space']!=1 or choice['options'][-1]['label'] is not None or '\n' in data.text:
                        raise ValueError('PET choice single-line padded label')
                    choice['options'][-1]['label']=dict(id=data.key,text=data.text,width=advance(data.text))
                    if data.key in selected_ids:selected_here.add(data.key)
                    continue
                if waiting:raise ValueError('Quick text after wait without clear')
                for i,line in enumerate(data.text.split('\n')):
                    if i:widths.append(0)
                    widths[-1]+=advance(line)
                parts.append(dict(id=data.key,text=data.text));had_text=True
                if data.key in selected_ids:selected_here.add(data.key)
                continue
            name,args=data
            if name=='spacePx':
                if args!='\t\tcount = 16\n' or parts or waiting or widths!=[0] or choice is not None:
                    raise ValueError('PET choice exact16px empty cleared page')
                choice=dict(options=[],left_pad=16)
                continue
            if choice is not None:
                if name=='option':
                    n=len(choice['options'])
                    if n>=2 or n and choice['options'][-1]['label'] is None:raise ValueError('PET choice two complete options')
                    nav=re.fullmatch(r'\t\tbrackets = false\n\t\tleft = ([01])\n\t\tright = ([01])\n\t\tup = ([01])\n\t\tdown = ([01])\n',args)
                    if not nav:raise ValueError('PET choice canonical two-node navigation')
                    choice['options'].append(dict(space=0,label=None,navigation=list(map(int,nav.groups()))))
                elif name=='space':
                    if args!='\t\tcount = 1\n' or not choice['options'] or choice['options'][-1]['space'] or choice['options'][-1]['label'] is not None:raise ValueError('PET choice exact native pad')
                    choice['options'][-1]['space']=1
                elif name=='select':
                    pattern=(r'\t\tdefault = ([01])\n\t\tlastCancelSFX = false\n\t\tnoDelay = false\n'
                             r'\t\tBSeparate = false\n\t\tdisableB = false\n\t\tclear = true\n'
                             r'\t\ttargets = \[\n\t\t\tjump = (\d+|continue),\n\t\t\tjump = (\d+|continue),\n\t\t\tjump = (\d+|continue)\n\t\t\]\n')
                    m=re.fullmatch(pattern,args)
                    if not m or len(choice['options'])!=2 or any(o['label'] is None for o in choice['options']):raise ValueError('PET choice exact clear/cancel continuation')
                    extent=16+sum(8+o['label']['width'] for o in choice['options'])
                    if extent>132:raise ValueError('PET translated choice exceeds132px')
                    choice.update(kind='pet-fixed16-horizontal-choice',target_advance=extent,default=int(m[1]),targets=list(m.groups()[1:]),runtime_cursor_and_outcome_pending=True)
                    pages.append(choice);choice=None;choice_count+=1;waiting=True
                else:raise ValueError('PET choice unmodeled command '+name)
                continue
            if name=='printPlayerNickname':
                if waiting or args!=ARGS:raise ValueError('Quick nickname provider contract')
                widths[-1]+=nickname_bound
                parts.append(dict(kind='printPlayerNickname',bound=nickname_bound))
                had_text=True
            elif name=='keyWait':
                if waiting or args!='\t\tany = false\n':raise ValueError('Quick wait contract')
                finish_page();waiting=True
            elif name=='clearMsg':
                if not waiting or args:raise ValueError('Quick clear contract')
                widths=[0];parts=[];waiting=False
            elif name in ('flagSet','flagClear','flagSetNavi','flagClearNavi'):
                if parts or waiting or not re.fullmatch(r'\t\tflag = \d+\n',args):raise ValueError('Quick pre-text flag only')
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
        if not closed or not selected_here or choice is not None or choice_count!=1:raise ValueError('Quick terminal/selected identity')
        proof.append(dict(script=script,origin=[92,110],row_limits=[132,132,132],arrow=[225,141],pages=pages,native_nickname_bound=nickname_bound,automatic_Hangul_names_supported=False,horizontal_choice_count=choice_count,runtime_pending=True))
    if set(selected_ids)-{i.key for i in literals(target) if int(i.key.split(':')[1]) in scripts}:raise ValueError('Quick unbound ID')
    return proof
