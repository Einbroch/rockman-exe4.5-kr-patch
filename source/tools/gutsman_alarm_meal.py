"""One native-nickname meal sentence; five prior alarm units are read-only."""
import json
from build_visibility_poc import ROOT,require_hash
from gutsman_alarm_followup import validate_parent as validate_followup
from draft_gutsman_schedule_alarm import TPL_SHA
from tpl_literals import literals,replace_literals
PARENT='translations/gutsman_alarm_followup_ko.json'
PARENT_SHA='2885f95849e7a343476c5f2c97bad0418ae9de91a9efe45e0b70f7849f3b6bdb'
CHILD='translations/gutsman_alarm_meal_ko.json'
KEY='66651C:3:0'
DRAFT='、\n밥 먹을 시간이거스!'
def validate_parent(a):
    p=ROOT/PARENT;require_hash(p,PARENT_SHA);old=json.loads(p.read_text(encoding='utf8'));validate_followup(old)
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=5):raise ValueError('meal parent identity')
    if [u for u in a['units'] if u['id']!=KEY]!=old['units'] or {u['id'] for u in a['units']}!={u['id'] for u in old['units']}|{KEY}:raise ValueError('meal inherited five units')
def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/66651C.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));prior={u['id']:u for u in old['units']}
    units=[prior[x.key] if x.key in prior else dict(id=x.key,source=x.text,translation=DRAFT,state='needs_review') for x in literals(t) if x.key in prior or x.key==KEY]
    a=dict(old,scope_variant='alarm-meal-v1',parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=5),units=units,context='PET native nickname meal3:0 plus five unchanged prior alarm literals. Event-name first pages and alternate mugshot scripts original.',protected_policy='Six selected literals;15 source literals/23 spans preserved. Nickname command/comma/newline and event/flag/sound/wait/window/RTC/save controls unchanged.')
    validate_parent(a);replace_literals(t,units);p=ROOT/CHILD
    if p.exists():raise ValueError('preserve meal asset')
    p.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8');print('One meal literal plus five read-only inherited units serialized')
if __name__=='__main__':main()
