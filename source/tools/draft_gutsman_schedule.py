"""Authored six schedule expressions and six retained punctuation literals."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals
TPL_SHA='2f11d47888bf9857742cf94aa049c347dea49595302b2ddafed1c8affb9a5c64'
PAYLOAD_SHA='2facebf606327d4cf9df68310b945d90285de9b168999aef17c3697dd5ff4464'
DRAFT={1:['그러고 보니、곧'],2:['「','」'],3:['시간이거스!'],10:['오늘 등록된\n일정은・・・','아무것도 없거스!'],11:[':',' ','부터\n','「','」'],12:['이거스!']}
def main():
    c=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/c['source_profile']['filename'],c['source_profile']['sha256']);p=ROOT/'analysis/full_scope_v1/source_tpl/666F38.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');items=literals(t)
    if {x.key for x in items}!={f'666F38:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete literal population')
    u=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items];replace_literals(t,u);validate_literal_numerals(u,dict(preserve_literal_numerals=True));out=ROOT/'translations/gutsman_schedule_ko.json'
    if out.exists():raise ValueError('preserve translation')
    a=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=c['source_profile']['sha256'],archive='666F38',source_archive_sha256=PAYLOAD_SHA,consumer='normal-dialogue',context='GutsMan native group schedule root038134/intro+36. Upcoming1->2event loop->3; today10->11clock/name loop->12 or10 no-event. Complete14slots/12literals. Native variable commands unaffected.',voice='Existing 거츠/거스 development candidate; human wording review pending.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='Stable IDs/source/numerals/newline/all commands/hour/minutes/AMPM/event buffers/loops/keyWait/clear preserved. Six original quote/colon/space literals unchanged. Clock suffix source30px -> Korean24px, no growing dynamic prefix.',semantic_review=['12 closes the preceding event listing on a separate cleared page, not a new event.3 announces upcoming listed event time.','Dynamic event names and AMPM are original game supplies; this asset neither translates unknown name populations nor changes calendar values/RTC/save/input.','NumberMan4649 approval not reused.'],units=u);out.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8');print('Guts schedule12:6 translated/6 punctuation retained')
if __name__=='__main__':main()
