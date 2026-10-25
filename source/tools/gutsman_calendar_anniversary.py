"""One anniversary prompt; fourteen source-pinned parent units read-only."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals,skeleton
PARENT='translations/gutsman_calendar_register_ko.json';PARENT_SHA='69149e7c165163397725c1a7543924eea8bc0d2b3c8e17a7cc6cf211768d319a';CHILD='translations/gutsman_calendar_anniversary_ko.json';TPL_SHA='17f59df298ea973d4da8e1958eb42aa552104717c8922990c56dfd3621203a2e';NEW={'665698:31:0':'어떤 기념일이거스?\n'}
def validate_parent(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'))
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=14) or a['units'][:14]!=old['units'] or len(a['units'])!=15:raise ValueError('anniversary dialogue parent')
    p=ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');source={x.key:x.text for x in literals(t)}
    for u in a['units']:
        if u['source']!=source[u['id']] or u['state']!='needs_review' or u['source'].count('\n')!=u['translation'].count('\n'):raise ValueError('anniversary dialogue source/state/rows')
    if a['units'][-1]['translation']!=NEW['665698:31:0'] or skeleton(t)!=skeleton(replace_literals(t,a['units'])):raise ValueError('anniversary dialogue wording/controls')
