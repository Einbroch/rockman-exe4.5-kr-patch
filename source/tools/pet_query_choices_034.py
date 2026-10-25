"""Finite PET132px 2-choice pages, native pads8/16/24, source controls locked.

Geometry only. The source select may clear before post-choice text/flags and
terminal waitHold. This does not certify external editor/caller or flag effects.
"""
import re
from field_hint_capacity import events
from pet_choice_capacity_026 import PREFIX
from tpl_literals import skeleton
from nickname_capacity import advance,ARGS


def validate(original,target,scripts,selected_ids,nickname_bound):
    if skeleton(original)!=skeleton(target) or type(nickname_bound) is not int or not 0<=nickname_bound<=99 or not selected_ids or len(scripts)!=len(set(scripts)):raise ValueError('034 PET query protected scope')
    arc=re.search(r'^@archive (\w+)',original,re.M)[1];proof=[];all_seen=set()
    for script in scripts:
        if type(script) is not int or not 0<=script<255:raise ValueError('034 query script range')
        match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',target,re.M)
        if match is None:raise ValueError('034 query normal-font script')
        seq=events('@archive '+arc+'\n'+match[0])
        if len(seq)<4 or any(k!='command' for _,k,_ in seq[:4]) or [d for _,_,d in seq[:4]]!=PREFIX:raise ValueError('034 exact PET initializer')
        widths=[0];parts=[];pages=[];waiting=closed=False;choice=None;count=0;seen=set();flags=[];selected_clean=False
        def page():
            if not parts or len(widths)>3 or max(widths)>132:raise ValueError('034 query aggregate page width/rows')
            pages.append(dict(widths=list(widths),parts=list(parts)))
        for _,kind,data in seq[4:]:
            if closed:raise ValueError('034 query event after terminal')
            if kind=='literal':
                seen.add(data.key)
                if choice is not None:
                    if not choice['options'] or choice['options'][-1]['space']!=1 or choice['options'][-1]['label'] is not None or '\n' in data.text:raise ValueError('034 query one padded single-line option')
                    choice['options'][-1]['label']=dict(id=data.key,text=data.text,width=advance(data.text));continue
                if waiting:raise ValueError('034 query text after wait')
                for i,line in enumerate(data.text.split('\n')):
                    if i:widths.append(0)
                    widths[-1]+=advance(line)
                parts.append(dict(id=data.key,text=data.text));selected_clean=False;continue
            name,args=data
            if name=='spacePx' and choice is None:
                pad=re.fullmatch(r'\t\tcount = (8|16|24)\n',args)
                if pad is None or waiting or count or not 1<=len(widths)<=3 or widths[-1]!=0 or max(widths)>132:raise ValueError('034 query pad/empty option row')
                choice=dict(left_pad=int(pad[1]),row=len(widths)-1,prompt_widths=list(widths),prompt_parts=list(parts),options=[]);continue
            if choice is not None:
                if name=='option':
                    n=len(choice['options']);nav=re.fullmatch(r'\t\tbrackets = false\n\t\tleft = ([01])\n\t\tright = ([01])\n\t\tup = ([01])\n\t\tdown = ([01])\n',args)
                    if nav is None or n>=2 or n and choice['options'][-1]['label'] is None:raise ValueError('034 query two complete bounded nodes')
                    choice['options'].append(dict(navigation=list(map(int,nav.groups())),space=0,label=None))
                elif name=='space':
                    if args!='\t\tcount = 1\n' or not choice['options'] or choice['options'][-1]['space'] or choice['options'][-1]['label'] is not None:raise ValueError('034 query native8px label pad')
                    choice['options'][-1]['space']=1
                elif name=='select':
                    pattern=(r'\t\tdefault = ([01])\n\t\tlastCancelSFX = false\n\t\tnoDelay = false\n\t\tBSeparate = false\n\t\tdisableB = false\n\t\tclear = true\n'
                             r'\t\ttargets = \[\n\t\t\tjump = (\d+|continue),\n\t\t\tjump = (\d+|continue),\n\t\t\tjump = (\d+|continue)\n\t\t\]\n')
                    m=re.fullmatch(pattern,args);options=choice['options']
                    if m is None or len(options)!=2 or any(o['label'] is None for o in options):raise ValueError('034 query exact native select/cancel/clear')
                    if any(any(v!=1-i for v in o['navigation'][:2]) or o['navigation'][2:]!=[i,i] for i,o in enumerate(options)):raise ValueError('034 query canonical horizontal graph')
                    extent=choice['left_pad']+sum(8+o['label']['width'] for o in options)
                    if extent>132:raise ValueError('034 query translated options exceed132px')
                    choice.update(kind='pet-query-two-choice',target_advance=extent,default=int(m[1]),targets=list(m.groups()[1:]),clear=True,BSeparate=False,runtime_cursor_and_outcome_pending=True)
                    pages.append(choice);choice=None;count+=1;widths=[0];parts=[];waiting=False;selected_clean=True
                else:raise ValueError('034 query unsupported selector event '+name)
                continue
            if name=='printPlayerNickname':
                if waiting or args!=ARGS:raise ValueError('034 query nickname state/arguments')
                widths[-1]+=nickname_bound;parts.append(dict(kind=name,bound=nickname_bound,conditional_valid_native_name=True));selected_clean=False
            elif name=='keyWait':
                if waiting or args!='\t\tany = false\n':raise ValueError('034 query native keyWait')
                page();waiting=True;selected_clean=False
            elif name=='clearMsg':
                if args or not(waiting or selected_clean):raise ValueError('034 query clear only after wait or native cleared select')
                widths=[0];parts=[];waiting=False
            elif name in ('flagSet','flagClear'):
                m=re.fullmatch(r'\t\tflag = (\d+)\n',args)
                if m is None or not 0<=int(m[1])<=65535:raise ValueError('034 query fixed source flag argument')
                flags.append(dict(command=name,arguments=args,effects_runtime_pending=True))
            elif name in ('waitHold','end'):
                if args or count!=1 or not pages or parts and not waiting:raise ValueError('034 query terminal only after completed/cleared page')
                closed=True
            else:raise ValueError('034 query unmodeled command '+name)
        if not closed or count!=1 or choice is not None or not seen&set(selected_ids):raise ValueError('034 query complete source/selected script')
        all_seen|=seen
        proof.append(dict(script=script,origin=[92,110],row_limits=[132]*3,arrow=[225,141],pages=pages,preserved_flags=flags,native_nickname_bound=nickname_bound,
                          source_post_select_clear_and_terminal_preserved=True,source_flag_effects_and_external_editor_runtime_pending=True,product_admitted=False,runtime_pending=True))
    if set(selected_ids)-all_seen:raise ValueError('034 query selected literal outside bound scripts')
    return proof
