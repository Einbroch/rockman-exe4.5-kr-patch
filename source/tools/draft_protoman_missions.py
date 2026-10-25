"""Individually authored mission253; immutable source and draft-only output."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/6DE3E0.tpl'
SOURCE_SHA='5528d21f924cdc5bf3f35ed3e42432648a08817879b5aada1317d006e2072f8c'
OUT='translations/protoman_missions_draft_ko.json'
# Explicitly authored per source entry, not rule-based prose substitution.
DRAFT={
27:['뭘 하고 있는 건가!','평소의 자네답지 않군\n잠시 머리를\n식히도록 하게','물론, 보상은\n없네!!'],
28:['잘해 주었네!','자네라면 신속하게\n임무를 완수해\n줄 거라 생각했네','보상 데이터를\n첨부했으니,\n받아 주게',',\n「','」\n획득!!'],
29:[',\n「','제니」\n획득!!'],
30:[',\n「버그 조각」\n총 ','개 획득!!'],
31:['다음에도 부탁하네!'],
33:['지령이다...','인터넷1에서\n바이러스가 날뛰고 있다','60분 안에 바이러스를\n삭제해 주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
34:['지령이다...','인터넷2에서\n바이러스가 날뛰고 있다','60분 안에 바이러스를\n삭제해 주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
35:['지령이다...','연쇄 절도 사건의\n범인 내비가','인터넷3으로\n도망친 것 같군','40분 안에\n현장으로 가서,\n상황을 확인해 주게','범인은 초록색\n노멀 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
36:['지령이다...','오피셜 파출소에서\n도망친 강도 내비가','인터넷4에\n숨어 있는 것 같군','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인의 특징은\n검은 여성형 내비라는군','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
37:['지령이다...','연쇄 방화 사건의\n범인 내비가','인터넷1에\n숨어 있는 것 같군','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인은,\n초록색 노멀 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
38:['지령이다...','폭행 사건의\n범인이','인터넷2에\n나타났다는 신고가\n근처 내비에게서 왔네','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인은 보라색\n노멀 타입 내비다','미안하지만 정보는\n이것뿐이네','이제 자네의 감만\n믿을 수밖에 없네!!','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
39:['지령이다...','무차별 습격 사건의\n범인을','인터넷3에서\n목격했다는\n정보가 들어왔네','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인은 초록색\n노멀 타입 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
40:['지령이다...','지명 수배 중인\n은행 강도 일당의\n1명이','인터넷4에\n와 있다고 하네','즉시 현장으로 가서,\n30분 안에\n삭제해 주게','범인은 보라색의\n험상궂게 생긴 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
41:['지령이다...','인터넷5에서\n바이러스가 날뛰고 있다','50분 안에 바이러스를\n삭제해 주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
42:['지령이다...','인터넷6에서\n바이러스가 날뛰고 있다','50분 안에 바이러스를\n삭제해 주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
43:['지령이다...','항공기 납치 사건의\n범인 일당 중 1명이','인터넷7에서\n목격되었네','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인은 초록색\n노멀 타입 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
44:['지령이다...','불량배 내비가\n인터넷8에서\n날뛰는 것 같군','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인은 보라색\n노멀 타입 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
45:['지령이다...','버스 납치범\n일당 중 1명이','인터넷5에서\n목격되었네!','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인은 초록색\n노멀 내비다','이제 자네의 감만\n믿을 수밖에 없네...','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
46:['지령이다...','가짜 다크 칩을\n밀매하는 자가','인터넷6에서\n장사를\n하고 있는 것 같군','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인은 초록색\n노멀 타입 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
47:['지령이다...','계속 바이러스를 만드는\n크래커 내비가','인터넷7에\n있는 것 같군','30분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','범인은 노란색\n여자아이형 내비지만,','엄연히 남자다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
48:['지령이다...','어느 범죄 조직의\n간부급 내비가','인터넷8에\n있는 것 같군','30분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','그 간부급 내비는,\n상당히 험상궂게 생긴\n내비라고 하네','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
49:['지령이다...','인터넷9에서\n바이러스가 날뛰고 있다','50분 안에 바이러스를\n삭제해 주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
50:['지령이다...','인터넷10에서\n바이러스가 날뛰고 있다','40분 안에 바이러스를\n삭제해 주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
51:['지령이다...','넷 교도소에서\n탈옥한 여성 내비가','인터넷11에서\n발견되었네','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','목표 내비는\n검은 여성형\n내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
52:['지령이다...','다크 칩 신디케이트를\n자칭하는 내비가\n인터넷12에 있다','40분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','목표는 초록색\n노멀 타입 내비다','오피셜을\n얕보면 어떻게 되는지\n가르쳐 주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
53:['지령이다...','폭주족\n「바리바리본」의\n멤버가 소유한 내비가','인터넷9에\n있다는 정보가\n들어왔네','「바리바리본」에게\n오피셜 내비 몇 대가\n삭제당했네','40분 안에\n현장으로 가서,\n불심 검문을 해 주게','상황에 따라서는,\n삭제해도 좋네','목표는 초록색\n노멀 타입 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
54:['지령이다...','인터넷10에서\n내비가 폭주한다는\n신고가 들어왔네','30분 안에\n현장으로 가서,\n상황을 확인해 주게','상황에 따라서는,\n삭제해도 좋네','폭주하는 것은,\n검고 눈매가 날카로운\n악당처럼 생긴 내비다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
55:['지령이다...','그림자 군단을 자칭하는\n수수께끼 집단의 1명이','오피셜에게\n도전장을\n내밀었다고 하네','인터넷11에\n있다고 하니,','30분 안에\n처리해 주게','너무 소란스럽게 굴면\n삭제해도 좋네','그림자 군단의 내비는\n딱 봐도 험상궂게 생긴\n녀석이라고 하네','가서 혼쭐을 내\n주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
56:['지령이다...','언더인터넷에서\n온 것으로 보이는\n내비가,','인터넷12에\n있는 것 같군...','자네라면, 20분이면\n충분하겠지','잠시 상황을 살펴보고\n경우에 따라서는,\n삭제해도 좋네','목표 내비는,\n힐 내비다','자네의 뛰어난 감으로\n찾아내 주게!!','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
57:['지령이다...','과학성에서 연구하던\n바이러스가,','언더인터넷1로\n유출되고 말았네','바이러스에는 과학성의\n극비 데이터가\n들어 있네','범죄자의 손에\n넘어가기 전에\n삭제해 주게','제한 시간은 40분이다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
58:['지령이다...','해외의 프로그램 마니아가\n개발한 바이러스가,','언더인터넷2로\n보내진 것 같군','무슨 일이 날지 모르니\n골치 아픈 일이 되기 전에\n삭제해 주게','제한 시간은 40분이다','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
59:['지령이다...','언더인터넷에서\n빠져나오려 하는\n범죄자 내비가 있다','현재, 그 내비는\n언더인터넷3에\n잠복 중이라고 하네','언더의 주민을\n일반 인터넷에 나오게\n할 수는 없지','40분 안에\n계획을 저지해 주게','아마 격렬한\n전투가 될 걸세','각오해 두게','목표 내비는,\n일반인으로 위장하려고','빨간 노멀 타입의\n모습을 하고 있다고 하네','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
60:['지령이다...','일반 인터넷에\n공격을 가하려고\n계획 중인 내비가','언더인터넷4에\n숨어 있는 것 같군','40분 안에\n체포하거나 삭제해\n주게','목표 내비는,\n일반인으로 위장하려고','초록색\n노멀 타입의 모습을\n하고 있다고 하네','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
61:['지령이다...','언더인터넷1에\nWWW(월드 스리)를\n자칭하는 내비가 있다네','노란 여성형\n노멀 내비인 것 같지만\n결코 방심할 수는 없네','20분 안에\n체포하거나 삭제해\n주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
62:['지령이다...','언더인터넷2에\n고스펠을 자칭하는 내비가\n있는 것 같군...','악당처럼 생긴 검은\n내비라고 하네','무슨 짓을 할지\n모르겠군','20분 안에\n체포하거나 삭제해\n주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
63:['지령이다...','언더인터넷3에\n네오 WWW\n(월드 스리)를 자칭하는','내비가 있는 것 같군','그 내비의 특징은\n악당처럼 생겼다는 걸세','20분 안에\n체포하거나 삭제해\n주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
64:['지령이다...','바이러스 제조\n집단의 1명이','언더인터넷4에\n와 있는 것 같군','상당히 눈매가 험한\n내비라고 하네...','20분 안에\n체포하거나 삭제해\n주게','성공 보상은\n나중에 보낼 메일에\n첨부하겠네','성공을 빌겠네!'],
65:['이 임무는\n이미 종료되었네']
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA)
    original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    if not all(s in original for s in ('mugshot = SciLabMan','callProtoManMissionBegin','checkProtoManMission','jumpIfMission1 = 33','jumpIfMission32 = 64','jumpIfNone = 65','checkProtoManMissionReward','mugshotHide')):raise ValueError('mission context changed')
    values={f'6DE3E0:{s}:{i}':t for s,rows in DRAFT.items() for i,t in enumerate(rows)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=253 or set(values)!={x.key for x in selected}:raise ValueError('mission253 scope '+str(set(values)^{x.key for x in selected}))
    units=[]
    for x in selected:
        script=int(x.key.split(':')[1]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('source row topology '+x.key)
        if re.findall(r'\d+|\[[^\]]+\]',t)!=re.findall(r'\d+|\[[^\]]+\]',x.text):raise ValueError('source numbers/tokens '+x.key)
        speaker='system-reward' if script in (29,30) or (script==28 and int(x.key.split(':')[2])>=3) else 'SciLabMan'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,context='Native ProtoMan mission begin/check32 branches, success/failure and reward; speaker inherited from SciLabMan root0/27/28, hidden portrait reward fragments distinguished',variable_context='printCurrentNavi/printItem/printBuffer preserved; invariant comma and acquisition noun avoid name-dependent Korean particles; full consumer/layout runtime review pending'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x6DE3E0)
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6DE3E0',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue',context='All253 Japanese literals in66-slot mission archive; 32 native mission dispatch targets33..64 plus ended65 and outcome27..31. Exact commands retained, no mission execution or reward mutation.',voice='SciLabMan commanding conversational register drawn from source; narration distinct from portrait dialogue. Existing 내비/오피셜/제니/버그 조각 vocabulary reused as candidates.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve all source IDs, time limits, numbered destinations, criminal appearance, conditional delete/arrest instructions, amounts/mission state commands and newline topology. No ROM or save writes.',semantic_review=['언더인터넷/과학성/바리바리본/그림자 군단/월드 스리 and organization names are source-backed draft candidates, not new human approvals.', 'Mission47 retains source distinction between female-type appearance and male identity; mission36/51 black female-type, mission61 yellow female-type, mission59 red disguise and mission60 green disguise remain distinct.', 'Mandatory delete40 vs optional delete others and arrest-or-delete60..64 are not conflated. Times and numbered destinations mechanically checked.', 'Reward comma phrasing avoids variable-final-consonant dependence; real variable width, reward lookups and all mission runtime branches unverified.'],units=units)

def main():
    a=create();path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored mission253 draft only; ROM unchanged')

if __name__=='__main__':main()
