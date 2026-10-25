"""Native weak-subject entry heading; inherited confirmation16 unchanged."""
import json
from build_visibility_poc import ROOT,require_hash
from input_confirmation import validate as previous,replace as replace_previous
from tpl_literals import literals,serialize,skeleton
PARENT='translations/input_confirmation_ko.json'
PARENT_SHA='94272bf515ad3d177ef44a0bfffd5ddcd322165b3e9e4758ef4f778a797b6a17'
CHILD='translations/input_heading_ko.json'
ADDED=dict(id='6368E8:33:0',source='にがてな かもくは?',translation='어려운 과목은?',state='needs_review')

def validate(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));previous(old)
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=16) or a['units'][:16]!=old['units'] or a['units'][16:]!=[ADDED]:raise ValueError('heading immutable parent16 / selected33')
    source={x.key:x for x in literals((ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig'))}
    x=source[ADDED['id']]
    if x.text!=ADDED['source'] or x.language!='mmbn45s' or len(ADDED['translation'])>10 or '\n' in ADDED['translation']:raise ValueError('native heading ten visible mono cells')
    return old

def replace(original,units):
    old=validate(dict(parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=16),units=units))
    target=replace_previous(original,old['units']);x=next(x for x in literals(target) if x.key==ADDED['id'])
    if x.text!=ADDED['source'] or x.language!='mmbn45s':raise ValueError('heading source/language')
    target=target[:x.start]+serialize(ADDED['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('heading controls')
    return target

def prepare():
    require_hash(ROOT/PARENT,PARENT_SHA);a=json.loads((ROOT/PARENT).read_text(encoding='utf8'))
    a.update(scope_variant='input-heading-v1',parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=16),context='Common keyboard weak-subject heading33, native question29 then input initialization; neutral UI matching existing GutsMan 어려운 과목은. No input record/keyboard changes.',evidence='poc/runtime/input-entry-v1-header-source/step_003.png',decision_evidence='Manually authored UI draft; wording/presentation human review pending.',protected_policy='Inherited16 immutable; heading33 end and all other scripts unchanged. Native mono provider08619EF8, two tile rows / ten visible 8px columns; unchanged twenty-cell transfer.',insertion_state='development input; explicit --input-heading')
    a['units']=a['units']+[ADDED];validate(a);p=ROOT/CHILD
    if p.exists():raise ValueError('preserve existing asset')
    p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
if __name__=='__main__':prepare()
