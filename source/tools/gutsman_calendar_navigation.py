"""Source-pinned calendar navigation extension; immutable parent."""
import json
from build_visibility_poc import ROOT,require_hash
from calendar_anniversary_confirmation import validate as validate_previous
from tpl_literals import literals
PARENT='translations/gutsman_calendar_anniversary_confirmation_ko.json'
CHILD='translations/gutsman_calendar_navigation_ko.json'
PARENT_SHA='29c13a0201adc777d88d4c10d03d96c6e20c36ee421e1e28db50d1ed7cc7a353'
NEW=[["665698:6:0","どの日の よていを\nみるでガス?","어느 날의 일정을\n볼 거스?"],["665698:7:0","なにを とうろくするでガス?\n","뭘 등록하거스?\n"],["665698:7:1","スケジュール\n","일정\n"],["665698:7:2","きねん日","기념일"]]
def validate(a):
    require_hash(ROOT/PARENT,PARENT_SHA)
    old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));validate_previous(old)
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=18) or a['units'][:18]!=old['units'] or len(a['units'])!=22:raise ValueError('calendar navigation parent projection')
    source={x.key:x.text for x in literals((ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig'))}
    expected=[dict(id=k,source=s,translation=t,state='needs_review') for k,s,t in NEW]
    if a['units'][18:]!=expected or any(source[u['id']]!=u['source'] for u in expected):raise ValueError('calendar navigation exact source/wording/state')
    return old
