"""Three confirmation literals; four source-pinned parent questions read-only."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals,skeleton
PARENT='translations/gutsman_calendar_content_ko.json'
PARENT_SHA='aad9306111de737da84a8f5ff7c1cd730bea5fc4db130c8d83f46064b88c8d43'
CHILD='translations/gutsman_calendar_confirmation_ko.json'
TPL_SHA='17f59df298ea973d4da8e1958eb42aa552104717c8922990c56dfd3621203a2e'
NEW={'665698:24:0':'이렇게 하면 되거스?\n\n','665698:24:1':'예  ','665698:24:2':'아니오'}
def validate_parent(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'))
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=4):raise ValueError('confirmation parent identity')
    if a['units'][:4]!=old['units'] or len(a['units'])!=7 or {u['id'] for u in a['units']}!={u['id'] for u in old['units']}|set(NEW):raise ValueError('confirmation inherited four units')
    p=ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');source={x.key:x.text for x in literals(t)}
    for u in a['units']:
        if u['source']!=source[u['id']] or u['state']!='needs_review' or u['source'].count('\n')!=u['translation'].count('\n'):raise ValueError('confirmation source/state/rows')
        if u['id'] in NEW and u['translation']!=NEW[u['id']]:raise ValueError('confirmation selected draft identity')
    if not a['units'][-2]['translation'].endswith('  ') or a['units'][-2]['translation'].endswith('   '):raise ValueError('confirmation Yes exact two-space padding')
    if skeleton(t)!=skeleton(replace_literals(t,a['units'])):raise ValueError('confirmation controls drift')
