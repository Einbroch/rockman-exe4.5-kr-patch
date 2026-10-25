"""Narrow development full-box layout contract; not a quick-window override."""
import re
from tpl_literals import literals
from nickname_capacity import advance

def validate(original,target,profiles,selected_ids):
    archive=re.search(r'^@archive (\w+)',original,re.M).group(1);seen=set();proof=[]
    for p in profiles:
        if not {'script','ids'}<=set(p) or set(p)-{'script','ids','entry_guards','portrait_changes'} or ('portrait_changes' in p and p['portrait_changes'] is not True) or p['script'] in seen or not p['ids'] or not set(p['ids'])<=selected_ids:raise ValueError('Full-box selected profile')
        script=p['script'];seen.add(script)
        pattern=r'^script '+str(script)+r'\s+mmbn45\s*\{[\s\S]*?(?=^script\s|\Z)'
        src=re.search(pattern,original,re.M);dst=re.search(pattern,target,re.M)
        if not src or not dst:raise ValueError('Full-box script language')
        section=src.group()
        if 'entry_guards' in p:
            match=re.match(r'^script \d+ mmbn45 \{\s*\n(?P<preamble>[\s\S]*?)\tmugshotShow\n\t\tmugshot = \w+\n\tmsgOpen\n',section)
            if not match:raise ValueError('Full-box guarded initializer')
            pre=match.group('preamble');guards=re.findall(r'^\t(\w+)\b',pre,re.M)
            allowed={'checkFlag','checkFlagNavi','checkItem','checkGlobal','flagSet','flagClear','flagSetNavi','flagClearNavi','storeGlobal16'}
            if not guards or guards!=p['entry_guards'] or set(guards)-allowed or '"' in pre:raise ValueError('Full-box entry guard contract')
        elif not re.match(r'^script \d+ mmbn45 \{\s*\n\tmugshotShow\n\t\tmugshot = \w+\n\tmsgOpen\n',section):raise ValueError('Full-box native initializer')
        commands=re.findall(r'^\t(\w+)\b',section,re.M)
        portrait_count=commands.count('mugshotShow')
        if commands.count('msgOpen')!=1 or (portrait_count<1 if p.get('portrait_changes') else portrait_count!=1) or any(c.startswith(('print','position','option','select','msgOpenQuick','mugshotHide','msgWidth','msgHeight')) for c in commands):raise ValueError('Full-box context changes')
        prefix='@archive '+archive+'\n';ss=literals(prefix+section);tt={i.key:i for i in literals(prefix+dst.group())};last=None;rows=[]
        for literal in ss:
            if last is not None:
                between=(prefix+section)[last.end:literal.start]
                if not re.search(r'^\tclearMsg\s*$',between,re.M):raise ValueError('Full-box composite page')
            last=literal
            if literal.key not in p['ids']:raise ValueError('Full-box incomplete literal page scope')
            value=tt[literal.key].text;w=list(map(advance,value.split('\n')))
            if len(w)>3 or any(n>(168 if i==2 else 180) for i,n in enumerate(w)):raise ValueError('Full-box page extent')
            rows.append(dict(id=literal.key,widths=w))
        if set(p['ids'])!={i.key for i in ss}:raise ValueError('Full-box exact literal identity')
        proof.append(dict(script=script,origin=[52,110],row_limits=[180,180,168],pages=rows,development_runtime_pending=True))
    return proof
