"""Two content/person questions; two source-pinned parent questions read-only."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals,skeleton
PARENT='translations/gutsman_calendar_prompts_ko.json'
PARENT_SHA='58ccc8ac8c45883f13c47ee7dd389df8c05568a7c3bcad202ea452daa537b5ec'
CHILD='translations/gutsman_calendar_content_ko.json'
TPL_SHA='17f59df298ea973d4da8e1958eb42aa552104717c8922990c56dfd3621203a2e'
NEW={'665698:22:0':'어떤 내용이거스?','665698:23:0':'누구와 약속이거스?'}
def validate_parent(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'))
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=2):raise ValueError('calendar parent identity')
    if [u for u in a['units'] if u['id'] not in NEW]!=old['units'] or len(a['units'])!=4 or {u['id'] for u in a['units']}!={u['id'] for u in old['units']}|set(NEW):raise ValueError('calendar inherited two units')
    p=ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');ls={x.key:x for x in literals(t)}
    for u in a['units']:
        if u['source']!=ls[u['id']].text or u['state']!='needs_review' or '\n' in u['translation']:raise ValueError('calendar question source/state/row')
        if u['id'] in NEW and u['translation']!=NEW[u['id']]:raise ValueError('calendar selected draft identity')
    if skeleton(t)!=skeleton(replace_literals(t,a['units'])):raise ValueError('calendar controls drift')
