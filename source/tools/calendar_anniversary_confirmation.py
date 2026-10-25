"""Source-pinned confirmation and two bounded anniversary preset names."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals,serialize,skeleton
from korean_codec import encode_hangul
from gutsman_calendar_anniversary import validate_parent as validate_dialogue_parent
from calendar_anniversary_labels import validate_parent as validate_labels_parent,replace as replace_labels
DIALOGUE='translations/gutsman_calendar_anniversary_confirmation_ko.json'
LABELS='translations/calendar_anniversary_presets_ko.json'
PARENTS={
    '665698':('translations/gutsman_calendar_anniversary_ko.json','9bed1f8d18dee9b5dbaa1e60a31097028f664a599652083bcf5330c63eadf8b1',15,validate_dialogue_parent),
    '6368E8':('translations/calendar_anniversary_labels_ko.json','68b7495815a8e69e1f2130115f0fe8d6a5d731a2d53817f30d14e3beca7f96a0',5,validate_labels_parent),
}
NEW={
    '665698':{'665698:33:0':('これでいいでガス?\n\n','이렇게 하면 되거스?\n\n'),'665698:33:1':('はい  ','예  '),'665698:33:2':('いいえ','아니오')},
    '6368E8':{'6368E8:74:0':('たんじょう日','생일'),'6368E8:75:0':('そうりつきねん日','개교기념일')},
}
def validate(a):
    arc=a['archive'];parent,digest,count,check=PARENTS[arc];require_hash(ROOT/parent,digest);old=json.loads((ROOT/parent).read_text(encoding='utf8'));check(old)
    if a.get('parent_asset')!=dict(path=parent,sha256=digest,carry_units=count) or a['units'][:count]!=old['units'] or len(a['units'])!=count+len(NEW[arc]):raise ValueError('anniversary confirmation parent projection')
    source={x.key:x.text for x in literals((ROOT/f'analysis/full_scope_v1/source_tpl/{arc}.tpl').read_text(encoding='utf-8-sig'))}
    for u in a['units'][count:]:
        if u['id'] not in NEW[arc] or (u['source'],u['translation'])!=NEW[arc][u['id']] or source[u['id']]!=u['source'] or u['state']!='needs_review':raise ValueError('anniversary confirmation source/wording/state')
        if arc=='6368E8':
            data=encode_hangul(u['translation'])+b'\xe5'
            if len(data)>22 or len(u['translation'])>10 or b'\xe5' in data[:-1]:raise ValueError('anniversary name raw-copy/record capacity')
    return old
def replace(original,a):
    old=validate(a)
    if a['archive']=='665698':return replace_literals(original,a['units'])
    target=replace_labels(original,old['units'])
    for u in a['units'][5:]:
        xs=[x for x in literals(target) if x.key==u['id']]
        if len(xs)!=1 or xs[0].text!=u['source'] or xs[0].language!='mmbn45s':raise ValueError('anniversary preset literal')
        x=xs[0];target=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('anniversary preset controls')
    return target
