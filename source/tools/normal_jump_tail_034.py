"""Geometry projection only: one source E6 after an unconditional EF00 jump.

The actual source/target still contain both instructions. No ROM transform.
"""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from normal_timing_capacity_025 import validate as core


def project(one):
    seq=events(one)
    if len(seq)<3 or seq[-1][1:]!=('command',('end','')) or seq[-2][1]!='command' or seq[-2][2][0]!='jump' or seq[-3][1:]!=('command',('clearMsg','')):raise ValueError('034 exact clear/jump/one-end tail')
    match=re.fullmatch(r'\t\ttarget = (\d+)\n',seq[-2][2][1])
    if match is None or not 0<=int(match[1])<255:raise ValueError('034 unconditional non255 jump required')
    at=seq[-1][0]
    if one[at:at+5]!='\tend\n':raise ValueError('034 canonical trailing end span')
    return one[:at]+one[at+5:],int(match[1])


def validate(original,target,scripts,selected_ids,nickname_bound):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('034 jump-tail protected scope')
    arc=re.search(r'^@archive (\w+)',original,re.M)[1]
    if arc not in {'716DE4','71A66C'}:raise ValueError('034 jump-tail finite source roots')
    pattern=r'^script '+str(scripts[0])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)'
    sections=[re.search(pattern,t,re.M) for t in (original,target)]
    if any(s is None for s in sections):raise ValueError('034 jump-tail script language')
    (src,a),(dst,b)=[project('@archive '+arc+'\n'+s[0]) for s in sections]
    if a!=b:raise ValueError('034 jump-tail target changed')
    result=core(src,dst,scripts,selected_ids,nickname_bound,88)
    result[0].update(source_trailing_end_after_unconditional_jump_preserved=True,native_jump_target=a,projection_only=True,full_jump_destination_and_progression_runtime_pending=True)
    return result
