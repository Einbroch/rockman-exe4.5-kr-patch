"""Two variable-free second pages; previous three units are read-only inputs."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from draft_gutsman_schedule_alarm import TPL_SHA,PAYLOAD_SHA
from tpl_literals import literals,replace_literals
PARENT_SHA='36eeaab87a9091d0c59e1df75d4d4bf1ab953a378f3b69b95fbe7c39f117b9a0'
PARENT='translations/gutsman_schedule_alarm_ko.json'
CHILD='translations/gutsman_alarm_followup_ko.json'
DRAFT={'66651C:1:1':'서두르지 않으면、\n오프닝을\n놓치겠거스!!','66651C:2:1':'거츠맨도\n기대되거츠!!'}

def validate_parent(asset):
    p=ROOT/PARENT;require_hash(p,PARENT_SHA)
    if asset.get('parent_asset')!={'path':PARENT,'sha256':PARENT_SHA,'carry_units':3}:raise ValueError('alarm parent identity')
    old=json.loads(p.read_text(encoding='utf8'))['units']
    if [u for u in asset['units'] if u['id'] not in DRAFT]!=old:raise ValueError('alarm three inherited units changed')
    if {u['id'] for u in asset['units']}!={u['id'] for u in old}|set(DRAFT):raise ValueError('alarm five-unit scope')

def main():
    c=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/c['source_profile']['filename'],c['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/66651C.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig')
    old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));prior={u['id']:u for u in old['units']}
    units=[prior[x.key] if x.key in prior else dict(id=x.key,source=x.text,translation=DRAFT[x.key],state='needs_review') for x in literals(t) if x.key in prior or x.key in DRAFT]
    a=dict(old,scope_variant='alarm-followup-v1',parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=3),units=units,
           context='PET TV/promise second pages1:1/2:1 plus unchanged prior4/6. Dynamic first pages and alternate mugshot scripts remain original.',
           protected_policy='Five selected literals;16 source literals/24 script spans preserved. All event buffer/nickname/control/sound/flag/RTC/save operations unchanged.')
    validate_parent(a);replace_literals(t,units);out=ROOT/CHILD
    if out.exists():raise ValueError('preserve existing alarm followup')
    out.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8');print('Alarm second pages2 plus inherited3 serialized')
if __name__=='__main__':main()
