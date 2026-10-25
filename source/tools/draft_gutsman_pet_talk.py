"""Individually authored 31 GutsMan progress prompts; chip104 script preserved."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
TPL_SHA='4793441d1f3ead084ccfa048476540e9ea24b0e31127d0615a59ad58ab0dbd67'
PAYLOAD_SHA='ab59357517b022252695e2b9785bf85a45fbab48e3444c5964d75e9c0d930795'
DRAFT={
10:['거츠、거츠!\n인터넷 이곳저곳을\n돌아다녀 보거스!'],
11:['거츠맨、\n견습 라이선스가\n갖고 싶거스!!'],
12:['、\n견습 라이선스 시험\n힘내는거츠!'],
14:['견습 라이선스를\n받으러 가거스!'],
15:['견습 라이선스 시험\n수고했거스!\n플러그아웃하거스?'],
16:['인터넷3에서\n일어난 사건이\n신경 쓰이는거스・・・'],
17:['방금 쓰러뜨린 내비가\n사건의 범인이었던\n것 같거스・・・','피곤하거스?\n한번 플러그아웃\n하겠거스?'],
18:['인터넷5에서\n일어난 사건이\n신경 쓰이는거스・・・'],
19:['인터넷7에서\n일어난 사건이\n신경 쓰이는거스・・・'],
20:['인터넷9에서\n일어난 사건이\n신경 쓰이는거스・・・'],
21:['인터넷10에서\n일어난 사건이\n신경 쓰이는거스・・・'],
22:['인터넷12에서\n일어난 사건이\n신경 쓰이는거스・・・'],
23:['블랙 워크스에게서\n「마이너스 키」를\n되찾겠거스!!'],
24:['「마이너스 키」는、\n다른 내비1체가\n가진 것 같거스!!'],
25:['「마이너스 키」를\n인터넷9에 있는','내비에게\n가져가거스!'],
26:['오피셜\n토너먼트의','참가 신청 장소에\n가거스!!'],
27:['우라인터넷으로\n가거스!','쓰러뜨릴 내비의\n표식은\n관이거스!'],
28:['거츠、거츠!!','오피셜\n토너먼트에 참가\n신청하러 가거스!!'],
29:['주말은 오피셜\n토너먼트거스!\n함께 힘내거스!!'],
30:['오피셜 토너먼트\n불타오르는거스!!'],
31:['、\n인터넷을','힘차게\n탐색하거스!!'],
32:['오피셜\n토너먼트 예선에\n참가하러 가거스!'],
33:['방금 도착한 메일을\n읽어 보거스!'],
34:['주가 바뀌면、\n오피셜\n토너먼트에','참가 신청하러\n가거스!']}
def main():
    c=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/c['source_profile']['filename'],c['source_profile']['sha256']);p=ROOT/'analysis/full_scope_v1/source_tpl/66A844.tpl';require_hash(p,TPL_SHA);t=p.read_text(encoding='utf-8-sig');items=literals(t);selected={f'66A844:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}
    if len(items)!=33 or {x.key for x in items if x.key.split(':')[1]!='13'}!=selected:raise ValueError('source31/33 population')
    u=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items if x.key in selected];replace_literals(t,u);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text())['archives']['66A844'];validate_literal_numerals(u,scope);validate_nickname_suffix(u,'66A844',scope);out=ROOT/'translations/gutsman_pet_talk_ko.json'
    if out.exists():raise ValueError('preserve translation')
    a=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=c['source_profile']['sha256'],archive='66A844',source_archive_sha256=PAYLOAD_SHA,consumer='normal-dialogue',context='Native GutsMan R root038148/intro+56.31 of33source literals: exploration/license/incident/key delivery/tournament/undernet/mail/weekday. Full chip104 script13 remains source Japanese pending own consumer. Player nickname commands12/31 preserved.',voice='Existing 거츠/거스 development candidate; shared terms match prior Roll candidates, not human approval.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='Stable source IDs/bytes/newlines/numerals, nickname first-line comma, branch order/flags/items/tournament/date/keyWait/clear/waitHold and231 unselected script spans preserved.',semantic_review=['25 two pages jointly direct carrying the key to the Navi in internet9; not taking a key from that Navi.','27 target Navi coffin sign retained; original weekday checks0/6 and weekday alternatives26/28/29/34 unchanged.','24 retains numeral1 for another Navi; 16/18/19/20/21/22 and25 retain area numbers.','17 preserves suspect attribution as seeming rather than certainty; 15/17 plugin-out questions kept as questions.','No NumberMan4649 human decision reused.'],units=u)
    out.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8');print('Guts R talk31 selected/33source;2 chip literals preserved')
if __name__=='__main__':main()
