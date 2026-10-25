"""Explicit date/save17 development selection retaining common UI38."""
import json
from build_visibility_poc import ROOT,require_hash
from input_remaining import prepare as prepare_parent,validate as validate_parent,replace as replace_parent
from verify_calendar_date_save_draft import ASSET,IDS,validate as validate_delta
from tpl_literals import literals,serialize,skeleton
PARENT='analysis/input_remaining_v1/selected_asset.json'
PARENT_SHA='d2aff7aadcd997c2accab52f761bce57ecf47926b9986f93c4bfec710fc58647'
GENERATED='analysis/calendar_date_save_v1/selected_asset.json'
SCRIPTS=[76,90,91,92,93,94]

def inputs():
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));validate_parent(old)
    delta=json.loads((ROOT/ASSET).read_text(encoding='utf8'))
    if any(delta[k]!=old[k] for k in ('source_sha256','source_archive_sha256','archive','policy')):raise ValueError('date/save baseline')
    original=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
    validate_delta(delta,original,set(range(0xAC00,0xD7A4)))
    return old,delta

def validate(a):
    old,delta=inputs()
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=38) or a['units']!=old['units']+delta['units']:raise ValueError('immutable common38/date17')
    return old

def replace(original,units):
    old,delta=inputs();validate(dict(parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=38),units=units))
    target=replace_parent(original,old['units']);lookup={x.key:x for x in literals(target)}
    for u in sorted(delta['units'],key=lambda u:lookup[u['id']].start,reverse=True):
        x=lookup[u['id']]
        if x.text!=u['source']:raise ValueError('date/save source')
        target=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('date/save commands')
    return target

def prepare():
    prepare_parent();old,delta=inputs();a=dict(old)
    a.update(scope_variant='calendar-date-save-v1',parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=38),units=old['units']+delta['units'],context=delta['context'],protected_policy=delta['protected_policy'],insertion_state='development input; explicit --calendar-date-save; generated read-only')
    validate(a);p=ROOT/GENERATED;p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return GENERATED
