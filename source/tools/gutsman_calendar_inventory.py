"""Possessions template: immutable parent54 and a source-pinned nickname gap."""
import json,re
from build_visibility_poc import ROOT,require_hash
from gutsman_calendar_schedule_delete import validate as previous
from tpl_literals import literals,skeleton,replace_literals,serialize
PARENT='translations/gutsman_calendar_schedule_delete_ko.json'
PARENT_SHA='b1de499497e670a1862ef8d47c40c7a75e0e27f057c8763ede8555c8860bbb7d'
CHILD='translations/gutsman_calendar_inventory_ko.json'
ADDED=[{'id':'665698:10:0','source':'これが','translation':'이건 ','state':'needs_review'},{'id':'665698:10:1','source':'の\nしょじひんでガス!\n','translation':'의\n소지품이거스!\n','state':'needs_review'},{'id':'665698:10:2','source':'キーアイテムのかくにん','translation':'키 아이템 확인','state':'needs_review'}]
PROFILE={'script':10,'prefix_literal':0,'suffix_literal':1,'source_prefix':'これが','source_suffix':'の','prefix':'이건 ','suffix':'의','static_advance':44}
GAP='printPlayerNickname\n\t\tcapitalizeFirst = false\n\t\tcapitalizeAll = false\n\t\tprintN = false'
def advance(t):return sum(8 if c==' 'else 12 if '\uac00'<=c<='\ud7a3'else 11 for c in t)
def template(units,profile,original):
    if profile!=PROFILE:raise ValueError('unregistered nickname aggregate profile')
    us={u['id']:u for u in units};p=us['665698:10:0'];s=us['665698:10:1']
    if (p['source'],s['source'].split('\n')[0],p['translation'],s['translation'].split('\n')[0])!=(PROFILE['source_prefix'],PROFILE['source_suffix'],PROFILE['prefix'],PROFILE['suffix']):raise ValueError('nickname aggregate wording/source drift')
    items={x.key:x for x in literals(original)};left=items[p['id']];right=items[s['id']]
    if original[left.end:right.start].strip()!=GAP:raise ValueError('nickname aggregate intervening consumer changed')
    before=advance(p['source'])+advance(s['source'].split('\n')[0]);after=advance(p['translation'])+advance(s['translation'].split('\n')[0])
    if before!=44 or after!=44:raise ValueError('nickname aggregate width changed')
    return {'source_static_advance':before,'translated_static_advance':after,'nickname_command_unchanged':True}
def validate(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));previous(old)
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=54)or a['units'][:54]!=old['units']or a['units'][54:]!=ADDED or len(a['units'])!=57:raise ValueError('inventory parent/new projection')
    original=(ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig');items={x.key:x.text for x in literals(original)}
    for u in ADDED:
        if items[u['id']]!=u['source']or u['source'].count('\n')!=u['translation'].count('\n')or u['state']!='needs_review':raise ValueError('inventory source/rows/state')
    template(a['units'],PROFILE,original);return old
def replace(original,units):
    old=validate(dict(parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=54),units=units))
    template(units,PROFILE,original);target=replace_literals(original,old['units'])
    # The one new separator belongs to the exact prefix/nickname template,
    # not general choice padding. No global trailing-space rule is relaxed.
    for u in units[54:]:
        xs=[x for x in literals(target)if x.key==u['id']]
        if len(xs)!=1 or xs[0].text!=u['source']or xs[0].language!='mmbn45':raise ValueError('inventory literal identity')
        x=xs[0];target=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('inventory controls')
    return target
