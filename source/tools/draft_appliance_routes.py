"""Manual64 appliance/venue/battle/shop candidates; ROM untouched."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7B76D4':('3db5488632a59aa5a393ef03c61afb4eeb74296e66ddd0ed2865d665f0fca5a5',2,'translations/factory_panels_draft_ko.json'),
'7B7AF0':('19339182b6c04d28e0cdac9ece8a640a1dc73993be779d6a8ccb3ace95eca9c4',1,'translations/factory_passion_draft_ko.json'),
'7B7EF8':('cf8bd7fbada77692311716944f1330fe35b5d98533f69b2967e6c0bdc7ad05b2',1,'translations/factory_parts_draft_ko.json'),
'7B827C':('a72d3518a6e05bc84c4f8599878c14cee00cc5ff9eefe2e7d8624bc2185b24fa',22,'translations/appliance_battlers_draft_ko.json'),
'7B84C8':('76132ef25aae92fb24be4fcdee473bf216675fa6ac6a06949580c8acd0e465aa',19,'translations/toy_parts_shop_draft_ko.json'),
'7B8AB4':('5bf1041daf9c3fc10fad14ef6e9948e071bbc527d5d18a0e5ace7696830291fc',19,'translations/radio_venue_draft_ko.json'),
}
DRAFT={
'7B76D4':{0:['여기는 철판을\n만드는 공장의\n전뇌 세계입니다!','그래서 바닥이\n메탈 패널인 거예요']},
'7B7AF0':{0:['저희는\n철도 녹일 열정으로\n이 일을 하고 있습니다!']},
'7B7EF8':{0:['저희가 만든\n철판은, 배나 자동차의\n부품으로 쓰입니다!']},
'7B827C':{
0:['안녕하십니까!!','저, 배틀에 강해지고 싶어서\n수련 중임다!!','강해지려면, 실전이\n최고임다!!','저랑 배틀해 주십쇼','응  ','싫슴다','배틀해 주십쇼~!!'],
1:['배틀 시작하겠슴다!!','배틀 오퍼레이션, 세트!','인임다!!'],
2:['져, 졌슴다!!\n저, 더 단련하겠슴다!'],
3:['오늘은 위팔 두갈래근의\n상태가 좋슴다!!'],
4:['내 특별한\n바이러스들과 싸워 볼래?','뒷세계 바이러스 심사회에서\n심사위원 특별상을 받은\n자랑스러운 바이러스야!','배틀해 볼래?','응  ','싫슴다','젠장, 도망가 버렸네...'],
5:['가라! 내 바이러스야!','배틀 오퍼레이션, 세트!\n인!!'],
6:['아아~!\n내 바이러스가!!'],
7:['바이러스에게 최고의\n영양분은 내비의 에너지야!'],
},
'7B84C8':{
0:['장난감 부품은,\n꽤 자주 잃어버리죠?','로켓 펀치의 손 같은 거요','그런 걸 잃어버리지 않게\n관리하는 게, 제\n일입니다!'],
221:['다시 찾아와 주세요!'],
222:['아쉽지만,\n품절입니다...'],
223:['저는 넷 상인...\n좋은 물건 있어요?\n','보기  ','안 보기'],
224:['저는 넷 상인!\n오늘은 일주일에 한 번 있는\n레이디스 데이!!','여자분들께는 팍팍\n서비스해 드릴게요!','좋은 물건 있어요!?\n','보기  ','안 보기'],
225:['어서 오세요!\n저는 넷 상인!','당신, 운이 좋으시네요!\n오늘 저는\n기분이 최고거든요!','서비스해 드릴 테니,\n많이 사 가\n주세요!!','평소에는 볼 수 없는\n좋은 물건 있어요!?\n','보기  ','안 보기'],
},
'7B8AB4':{
0:['저는 라디오의\n소리를 내는 일을 해요','그런데, 제 동료인\n튜너 담당\n프로그램이 고장 나서,','곤란한 상황이에요...'],
1:['아파파파파...\n뀨우우웅 레레레레레...'],
10:['이 구역은,\n에브리데이 토너먼트\n대회장이야!!','자세한 건,\n저 토너먼트 게시판을\n정독할 것!'],
11:['에브리데이 토너먼트는\n매일매일 짜릿해!'],
12:['휘유~!!\n나도 배틀하고 싶어!!'],
13:['강한 내비는 정말\n멋있어!!','불타오르네!!'],
14:['에브리데이 토너먼트는\n스트레스 해소에\n딱이야!!','실컷 소리 지르면서,\n일하며 쌓인 울분을 풀겠어!!'],
15:['에브리! 에브리!\n에브리! 에브리!'],
16:['나도 언젠가는\n이 토너먼트에\n참가하겠어...','지금은 재충전하는 기간이지'],
17:['우승 축하해!\n또 참가해 줘!!'],
20:['축하합니다!!\n정말 멋진 배틀이었어!',' 선수,\n또 도전해 줘!!'],
21:['아쉬웠겠네~!\n또 도전해 줘!!'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('appliance scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown and not (archive=='7B84C8' and s==221):raise ValueError('actor missing '+x.key)
        portrait=shown[-1] if shown else 'NormalNaviYellow';visibility=('visible' if events[-1].group(1) else 'hidden') if events else 'inherited-from-caller'
        choice=(archive=='7B827C' and ((s==0 and i in (4,5)) or (s==4 and i in (3,4)))) or (archive=='7B84C8' and ((s==223 and i in (1,2)) or (s==224 and i in (3,4)) or (s==225 and i in (4,5))))
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('appliance topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('appliance tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Factory programs, trainee and virus owner, toy-parts administrator/merchant or radio programs/tournament spectators/results. Local branches read together.',variable_context='Radio20 printCurrentNavi suffix separate; toy shop221 inherits NormalNaviYellow from223/224/225. Source global/time/Navi/shop gates untouched.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-and-shop',context='All Japanese literals in source archive, complete local branches read;64 total across6 archives.',voice='Polite programs/merchant, clipped trainee 임다/슴다, virus owner informal, cheering spectators separated; candidates not approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Source/global7=2/global6=1 alternate-shop checks, weekday3/Navi1, shops3/13, battles180/181 and time/flag1877 preserved. No pricing or player-gender assumptions.',semantic_review=['Trainee ッス and choice いやッス have clipped-polite Korean candidates even in the different virus-owner scene. Do not assign choice prose to NPC portrait.', '上腕二頭筋 is rendered 위팔 두갈래근, not an invented stat or strength buff; boast and virus judges special-award remain speaker claims, not gameplay rewards.', 'Toy shop225 special stock is reached by global7=2 or global6=1 before weekday/Navi gates. The source does not name those globals or state an exact discount; retain uncertainty.', 'Radio tuner is a broken partner program; glitch onomatopoeia phonetic candidate remains review-needed. Charging period is rest/preparation, not an added energy-meter mechanic.', 'Factory iron-melting passion is figurative, metal-panel/source ship-car parts are retained. New panel/body-part terms, clipped voice and エブリー chant require human review.', 'Static checks do not prove battle, clock, purchases, special stock, radio sound, name redisplay, save or actual screens.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve appliance draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')

if __name__=='__main__':main()
