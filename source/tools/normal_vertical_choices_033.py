"""Finite033 normal vertical choices:2/3nodes, width1..13, native rows.

Only71551C/71A66C/766134 roots, source controls untouched. Conditional CPU
geometry is separate from EA/EC input/outcome/runtime and product admission.
"""
import re
from field_hint_capacity import events, GUARDS
from tpl_literals import literals, skeleton
from nickname_capacity import advance, ARGS

# Spatially neutral source conditionals only. No claim about choosing or
# reaching their branches: exact source commands/arguments remain protected.
ENTRY_CONDITIONALS = frozenset(('checkSubArea','checkNavi','checkNaviAll','checkPackChipCode','checkNetTime'))


def validate(original, target, scripts, selected_ids, nickname_bound, chip_bound):
    if skeleton(original) != skeleton(target) or not scripts or len(set(scripts)) != len(scripts) or not selected_ids or any(type(x) is not int or not 0 <= x < 255 for x in scripts):
        raise ValueError('Normal protected scope')
    if any(type(x) is not int or x < 0 for x in (nickname_bound,chip_bound)):
        raise ValueError('Normal provider bounds')
    archive = re.search(r'^@archive (\w+)', original, re.M)[1]
    if archive not in {'71551C','71A66C','766134'}:
        raise ValueError('033 vertical declared finite source roots only')
    proofs = []
    bound_ids = set()
    for script in scripts:
        match = re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)', target, re.M)
        if not match:
            raise ValueError('Normal script language')
        seq = events('@archive '+archive+'\n'+match[0])
        first = next((i for i,e in enumerate(seq) if e[1:] == ('command',('msgOpen',''))),None)
        if first is None:
            raise ValueError('Normal explicit msgOpen required')
        preamble = []
        for _, kind, data in seq[:first]:
            if kind != 'command' or data[0] not in GUARDS | ENTRY_CONDITIONALS | {'mugshotShow','mugshotHide'}:
                raise ValueError('Normal unmodeled entry')
            preamble.append(data[0])
            if data[0] in ('checkTournament','checkNetDateWeekday'):
                raise ValueError('Normal specialized entry requires dedicated proof')
            if data[0] == 'mugshotShow' and not re.fullmatch(r'\t\tmugshot = \w+\n',data[1]):
                raise ValueError('Normal portrait arguments')
            if data[0] == 'mugshotHide' and data[1]:
                raise ValueError('Normal hide arguments')
            if data[0] in ENTRY_CONDITIONALS and not re.fullmatch(r'(?:\t\t[A-Za-z][A-Za-z0-9]* = (?:\d+|continue|[A-Z])\n)+',data[1]):
                raise ValueError('Normal conditional canonical arguments')
        widths, parts, pages = [0], [], []
        waiting = ended = False
        terminal = None
        trailing_ends = 0
        here = set()
        choice = None
        choice_count = 0
        for _, kind, data in seq[first+1:]:
            if ended:
                if terminal == 'end' and kind == 'command' and data == ('end',''):
                    trailing_ends += 1
                    continue
                raise ValueError('Normal event after terminal')
            if kind == 'literal':
                if choice is not None:
                    if not choice['options'] or choice['options'][-1]['space']!=1 or choice['options'][-1]['label'] is not None or data.text.count('\n')>1 or ('\n' in data.text and not data.text.endswith('\n')):
                        raise ValueError('Choice one padded literal per option')
                    choice['options'][-1]['label']=dict(id=data.key,text=data.text,width=advance(data.text.rstrip('\n')))
                    if data.key in selected_ids:here.add(data.key)
                    continue
                if waiting:
                    raise ValueError('Normal text after wait')
                for n,line in enumerate(data.text.split('\n')):
                    if n:
                        widths.append(0)
                    widths[-1] += advance(line)
                parts.append(dict(kind='literal',id=data.key,text=data.text))
                if data.key in selected_ids:
                    here.add(data.key)
                continue
            name,args = data
            if name == 'positionOptionVertical' and choice is not None:
                options=choice['options']
                if not 1<=len(options)<3 or options[-1]['label'] is None or not options[-1]['label']['text'].endswith('\n') or choice['position_ready']:
                    raise ValueError('033 vertical repeat center requires preceding LF option')
                if args!='\t\twidth = '+str(choice['native_width'])+'\n':
                    raise ValueError('033 vertical consistent native width')
                choice['position_ready']=True
                continue
            if name == 'positionOptionVertical':
                valid_empty=widths==[0] and not parts
                valid_prompt=len(widths)==2 and widths[-1]==0 and 0<widths[0]<=180 and bool(parts)
                if waiting or not(valid_empty or valid_prompt):
                    raise ValueError('033 vertical empty row after at most one prompt row')
                m=re.fullmatch(r'\t\twidth = (\d+)\n',args)
                if not m or not 1<=int(m[1])<=13:
                    raise ValueError('033 vertical native width1..13 only')
                choice=dict(native_width=int(m[1]),allocated_advance=11*int(m[1])+8,options=[],
                            prompt_widths=list(widths),prompt_parts=list(parts),first_row=len(widths)-1,position_ready=True)
                continue
            if choice is not None:
                if name=='option':
                    n=len(choice['options'])
                    if n>=3 or not choice['position_ready'] or n and choice['options'][-1]['label'] is None:
                        raise ValueError('033 vertical exactly2or3 positioned linked options')
                    nav=re.fullmatch(r'\t\tbrackets = false\n\t\tleft = ([0-2])\n\t\tright = ([0-2])\n\t\tup = ([0-2])\n\t\tdown = ([0-2])\n',args)
                    if nav is None:
                        raise ValueError('033 vertical bounded source navigation')
                    choice['options'].append(dict(space=0,label=None,navigation=list(map(int,nav.groups()))))
                    choice['position_ready']=False
                elif name=='space':
                    if args!='\t\tcount = 1\n' or not choice['options'] or choice['options'][-1]['space'] or choice['options'][-1]['label'] is not None:
                        raise ValueError('033 vertical single native space')
                    choice['options'][-1]['space']=1
                elif name=='select':
                    options=choice['options'];count=len(options)
                    pattern=(r'\t\tdefault = ([0-2])\n\t\tlastCancelSFX = false\n\t\tnoDelay = false\n'
                             r'\t\tBSeparate = (false|true)\n\t\tdisableB = (false|true)\n\t\tclear = true\n'
                             r'\t\ttargets = \[\n((?:\t\t\tjump = (?:\d+|continue),?\n){3,4})\t\t\]\n')
                    match=re.fullmatch(pattern,args)
                    if count not in (2,3) or choice['position_ready'] or any(o['label'] is None for o in options) or match is None:
                        raise ValueError('033 vertical complete2or3 select/cancel')
                    targets=re.findall(r'jump = (\d+|continue)',match[4])
                    default=int(match[1]);first_row=choice['first_row']
                    if len(targets)!=count+1 or default>=count or first_row+count>3:
                        raise ValueError('033 vertical row/default/continuation denominator')
                    for index,option in enumerate(options):
                        text=option['label']['text']
                        if text.count('\n')!=(1 if index<count-1 else 0) or index<count-1 and not text.endswith('\n'):
                            raise ValueError('033 vertical exact row-ending option topology')
                        if any(v>=count for v in option['navigation']):
                            raise ValueError('033 vertical navigation outside declared nodes')
                    reachable={default}
                    while True:
                        more=reachable|{v for i in reachable for v in options[i]['navigation']}
                        if more==reachable:break
                        reachable=more
                    if reachable!=set(range(count)):
                        raise ValueError('033 vertical inaccessible source option')
                    extent=max(8+o['label']['width'] for o in options)
                    if extent>choice['allocated_advance'] or any(8+o['label']['width']>(168 if first_row+i==2 else 180) for i,o in enumerate(options)):
                        raise ValueError('033 vertical label exceeds native allocation/row')
                    choice.update(target_advance=extent,default=default,disable_b=match[3]=='true',BSeparate=match[2]=='true',
                                  targets=targets,kind='vertical-'+str(count)+'-choice',option_count=count,
                                  rows=list(range(first_row,first_row+count)),runtime_cursor_and_outcome_pending=True)
                    pages.append(choice);choice=None;choice_count+=1;waiting=True
                else:raise ValueError('033 vertical unmodeled choice command '+name)
                continue
            if name == 'mugshotShow':
                if not re.fullmatch(r'\t\tmugshot = \w+\n',args):
                    raise ValueError('Normal portrait arguments')
            elif name == 'mugshotHide':
                if args:
                    raise ValueError('Normal hide arguments')
            elif name == 'textSpeed':
                if waiting or args!='\t\tdelay = 0\n':raise ValueError('Choice explicit native zero-delay contract')
            elif name in ('wait','waitSkip'):
                if waiting or not re.fullmatch(r'\t\tframes = \d+\n',args):
                    raise ValueError('Normal wait arguments/state')
            elif name in ('storeGlobal8','storeGlobal16'):
                m=re.fullmatch(r'\t\tglobal = (\d+)\n\t\tvalue = (\d+)\n',args)
                if parts or waiting or widths!=[0] or m is None:raise ValueError('026 global writes only at empty page')
                index,value=map(int,m.groups())
                if not ((name=='storeGlobal8' and index in (8,9) and 0<=value<=255) or (name=='storeGlobal16' and index==10 and 0<=value<=65535)):
                    raise ValueError('026 finite battle global slots')
            elif name in ('flagSet','flagClear','flagSetNavi','flagClearNavi'):
                if not re.fullmatch(r'\t\tflag = \d+\n',args):
                    raise ValueError('Normal fixed flag arguments')
            elif name == 'printPlayerNickname':
                if waiting or args != ARGS:
                    raise ValueError('Normal nickname provider')
                widths[-1] += nickname_bound
                parts.append(dict(kind=name,bound=nickname_bound))
            elif name == 'printChip':
                if waiting or args != '\t\tbuffer = 0\n\t\tchip = 104\n':
                    raise ValueError('Normal chip provider')
                widths[-1] += chip_bound
                parts.append(dict(kind=name,bound=chip_bound))
            elif name == 'keyWait':
                if waiting or args != '\t\tany = false\n' or not parts or len(widths)>3 or any(w>(168 if i==2 else 180) for i,w in enumerate(widths)):
                    raise ValueError('Normal aggregate wait/page extent '+str(widths))
                pages.append(dict(widths=list(widths),parts=list(parts)))
                waiting = True
            elif name == 'clearMsg':
                if not waiting or args:
                    raise ValueError('Normal clear contract')
                widths,parts,waiting = [0],[],False
            elif name == 'end':
                if args or not pages or not waiting and parts:
                    raise ValueError('Normal end contract')
                ended = True
                terminal = 'end'
            elif name == 'jump':
                if parts or waiting or not pages or not re.fullmatch(r'\t\ttarget = \d+\n',args):
                    raise ValueError('Normal jump after waited cleared page only')
                ended = True
                terminal = 'jump'
            else:
                raise ValueError('Normal unmodeled body '+name)
        if not ended or not here or choice is not None or choice_count!=1:
            raise ValueError('Normal terminal/selected scope')
        bound_ids |= here
        proofs.append(dict(script=script,origin=[52,110],row_limits=[180,180,168],entry_commands=preamble,initializer='msgOpen',pages=pages,terminal=terminal,source_trailing_ends=trailing_ends,vertical_choice_count=choice_count,source_conditional_and_flag_effects_runtime_pending=True,runtime_pending=True))
    if bound_ids != set(selected_ids):
        raise ValueError('Normal unbound IDs')
    return proofs
