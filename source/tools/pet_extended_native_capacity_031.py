"""031 analysis-only opponent-chip/player-name PET widths; NOT admission.

Requires successful native cache preparation from valid legacy records and
preserved lifetime through F90C. CPU proof alone does not establish callers.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton,literals
from nickname_capacity import advance,ARGS
from profile_provider_bounds_027_v2 import FIELDS
from inspect_profile_chip_pools_030 import CHIPS as PRIOR_CHIPS
CHIPS=dict(PRIOR_CHIPS,printMostLostToOpponentsChip=(18,20,None),printMostDefeatedOpponentsChip=(20,22,None))
NEW_PROVIDERS={'printMostLostToOpponentsChip','printMostDefeatedOpponentsChip','printPlayerName'}
CHIP_BOUNDS={name:88 for name in CHIPS}
ARRAY_CAPS={'printOlderBro':6,'printYoungerBro':6,'printOlderSis':6,'printYoungerSis':6,'printFriend':6,'printHobby':8,'printFavShow':8,'printWish':8}
PROVIDER_BOUNDS={name:cap*11 for name,(_,_,cap,_,_) in FIELDS.items()}
PROVIDER_BOUNDS.update({name:cap*11 for name,cap in ARRAY_CAPS.items()})
PROVIDER_BOUNDS.update(CHIP_BOUNDS)
PROVIDER_BOUNDS['printPlayerName']=66

PREFIX=[('positionBox','\t\tleft = 10\n\t\ttop = 12\n\t\ttype = 1\n'),('msgOpenQuick',''),('positionText','\t\tleft = 92\n\t\ttop = 110\n\t\tarrowDistance = 3\n'),('positionArrow','\t\tleft = 225\n\t\ttop = 141\n')]


def validate(original,target,scripts,selected_ids,nickname_bound):
    if type(nickname_bound) is not int or not 0<=nickname_bound<=99:raise ValueError('Quick nickname applicability bound')
    if skeleton(original)!=skeleton(target) or len(scripts)!=len(set(scripts)) or not selected_ids:raise ValueError('Quick protected scope')
    archive=re.search(r'^@archive (\w+)',original,re.M).group(1);proof=[]
    for script in scripts:
        match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
        if match is None:raise ValueError('Quick source script')
        seq=events('@archive '+archive+'\n'+match.group())
        if not any(kind=='command' and data[0] in NEW_PROVIDERS for _,kind,data in seq):raise ValueError('027 direct provider required in selected script')
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
            if name in PROVIDER_BOUNDS:
                if waiting or args!=ARGS:raise ValueError('027 direct native provider arguments/state')
                bound=PROVIDER_BOUNDS[name];widths[-1]+=bound
                parts.append(dict(kind=name,bound=bound,valid_native_editor_record_only=name not in CHIP_BOUNDS,finite_native_chip_pool_required=name in CHIP_BOUNDS,conditional_cache_prepared_and_lifetime_required=name in ARRAY_CAPS))
                had_text=True
            elif name=='printPlayerNickname':
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
            elif name in ('flagSet','flagClear'):
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
        if not closed or not selected_here:raise ValueError('Quick terminal/selected identity')
        proof.append(dict(script=script,origin=[92,110],row_limits=[132,132,132],arrow=[225,141],pages=pages,native_nickname_bound=nickname_bound,direct_native_profile_bounds=PROVIDER_BOUNDS,automatic_Hangul_names_supported=False,runtime_pending=True,product_admitted=False,cache_preparation_caller_unproven=True))
    if set(selected_ids)-{i.key for i in literals(target) if int(i.key.split(':')[1]) in scripts}:raise ValueError('Quick unbound ID')
    return proof
