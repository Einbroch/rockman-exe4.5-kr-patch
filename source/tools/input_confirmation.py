"""Common name-entry confirmation; source-pinned controls and immutable parent13."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import replace_literals,skeleton
from possessions_statistics import validate as previous,replace as replace_previous
PARENT='translations/possessions_statistics_ko.json'
PARENT_SHA='26f9ca2c323390ba8ce7107baa7dde6bd634ea4b62d7684f103d0e8836448cb0'
CHILD='translations/input_confirmation_ko.json'
IDS={f'6368E8:10:{i}' for i in range(3)}
def validate(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));previous(old)
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=13) or a['units'][:13]!=old['units'] or len(a['units'])!=16 or {u['id'] for u in a['units'][13:]}!=IDS:raise ValueError('confirmation immutable parent13 / selected3')
    indexed={u['id']:u['translation'] for u in a['units'][13:]}
    def width(s):return sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in s)
    for i in [1,2]:
        if '\n' in indexed[f'6368E8:10:{i}'] or 8+width(indexed[f'6368E8:10:{i}'])>88:raise ValueError('confirmation native width8 horizontal option slot')
    if 16+width(indexed['6368E8:10:1'])+width(indexed['6368E8:10:2'])>88:raise ValueError('confirmation native width8 total choice group')
    prompt=indexed['6368E8:10:0']
    if not prompt.endswith('\n') or prompt.count('\n')!=1 or width(prompt[:-1])>184:raise ValueError('confirmation observed x52..236 prompt extent')
    return old
def replace(original,units):
    old=validate(dict(parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=13),units=units))
    target=replace_literals(replace_previous(original,old['units']),units[13:],language='mmbn45')
    if skeleton(original)!=skeleton(target):raise ValueError('confirmation control topology')
    return target
