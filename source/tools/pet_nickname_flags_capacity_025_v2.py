"""Spatial projection of unchanged fixed flags outside writable text pages.

This does not execute or approve the flag/event effects. Source/target command
identity is mandatory; the old exact PET prefix/page validator remains owner
of geometry. No product registration is provided by this analysis adapter.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from pet_nickname_capacity_025 import validate as core


def projection(tpl):
    edits, flags = [], []
    dirty = waiting = closed = False
    for pos, kind, data in events(tpl):
        if kind == 'literal':
            dirty = True
            continue
        name,args = data
        if name.startswith('print'):
            dirty = True
        if name in ('end','jump','waitHold'):
            closed = True
        if name == 'keyWait':
            waiting = True
        elif name == 'clearMsg':
            dirty = waiting = False
        elif name in ('flagSet','flagClear'):
            if closed or dirty or waiting or not re.fullmatch(r'\t\tflag = \d+\n',args):
                raise ValueError('PET flag outside empty-page boundary')
            raw = '\t'+name+'\n'+args
            if tpl[pos:pos+len(raw)] != raw:
                raise ValueError('PET canonical flag span')
            edits.append((pos,pos+len(raw)))
            flags.append(dict(command=name,arguments=args))
    out = tpl
    for start,end in reversed(edits):
        out = out[:start]+out[end:]
    return out, flags


def validate(original,target,scripts,selected_ids,nickname_bound):
    if skeleton(original) != skeleton(target) or len(scripts)!=1:
        raise ValueError('PET flag source scope')
    # Work on only this script, never infer cross-script flag/page state.
    header = re.search(r'^@archive \w+',original,re.M)[0]+'\n'
    pattern = r'^script '+str(scripts[0])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)'
    so,st = (re.search(pattern,t,re.M) for t in (original,target))
    if not so or not st:
        raise ValueError('PET flag script identity')
    source, flags = projection(header+so[0])
    transformed, target_flags = projection(header+st[0])
    if not flags or target_flags != flags:
        raise ValueError('PET flag unchanged denominator')
    proof = core(source,transformed,scripts,selected_ids,nickname_bound)
    proof[0]['preserved_zero_width_flags'] = flags
    proof[0]['flag_effects_runtime_pending'] = True
    return proof

