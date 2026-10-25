"""Three manually authored, variable-free GutsMan PET alarm expressions."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
TPL_SHA='8286cb9ad04ff3ac3ec9f09570327fd24da70450943fd7f4e5209a19d6e1dce1'
PAYLOAD_SHA='16cd2ff2d4af233f94277cb9077169046a4abe04f4789c735e77495697f18852'
DRAFT={'66651C:4:0':'학원 갈\n시간이거스!!','66651C:4:1':'공부、공부!\n힘내는거츠!!','66651C:6:0':'그리고・・・'}
def main():
    c=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/c['source_profile']['filename'],c['source_profile']['sha256']);p=ROOT/'analysis/full_scope_v1/source_tpl/66651C.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');items=literals(t)
    if len(items)!=21:raise ValueError('source population')
    u=[dict(id=x.key,source=x.text,translation=DRAFT[x.key],state='needs_review') for x in items if x.key in DRAFT]
    if len(u)!=3:raise ValueError('selected population')
    replace_literals(t,u);out=ROOT/'translations/gutsman_schedule_alarm_ko.json'
    if out.exists():raise ValueError('preserve translation')
    a=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=c['source_profile']['sha256'],archive='66651C',source_archive_sha256=PAYLOAD_SHA,consumer='normal-dialogue',context='PET school alarm script4 two pages and additional-event script6 only; root038124. Not alternate mugshot24/26. Script6 diagnostic stops before event dispatch.',voice='Existing 거츠/거스 speech; human wording review pending.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='21 source literals:3 selected/18 preserved. All controls, sounds, waits, event flags, window/arrow geometry, callCheckNowEvent/callFindNowEventType, buffers, 26 unselected script spans unchanged. No name/RTC/save mutation.',units=u)
    out.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8');print('Guts PET alarm:3 translated,18 preserved')
if __name__=='__main__':main()
