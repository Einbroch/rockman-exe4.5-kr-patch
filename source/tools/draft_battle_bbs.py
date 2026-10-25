"""Individually authored battle BBS125; immutable source, draft-only output."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/7000AC.tpl'
SOURCE_SHA='2bb6f588838a89ed753d365b6aa019cb1ee714b7ec37954c4f6e70de2bb063d3'
OUT='translations/battle_bbs_draft_ko.json'
DRAFT={
0:['어서 와!\n여기는 배틀 게시판!','다들 바이러스 버스팅\n연습 프로그램은\n통과했지?','이 게시판은\n더 뛰어난 기술에 대해\n이야기하는 곳이야!','다들 자기가 발견한\n기술을 적극적으로\n글로 올려 줘!','그럼 우선 내가\nLR 버튼으로 쓰는 장비를\n설명해 줄게!'],
1:['L 버튼, R 버튼으로 쓰는\n장비는 내비마다 달라','내비는 각각 3종류의\n장비를 가지고 있어','그중 2종류를 골라\nLR에 배정할 수 있지','참고로 R 버튼은 처음엔\n모두 버스터로 설정되어 있어','쓰는 장비를 바꾸려면\nPET 화면의 장비 항목을\n선택하고...','L과 R 각각의 장비를\n바꾸면 OK야!'],
2:['LR로 쓰는 장비 중에는\n방어 타입도 있어','예를 들면 실드 같은 게\n여기에 해당하는데...','방어 타입 장비를 쓰면\n커스텀 게이지가\n조금 소모돼'],
3:['나도 실전에서 쓸 만한\n기술을 찾았어!','배틀 칩을 쓰는 데\n필요한 커스텀 게이지!\n시간이 지나면 차오르지만','놀랍게도 버스터를 쏘면\n게이지가 더 빨리 차올라!\n엄청난 발견이지!'],
4:['커스텀 게이지를 효율적으로\n늘리는 방법인가! 흠흠...','버스터를 쏘면 게이지가\n더 빨리 차는 건 맞지만\n더 굉장한 기술도 있어!','그건...\n바로 카운터야!','카운터는\n상대가 막 공격하려는\n바로 그 순간에...','칩 공격을\n명중시키는 거야!','당황한 상대는\n잠시 마비될 뿐만 아니라\n게이지도 단숨에 확 늘어나!','벌컨처럼\n연사가 되는 칩이면\n노리기 쉬워!'],
5:['내비에게 배틀 칩을\n보내면 말이야','적에게 맞힐 수 있도록\n자동으로 이동한 뒤에\n써 주잖아','그런데 그 자리에서 바로\n쓰는 때도 있는 것 같아\n왜 그런 걸까?'],
6:['확실히 대부분의 칩은\n자동으로 이동한 뒤에\n써 주지','하지만 몇몇 칩은\n그 자리에서 바로 쓰도록\n되어 있어','어떤 칩이 그런지는\n직접 확인해 봤으면 해','참고로 쓸 때\n시간이 멈추고\n화면이 어두워지는 칩은','그 자리에서 바로 쓰니까\n내비를 제대로 유도한 뒤에\n쓰면 좋아!'],
7:['바이러스에게서 도망치려면\n작전 화면에서 L 버튼을\n누르면 되지만','도망치지 못했다면\n커스텀 게이지가 파란색까지\n차오르기 전에는','다시 도망칠 수\n없어\n다들 조심하는 게 좋아'],
8:['처음 뵙겠습니다!\n오늘 배틀 칩 게이트를\n사 왔어요!','게이트를 달면 어떻게 되는지\n간단히 알려 드릴게요!','기본적인 배틀 규칙은\n게이트가 없을 때와\n딱히 다르지 않은 것 같아요','평소처럼 폴더 안의\n30장 칩을\n쓸 수 있는데...','배틀 칩 게이트에\n슬롯 인하는 것으로도\n칩 공격이 가능해요!','폴더 안의 칩과 달리\n원하는 칩을 언제든\n쓸 수 있어서 꽤 좋아요!','다만 게이트로 쓰는 칩은\n칩마다 사용 횟수가\n정해져 있어요','사용 횟수는\n플러그아웃하지 않으면\n원래대로 돌아오지 않으니','계획적으로\n칩을 사용하는 것이\n요령이네요!'],
9:['칩 게이트를 사셨군요!\n좋지요!\n저도 어제 사 왔어요!','참고로 인터넷 어딘가에는\n칩 사용 횟수를\n회복해 주는 곳도 있어요','슬롯 인할까 말까!\n이런 전략성이\n칩 게이트의 묘미죠!','그리고 이런 메일이\n도착해서\n소개해 드릴게요!!','「넷 배틀러 여러분\n 실례하겠습니다\n 이벤트 안내입니다',' 현재 전기레인지 전뇌에서\n 배틀 대회를 개최 중입니다',' 이름은 에브리데이 토너먼트\n 이름 그대로 매일\n 개최하고 있습니다',' 사전 참가 신청은\n 필요 없습니다\n 많은 참가 바랍니다!',' 또한, 이 대회는\n 주말 토너먼트와\n 아무 관계도 없습니다',' 주의해 주세요」'],
15:['여러분\n솔깃한 정보를\n얻었어요!','에브리데이 토너먼트의\n우승 상품은\n티켓이라고 하네요'],
16:['저도 배틀 등으로 여러모로\n바쁘지만 일단\n한마디 할게요!','그게 무슨 티켓인데요!!'],
17:['안녕하세요','에브리데이 토너먼트가\n인기 있는 건가요?','여러 장소에서\n열리고\n있는 것 같아요','그리고 그 티켓으로\n어딘가의 전뇌 문을\n열 수 있다고 해요'],
18:['배틀 중 상대 내비가\n프로그램 어드밴스라는\n특이한 공격을 했어요','앗!!','하는 사이에 졌어요\n정말 장난이 아니었어요!','그 굉장한 기술은\n뭘까요?'],
19:['프로그램 어드밴스 말이구나\n맡겨 둬\n코에츠 형이 답해 줄게!','정해진 순서로 칩을\n3장 보내면 칩이\n합체할 때가 있어','방법은 셀렉트 버튼을\n누르면 칩 입력 시간이\n시작되니까...','그동안 순서대로\n칩을 고르면 돼','합체한 칩은\n엄청 강력해!\n분명 푹 빠질 거야','참고로 한번 찾은\n조합은 P.A 메모에\n자동으로 등록돼','다들 꼭 찾아보자!!'],
20:['방어 계열 장비를\n쓰면 커스텀 게이지가\n줄잖아?','그런데 상대 공격을\n제대로 막아 내면\n이번엔 게이지가 늘어나!','방어를 잘하면\n공격으로도 곧바로\n전환할 수 있다는 거지!','어때? 도움 됐지?'],
21:['다마라는\n달마 인형 같은 바이러스를\n가끔 보지?','그 녀석의 벽에 튕기는\n공격은 예측하기 어려워서\n성가시지 않아?','항상 애를 먹는데\n간단히 삭제하는\n방법은 없을까?'],
22:['다마가 상대라면\n크랙아웃이 엄청\n쓸 만해!','패널에 구멍이 나 있으면\n다마의 공격은\n구멍에 빠져! 한심하지!','공격 못 하는 다마는\n그냥 달마 인형이지?\n헤헤헤!'],
23:['구멍을 내면\n싸우기 쉬워지는\n바이러스가 있긴 하죠','제가 아는 건\n마루모코예요','그 녀석의 돌진이\n닿지 않게 될 줄\n생각하셨나요?','크랙아웃이\n잔뜩 있었으면 하는\n요즘입니다'],
24:['토너먼트 상대가\n무척 잘생긴\n내비였어','나도 모르게 마그볼트로\n끌어당겨 끌어안았지\n에헤','사랑에 빠지기 쉬운 소녀에게\n마그볼트는\n필수 아이템이야!'],
25:['요즘 이 근처에서도\n오피셜의 순찰을\n자주 보네','표정이 험한 걸 보니\n보통 일이 아닌가 봐','무슨 일이 생긴 걸까?'],
26:['아는 오피셜에게\n물어봤는데요,','다크로이드라는\n수상한 내비를 경계하고\n있는 것 같아요','토너먼트에 영향이\n없으면 좋겠네요'],
27:['어라?\n정말 부지런한\n바이러스가 있네!!','그렇게 생각하며 흐뭇해하다가\n당하고 말았어요','그 녀석이 열심히\n나르는 짐의\n정체는 폭탄이에요','그 폭탄이 방벽도 되어서\n본체에 공격이\n맞지 않더라고요','그 폭탄을\n우리 에어리어까지 운반하면\n쾅 터지는 거예요','여러분이라면 어떻게 하세요?'],
28:['그 바이러스는 봄보이예요\n폭탄은 보이즈봄이라고\n한다고 하네요','보이즈봄은 폭발하기 전에\n파괴할 수 있지만\n좀 귀찮죠?','저라면 1칸 뒤까지\n관통하는 칩으로 공격해요\n벌컨 계열 같은 거요','그래서 보이즈봄이\n다가오기 전에 빨리 쓰러뜨린다!\n그게 답 아닐까요?'],
29:['안녕, 바이러스 연구도\n잊지 않는 공부꾼\n코에츠 형이야','흠흠...\n사무조군의 말도\n맞는 말이네','하지만 더\n편한 방법도\n있어','봄보이는 곧장 앞으로만\n갈 수 있지\n그렇다는 건........','똑똑한 너희라면\n이제 알겠지!','봄보이가 가는 방향에\n장애물이나 구멍을\n만드는 거야!','그것만으로\n봄보이는 더 나아갈 수\n없게 될 거야','이제 너희가 원하는 대로\n요리해 주면 돼\n쉬운 일이지!'],
32:['퀵 게이지라는 칩은\n엄청 편리해!','이 칩으로\n커스텀 게이지가 차는\n속도를 높일 수 있어','이야, 편리해!'],
33:['반대로 게이지 속도를\n늦추는 칩도\n있었지요?','이름이 아마\n헤비 게이지였던가요?','세상엔 다양한 칩이\n있네요'],
34:['퀵 게이지든\n헤비 게이지든...','칩을 쓸 때\n커스텀 게이지가\n줄지 않는다는 건 알아?','그 밖에도 쓸 때\n게이지가 소모되지\n않는 칩이 있어','그걸 모르는 사람이\n가끔 있더라고','배틀 중에는 커스텀 게이지를\n잘 살펴봐!']
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA);original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    if not all(t in original for t in ('ここは バトルケイジバン','コーエツにいさん','BBS00 ID','left = 32','top = 68','セレクトボタン','カウンター')):raise ValueError('battle BBS context changed')
    values={f'7000AC:{s}:{i}':t for s,rows in DRAFT.items() for i,t in enumerate(rows)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=125 or set(values)!={x.key for x in selected}:raise ValueError('battle125 scope '+str(set(values)^{x.key for x in selected}))
    units=[]
    for x in selected:
        s=int(x.key.split(':')[1]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('source row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('source numbers/tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='Koetsu-self-identified' if s in (19,29) else f'BBS-post-{s}; author not inferred',context='Complete battle BBS posts0..9/15..29/32..34; adjacent replies read together. Nested quoted event mail9 distinguished. Gameplay advice kept as authored source explanation, not a new technical behavior claim.',variable_context='Original post/page/quote boundaries retained; no dynamic name substitutions. ASCII BBS placeholders unchanged; actual BBS layout and poster headers need separate review.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x7000AC)
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='7000AC',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='bbs-text',context='All125 Japanese literals in49-slot battle BBS archive; local posts, replies and quoted event announcement read together. No author identity inferred from nearby names alone.',voice='Source casual and polite poster registers retained as drafts; Koetsu19/29 explicit self-introductions. Existing gold_bbs_draft_ko.json wording candidates for common system terms, not new approval.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve IDs, numeric counts3/2/30/1, L/R/SELECT and input order, equipment vs chips, gauge consumption vs gain, escape retry prerequisite, nested event quote, conditions/uncertainty and command/newline topology. ROM/save unchanged.',semantic_review=['크랙아웃/보이즈봄/마루모코 follow existing chip description candidates. 다마/달마/봄보이/사무조군/마그볼트/퀵 게이지/헤비 게이지 remain source-backed candidates for glossary review, not approved names.', 'Source8 says plug-out restores chip count; reply9 mentions an Internet restoration place. Both source statements retained, no deletion of apparent exception and no assertion that one disproves the other.', 'Source counter timing is enemy attack instant plus chip hit, not buster counter; defensive equipment costs gauge, successful block increases it; quick/heavy chips speed gauge while not consuming it.', 'Source quoted everyday event says electric-stove cyberworld, no advance registration, unrelated to weekend tournaments; no inferred replacement venue added.', 'BBS widths, complete instruction runtime correctness and author headers not verified; mechanical pass is not semantic or human approval.'],units=units)

def main():
    a=create();path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored battle BBS125 draft only; ROM unchanged')

if __name__=='__main__':main()
