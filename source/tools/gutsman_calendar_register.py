"""Four normal registration-menu literals; ten source-pinned parent units read-only."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals,skeleton
PARENT='translations/gutsman_calendar_home_ko.json'
PARENT_SHA='4f60c8a74156a3247e526f29f7182b8001680ed7433ec431fb1bafe43df3f1a6'
CHILD='translations/gutsman_calendar_register_ko.json'
TPL_SHA='17f59df298ea973d4da8e1958eb42aa552104717c8922990c56dfd3621203a2e'
NEW={'665698:1:0':'어느 날의 일정을\n입력하거스?','665698:2:0':'뭘 등록하거스?\n','665698:2:1':'일정\n','665698:2:2':'기념일'}
def validate_parent(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'))
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=10):raise ValueError('calendar register parent identity')
    if a['units'][:10]!=old['units'] or len(a['units'])!=14 or {u['id'] for u in a['units']}!={u['id'] for u in old['units']}|set(NEW):raise ValueError('calendar register inherited ten units')
    p=ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');source={x.key:x.text for x in literals(t)}
    for u in a['units']:
        if u['source']!=source[u['id']] or u['state']!='needs_review' or u['source'].count('\n')!=u['translation'].count('\n'):raise ValueError('calendar register source/state/rows')
        if u['id'] in NEW and u['translation']!=NEW[u['id']]:raise ValueError('calendar register selected draft identity')
    if skeleton(t)!=skeleton(replace_literals(t,a['units'])):raise ValueError('calendar register controls drift')
