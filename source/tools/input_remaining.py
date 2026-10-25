"""Explicit development selection of parent17 plus manually authored UI21.

Generated asset is read-only; wording authority remains the delta JSON.
"""
import json
from build_visibility_poc import ROOT,require_hash
from input_heading import validate as previous,replace as replace_previous
from tpl_literals import literals,serialize,skeleton
PARENT='translations/input_heading_ko.json'
PARENT_SHA='3aeea8e1b6d5956e0ba2d6a635d6b2932e45c82223bd7cc46eddf7334107e884'
DELTA='translations/input_remaining_draft_ko.json'
GENERATED='analysis/input_remaining_v1/selected_asset.json'
SCRIPTS=[11,21,23,24,25,26,27,28,29,30,31,32,34,35,36,37,38,39,40,41,42]

def inputs():
    require_hash(ROOT/PARENT,PARENT_SHA)
    old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));previous(old)
    delta=json.loads((ROOT/DELTA).read_text(encoding='utf8'))
    if delta['parent_asset']!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=17) or delta['policy']!=old['policy'] or delta['source_sha256']!=old['source_sha256'] or delta['source_archive_sha256']!=old['source_archive_sha256'] or delta['review']['release_eligible']:raise ValueError('delta baseline/policy')
    units=delta['units'];keys=[u['id'] for u in units]
    if len(keys)!=21 or set(keys)!={f'6368E8:{s}:0' for s in SCRIPTS}:raise ValueError('delta IDs')
    return old,delta

def validate(a):
    old,delta=inputs()
    if a.get('parent_asset')!=delta['parent_asset'] or a['units']!=old['units']+delta['units']:raise ValueError('immutable parent17/delta21')
    source={x.key:x for x in literals((ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig'))}
    for u in delta['units']:
        x=source[u['id']];text=u['translation'];notice=u['id']=='6368E8:11:0'
        if x.text!=u['source'] or u['state']!='needs_review' or x.language!=('mmbn45' if notice else 'mmbn45s'):raise ValueError('source/state/language')
        if not text:raise ValueError('empty translation')
        if notice:
            widths=[sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line) for line in text.split('\n')]
            if len(widths)>3 or max(widths)>132:raise ValueError('notice geometry')
        elif '\n' in text or len(text)>10:raise ValueError('heading ten cells')
    return old

def replace(original,units):
    old,delta=inputs();validate(dict(parent_asset=delta['parent_asset'],units=units))
    target=replace_previous(original,old['units'])
    lookup={x.key:x for x in literals(target)}
    for u in sorted(delta['units'],key=lambda u:lookup[u['id']].start,reverse=True):
        x=lookup[u['id']]
        if x.text!=u['source']:raise ValueError('target baseline')
        target=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('input controls')
    return target

def prepare():
    old,delta=inputs();a=dict(old)
    a.update(scope_variant='input-remaining-v1',parent_asset=delta['parent_asset'],units=old['units']+delta['units'],context=delta['context'],insertion_state='development input; explicit --input-remaining; generated read-only asset',protected_policy=delta['protected_policy'])
    validate(a);p=ROOT/GENERATED;p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return GENERATED
