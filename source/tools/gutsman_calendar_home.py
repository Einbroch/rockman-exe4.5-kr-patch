"""Three dynamic calendar-home literals; seven source-pinned parent units read-only."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals,skeleton
PARENT='translations/gutsman_calendar_confirmation_ko.json'
PARENT_SHA='53b30915c51d51daeb4b4ca05d7f681c83eedc45ec1d07d8f99cf4214310b6dc'
CHILD='translations/gutsman_calendar_home_ko.json'
TPL_SHA='17f59df298ea973d4da8e1958eb42aa552104717c8922990c56dfd3621203a2e'
NEW={'665698:0:0':'오늘은 ','665698:0:1':'월','665698:0:2':'일이거스\n뭘 할 거스?'}
def validate_parent(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'))
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=7):raise ValueError('calendar home parent identity')
    if a['units'][:7]!=old['units'] or len(a['units'])!=10 or {u['id'] for u in a['units']}!={u['id'] for u in old['units']}|set(NEW):raise ValueError('calendar home inherited seven units')
    p=ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');source={x.key:x.text for x in literals(t)}
    for u in a['units']:
        if u['source']!=source[u['id']] or u['state']!='needs_review' or u['source'].count('\n')!=u['translation'].count('\n'):raise ValueError('calendar home source/state/rows')
        if u['id'] in NEW and u['translation']!=NEW[u['id']]:raise ValueError('calendar home selected draft identity')
    if not a['units'][-3]['translation'].endswith(' ') or a['units'][-3]['translation'].endswith('  '):raise ValueError('calendar home exact one-space prefix padding')
    if skeleton(t)!=skeleton(replace_literals(t,a['units'])):raise ValueError('calendar home controls drift')
