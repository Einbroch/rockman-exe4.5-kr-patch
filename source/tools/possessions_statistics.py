"""Four fixed-cell possessions headings; immutable calendar parent12."""
import json
from build_visibility_poc import ROOT,require_hash
from calendar_frequency_names import validate as previous,replace as replace_previous
from tpl_literals import literals,serialize,skeleton

PARENT='translations/calendar_frequency_names_ko.json'
PARENT_SHA='9e599bbf61c68497a7b8eb37ee9d545db97278ca3c33124e7ef12c213526a924'
CHILD='translations/possessions_statistics_ko.json'
LABELS=('컵','크레딧','버그 조각','대전 전적')
ADDED=dict(id='6368E8:80:0',source='カップ             クレジット           バグのかけら          たいせんせいせき        ',translation=''.join(x.ljust(16) for x in LABELS),state='needs_review')

def validate(a):
    require_hash(ROOT/PARENT,PARENT_SHA)
    old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));previous(old)
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=12) or a['units'][:12]!=old['units'] or a['units'][12:]!=[ADDED] or len(a['units'])!=13:
        raise ValueError('statistics immutable parent12/source projection')
    source={x.key:x.text for x in literals((ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig'))}
    if source[ADDED['id']]!=ADDED['source'] or len(ADDED['source'])!=64 or len(ADDED['translation'])!=64:
        raise ValueError('statistics source/cell64')
    for i,label in enumerate(LABELS):
        row=ADDED['translation'][i*16:(i+1)*16]
        if len(label)>10 or row!=label.ljust(16) or row[10:]!=' '*6:
            raise ValueError('statistics four rows16 / visible10 / protected padding6')
    return old

def replace(original,units):
    a=dict(parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=12),units=units)
    old=validate(a);target=replace_previous(original,old['units'])
    xs=[x for x in literals(target) if x.key==ADDED['id']]
    if len(xs)!=1 or xs[0].text!=ADDED['source'] or xs[0].language!='mmbn45s':
        raise ValueError('statistics literal identity')
    x=xs[0];target=target[:x.start]+serialize(ADDED['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('statistics controls')
    return target

def prepare():
    """Serialize authored ADDED above, copying parent12 without prose changes."""
    require_hash(ROOT/PARENT,PARENT_SHA);a=json.loads((ROOT/PARENT).read_text(encoding='utf8'))
    a.update(scope_variant='possessions-statistics-v1',parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=12),
        context='Possessions statistics upper BG2 box: four16-cell rows, first10 visible at32,24; preserve counters in scripts81/82 and Z unit.',
        evidence='poc/runtime/keyitem-empty-v1-empty-close/step_002_fixedcells.json',
        decision_evidence='Development UI draft: cup, credit, bug fragments, battle record. Human wording review pending.',
        insertion_state='development input; explicit --possessions-statistics',
        protected_policy='Parent12 immutable; four16-cell rows and six hidden spaces per row; E5 terminator, scripts81/82 and all counter/unit values unchanged. Cell count64 is supplied by caller, not a script prefix.')
    a['units']=a['units']+[ADDED];validate(a)
    p=ROOT/CHILD
    if p.exists():raise ValueError('preserve existing statistics asset')
    p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
if __name__=='__main__':prepare()
