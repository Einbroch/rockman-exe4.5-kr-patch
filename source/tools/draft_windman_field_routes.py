"""Manual118 program/WindMan/ProtoMan field candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7BFE4C':('620dc7b9e561f5efc7a3aa4a9483f914b922a1ad4587f4e6bd1fef072884780d',2,'translations/chuckling_program_draft_ko.json'),
'7C0668':('a98ca9e73f2d60dc2aa74150e651e1545326732f1852cae2e5feb2d3c7cea219',10,'translations/windman_flying_program_draft_ko.json'),
'7C0F8C':('edf11d34b1b2274c04e6db071af44634953839431adc02c2f660dbeb7fd85092',106,'translations/protoman_field_encounters_draft_ko.json'),
}
# Script0 of7C0F8C is an unresolved provisional battle test, not selected.
DRAFT={
'7BFE4C':{0:['기시시...','니시시...']},
'7C0668':{
0:['핫!\n으랴!\n토랴아아!','하아...\n조금만 더 하면','저\n넓은 하늘로 날아오를 수\n있을 것 같은데요',',\n이 고민 많은 프로그램을\n도와주도록 하자','좋아  ','싫어','저, 정말인가요?\n꼭 부탁드립니다','푸슈우\n약한 이를 돕다니\n좋은 마음가짐이다','바람의 힘이 모이는\n인터넷1에서\n의식을 치르도록 하자'],
1:['푸슈우\n그렇다면 어쩔 수 없구나'],
},
'7C0F8C':{
1:['목표, 삭제...\n임무를 완수했습니다'],
2:['큭...\n임무, 실패입니다...','면목이... 없습니다'],
10:['목표 바이러스를\n발견!!','삭제하겠습니다'],
11:['목표 바이러스를\n발견!!','삭제하겠습니다'],
12:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','오, 오피셜!?','난 잡히지 않아!','삭제해 주마!\n으랴아아앗!'],
13:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','쳇! 오피셜이냐!\n귀찮은 녀석이 나타났네...','내 바이러스들아!\n저 오피셜을\n해치워 버려!!'],
14:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','너, 네놈, 오피셜이냐!','내, 내 즐거움을\n방해하게 둘까 보냐!!','으라라아!!'],
15:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','오피셜!?','난 잡히지 않아!!\n우호오오오!!'],
16:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','시, 시, 싫어어어!!\n체포되는 건 싫어!','와아아아아아아!!'],
17:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','웃기지 마!!','난 잡히지 않아!\n쿠오라아!!'],
18:['목표 바이러스를\n발견!!','삭제하겠습니다'],
19:['목표 바이러스를\n발견!!','삭제하겠습니다'],
20:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','쳇!!','에잇! 될 대로 돼라!!'],
21:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','오피셜이라고!?','시끄러워!\n이거나 받아라!'],
22:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','쳇!\n벌써 냄새를 맡고 왔나!','카앗!!'],
23:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','나, 난 아직\n잡힐 수는\n없어...','잡힐 수는 없어어어어!!'],
24:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','나, 난 아무 짓도\n안 했어...','...뭐야...','잡을 수 있으면,\n잡아 보라고!!','으랏!!'],
25:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','...알았다\n얌전히 붙잡혀 주지...','...라고 할 줄 알았냐!\n빈틈이다아아!!'],
26:['목표 바이러스를\n발견!!','삭제하겠습니다'],
27:['목표 바이러스를\n발견!!','삭제하겠습니다'],
28:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','오, 오피셜!?','시, 싫어...\n다시 그곳으로 돌아가기는\n싫어!!','그곳으로 돌아갈 바에는,\n삭제되는 편이 낫겠어!','키이잇!!!'],
29:['오피셜이다...','크크! 왔구나...\n겁도 없는 녀석이군!','너를 쓰러뜨려,\n내 강함을\n과시하겠어!!','쇼랴아아아!!'],
30:['오피셜이다...','내가 오피셜이라는\n이름 따위에 겁먹을 거라고\n생각했나!?','얕보지 마!!\n바리바리보오온!!'],
31:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','오, 오피셜...?','시, 시, 샤...\n샤라바라하라바아!!'],
32:['오피셜이다...','크크크... 왔군...','너희 오피셜을\n쓰러뜨리고,','우리 그림자 군단의\n무서움을 온 세상에\n보여 주겠어!!','쿄에에에에에엣!!'],
33:['오피셜이다...\n잠깐, 이야기를\n들려주겠나?','오피셜인가...','유감이지만, 날 언더로\n돌려보낼 수는 없을걸','왜냐하면, 넌 여기서\n나한테 삭제될 테니까!'],
34:['목표 바이러스를\n발견!!','삭제하겠습니다'],
35:['목표 바이러스를\n발견!!','삭제하겠습니다'],
36:['오피셜이다...','언더에서 한 발짝도\n밖으로 내보내지 않겠다!','흥!\n막을 수 있으면,\n막아 보시지!','키에에엣!!'],
37:['오피셜이다...','너희 계획은\n여기서 막아 보이겠다!!','구겍!!','하지만, 여기는 우리의\n구역... 오피셜이라도\n두려울 건 없다!!','우라샤아!!'],
38:['오피셜이다...','쳇!\n오피셜 녀석, 바이러스나\n먹어라!!'],
39:['네놈, 오피셜이구나!?','언더인터넷에\n제 발로 찾아오다니,','배짱이 있는 건지\n멍청한 건지...','하지만, 결말은\n똑같다... 사라져라!!'],
40:['움직이지 마라...\n오피셜이다...','...오피셜이\n...뭐 그리 대단하냐!!','삭제해 주마!!\n후가아!!'],
41:['오피셜이다...\n네놈에게 할 말이 있다','같이 가 줘야겠다','...시끄러워!!','너와 할 이야기 따위는\n...없다!!','혼가앗!!'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text) and not (archive=='7C0F8C' and x.key=='7C0F8C:0:0')]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('organ scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        choice=archive=='7C0668' and s==0 and i in (4,5)
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('organ topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('organ tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Chuckling program, flying-program request with WindMan and ProtoMan mission field exchanges. All local scripts including unresolved test read.',variable_context='7C0668:0:3 follows printPlayerNickname; comma avoids variable-final-consonant vocative. Portrait changes within scripts determine speaker. Commands untouched.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-mission-field',context='118 Japanese literals from3 archives.2 chuckles,10 flying-program request,106 mission field/results. Provisional7C0F8C:0:0 excluded from this draft, retained unresolved.',voice='Program polite, WindMan dignified, ProtoMan polite mission reporting but firm speech to suspects; each suspect rough/distinct. Candidates not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='WindMan flag4929/7701, nickname command, Internet1 and options; field scripts10..41 global15=513/flags5473/7701 and portrait boundaries intact. Test0 kept source.',semantic_review=['WindMan offers to help the program fly; ritual at Internet1 without invented duration/reward. Source nickname+よ drafted nickname+comma rather than an invariant Korean vocative particle.', 'ProtoMan reports mission completion/failure formally, questions suspects firmly. Source portraits, not repeated source text, assign later reactions. No actual arrest/reward/save effects inferred from dialogue.', 'Prior mission6DE3E0 terms 그림자 군단/바리바리본/언더인터넷 retained; ウラ shorthand drafted 언더 without inventing specific numbered destination.', '7C0F8C28 retains unnamed 그곳, not guessed prison name.25 feigned surrender then attack preserved; deletion threats not softened into ordinary loss.', '7BFE4C has only two chuckles; no appliance or mission identity guessed.7C0970:0:0 and7C0F8C:0:0 provisional minigame/battle-test consumers remain unresolved, never silently excluded from overall denominator.', 'Static protection only, no normal-play ritual/mission/encounter/results/nickname/save/screen verification. Voice, sound rendering and layout need review.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve organ draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
