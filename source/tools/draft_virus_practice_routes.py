"""Manual186 virus-practice and ShadowMan failure candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7C714C':('126a71d424d00c043fd7c388d15b23c2d6a0b55aa53c58ca0de46b681a697ae3',1,'translations/shadowman_failed_request_draft_ko.json'),
'7C7188':('c761f2413b3463cdce3e8ab171130fc08435d77719f1ca73318608d005b41a7f',130,'translations/virus_practice_intro_retry_draft_ko.json'),
'7C802C':('e7c685cf4a4bb710471ad400dbeb718d244015ce799f62a8efa8c3e3574c53e4',55,'translations/virus_practice_success_draft_ko.json'),
}
DRAFT={
'7C714C':{0:['이런 의뢰에서\n실패하다니...\n...분하다!!']},
'7C7188':{
0:['인터넷에 오는 건\n처음이지?','넷 배틀러의 기본,\n바이러스 버스팅을\n연습해 두자!','그럼, 간다!!'],
1:['있지, 바이러스 버스팅을\n어떻게 하는지 알아?','여기서부터는\n바이러스가 돌아다니니까,\n가볍게 연습해 두자!','그럼 시작할게!'],
2:['거츠 거츠!','근처에 바이러스의 기척이\n느껴진다, 가스!!','갑자기 습격당하면\n곤란하다, 가스...','여기서 연습하고\n가겠다, 가스!','시작한다, 가스!!'],
3:['그런데...','넷 배틀러라면,\n바이러스 버스팅은\n기본 중의 기본...','앞으로 수많은 싸움을\n헤쳐 나가게 될 것이네','우선 여기서 싸우는 법을\n익혀 두게나...','준비는 됐겠지,\n가겠네...'],
4:['...레이더에 다수의\n바이러스 확인...','작전을 더욱 확실히\n수행하기 위해,','바이러스 버스팅의\n방법을 확인해\n두도록 하죠...','...시작합니다!'],
5:['참, 그렇지...','난 아직 네\n배틀 실력을 몰라','그렇다고 해도, 너도\n나와 짝을 이루는 건 처음이지','인사 대신\n가볍게 바이러스 버스팅을\n연습해 둘까!','그럼, 시작한다!'],
6:['여기서부터는\n바이러스가 나타나는\n구역이다...','우선 바이러스 버스팅을\n연습해 두는 편이\n좋겠군...','시작한다...'],
7:['인터넷...\n사람들이 모이는\n즐거운 곳입니다','하지만, 그와 동시에,\n바이러스가 나타나는\n위험한 곳이기도 합니다','우선 바이러스 버스팅을\n연습해서,','위험에 대처할 수 있도록\n준비해 둡시다','그럼, 시작합니다!'],
8:['자, 인터넷에\n도착했네요...','우, 우선\n바이러스 버스팅을\n연습해 두죠','아무 준비도 없이\n인터넷을 돌아다니는 건\n불안하니까요...','그럼 시작할게요'],
9:['인터넷을 나아가기 전에\n바이러스 버스팅을\n연습해 두자','난 내\n주먹에 절대적인 자신이\n있지만,','네 오퍼레이팅에는\n아직 불안한 점이 있다','그 불안을 떨쳐 내려면\n연습하는 수밖에 없다','간다...'],
10:['여, 여기부터 바이러스가\n나타나게 된다...','내가 삭제되느냐\n살아남느냐는, 네\n오퍼레이팅에 달렸다...','한 번, 연습해\n두자...','시, 시작한다...'],
11:['퓨퓨!','여기저기에 바이러스가\n있어, 퓨...','바이러스한테 갑자기\n습격당하면 무서우니까, 퓨','여기서 연습하고\n가자, 퓨!','자, 시작하자, 퓨!'],
12:['오, 그렇지...','인터넷을 돌아다니기 전에,\n바이러스 버스팅을\n연습해 두자','앞으로 어떤 위험이\n기다릴지 모르니까','시작한다...'],
13:['그러고 보니,\n바이러스 버스팅을\n어떻게 하는지 알아?','아무튼, 여기서 연습하고\n가자','앞으로는 바이러스가\n자주 나타나니까','그럼, 간다!'],
14:['느껴지는군...\n바이러스들의 살기가...','그대, 바이러스 버스팅은\n알고 있겠지...','아무튼, 나와 행동을\n함께하려면,','최소한의 기본은\n배워 두어야겠지...','수련을 시작한다'],
15:['인터넷에\n오게 됐습니다만,','바이러스 버스팅은\n알고 계시겠지요?','인터넷을\n나아가려면, 반드시\n필요한 것이지요','바이러스 버스팅을\n연습해 둡시다','자, 솜씨를 보겠습니다!!'],
16:['그러고 보니,\n너 바이러스 버스팅은\n할 줄 알겠지?','기본적으로는,\n나한테 맡겨 두면 되지만,','꼭 필요한 최소한의 것은\n익혀 둬야지','일단, 연습이다\n간다, 으랴아!!'],
17:['인터넷에는\n바이러스가 우글거린다는 걸\n알고 있나요?','지금 미리\n바이러스 버스팅을\n연습해 두는 거예요!','시작하는 거예요!!'],
18:['먼저 말해 두겠는데,','인터넷에서는\n바이러스와의 배틀을\n피할 수 없다...','여기서 기본을\n연습하고 가도록 하자','곧바로 간다!'],
19:['넌 바이러스 버스팅을\n알고 있니?','바이러스와 싸우는 걸\n말하는데,','싸우는 법의 기본을\n모르면 멋지게 꽃피우기는\n어려우니까','가볍게 가르쳐 줄까\n시작할게...'],
20:['네놈...\n내 오퍼레이터가\n되는 이상,','배틀의 기본은\n확실히 익혀 둬라','그 몸으로 말이다'],
21:['이런 곳에서 막힐 수는\n없어!','한 번 더 간다!'],
22:['정말, 뭐 하는 거야!','다시 한 번, 간다!!'],
23:['거츠 거츠!!','분하다, 가스!\n한 번 더 간다, 가스!!'],
24:['아직 멀었군...\n다시 한 번이네...'],
25:['이 상태로는 인터넷을\n나아갈 수 없습니다!','다시 한 번 갑니다!!'],
26:['실수했군!!\n그 정도 바이러스는,\n단번에 해치우라고!','다시 한 번이다, 간다!!'],
27:['뭘 하는 건가,\n정신 차려라!','다시 한 번이다!'],
28:['죄송합니다...\n다시 한 번 기회를!!','핫!!'],
29:['당해 버렸네요...','......\n네, 납득할 수 없다고요?','그, 그렇죠,\n그럼 한 번 더 갑니다!'],
30:['다시 한 번 간다','침착하게 하면\n괜찮다!','간다!!'],
31:['그 정도 바이러스도\n못 쓰러뜨리면, 앞날이 불안하다\n다시 한 번 도전한다!'],
32:['제대로 하지 않으면\n안 돼, 퓨!','한 번 더 가자, 퓨!'],
33:['다시 한 번 한다...\n넌 하면 될 거다\n힘내라!!'],
34:['정말, 정신 좀 차려','그럼, 한 번 더 할게\n이번에는 힘내'],
35:['수련이 부족하군...','...다시 한 번이다...'],
36:['뭘 하고 계십니까!!','나이트가 그 정도\n바이러스에게 뒤처지다니!','다시 한 번 도전하겠소!'],
37:['바보 녀석!\n뭘 하는 거야!!','내 발목을\n잡지 마!!','자, 한 번 더 간다!'],
38:['실패해 버렸네요!','다음에는 실패하지 않도록\n힘내는 거예요!!'],
39:['조금 더 나은\n오퍼레이팅을 기대했는데','다음에는 실망시키지 마'],
40:['아름답지 않은\n배틀이었어...','한 번 더 할게\n이번에는, 아름다운\n오퍼레이팅을 보여 줘'],
41:['...흥,\n네놈의 기술이\n고작 그 정도인가...','다시 한 번이다...'],
},
'7C802C':{
0:[',\n수고했어!','자, 앞으로 나아가자!'],
1:['수고했어!',',\n이제 바이러스 버스팅은\n완벽하네!!','자, 앞으로 나아가자!'],
2:[',\n수고했다, 가스!','어떤 바이러스라도\n덤벼라, 가스!!','쭉쭉 나아간다, 가스!'],
3:['바이러스 버스팅의\n「기초」는\n익혔겠지...','그럼, 앞으로 나아가겠네...'],
4:['임무 완료',',\n수고하셨습니다','그럼, 앞으로 나아갑시다'],
5:['하면 되잖아!','자, 배틀의 기본도\n익혔으니,\n쭉쭉 나아간다!!'],
6:['좋은 오퍼레이팅이었다...\n이제 경험을\n쌓기만 하면 되겠군...','앞으로 나아가 볼까'],
7:[',\n수고하셨습니다','그럼,\n앞으로 나아갑시다'],
8:['멋진 오퍼레이팅이에요!','제법 하시네요\n이 근처 바이러스라면\n가볍게 삭제할 수 있겠네요','자, 슬슬\n가 볼까요'],
9:['음, 그럭저럭 괜찮은\n오퍼레이팅이었다','앞으로도 그 기세로\n부탁한다'],
10:[',\n수고했다...','제법 하는구나\n나, 나는 안심했다','자, 앞으로 나아가자...'],
11:['수고했어, 퓨!','아까처럼 오퍼레이팅하면\n이 근처 바이러스한테\n당할 일은 없을 것 같아, 퓨','앞으로 나아가자, 퓨!'],
12:['좋은 오퍼레이팅이었다','지금의 감각을, 잊어서는\n안 된다...','앞으로 나아가 볼까'],
13:[',\n수고했어!','배틀의 감각은\n잡은 것 같네','그럼, 앞으로 나아가자!'],
14:['...그럭저럭 괜찮은 오퍼레이팅이다\n닌자란, 하루하루가\n수련이지...','앞으로 더욱 실력을\n갈고닦아라','그럼, 슬슬\n출발할까...'],
15:['훌륭하군요!!','제법 훌륭한\n오퍼레이팅이었소','계속 단련하며\n솜씨를 갈고닦읍시다','자, 앞으로 나아갑시다'],
16:['좀 부족한데...\n더 강한 바이러스가 있는\n구역으로 가자'],
17:['수고하셨어요~!','이제 배틀 방법은\n확실히 익혔네요!','그럼,\n앞으로 나아가는 거예요!'],
18:['오퍼레이팅 실력은\n그럭저럭 괜찮군...','일단, 다시 한번\n잘 부탁한다고 해 두지','자, 앞으로 나아가 볼까'],
19:['제법 아름다운\n오퍼레이팅이었어','인터넷을\n계속 나아가며,','더 멋진 꽃을\n피워 보자'],
20:['흥, 그럭저럭 괜찮군...','...간다'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('organ scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('organ topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('organ tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=portrait,origin_portrait=portrait,portrait_visibility=visibility,context='All21 Navi first virus-practice introductions/retries/success messages or ShadowMan request failure; all scripts read.',variable_context='Success0/1/2/4/7/10/13 nickname+comma boundaries retained; each script source portrait identifies Navi. Real nickname widths unresolved.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-virus-practice',context='All186 Japanese literals from3 archives.21 first-practice offers,21 forced retry comments,21 success comments and ShadowMan failure read.',voice='Keep friendly/formal/rough/dignified personalities distinct. GutsMan 가스/AquaMan 퓨 tics, JunkMan hesitant robot speech, IceMan childlike polite, Bass terse; candidate voices not approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='21-Navi routing0/21 with unused1/2 continue, all42 intro/retry flag3863, source nickname commands and page boundaries retained. Success no retry flag added.',semantic_review=['ウイルスバスティング drafted 바이러스 버스팅 as tutorial topic; ネットバトラー/オペレート/オペレーター distinct 넷 배틀러/오퍼레이팅/오퍼레이터 candidates.', 'Source asks rhetorical questions without menu in these scripts; no fabricated yes/no or skip option. Failure scripts21..41 force flag3863 retry; success archive does not set it.', 'Nickname+comma fixed suffix avoids Korean final-consonant particle. Some praise predicts ability, not actual immunity to virus loss; AquaMan seems unlikely remains 것 같아.', 'WindMan いろは adapted 기초 without alphabet instruction. PlantMan flower image preserved. Bass body threat, JunkMan deletion risk, NapalmMan rough reprimand not softened into generic encouragement.', 'GutsMan source ガス maintained candidate 가스; JunkMan robot spelling and IceMan childlike politeness adaptation remain human-review candidates, not approved speech rules.', 'ShadowMan7C714C failure of request is separate from tutorial retry35 and has no flag3863/retry; no invented success or reward.', 'No normal-play first-entry/tutorial-battle/retry/success/Navi unlock/nickname/save/screen verification. Static source protection not runtime or presentation approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve organ draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
