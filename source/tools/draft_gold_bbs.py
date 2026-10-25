"""Individually authored Gold-tournament BBS90, original post boundaries."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/7011F0.tpl'
SOURCE_SHA='c9ee3225f3d99f31127b6f284caf83ab3e8dfe27e558e353b2de3d43508d4964'
OUT='translations/gold_bbs_draft_ko.json'
DRAFT={
0:['이 게시판은\n골드 토너먼트에 도전하는\n배틀러 여러분께서,','정보와 의견을\n교환하실 수 있도록\n마련한 곳입니다','골드 토너먼트를\n목표로 하는 분이라면\n어린이부터 어른까지,','자유롭게 글을 올려\n주셔도 됩니다','원하신다면\n제 경험담 등도\n들려 드리겠습니다!'],
1:['골드 토너먼트의\n참가 시험은\n꽤 어렵지 않나요?','저는 두 번째\n버스팅 레벨 심사를\n도저히 통과 못 하겠어요','좋은 비결은\n없을까요?','댓글\n잘 부탁드려요!','상관없는 얘기지만\n3번째 시험관 내비는\n좀 귀엽지 않나요?'],
2:['버스팅 레벨을 올리려면\n동시 격파가 효과적이라고\n자주들 말하지','동시 격파란\n말 그대로 여러 바이러스를\n동시에 쓰러뜨리는 거야','또 카운터도\n점수가 높다는군!','한마디로\n멋지게 승리하라!!\n이걸 가슴에 새겨!'],
3:['뭔가\n잊으신 것 아닙니까?\n형씨!','버스팅 레벨에는\n속도도 중요하단\n말씀입죠!','눈 깜짝할 새에 바이러스를\n싹 쓸어버린다!\n질풍처럼 말입죠!','속도는 배틀의 꽃!!\n부지런히 실력을\n갈고닦으십쇼'],
4:['역시\n버스팅 레벨을\n올리려면','평소의 노력이\n최고지!!\n뻔한 말이지만 말이야'],
5:['모치미치님 말씀대로\n맞는 말이네요','그런데 여러분\n평일에는 배틀 연습을\n어떻게 하시나요?','저는 에브리데이 토너먼트에\n참가해서 기술을\n갈고닦고 있어요','이 근처라면\n고장 난 라디오 전뇌에서\n열리고 있어요','만나면 말 걸어 주세요'],
6:['이 글을 쓰는 날은\n화요일인데,','인터넷 에어리어에서\n유난히 탄내가 나더라고','왜냐고? 불 속성\n바이러스가 이상하게\n많았기 때문이었지!','화요일이라 불인가...','요즘 바이러스는\n말장난도 통하나 봐'],
7:['아래 글을 쓴 뒤,\n하룻밤이 지났어요\n그러니까 수요일이에요','이번엔 물 속성이었어요!','좀 뻔하네요'],
15:['폭주 내비가\n계속해서 나타나니\n정말 곤란하네요!','원인이 뭘까요?'],
16:['저도 자세히는\n모르지만...','폭주의 원인은\n그 내비 자체에\n있는 것이 아니라...','다른 커다란\n힘이 영향을\n주는 것 같아요','왠지 불안한\n기분이 드네요'],
17:['경솔한 이야기라\n죄송하지만..','폭주 내비를\n한번 보고 싶지\n않으신가요?','위험하다! 할수록\n보고 싶어지는 이 기분...','여러분도 아시겠죠?'],
18:['배틀을 공부하려고\n오피셜 토너먼트를\n보러 갔어','으아아아','소리가 날 정도로 달랐어\n정말 최고봉이라는 느낌!','하아...','나도 언젠가는 그곳에서,\n배틀해 보고 싶어'],
19:['오피셜 토너먼트는\n참가 등록만 해도\n꽤 힘들다고 하오','소문에 따르면 말이오...','어둠의 인터넷에서\n무사히 돌아오는 것이\n조건이라고 하오','게다가 정체 모를\n프로그램과 싸워야\n한다고 들었소','뭔가\n다른 세상\n이야기 같지 않소'],
20:['안녕하십니까! 저는 텟신임다','저는 골드 토너먼트에\n처음 참가했는데\n1회전에서 박살 났슴다','분하고 분해서\n베개를 눈물로\n적셨슴다','지금은 복수를 위해\n맹훈련 중임다','저는 필사적임다!\n이대로는 고향 부모님을\n뵐 면목이 없슴다!!'],
21:['또 토너먼트에서\n져 버린 텟신임다','아아, 전뇌의 신이시여!','저는 이렇게 노력하고\n있는데\n왜 이길 수 없슴까?','그러고 보니\n토너먼트 다음 날은\n쓰레기 수거일이라 들었슴다','넷 배틀러를 포기하고\n쓰레기 줍는 일로 전직할까\n생각 중임다..'],
22:['텟신님\n포기하시면 안 돼요!!','좌절은 어떤\n넷 배틀러든 한 번은\n거치는 길이에요!','노력은 재능을\n뛰어넘는다고\n믿으세요!!'],
23:['안녕하십니까! 텟신임다\n유키님, 격려의 말씀\n감사함다!','유키님의 기대에\n보답하기 위해서라도\n포기하지 않기로 했슴다','그래서 저는\n배틀 칩 게이트를\n써 보기로 했슴다','칩 게이트를 쓰기 시작하니\n상황에 맞춰 칩을\n쓸 수 있게 되었슴다','이걸 잘 다루게 되면\n토너먼트 제패도\n불가능하지 않겠슴다!','꿈이 커져 가는 검다!!!'],
24:['텟신님, 안녕하세요!','게이트에 쓰는 칩은\n칩마다 사용 횟수가\n정해져 있다는 건 아시죠?','남은 횟수가 적어지면\n금색 프로그램군에게\n말을 걸어 보세요','그 자리에서\n배틀 칩의 사용 횟수를\n회복해 준답니다!','금색 프로그램군은\n인터넷\n어딘가에 있어요','금색은 눈에 띄니까\n분명 찾을 수 있을 거예요'],
25:['칩 게이트를\n쓰고 있을 때도','동시에 일반\n칩 폴더의 칩도\n함께 쓰면 좋아','전략의 폭이\n더 넓어지는 거지!'],
26:['기초적인\n질문이라고\n웃지 마...','「칩 게이트에서\n 프로그램 어드밴스는\n 어떻게 쓰나요?」','젠장! 엄청 창피하네\n이러면 초보자라는 게\n너무 티 나잖아!'],
27:['배틀 이야기가 나오면\n꼭 달려오는 남자\n코에츠 형이야!','칩 게이트 이야기로\n한창 신난 모양이네!','칩 게이트에서 프로그램\n어드밴스를 쓰는 방법은,\n그렇게 복잡하지 않아','셀렉트 버튼을 누르면,\n칩을 입력할 수 있는\n시간이 시작되고...','순서대로 배틀 칩 3개를\n게이트에 슬롯 인!','이걸로 OK야\n칩 게이트가 없을 때와\n그렇게 다르지 않지?']
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA);original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    if not all(t in original for t in ('このケイジバンは','ゴールドトーナメント','テッシン','セレクトボタン','BBS01 ID15','BBS01 ID2F','left = 32','top = 68')):raise ValueError('BBS context changed')
    values={f'7011F0:{s}:{i}':t for s,rows in DRAFT.items() for i,t in enumerate(rows)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=90 or set(values)!={x.key for x in selected}:raise ValueError('bbs90 scope '+str(set(values)^{x.key for x in selected}))
    units=[]
    for x in selected:
        s=int(x.key.split(':')[1]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('source row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('source numbers/tokens '+x.key)
        speaker='Tesshin-self-identified' if s in (20,21,23) else 'Koetsu-self-identified' if s==27 else f'BBS-post-{s}; author not inferred'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,context='Complete Gold-tournament BBS posts0..7/15..27: admission, busting-level advice, weekdays, rampaging Navi concern, tournament impressions, Tesshin encouragement/recovery and Chip Gate instructions',variable_context='No dynamic name substitutions; each source post and page boundary retained. Quoted ASCII BBS placeholder IDs remain untouched; actual BBS width and post ordering runtime review pending.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x7011F0)
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='7011F0',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='bbs-text',context='All90 Japanese literals in48-slot Gold BBS archive. Whole posts and quoted reply relationships read together, no inferred identity for unidentified posters. ASCII placeholders are not localized or excluded from other-review ledger.',voice='Source formal/modest/casual/rough registers distinguished per post. Tesshin marked ッス drafted as 임다/슴다 candidate; original19 ゴワス as 하오 candidate. Human voice review pending.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve source IDs, reply/page/quote boundaries, weekday-element wordplay, instruction order SELECT then3 ordered chips, limits/restoration vs chip availability, and all command arguments. No ROM or save writes.',semantic_review=['Names 텟신/유키/코에츠/모치미치 and 프로그램군/버스팅 레벨/프로그램 어드밴스/배틀 칩 게이트 are source-backed draft candidates, not new human approvals. 에브리데이 토너먼트 follows existing keyitem_full_rom_ko.json.', 'Source26 asks a question and27 answers; source20..24 refusal to give up and restoration advice read together. Source19 rumor remains hearsay, not a verified required route.', '火曜/水曜 weekday-element wordplay works with 화요일/수요일 in Korean; preserve joke and adjacent reply without changing game behavior.', 'Instructions retain button then timed chip acceptance then3 chips in order; golden program restores usage count, not newly grants chips. BBS final layout and each post author binding outside the source body are unverified.'],units=units)

def main():
    a=create();path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored gold BBS90 draft only; ROM unchanged')

if __name__=='__main__':main()
