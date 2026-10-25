"""Five finite frequency names layered on immutable seven calendar units."""
import json
from build_visibility_poc import ROOT,require_hash
from calendar_anniversary_confirmation import validate as previous,replace as replace_previous
from tpl_literals import literals,serialize,skeleton
from korean_codec import encode_hangul
PARENT='translations/calendar_anniversary_presets_ko.json'
PARENT_SHA='0648d4550c74fd9a7308c74a042bbf9cc8ae4ee02016a0f9dc5bf97c55d4d451'
CHILD='translations/calendar_frequency_names_ko.json'
ADDED=[{"id":"6368E8:119:0","source":"1回のみ","translation":"1회만","state":"needs_review"},{"id":"6368E8:120:0","source":"毎日","translation":"매일","state":"needs_review"},{"id":"6368E8:121:0","source":"毎週","translation":"매주","state":"needs_review"},{"id":"6368E8:122:0","source":"毎月","translation":"매월","state":"needs_review"},{"id":"6368E8:123:0","source":"毎年","translation":"매년","state":"needs_review"}]
def raw(text):
    return b''.join(b'\x02'if c=='1'else encode_hangul(c)for c in text)+b'\xe5'
def validate(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));previous(old)
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=7) or a['units'][:7]!=old['units'] or a['units'][7:]!=ADDED or len(a['units'])!=12:raise ValueError('frequency parent/source projection')
    source={x.key:x.text for x in literals((ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig'))}
    for u in ADDED:
        b=raw(u['translation'])
        if source[u['id']]!=u['source'] or len(b)>32 or b'\xe5'in b[:-1] or '\n'in u['translation'] or u['state']!='needs_review':raise ValueError('frequency source/raw32/E5/rows')
    if ADDED[0]['translation'][0]!='1':raise ValueError('frequency once numeral')
    return old
def replace(original,units):
    a=dict(parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=7),units=units);old=validate(a);target=replace_previous(original,old)
    for u in units[7:]:
        xs=[x for x in literals(target)if x.key==u['id']]
        if len(xs)!=1 or xs[0].text!=u['source'] or xs[0].language!='mmbn45s':raise ValueError('frequency literal identity')
        x=xs[0];target=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('frequency controls')
    return target
