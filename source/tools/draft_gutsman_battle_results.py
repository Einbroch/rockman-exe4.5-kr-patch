"""Manually authored GutsMan PET defeat/victory/draw prose; no batch rule."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
TPL_SHA='7ec86c57444a12203d07ad7b5ce6ca2e305d7318b83fd810c049316a3af1df0f'
PAYLOAD_SHA='753a10f34b5f83d27f12a67eed539c95344366e0caad8dbcd31f1915d846a115'
DRAFT={'66A7A8:1:0':'저、졌거스・・・\n충격이거스~','66A7A8:2:0':'거츠、거츠!\n이게 거츠맨의\n실력이거스!!','66A7A8:3:0':'비겼지만、\n멋진 승부였거스!'}
def main():
    c=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/c['source_profile']['filename'],c['source_profile']['sha256']);p=ROOT/'analysis/full_scope_v1/source_tpl/66A7A8.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');items=literals(t)
    if {x.key for x in items}!=set(DRAFT):raise ValueError('complete source population')
    u=[dict(id=x.key,source=x.text,translation=DRAFT[x.key],state='needs_review') for x in items];replace_literals(t,u);out=ROOT/'translations/gutsman_battle_results_ko.json'
    if out.exists():raise ValueError('preserve translation')
    a=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=c['source_profile']['sha256'],archive='66A7A8',source_archive_sha256=PAYLOAD_SHA,consumer='normal-dialogue',context='GutsMan own group result root038130/intro+32, defeat1/victory2/draw3; full source5slots/3literals. No variables. Native battle result prerequisites unverified.',voice='Existing 거츠/거스 development voice; human review pending.',semantic_review=['Defeat includes stammer and shock; victory proudly attributes strength to GutsMan; draw retains both tie and positive appraisal.','No NumberMan4649 decision reused. No independent release review or human approval inferred.'],review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='Stable source IDs/bytes/numerals/newline, PET window/text/arrow geometry and all keyWait/clearMsg/waitHold commands preserved. Empty slots0/4 source-identical.',units=u)
    out.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8');print('Guts battle results:3 complete translated literals')
if __name__=='__main__':main()
