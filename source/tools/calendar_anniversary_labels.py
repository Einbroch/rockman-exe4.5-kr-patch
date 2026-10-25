"""Three fixed 16-cell anniversary labels layered on the preset asset."""
import json
from build_visibility_poc import ROOT,require_hash
from calendar_presets import validate as validate_presets,replace as replace_presets
from tpl_literals import literals,serialize,skeleton
PARENT='translations/calendar_presets_ko.json';PARENT_SHA='f05540b579175a7f18a555b142ff3997935d4e27b55154ac2af613d4826242af';CHILD='translations/calendar_anniversary_labels_ko.json';TPL_SHA='a35f1a707f8ecf9e4556c31f6ef7f080afcc449fc2cec169d87ddae254c929c7';KEY='6368E8:73:0';SOURCE='自分のたんじょう日       そうりつきねん日        そのた             ';LABELS=('내 생일','개교기념일','기타')
def validate_parent(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'))
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=4) or a['units'][:4]!=old['units'] or len(a['units'])!=5:raise ValueError('anniversary labels parent')
    validate_presets(a['units'][:4]);u=a['units'][-1];text=u['translation']
    if u['id']!=KEY or u['source']!=SOURCE or u['state']!='needs_review' or len(text)!=48 or '\n' in text:raise ValueError('anniversary labels source/extent')
    for i,label in enumerate(LABELS):
        if text[i*16:(i+1)*16]!=label.ljust(16):raise ValueError('anniversary 16-cell segment/padding')
def replace(original,units):
    a={'parent_asset':dict(path=PARENT,sha256=PARENT_SHA,carry_units=4),'units':units};validate_parent(a);target=replace_presets(original,units[:4]);u=units[-1];xs=[x for x in literals(target) if x.key==KEY]
    if len(xs)!=1 or xs[0].text!=SOURCE or xs[0].language!='mmbn45s':raise ValueError('anniversary label literal')
    x=xs[0];result=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(result):raise ValueError('anniversary label controls')
    return result
