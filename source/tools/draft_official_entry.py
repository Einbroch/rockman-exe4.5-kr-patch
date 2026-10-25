"""Manual Official registration124 and nearby generic battle38 drafts."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
 '7B1FF4':('b35aa13c9b136ad2780b0bedfa6fb940063acd6bde7fd11e508b3928af75f239',124,'translations/official_entry_draft_ko.json'),
 '7B0638':('11650aee82b3225e995b03e1159c1412c07385817b2e27cc2796a193ad60a4ed',38,'translations/generic_battlers_draft_ko.json'),
}
ENTRY={
0:['여기까지 오셨다는 것은\n당신은 선택받은 내비...','오피셜 토너먼트에\n참가할 자격이\n있다는 뜻이군요...','참가할 마음이 있으시면,\n오피셜 토너먼트에\n신청하실 수 있습니다','삐삐삐삐!!','아, 통신이군...\n잠깐 기다려 주세요...','네, 언더인터넷\n감시소입니다!','...뭐라고!?\n흉악범이?','흠... 그래,\n마침 잘됐군...','당신의 실력을\n시험해 보겠습니다','그 문 너머는\n언더인터넷으로\n이어져 있습니다','언더인터넷4에\n흉악범이\n숨어 있다는','정보가 들어왔습니다','그 흉악범을\n삭제하고 와 주셨으면 합니다','만약 당신이 흉악범을\n쓰러뜨릴 수 있다면,','무료로 등록해\n드리겠습니다','결코 당신의\n실력을 의심하는\n것은 아닙니다...','다만, 오피셜 토너먼트는\n수준이 높은\n대회니까요...','그럼, 힘내 주세요\n후후후...','아, 참, 흉악범의\n특징은 관...\n이라고 하더군요','그럼 언더인터넷으로\n이어지는 문을 열겠습니다','...오픈!!'],
2:['언더인터넷4에\n숨어 있는 흉악범의\n특징은...','관...이라고 하더군요','그런데... 관...?\n들어 본 적이 없군...'],
3:['...흉악범을\n쓰러뜨리고 오셨다고요!?','당신께 한 가지\n사과드려야겠습니다','저희는 항상\n오피셜 토너먼트에','출전하는 내비의\n실력을 시험하기 위해','언더인터넷에서\n시험용 내비를 쓰러뜨려\n달라고 하는데요,','이번에는 저희 실수로\n진짜 흉악범의 정보가\n들어온 모양입니다','당신이 쓰러뜨린 내비는\n초S급 범죄자,\n셰이드맨이었습니다','하지만 그 셰이드맨을\n쓰러뜨린 실력은,\n틀림없는 진짜입니다!','바로,\n오피셜 토너먼트에\n신청하시겠습니까?','물론, 무료로\n등록해 드리겠습니다!','신청하시겠습니까?','예  ','아니요','그러신가요...\n그럼 언제든 와 주세요'],
4:['그럼, 등록비로,\n1000제니 부탁드립니다','......네,\n1000제니\n받았습니다','그럼, 참가 신청\n절차를 진행하겠습니다','타닥타닥타닥...\n삐키이이이잉!!','등록 완료!','주말 토너먼트에서,\n힘내 주세요!'],
5:['그럼, 참가 신청\n절차를 진행하겠습니다','타닥타닥타닥...\n삐키이이이잉!!','등록 완료!','주말 토너먼트에서,\n힘내 주세요!'],
6:['유감이지만,\n돈이 부족합니다...','1000제니를 모으신 뒤\n다시 와 주세요...'],
7:['이런, 유감이지만,\n오늘의 등록은\n마감되었습니다...'],
8:['여기까지 오셨다는 것은\n당신은 선택받은 내비...','오피셜 토너먼트에\n참가할 자격이\n있다는 뜻이군요...','참가할 마음이 있으시면,\n오피셜 토너먼트에\n신청하실 수 있습니다','등록비로\n1000제니가 드는데,\n신청하시겠습니까?','예  ','아니요','그러신가요...'],
9:['여기는,\n오피셜 토너먼트의\n참가 접수처입니다만,','주말에는 참가 신청\n접수를 하지 않습니다','월요일부터 금요일\n사이에 와 주세요'],
20:['뭐냐, 이 녀석아!','휴... 바이러스인 줄\n알았습니다...\n놀라게 하지 말아 주세요'],
21:['이 에어리어 안쪽은,\n언더인터넷이야','하지만 오피셜 내비가\n감시해 주고 있으니,\n안심이야!!'],
22:['이 근처 바이러스는\n모두 흉폭해서\n무서워...'],
30:['내 꿈은\n오피셜 넷 배틀러가\n되는 거야!'],
31:['언더인터넷은,\n무섭지만, 솔직히\n조금 관심이 있어!'],
40:['어두워졌네...','이 근처는 해가 지면\n언더인터넷 쪽에서','낮고 무서운\n울음소리가 들려와','그건 바로 망자의\n신음 소리...','라는 건 농담이야!\n조금 무서웠어?'],
41:['오피셜이 지켜\n준다고 생각해도,\n어두워지면 무섭네...'],
50:['너무 늦게까지\n인터넷을 해선 안 된다','그러지 않으면...\n언더인터넷에서','검은 손이 뻗어 나와\n끌고 들어가 버린다아'],
60:['우오오오옷!!\n배틀을 하고 싶어 못 참겠어!','어이, 너,\n나와 배틀해라!!','응  ','그만둘래','뭐라고오오오!\n웃기지 마!!'],
61:['제기랄...','또 울분이\n쌓여 버렸군...'],
62:['햐아하하하하하!!','최고의 기분이다!!'],
63:['살기가 느껴지는군\n네놈, 나를\n노리고 있는 건가?','그렇다!  ','아니야!','이미 네놈은\n내 공격 범위 안에 있다,\n현명한 선택이다...'],
64:['쳇!!\n파고드는 게 부족했나!?'],
65:['네놈의 스피드로는,\n나를 잡을 수 없다!'],
66:['새까맣게 태워 주마!!','배틀 오퍼레이션, 세트!!\n인!!'],
67:['...베겠다!!'],
68:['우오오오옷!!\n배틀을 하고 싶어 못 참겠어!','음, 너, 어디선가\n본 얼굴이군!','뭐, 그런 건 아무래도 좋아!\n나와 배틀해라!!','응  ','그만둘래','뭐라고오오오!\n웃기지 마!!'],
69:['...훗','그런 모습을 하고\n내가 놀랄 거라고\n생각했나...','모습만 흉내 낸다고\n이 브루스를 쓰러뜨릴 수는\n없다!!','덤벼라,\n진짜 칼날의 날카로움을\n보여 주겠다!!','간다!  ','미안!','훗... 현명한 선택이다'],
70:['키라키라키라라~!!','저는 금색 프로그램!','배틀 칩 게이트에서\n다 써 버린 칩의\n사용 횟수를...','회복시켜 드리겠습니다!!','키라라키라!!'],
80:['다크로이드가 언더에','.','.','.','우리의 감시를\n빠져나가다니...'],
81:['셰이드맨이 아직 완전히\n소멸했다고는 생각하기\n어렵군...','게다가, 그 에어리어에\n있다고 하는 다크로이드도\n신경 쓰이는군...'],
82:['흠, 다크로이드는\n아닌 모양이군...'],
83:['다크로이드가 숨은\n곳은 대충 짐작이\n가는데도,','당장 움직일 수 없다니,\n참으로 답답하군!'],
90:['토너먼트 참가 접수는,\n평일 아침6시부터\n밤12시까지입니다!'],
}
BATTLERS={
0:['어이, 이 몸과\n배틀하지 않겠나!?','혈기 넘치는 이 몸은,\n매주 이날이\n기다려져서 못 참겠어','빨리 배틀하자고!!','응!  ','싫어!','우오옷!','이 몸의 배틀에 대한\n열정을 어디에 쏟으면\n좋으냐고!!'],
1:['시작한다...','배틀 오퍼레이션, 세트!\n인!!'],
2:['헤헤헤...\n제법이군...'],
3:['벌써 끝이냐!!\n이 정도로는 부족하다고!'],
4:['이봐, 너,\n지금 나랑 눈이 마주쳤지?','그건 배틀하자는\n뜻이지?','나랑 배틀하고\n싶은 거지?','좋아, 덤벼라!!','간다!  ','오해예요!','쳇, 기대하게 해 놓고!'],
5:['팔 하나나 둘쯤은,\n각오하라고!!','배틀 오퍼레이션, 세트!\n인!!'],
6:['으헤! 제법이잖아!!','배틀을 신청할 만한\n실력이 있군...'],
7:['뭐냐,\n그 겁먹은 자세는!!','그렇게 해서는, 100만 번\n배틀을 해도 날\n이길 수 없어!!'],
8:['어라, 오랜만이잖아!\n나야, 나!!','이야, 그립네!!\n그래, 배틀하자고, 배틀!','항상 여름 방학 때,\n했었잖아!','빨리 시작하자고!!','간다!  ','오해예요!','큭!','나야 나 넷 배틀이\n통하지 않다니... 제법이군!!'],
9:['나야 나 살법의 맛을\n보여 주마!!','배틀 오퍼레이션, 세트!\n인!!'],
10:['나야 나 살법을\n깨뜨리다니...','제, 제법이군...!!'],
11:['봤느냐!!\n나의, 나에 의한, 나를 위한\n나야 나 살법!!','바다를 가르고 대지를 찢는다!'],
}

def create(archive):
    source_sha,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,source_sha);original=(ROOT/source).read_text(encoding='utf-8-sig')
    rows=ENTRY if archive=='7B1FF4' else BATTLERS
    values={f'{archive}:{s}:{i}':t for s,v in rows.items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('entry scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)}
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        speaker=portrait if visibility=='visible' else 'system-communication-sfx' if archive=='7B1FF4' and (s,i)==(0,3) else 'player-choice'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('numbers/tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spaces '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,origin_portrait=portrait,portrait_visibility=visibility,context='Official entry test/revelation/free-first vs paid later registration, weekday/time restrictions and local Navi/NPC branches' if archive=='7B1FF4' else 'Three HeelNaviPurple battle encounters: weekly eager, eye-contact provocation, feigned acquaintance/オレオレ comic attack; acceptance/refusal and both outcomes read together.',variable_context='No runtime name/item variable interpolation; native portrait/sound/selection/time/event commands and original line topology remain unchanged. Actual callers/layout not verified.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive=archive,source_tpl=dict(path=source,sha256=source_sha),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-and-choice',context=f'All{count} unselected Japanese literals in255-slot archive; complete local source branches read, source and ROM payload pinned.',voice='Source Official courtesy/apology, NPC fears/joke, NapalmMan aggressive/ProtoMan terse, GoldProg magical cry; generic HeelNaviPurple bluff/feigned familiarity preserved as candidate. No new human approvals.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve IDs/source, numeric1000/4/6/12/100 and control arguments, free3->5 vs paid8->4->6, tournament bitmask4, weekend0/6 gates, flag513/1322/1345/4270/1598, self-Navi18/7, battle setup, timed30-frame dots, gate history clear and all choice spaces. No ROM/save/gameplay mutation.',semantic_review=['First task sends Navi toUnderInternet4 to delete criminal; coffin clue is hearsay. After success, examiner reveals administrative mixup and actual超S級ShadeMan, not a planned encounter with a harmless test Navi. S rank retained; names follow existing story_mail candidate.', 'First test-success3->5 registers free; later8->4 charges1000zenny with insufficient funds6. No blanket free registration claim. Weekend closed9 and Mon-Fri6am-midnight90 are native source instructions; time conventions not changed.', 'Radio beep0:3 with hidden portrait and track219 is system sound text, not a player option. Sound disable/enable and portrait transitions unchanged.', 'Darkloid81 says full disappearance is difficult to believe and another presence is reported; do not assert confirmed resurrection or a guessed area number.80 punctuation remains three separate wait30 literals.', 'GoldProg70 restores chip use counts via callClearBattleChipGateHistory; this is not new chips, HP recovery, or player-save erasure. キラ magical cries remain phonetic candidates.', 'Generic8 pretends prior acquaintance; オレオレ phrases use 나야 나 candidate, not real family history or instructions about financial fraud. 殺法/살법 identity and comic adaptation require human review.100万回 keeps digits100 and unit만.', 'Actual geometry, clock/calendar, registration charge/decline, battle and caller outcomes, gate recovery/persistence remain unverified.'],units=units)

def main():
    for archive,(_,count,out) in SOURCES.items():
        a=create(archive);path=ROOT/out
        if path.exists():
            if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation '+out)
        else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {archive} {count} draft only; ROM unchanged')

if __name__=='__main__':main()
