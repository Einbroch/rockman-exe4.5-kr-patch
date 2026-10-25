"""025 source-preserved normal pages and one finite horizontal two-choice row.

Only F607 widths1..11, two canonical linked EA options, EB00/1 padding,
and canonical EC continuation/clear are modeled. Native CPU applicability,
actual cursor/input/outcome runtime and product registration are separate.
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
                    if not choice['options'] or choice['options'][-1]['space']!=1 or choice['options'][-1]['label'] is not None or '\n' in data.text:
                        raise ValueError('Choice one padded literal per option')
                    choice['options'][-1]['label']=dict(id=data.key,text=data.text,width=advance(data.text))
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
            if name == 'positionOptionHorizontal':
                if choice is not None or waiting or not (1<=len(widths)<=3 and widths[-1]==0 and all(w<=(168 if i==2 else 180) for i,w in enumerate(widths))):raise ValueError('Choice requires empty cleared native page')
                m=re.fullmatch(r'\t\twidth = (\d+)\n',args)
                if not m or not 1<=int(m[1])<=11:raise ValueError('Choice native centered width1..11 only')
                choice=dict(native_width=int(m[1]),allocated_advance=11*(int(m[1])-1)+16,options=[],prompt_widths=list(widths),prompt_parts=list(parts))
                continue
            if choice is not None:
                if name=='option':
                    n=len(choice['options'])
                    if n>=2 or n and choice['options'][-1]['label'] is None:raise ValueError('Choice exactly two linked options')
                    nav=re.fullmatch(r'\t\tbrackets = false\n\t\tleft = ([01])\n\t\tright = ([01])\n\t\tup = ([01])\n\t\tdown = ([01])\n',args)
                    if nav is None:raise ValueError('Choice bounded two-node native navigation graph')
                    choice['options'].append(dict(space=0,label=None,navigation=list(map(int,nav.groups()))))
                elif name=='space':
                    if args!='\t\tcount = 1\n' or not choice['options'] or choice['options'][-1]['space'] or choice['options'][-1]['label'] is not None:raise ValueError('Choice single native space pad')
                    choice['options'][-1]['space']=1
                elif name=='select':
                    pattern=(r'\t\tdefault = ([01])\n\t\tlastCancelSFX = false\n\t\tnoDelay = false\n'
                             r'\t\tBSeparate = false\n\t\tdisableB = false\n\t\tclear = true\n'
                             r'\t\ttargets = \[\n\t\t\tjump = (\d+|continue),\n\t\t\tjump = (\d+|continue),\n\t\t\tjump = (\d+|continue)\n\t\t\]\n')
                    match=re.fullmatch(pattern,args)
                    if len(choice['options'])!=2 or any(o['label'] is None for o in choice['options']) or not match:raise ValueError('Choice complete canonical select/cancel')
                    extent=sum(8+o['label']['width'] for o in choice['options'])
                    if extent>choice['allocated_advance']:raise ValueError('Choice translated row exceeds original allocation')
                    choice.update(target_advance=extent,default=int(match[1]),targets=list(match.groups()[1:]),kind='horizontal-two-choice',runtime_cursor_and_outcome_pending=True)
                    pages.append(choice);choice=None;choice_count+=1;waiting=True
                else:raise ValueError('Choice unmodeled row command '+name)
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
        proofs.append(dict(script=script,origin=[52,110],row_limits=[180,180,168],entry_commands=preamble,initializer='msgOpen',pages=pages,terminal=terminal,source_trailing_ends=trailing_ends,horizontal_choice_count=choice_count,source_conditional_and_flag_effects_runtime_pending=True,runtime_pending=True))
    if bound_ids != set(selected_ids):
        raise ValueError('Normal unbound IDs')
    return proofs
