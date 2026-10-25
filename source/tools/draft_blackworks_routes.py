"""Manual, source-bound drafts for both BlackWorks brothers and nearby NPCs."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
    '7AF6D0':('d077caebae62ecb56b3c68b7cd3f0be8747ec74965a2e6b4ad6600cd83e1b378',92,'translations/blackworks_younger_draft_ko.json'),
    '7B09F4':('79b74aced02ec59177784a6f6a6f8216e8a94479c723d67a9cc6dd6cf0cdc8be',130,'translations/blackworks_elder_draft_ko.json'),
}
# Each entry is authored in its native scene; no source-string prose replacements.
YOUNGER={
0:['뭐냐, 네놈은!!','우리의 오피셜\n토너먼트 방해 작전을\n훼방 놓으려는 거냐!?','그... 그런 짓은\n못 하게 해...','못 하게 한다고오!!'],
1:['으윽...\n당해 버렸군...','...하지만,\n당하고 나서 깨달았어','......\n내가 잘못하고 있었다는 걸','헷, 너한테 당해서\n다행일지도 모르겠군...','그래... 부탁이 있어\n인터넷11에\n우리 형이 있어...','형은...\n우리 블랙워크스의\n보스야...','형을... 쓰러뜨려 줘...'],
2:['으윽...\n당해 버렸군...','......\n뭐, 형도 쓰러뜨렸다고!?','헷, 그럼 이건\n아무 쓸모도 없겠군...','자, 우리 반성의\n증거다... 가져가',',\n「','」\n획득!!','헷, 너한테 당해서\n다행일지도 모르겠군...','이제 오피셜에\n자수할 거야...','...고맙다'],
3:['인터넷11에 있는\n형을... 쓰러뜨려 줘...','그리고 정신을 차리게\n해 줘...'],
4:['이번 일로 정신이 들었어...','오피셜 토너먼트의\n예선에서 떨어져서,\n짜증이 났던 거야...','하지만 지금은 정말\n반성하고 있어...'],
10:['나도 언젠가는\n오피셜 토너먼트에\n나가 보고 싶어~'],
11:['자네, 돌아다니는 건 좋지만,\n바이러스는 조심하게!'],
20:['오피셜 토너먼트에\n참가 신청을 하려면,\n어떻게 해야 할까...'],
21:['이 에어리어 앞의\n인터넷12에는','오피셜 토너먼트의\n참가 접수장이\n있는데,','거기까지 갈 수 있는 내비는\n그리 많지 않아...'],
30:['이 근처 에어리어를\n왜 오피셜이\n관리하는지 알아?','이 앞에 있는\n인터넷12가','언더인터넷으로\n이어져 있기 때문이야'],
31:['해가 졌군...\n순찰을 철저히\n해야겠어...'],
40:['뭐냐, 어이!','착한 아이는 빨리\n자라는 말이야!'],
41:['깊은 밤은 범죄가\n가장 일어나기 쉬운\n시간대다...','자네도 빨리 플러그아웃\n하는 편이 좋겠어'],
50:['...무슨 일이냐?','나와 배틀을 하고 싶은 건가?','응  ','아니야!','그런가...','평온한 마음은\n중요하니까...'],
51:['강하군...','하지만 그 힘에\n도취되어선 안 된다...'],
52:['이것이 위대한\n대지의 힘이다!!'],
53:['싸움을 신청한 걸\n후회해도 난 모른다...','위대한 대지의 힘,\n마음껏 보거라!!'],
54:['별일도 다 있군\n그 모습을 보아하니,','너도 대지를 사랑하고\n지키는 자로군...','인사 대신 배틀이라도\n어떠냐?','응  ','싫어요','그런가...','평온한 마음을\n지니고 있군...'],
60:['언더인터넷을\n알고 있나?','인터넷의 어둠이지','범죄자와\n흉악한 바이러스가\n돌아다니고,','우리 오피셜조차\n쉽게 들어갈 수 없는\n위험한 에어리어다...','하지만 오피셜 토너먼트에\n출전하려면,\n피할 수 없는 길이지'],
70:['...이 앞의 에어리어로\n가고 싶은 모양이군...','네가 이 앞 에어리어에서\n싸울 힘이 있는지\n시험해 주겠다','시험을 통과하지 못하면,\n여길 지나가게 할 순 없다','시험을 받겠나?','예  ','아니요','그럼, 시험 내용을\n설명하겠다','지금부터 인터넷2에\n바이러스를 발생시키겠다...','제한 시간 안에\n그 바이러스들을\n모두 저격해라','그걸 해낸다면,\n시험에 합격한 것으로 하겠다','단, 지금부터 임무가\n끝날 때까지,','한 번이라도 플러그아웃하면,\n이번 시험은 실패로 하겠다','...이상이다'],
71:['그런가...'],
72:['시험 내용을\n확인하러 왔군...','그럼, 시험 내용을\n설명하겠다','지금부터 인터넷2에\n바이러스를 발생시키겠다...','제한 시간 안에\n그 바이러스들을\n모두 저격해라','그걸 해낸다면,\n시험에 합격한 것으로 하겠다','단, 지금부터 임무가\n끝날 때까지,','한 번이라도 플러그아웃하면,\n이번 시험은 실패로 하겠다','...이상이다'],
73:['바이러스를 쓰러뜨리고 왔군\n좋아, 시험 합격이다','지나가도 좋다...'],
74:['바이러스 저격에\n실패했군...','다시 도전하겠나?','예  ','아니요','좋다, 다시\n인터넷2로 돌아가라'],
75:['실력을 쌓은 뒤,\n다시 도전하도록 해라'],
}
ELDER={
0:['네놈, 누구냐?','미안하지만 여기부터는\n지나가게 할 수 없다!','꼭 지나가고\n싶다면...','나를 쓰러뜨리고 가라!!','샤아아아아아아아!!'],
1:['뭐냐? 자네,','여기가 어떤 곳인지\n알고 있나?','언더인터넷보다\n무서운,','우리 블랙워크스의\n아지트라고!!','그 사실을\n알아 버린 녀석을\n살려 보낼 순 없다!','샤바라바라바앗!!'],
2:['...으응?','샤아아아...\n슈라라...','슈라즈아앗...','데, 데, 데리이이초아아!!'],
3:['용케 여기까지 왔군...','내 심복들을\n쓰러뜨리다니, 제법\n실력이 있는 모양이다만...','오피셜이 보낸 놈인가?','뭐, 아무래도 좋다...','네놈은 우리의\n오피셜 토너먼트\n방해 작전을...','...막을 수 없다!!','쿄에에에에에에엣!!'],
4:['게하앗...','어, 어떤 놈이길래...\n이 나를 쓰러뜨리다니...','이, 이제 끝이다...\n나의 블랙워크스는\n......','이봐, 자네...\n내 부탁을\n들어 주겠나...','인터넷10에\n내 동생이 있어...','동생을...\n...막아 줘'],
5:['어, 어떤 놈이길래...\n이 나를 쓰러뜨리다니...','...뭐, 뭐라고!?\n내 동생도\n쓰러뜨렸다고!?','이, 이제 끝이다...\n나의 블랙워크스는\n......','자, 가져가라...','오피셜 센터에서\n훔친 물건이다...',',\n「','」\n획득!!','이제 이 바닥에서\n손을 씻겠어...'],
6:['부탁이다...\n인터넷10에 있는\n동생을 막아 줘!!','부탁해!!'],
7:['난 도대체,\n뭘 하고 있었던 걸까','지금 생각해 보면\n얼마나 어리석은 짓을...','앞으로는 성실하게\n훈련을 거듭해서,','언젠가는\n오피셜 토너먼트에\n나갈 수 있도록 노력할게'],
10:['안녕하세요!','여기는 인터넷11!\n이 앞은 인터넷12로\n이어집니다!!'],
11:['이 에어리어 안쪽에는\n인터넷10에서','인터넷12를\n경유해 돌아와야\n갈 수 있는 곳이 있어'],
12:['좋은 아침!!\n음, 멋진 아침이네!','현실 세계에서는,\n모르는 사람에게 인사하는 건\n좀처럼 하지 않는데,','넷에서는 자연스럽게\n할 수 있지!'],
13:['들은 이야기인데,\n오피셜 토너먼트에\n참가 신청을 하려면,','언더인터넷에 잠든\n흉악한 내비를\n쓰러뜨려야 한대!'],
20:['이 앞에 있는\n인터넷12는\n언더인터넷으로 이어져 있어','언더인터넷으로 이어지는\n에어리어를 우리 오피셜이\n관리해서,','범죄자나 흉악한\n바이러스가 나오지 못하게\n하고 있는 거야'],
21:['이 근처 에어리어에는\n오피셜 내비가\n항상 있어 주니까,','정말 안심이 돼!'],
30:['너무 늦어지지 않게\n플러그아웃하도록 해!'],
31:['자, 밤의 시작이다...','그렇다고 나쁜 짓을\n할 건 아니지만...','오피셜이 돌아다니는\n곳에서 범죄를 저지르다니,\n바보나 할 짓이지'],
40:['저쪽에서 서성거리는\n눈매 사나운 내비...','수상하군...'],
41:['뭐야, 난 쓰레기를 줍고\n있을 뿐이라고','한밤중에 쓰레기 줍는 건\n내 취미라고!!'],
50:['...그 눈빛, 나에게\n배틀을 신청할 생각인가?','그렇다!  ','아니야!','목숨을 건졌군...'],
51:['마, 말도 안 돼!! 작전은\n완벽했을 텐데...!!'],
52:['미션 완료...','예상대로의 결말이다'],
53:['누구냐...?','설마 아니겠지만,\n나에게 배틀을 신청하려는\n것은 아니겠지?','그렇다!  ','아니야!','...그런가'],
54:['제, 제법이군...!!','기사도에 따라\n깨끗이 패배를 인정하겠다','하지만 다시\n맞붙을 때는,\n이렇게 되진 않을 것이다!!'],
55:['실력 차이를\n알면서도, 나에게\n도전한','용기는 인정하겠다','무모한 도전은,\n목숨을 줄이는 결과를 낳는다'],
56:['타깃, 록온...','배틀 오퍼레이션, 세트\n인!!'],
57:['조금도 봐주지 않겠다!','배틀 오퍼레이션, 세트!\n인!!'],
58:['뭐냐, 그 모습은...\n나를 도발하고\n있는 건가?','그렇다!  ','아니야!','목숨을 건졌군...'],
59:['음!!\n뭐냐, 그 모습은!!','설마, 나는 아니겠지!\n난 그렇게 뚱뚱하지 않다!','나이트를 모욕하다니\n용서할 수 없다!!','네놈에게 결투를 신청한다!!','덤벼!  ','미안!','흥!','사과할 거라면,\n처음부터 그런 모습을\n하지 않았으면 될 것 아닌가!'],
60:['여기를 지나가고 싶으세요?','그렇다면, 오퍼레이터님\n저를 도와주셨으면 해요!','지금, 얼어붙은\n바이러스를 퇴치하고\n있는데요,','저 1명만으로는 좀처럼\n잘 안 돼요','만약 오퍼레이터님의\n도움으로 바이러스를\n쓰러뜨릴 수 있다면,','길을 열어 드릴게요!','도와주실 건가요?','예  ','아니요','그럼 부탁드릴게요!'],
61:['해냈어요!!\n덕분에 바이러스를\n쓰러뜨릴 수 있었어요!','그럼 약속대로,\n길을 열어 드릴게요!!','고마워요!!'],
62:['부우우...','안 됐어요!!\n그렇게 해서는,\n여길 지나가게 할 수 없어요!!'],
63:['그런 말씀은,\n하지 말아 주세요~'],
221:['또 오세요!'],
222:['유감이지만,\n품절입니다...'],
223:['저는 넷 상인...\n좋은 물건이 있답니다?\n','볼래  ','안 볼래'],
224:['저는 넷 상인!\n오늘은 일주일에 한 번인\n레이디스 데이!!','여자아이에게는 팍팍\n서비스해 드릴게요!','좋은 물건이 있답니다!?\n','볼래  ','안 볼래'],
225:['어서 오세요!\n저는 넷 상인!','손님, 운이 좋으시군요!\n오늘 저는\n기분이 최고로 좋거든요!','서비스해 드릴 테니,\n많이 많이 사 가\n주세요!!','평소에는 볼 수 없는\n좋은 물건이 있답니다!?\n','볼래  ','안 볼래'],
}

def create(archive):
    source_sha,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,source_sha);original=(ROOT/source).read_text(encoding='utf-8-sig')
    rows=YOUNGER if archive=='7AF6D0' else ELDER
    values={f'{archive}:{s}:{i}':t for s,v in rows.items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('route scope '+archive)
    blocks={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)}
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[blocks[s]:x.start]))
        if archive=='7B09F4' and s==221:
            portrait='NormalNaviYellow';visibility='inherited from native223/224/225 shop caller';speaker=portrait
        else:
            shown=[m.group(1) for m in events if m.group(1)]
            if not shown:raise ValueError('unresolved actor '+x.key)
            portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
            reward=(archive=='7AF6D0' and s==2 and i in (4,5)) or (archive=='7B09F4' and s==5 and i in (5,6))
            speaker=portrait if visibility=='visible' else 'system-reward' if reward else 'player-choice'
            # Native shop choices keep their portrait visible; visibility is not speaker identity.
            if archive=='7B09F4' and (s,i) in ((223,1),(223,2),(224,3),(224,4),(225,4),(225,5)):
                if 'option\n' not in original[blocks[s]:x.start]:raise ValueError('shop option context '+x.key)
                speaker='player-choice'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('numbers/tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,origin_portrait=portrait,portrait_visibility=visibility,context='Paired BlackWorks younger/elder routes linked by flags1230/1253 and item11; nearby NPCs, native Navi challenges, access-test minigames and elder-area shops. Source pages/branches read together.',variable_context='Reward printCurrentNavi then printItem11 order retained; comma/noun acquisition avoids variable-dependent particles. Choices, trailing blank lines, native flags and self-Navi branches unchanged. Variable/display/caller review pending.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive=archive,source_tpl=dict(path=source,sha256=source_sha),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-and-choice',context=f'All{count} unselected Japanese literals in255-slot archive; paired source files7AF6D0/7B09F4 establish兄/弟 and both defeat orders. No source plot or caller mutation.',voice='Younger rough remorse vs elder commanding/reformed speech; WoodMan solemn nature, SearchMan tactical, KnightMan pride, IceMan polite appeal, NPC/shop registers separated. Candidate wording, no new human approvals.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve source IDs/commands, item11 reward and flags1230/1253 defeat-order branches, Internet10/11/12/2 and number1, choice slots/cancel/default/width, minigame hard=false and plugout failure, native self-Navi and shop selection. No ROM/save/gameplay writes.',semantic_review=['Younger inInternet10 calls elder兄/boss inInternet11; elder calls younger弟 inInternet10. Keep younger request defeat/wake elder vs elder request stop younger distinct; either order rewards item11, no assumed fixed order.', '블랙워크스/오피셜/언더인터넷 and 타깃·록온 inherit existing candidate assets; new 오피셜 센터/레이디스 데이 remain source-backed candidates, not approved terms.', 'SearchMan test70/72 requires all viruses inInternet2 within unspecified time and fails on any plugout. No invented duration; retry74 returns toInternet2. Battle challenge SearchMan in other archive is separate.', 'KnightMan59 refers to ナイト; use 나이트 rather than silently resolving to knight profession or named identity. Self-appearance complaint and resulting challenge preserved. Shouted nonsense remains phonetic candidate requiring voice review.', 'IceMan help60/61 promises passage only after virus extermination success;62 refuses on failure. Childlike polite source voice is a candidate, not a grammar-wide conversion.', 'Shop221 inherits NormalNaviYellow from223/224/225. Normal shop2 vs special12, weekday3/Navi1 vs global override6/7 unchanged; source dialogue does not specify a discount percentage or fixed Korean weekday. No such additions.', 'Actual layout/maximum variable values, normal gameplay defeat order and access transitions, all minigames/battles/shops and persistence remain unverified.'],units=units)

def main():
    for archive,(_,count,out) in SOURCES.items():
        a=create(archive);path=ROOT/out
        if path.exists():
            if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation '+out)
        else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {archive} {count} draft only; ROM unchanged')

if __name__=='__main__':main()
