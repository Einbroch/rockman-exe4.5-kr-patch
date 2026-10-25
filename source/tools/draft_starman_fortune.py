"""Individually authored StarMan fortune/result129; draft only."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/6A3DD0.tpl'
SOURCE_SHA='adfb18edaca8c8b738d8a074d72ae4315c0290b618119a0e49dabb27173a69c2'
OUT='translations/starman_fortune_draft_ko.json'
DRAFT={
0:['팅클 팅클!','내 별점으로\n너의 운세를\n봐 줄게!!','팅클 팅클\n슈팅 스타!','.','.','.','반짝!','나왔어!!','오늘 너의 운세는\n.','.','.'],
1:['팅클 팅클!','스타맨의 별점\n오늘은 어떤 날이\n될까?','팅클 팅클\n슈팅 스타!','.','.','.','반짝!','나왔어!!','오늘 너의 운세는\n.','.','.'],
3:['샤이닝 스타!!','반짝, 엄청난 행운!\n어두운 우주를\n밝히는 빛의 별이야','반짝반짝반짝반짝!\n재물운이 오를\n예감이 팍팍!!','바이러스 버스팅에서\n제니의 향기가...','오늘의\n행운 아이템은...'],
4:['붉은 혜성!!','활활 타오르는\n불꽃의 별이네...','불과 관련된 것을\n조심해!','오늘의\n행운 아이템은...'],
5:['4등성!!','희미하게 빛나는 별이야','오늘은 그다지\n빛나지 못하겠네...','하지만, 너다운 모습을\n갈고닦으면,','강한 빛을 낼\n가능성이 있어!\n자신감을 가져!','오늘의\n행운 아이템은...'],
6:['위성!!','커다란 행성의\n주위를 도는\n작은 별이야!','인기 있는 사람 곁에\n있으면 좋은 일이 생길지도','싫어하지 않을 정도로\n가까이 가 보자!','오늘의\n행운 아이템은...'],
7:['슈팅 스타!!','어떤 소원이든\n맡겨 줘!!','칩 숍에서\n좋은 일이 생기기를!','.','.','.','이렇게 소원을\n빌어 보기도 하고!','오늘의\n행운 아이템은...'],
8:['1등성!!','번쩍번쩍 빛나는\n눈부신 별!!','오늘은 왠지\n스타가 될 것 같은\n예감이 드네!!','오늘의\n행운 아이템은...'],
9:['5등성!!','빛나고는 있지만\n좀 미묘한 느낌!','눈에 띄려 하면,\n역효과가\n날지도 몰라!','경솔한 발언을\n조심해!!','오늘의\n행운 아이템은...'],
10:['인공위성!!','이것이 바로\n과학의 결정체!!','첨단 기기에\n행운의 예감!!','오늘의\n행운 아이템은...'],
11:['스타더스트!!','우주를 떠도는\n별의 조각들!!','무언가의 조각과\n인연이 있을 것 같은 1일!','오늘의\n행운 아이템은...'],
12:['2등성!!','강한 빛을 내는 별!','오늘은 발언의 힘이\n커질 것 같아!','생각난 것은\n적극적으로\n말해 보자!','오늘의\n행운 아이템은...'],
13:['6등성...','희미하게 빛나는\n어두운 별!','그다지 눈에 띄지 않는\n1일이 될 것 같은\n예감이 드네','오늘의\n행운 아이템은...'],
14:['운석!!','사고가 날 예감!\n주위를\n잘 살펴봐!!','오늘의\n행운 아이템은...'],
15:['블랙홀...','빛마저 빨아들이는\n공포의 공간!','오늘은 위험한 1일이\n될 것 같아','이런 날에는 플러그인\n하지 말고 얌전히\n있는 편이...','오늘의\n행운 아이템은...'],
16:['3등성!!','환하게 빛나는\n밝은 별!!','친구와 우정이\n깊어질 것 같아!','적극적으로\n친구를 불러\n보면 좋겠어!','오늘의\n행운 아이템은...'],
17:['반짝이는 별!!','너의 재능이\n반짝 빛나는 1일이\n될 것 같아','자신 있는 분야에\n적극적으로\n도전해 보는 건 어때?','오늘의\n행운 아이템은...'],
18:['우메보시!!','뭔가 실수를\n저지르고 말 것 같아\n...','혹시 주변에\n폐를 끼쳤다면\n솔직하게 사과하자!','오늘의\n행운 아이템은...'],
20:['1~4의 숫자와\n관련된 곳에\n있을 것 같아!'],
21:['5~8의 숫자와\n관련된 곳에\n있을 것 같아!'],
22:['9~12의 숫자와\n관련된 곳에\n있을 것 같아!'],
23:['무서운 분위기의\n에어리어에 있을 것 같은\n예감이 들어!!'],
50:['실패하고 말았네\n별을 세는 건\n자신 있는데 말이야!'],
51:['해냈어!!','왠지, 머리를\n힘껏 굴린\n덕분에,','조금 성장한\n기분이 들어!!'],
52:['해냈어!!','...앗!\n드릴에 뭔가\n끼어 있어...','제니를\n얻었어!'],
53:['해냈어!!','...앗!\n드릴에 뭔가\n끼어 있어...','버그 조각','개를\n얻었어!'],
60:['아차...\n실패하고 말았어!'],
61:['해냈어!\n',',\n멋진 오퍼레이팅이야!','아, 잠깐만','편지 사이에서\n뭔가 나왔어\n......','「HP 메모리」다!!\n잘됐네!'],
62:['해냈어!\n',',\n멋진 오퍼레이팅이야!','아, 잠깐만','편지 사이에서\n뭔가 나왔어\n......','제니다!!\n잘됐네!!'],
63:['해냈어!\n',',\n멋진 오퍼레이팅이야!','아, 잠깐만','편지 사이에서\n뭔가 나왔어\n......','버그 조각','개다!!\n잘됐네!!']
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA);original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    if not all(t in original for t in ('スターマンのホシうらない','jumpIfInternet1 = 20','jumpIfInternet12 = 22','jumpIfUndernet4 = 23','callBufferRecordMinigameResults','checkGiveZenny','checkGiveBugFrags','printPlayerNickname')):raise ValueError('fortune context changed')
    values={f'6A3DD0:{s}:{i}':t for s,rows in DRAFT.items() for i,t in enumerate(rows)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=129 or set(values)!={x.key for x in selected}:raise ValueError('fortune129 scope '+str(set(values)^{x.key for x in selected}))
    units=[]
    for x in selected:
        t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('source row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('source numbers/tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='StarMan',context='Self-identified StarMan fortune0/1, random predictions3..18 and item-area hints20..23, arithmetic/drill and letter-minigame result branches50..63',variable_context='Native timed dots, printPlayerNickname, printBuffer and reward commands unchanged; comma after nickname avoids dependent particle. Source line topology preserved; consumer width and presentation pending.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x6A3DD0)
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6A3DD0',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='navi-home-quick-dialogue',context='All129 unselected Japanese literals in65-slot StarMan fortune/result archive. Original random weights and lucky-item native destinations unchanged. No game or reward execution.',voice='Playful friendly StarMan candidate register consistent with existing starman_seasonal_ko.json. Explicitly authored per entry, no automatic prose transformations.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve source IDs, numeric groups, timed literal boundaries, random branches, variable order, minigame/reward/flag commands, newline counts and trailing rows. Source ROM and baseline ROM untouched.',semantic_review=['우메보시18 is a conservative transliteration of umeboshi pickled plum, retaining the Japanese boshi/star joke as a review candidate rather than silently replacing it with a different food or star. Cultural wording/adaptation decision remains open.', '팅클 팅클/샤이닝 스타/슈팅 스타/스타더스트 are source-backed candidates; rank1..6 literal numbers retained. 1일 preserves source numeric1, wording/layout review pending.', 'Fortunes express predictions, not guarantees; program branch weights and lucky-item destinations are not translated into new gameplay rules.', 'Timed Japanese middle-dot literals explicitly drafted as ASCII dots at same boundaries; their waitSkip commands are unchanged. Numeric reward placement and real home/minigame display remain unverified.'],units=units)

def main():
    a=create();path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored fortune129 draft only; ROM unchanged')

if __name__=='__main__':main()
