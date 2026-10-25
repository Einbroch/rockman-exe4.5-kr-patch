"""Finite schedule conflict/delete extension; source and parent fail closed."""
import json,re
from build_visibility_poc import ROOT,require_hash
from gutsman_calendar_management import validate as previous
from tpl_literals import literals
PARENT='translations/gutsman_calendar_management_ko.json'
CHILD='translations/gutsman_calendar_schedule_delete_ko.json'
PARENT_SHA='566b28916af87697dbbf697a740cdb202fbdb33c64c342050357052533852b6d'
ADDED=[{"id":"665698:25:0","source":"、\nおなじ時間に べつのよていが\nあるでガス!","translation":"、\n같은 시간에 다른 일정이\n있거스!","state":"needs_review"},{"id":"665698:50:5","source":"」\nを さくじょするでガス!","translation":"」\n삭제하겠거스!","state":"needs_review"},{"id":"665698:50:6","source":"だいじょうぶでガス?\n\n","translation":"괜찮거스?\n\n","state":"needs_review"},{"id":"665698:50:7","source":"はい  ","translation":"예  ","state":"needs_review"},{"id":"665698:50:8","source":"いいえ","translation":"아니오","state":"needs_review"},{"id":"665698:51:6","source":"」\nを さくじょするでガス!","translation":"」\n삭제하겠거스!","state":"needs_review"},{"id":"665698:51:7","source":"だいじょうぶでガス?\n\n","translation":"괜찮거스?\n\n","state":"needs_review"},{"id":"665698:51:8","source":"はい  ","translation":"예  ","state":"needs_review"},{"id":"665698:51:9","source":"いいえ","translation":"아니오","state":"needs_review"}]
CHANGED={25,50,51}
def validate(a):
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));previous(old)
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=45) or a['units'][:45]!=old['units'] or a['units'][45:]!=ADDED or len(a['units'])!=54:raise ValueError('schedule deletion parent/new projection')
    source={x.key:x.text for x in literals((ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig'))}
    for u in ADDED:
        if source[u['id']]!=u['source'] or u['source'].count('\n')!=u['translation'].count('\n') or u['state']!='needs_review':raise ValueError('schedule deletion source/control/state')
        if u['source'].split('\n')[0] in ('、','」') and u['source'].split('\n')[0]!=u['translation'].split('\n')[0]:raise ValueError('dynamic name/nickname first line grew')
    return old
