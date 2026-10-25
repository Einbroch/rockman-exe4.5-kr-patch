"""Finite GutsMan calendar management; immutable parent and source controls."""
import json
from build_visibility_poc import ROOT,require_hash
from gutsman_calendar_navigation import validate as validate_previous
from tpl_literals import literals
PARENT='translations/gutsman_calendar_navigation_ko.json'
CHILD='translations/gutsman_calendar_management_ko.json'
PARENT_SHA='e06fdbba9ed5690c5d5dade841bcfeb966ff20768c6ca36a09a7398d67ab9d62'
DRAFT='analysis/gutsman_calendar_navigation_v1/next_calendar_drafts.json'
DRAFT_SHA='71bc413ac9de61ef3028b504cac7ade1556d0d18f18e49da9e9eb912c70a3926'
DELETION=[{"id":"665698:52:3","source":"」\nを さくじょするでガス!","translation":"」\n삭제하겠거스!","state":"needs_review"},{"id":"665698:52:4","source":"だいじょうぶでガス?\n\n","translation":"괜찮거스?\n\n","state":"needs_review"},{"id":"665698:52:5","source":"はい  ","translation":"예  ","state":"needs_review"},{"id":"665698:52:6","source":"いいえ","translation":"아니오","state":"needs_review"}]
CHANGED={3,4,5,8,30,32,40,41,42,43,44,45,52}
def validate(a):
    require_hash(ROOT/PARENT,PARENT_SHA);require_hash(ROOT/DRAFT,DRAFT_SHA)
    old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));validate_previous(old)
    draft=json.loads((ROOT/DRAFT).read_text(encoding='utf8'))
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=22) or a['units'][:22]!=old['units'] or a['units'][22:]!=draft['units']+DELETION or len(a['units'])!=45:raise ValueError('calendar management parent/draft projection')
    source={x.key:x.text for x in literals((ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig'))}
    for u in a['units'][22:]:
        if source[u['id']]!=u['source'] or u['state']!='needs_review' or u['source'].count('\n')!=u['translation'].count('\n'):raise ValueError('calendar management source/state/rows')
    tail=next(u for u in a['units'] if u['id']=='665698:52:3')
    if tail['source'].split('\n')[0]!=tail['translation'].split('\n')[0] or tail['translation'].split('\n')[0]!='」':raise ValueError('anniversary dynamic-name closing quote grew')
    return old
