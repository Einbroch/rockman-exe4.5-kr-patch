"""Analysis-only normal-window pages, including msgOpen-before-portrait.

No quick/positioned window, choices, unknown print command or caller-inherited
page is accepted. Native initializer and source-bound admission are separate.
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
        for _, kind, data in seq[first+1:]:
            if ended:
                if terminal == 'end' and kind == 'command' and data == ('end',''):
                    trailing_ends += 1
                    continue
                raise ValueError('Normal event after terminal')
            if kind == 'literal':
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
            if name == 'mugshotShow':
                if not re.fullmatch(r'\t\tmugshot = \w+\n',args):
                    raise ValueError('Normal portrait arguments')
            elif name == 'mugshotHide':
                if args:
                    raise ValueError('Normal hide arguments')
            elif name == 'textSpeed':
                if waiting or args!='\t\tdelay = 0\n':raise ValueError('Normal explicit native zero-delay contract')
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
        if not ended or not here:
            raise ValueError('Normal terminal/selected scope')
        bound_ids |= here
        proofs.append(dict(script=script,origin=[52,110],row_limits=[180,180,168],entry_commands=preamble,initializer='msgOpen',pages=pages,terminal=terminal,source_trailing_ends=trailing_ends,source_conditional_and_flag_effects_runtime_pending=True,runtime_pending=True))
    if bound_ids != set(selected_ids):
        raise ValueError('Normal unbound IDs')
    return proofs
