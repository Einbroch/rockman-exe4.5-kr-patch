"""Strict source-bound PET list caption/guard geometry; analysis only."""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from nickname_capacity import advance,ARGS
from pet_choice_capacity_026 import PREFIX


def validate(original,target,scripts,selected_ids,nickname_bound,field):
    if type(nickname_bound) is not int or not 0<=nickname_bound<=99:raise ValueError('List nickname applicability')
    script=field['list_selector'][0];count,cap=field['count'],field['cap']
    if scripts!=[script] or count not in (3,4,8) or cap not in (6,8) or field['list_selector'][1]!=10:raise ValueError('List source field selector')
    if skeleton(original)!=skeleton(target) or not selected_ids:raise ValueError('List protected control/scope')
    seq=events(target)
    if len(seq)<4 or any(k!='command' for _,k,_ in seq[:4]) or [d for _,_,d in seq[:4]]!=PREFIX:raise ValueError('List exact PET initializer')
    at=4
    def command(name,args=''):
        nonlocal at
        if at>=len(seq) or seq[at][1:]!=('command',(name,args)):raise ValueError('List expected '+name)
        at+=1
    if at>=len(seq) or seq[at][1]!='command' or seq[at][2][0]!='flagSet' or re.fullmatch(r'\t\tflag = \d+\n',seq[at][2][1]) is None:raise ValueError('List source initial flag')
    flag=seq[at][2][1];at+=1;rows=[0];parts=[];nickname=False;ids=set()
    while at<len(seq) and (seq[at][1]=='literal' or seq[at][1:] == ('command',('printPlayerNickname',ARGS))):
        if seq[at][1]=='command':
            if nickname:raise ValueError('List duplicate nickname')
            command('printPlayerNickname',ARGS);rows[-1]+=nickname_bound;nickname=True
            parts.append(dict(kind='printPlayerNickname',bound=nickname_bound))
            continue
        literal=seq[at][2];at+=1;ids.add(literal.key);parts.append(dict(id=literal.key,text=literal.text))
        for i,line in enumerate(literal.text.split('\n')):
            if i:rows.append(0)
            rows[-1]+=advance(line)
    if ids!=set(selected_ids) or not parts:raise ValueError('List caption selected identity')
    if len(rows)>3 or max(rows)>132:raise ValueError('List aggregate caption extent '+str(rows))
    command('keyWait','\t\tany = false\n');command('clearMsg')
    pages=[]
    for page in range((count+2)//3):
        if page:
            for n in range((page-1)*3+1,page*3+1):
                command('checkGlobal',f'\t\tvariable = 5\n\t\tvalue = {n}\n\t\tjumpIfEqual = {script+1}\n\t\tjumpIfNotEqual = continue\n')
        command('printStringBuffer'+str(page+1),ARGS)
        command('keyWait','\t\tany = false\n');command('clearMsg')
        pages.append(dict(buffer=page+1,conditional_active_count=[page*3+1,min(page*3+3,count)],maximum_rows=min(3,count-page*3),maximum_native_row_advance=cap*11,maximum_encoded_used_bytes=min(3,count-page*3)*(2*cap+1),valid_native_terminated_records_required=True))
    command('jump',f'\t\ttarget = {script+1}\n')
    if at!=len(seq):raise ValueError('List event after terminal')
    return [dict(script=script,profile_row=field['row'],origin=[92,110],row_limits=[132]*3,caption_widths=rows,caption_parts=parts,native_nickname_bound=nickname_bound if nickname else 0,pages=pages,preserved_initial_flag=flag,conditional_producer='08038CD8 valid legacy records, global5 active count and initialized page guards',scratch_descriptor_bytes=512,scratch_slot_stride=128,product_admitted=False,runtime_pending=True,full_VM_page_and_editor_lifetime_pending=True,automatic_Hangul_names_supported=False)]


