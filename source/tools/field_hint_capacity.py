"""Explicit full-box hint pages with bounded native insertions; fail closed.

This models layout, not event reachability. The caller must bind native guard
and variable-provider applicability; no generic allowance is added to fullbox.
"""
import re
from tpl_literals import literals, skeleton
from nickname_capacity import advance, ARGS

GUARDS = frozenset(('checkFlag','checkFlagNavi','checkItem','checkGlobal','flagSet','flagClear','flagSetNavi','flagClearNavi','storeGlobal16','checkTournament','checkNetDateWeekday'))


def events(tpl):
    """Only canonical TextPet commands outside protected literal spans."""
    items = literals(tpl)
    out = [(i.start,'literal',i) for i in items]
    for m in re.finditer(r'^\t([A-Za-z][A-Za-z0-9]*)\s*\n',tpl,re.M):
        if any(i.start <= m.start() < i.end for i in items):
            continue
        # Parameters are two-tab lines, separate from text and commands.
        end=m.end()
        while True:
            p=re.match(r'\t\t[^\n]*\n',tpl[end:])
            if p is None:break
            end+=p.end()
        out.append((m.start(),'command',(m.group(1),tpl[m.end():end])))
    return sorted(out,key=lambda e:e[0])


def validate(original,target,scripts,selected_ids,nickname_bound,chip_bound):
    if skeleton(original)!=skeleton(target) or type(nickname_bound) is not int or type(chip_bound) is not int or min(nickname_bound,chip_bound)<0:
        raise ValueError('Hint protected structure/provider bounds')
    archive=re.search(r'^@archive (\w+)',original,re.M).group(1)
    if (not scripts or len(set(scripts))!=len(scripts)
            or any(type(s) is not int or not 0<=s<255 for s in scripts)
            or not selected_ids):raise ValueError('Hint script denominator')
    proofs=[]
    for script in scripts:
        pattern=r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)'
        src=re.search(pattern,original,re.M);dst=re.search(pattern,target,re.M)
        if src is None or dst is None:raise ValueError('Hint script language/scope')
        header='@archive '+archive+'\n'
        seq=events(header+dst.group());source_items=literals(header+src.group())
        if not (set(selected_ids)&{i.key for i in source_items}):raise ValueError('Hint script has no selected literal')
        # Same original initializer as fullbox; preceding state guards have no
        # literals and are source-preserved, with new command applicability
        # bound independently to native CPU evidence by the invoking caller.
        first=next((i for i,e in enumerate(seq) if e[1]=='command' and e[2][0]=='mugshotShow'),None)
        if first is None or first+1>=len(seq) or seq[first+1][1:]!=('command',('msgOpen','')):
            raise ValueError('Hint full-box initializer')
        for _,kind,data in seq[:first]:
            if kind!='command' or data[0] not in GUARDS:raise ValueError('Hint unmodeled entry command')
            name,args=data
            if name=='checkTournament' and not re.fullmatch(r'\t\tbitmask = 4\n\t\tjumpIfNone = (?:continue|\d+)\n\t\tjumpIfTrue = (?:continue|\d+)\n\t\tjumpIfFalse = (?:continue|\d+)\n',args):
                raise ValueError('Hint tournament guard outside proven mask')
            if name=='checkNetDateWeekday':
                m=re.fullmatch(r'\t\tlower = ([06])\n\t\tupper = ([06])\n\t\tjumpIfInRange = (?:continue|\d+)\n\t\tjumpIfOutOfRange = (?:continue|\d+)\n',args)
                if m is None or m[1]!=m[2]:raise ValueError('Hint weekday outside proven singleton ranges')
        widths=[0];parts=[];pages=[];opened=False;waiting=False;ended=False
        def append_text(value,key):
            for i,line in enumerate(value.split('\n')):
                if i:widths.append(0)
                widths[-1]+=advance(line)
            parts.append(dict(kind='literal',id=key,text=value))
        def check_page():
            if not parts or len(widths)>3 or any(w>(168 if i==2 else 180) for i,w in enumerate(widths)):
                raise ValueError('Hint aggregate page extent: '+str(widths))
        for _,kind,data in seq[first:]:
            if ended:raise ValueError('Hint events after end')
            if kind=='literal':
                if not opened or waiting:raise ValueError('Hint literal without writable page')
                append_text(data.text,data.key);continue
            name,args=data
            if name=='mugshotShow':
                if not re.fullmatch(r'\t\tmugshot = \w+\n',args):raise ValueError('Hint portrait arguments')
            elif name=='msgOpen':
                if opened or args:raise ValueError('Hint repeated/window-changing initializer')
                opened=True
            elif name=='printPlayerNickname':
                if not opened or waiting or args!=ARGS:raise ValueError('Hint nickname command arguments/state')
                widths[-1]+=nickname_bound;parts.append(dict(kind=name,bound=nickname_bound))
            elif name=='printChip':
                if not opened or waiting or args!='\t\tbuffer = 0\n\t\tchip = 104\n':raise ValueError('Hint chip command arguments/state')
                widths[-1]+=chip_bound;parts.append(dict(kind=name,bound=chip_bound))
            elif name=='keyWait':
                if waiting or args!='\t\tany = false\n':raise ValueError('Hint wait contract')
                check_page();pages.append(dict(widths=list(widths),parts=list(parts)));waiting=True
            elif name=='clearMsg':
                if not waiting or args:raise ValueError('Hint page clearing contract')
                widths=[0];parts=[];waiting=False
            elif name=='end':
                if not waiting or args:raise ValueError('Hint end without page wait')
                ended=True
            else:raise ValueError('Hint unmodeled display command '+name)
        if not ended:raise ValueError('Hint missing end')
        proofs.append(dict(script=script,origin=[52,110],row_limits=[180,180,168],entry_guards=[e[2][0] for e in seq[:first]],pages=pages,runtime_verification_pending=True))
    if set(selected_ids)-{i.key for i in literals(original) if int(i.key.split(':')[1]) in scripts}:
        raise ValueError('Hint selected literal scope')
    return proofs


def validate_source(source,archive,original,target,scope):
    """Adopted source-bound compile gate; no fuzzy catalog or global bypass."""
    import struct
    from build_visibility_poc import ROOT,sha,require_hash
    from cumulative_batch500 import read
    from nickname_capacity import native_bound
    from archive_scripts import script_spans
    if (scope.get('field_hint_capacity_profile')!='b0-native-insertions-v1'
            or scope.get('script_count')!=255 or scope.get('consumer')!='normal-dialogue'
            or scope.get('literal_language')!='mmbn45' or scope.get('max_literal_rows')!=3
            or scope.get('max_line_advance')!=180):raise ValueError('B0 source-bound capacity scope')
    cfg=read('project.json')
    if sha(source)!=cfg['source_profile']['sha256']:raise ValueError('B0 capacity revision')
    if struct.unpack_from('<II',source,0x54060)!=(0x08054238,0x08054294):raise ValueError('B0 finite table boundaries')
    pointers=struct.unpack_from('<23I',source,0x54238)
    if pointers.count(0)!=2 or pointers[13:15]!=(0,0) or 0x08000000+int(archive,16) not in pointers:
        raise ValueError('B0 source archive membership')
    path='analysis/pending_insertion_500_023_guard_v1/native_guard_cpu.json'
    cpu=read(path)
    if not cpu['passed'] or cpu['source_sha256']!=sha(source) or cpu['case_counts']!={'tournament':2944,'weekday':56}:
        raise ValueError('B0 native guard CPU evidence')
    for r in cpu['native_code']:
        if sha(source[r['offset']:r['offset']+r['bytes']])!=r['sha256']:raise ValueError('B0 native guard source applicability')
    name=script_spans(source[0x765190:0x765190+2437],256)[104]
    if name!=bytes.fromhex('4b593d243a298202e5'):raise ValueError('Native chip104 source')
    widths=struct.unpack_from('<441I',source,0x5290C)
    chip_bound=sum(widths[ch] for ch in name[:-1]);name_bound=native_bound(source)
    proof=validate(original,target,scope['literal_scripts'],set(scope['literal_ids']),name_bound,chip_bound)
    return dict(profile=scope['field_hint_capacity_profile'],native_nickname_bound=name_bound,native_chip104_bound=chip_bound,guard_cpu=dict(path=path,sha256=sha((ROOT/path).read_bytes())),pages=proof,runtime_pending=True)
