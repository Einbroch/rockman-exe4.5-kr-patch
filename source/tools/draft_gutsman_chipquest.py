"""Two authored literals plus read-only, hash-checked projection of prior31."""
import copy,json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from gutsman_chipquest_model import FIRST,LAST,PARENT_SHA,validate_parent
from draft_gutsman_pet_talk import TPL_SHA

def main():
    p=ROOT/'translations/gutsman_pet_talk_ko.json';require_hash(p,PARENT_SHA);parent=json.loads(p.read_text(encoding='utf8'));tpl=ROOT/'analysis/full_scope_v1/source_tpl/66A844.tpl';require_hash(tpl,TPL_SHA);items=literals(tpl.read_text(encoding='utf-8-sig'));old={u['id']:u for u in parent['units']};new={f'66A844:13:{i}':text for i,text in enumerate([FIRST,LAST])}
    if len(items)!=33 or set(old)|set(new)!={x.key for x in items}:raise ValueError('complete literal33 projection')
    a=copy.deepcopy(parent);a['units']=[copy.deepcopy(old[x.key]) if x.key in old else dict(id=x.key,source=x.text,translation=new[x.key],state='needs_review') for x in items]
    a.update(scope_variant='gutsman-chipquest-v1',parent_asset=dict(path='translations/gutsman_pet_talk_ko.json',sha256=PARENT_SHA,carry_units=31),context='All33 Guts R literals; two added chip104 literals. Derived31 units remain parent-owned and byte-for-byte unchanged. Native printChip0/104/keyWait/clear/waitHold preserved. Korean chip name reuses existing draft wording without counting it again.',protected_policy='Source/control/numeral/nickname anchors and230 unselected spans preserved. Three-row chip page budgets include native88px and Korean47px variable name.')
    validate_parent(a);replace_literals(tpl.read_text(encoding='utf-8-sig'),a['units']);out=ROOT/'translations/gutsman_pet_chipquest_ko.json'
    if out.exists():raise ValueError('preserve translation evidence')
    out.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8');print('Guts complete33 literals: prior31 unchanged +2 chip drafts')

if __name__=='__main__':main()
