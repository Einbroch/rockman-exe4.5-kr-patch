"""Individually authored ElecMan seasonal draft; not a prose transformation."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['아,\n새해 복 많이 받아!','뭐,새해 인사\n정도는 활기차게\n해야겠지'],
2:['오늘은 절분인가・・・\n콩을 뿌려야겠군','뭐,뭐야 그 눈빛은\n・・・!?','내 머리\n양쪽이\n뾰족하다고 해서,','난,도깨비가 아니야!','게다가 전기를\n다룬다고 해서\n천둥신도 아니라고!','나보단 오히려\n썬더맨 쪽이,\n도깨비 같잖아!!'],
3:['그러고 보니,오늘은\n발렌타인데이군','그렇게 초조해 마\n의리 초콜릿\n1개쯤은 받겠지'],
4:['그러고 보니,오늘은\n발렌타인데이군','여자아이에게,\n오늘은 어떤 의미로,\n승부의 날이지・・・'],
5:['오늘은 히나마쓰리군','요즘 히나 등은\n촛불이 아니라\n전구를 쓰더군','그만큼 전기가\n안전하고 쓰기\n편하다는 거지','・・・그래그래'],
6:['오늘은 5월5일\n어린이날이군','잉어 깃발도,성탄\n트리처럼,','전구를 달아서\n빛나게 하면 좋겠군'],
7:['오늘은 칠석인가・・・','오늘 밤만큼은,\n불을 끄고\n은하수를 봐야겠군'],
8:['오늘,크리스마스이브다','난 말이지,온 거리가\n전기로 반짝이는\n크리스마스가 좋아!'],
9:['메리 크리스마스!!','크리스마스는 24일이\n절정이지・・・','25일 밤이면,\n전구 장식은\n철거돼 버려!','내겐,\n오늘이 1년 중 가장\n쓸쓸한 날이라고!'],
10:['오늘은 섣달그믐인가','올해1년,여러 일이\n있었지만,오늘로 전부\n리셋이다!!','싫었던 일도・・・\n힘들었던 일도・・・','전부,그래,전부\n리세에에에엣!!'],
11:['오늘이 네\n생일이었지','축하한다','특별히 선물은\n없어'],
12:['오늘은 학교\n개교 기념일이군','쉬는・・・날이었지?'],
17:['오늘은'],18:['「','」'],19:['이군・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6CB184.tpl';require_hash(p,'713d09a2ee410de78b1a9406fc617a8c09516c7e37b169eadd7f2766e515ff8b');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6CB184:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6CB184'];validate_literal_numerals(units,scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6CB184',source_archive_sha256='8680c27d7155f430cd1e739b0e770ccb72822c744471144008546f423963d257',consumer='normal-dialogue',context='ElecMan seasonal/birthday dialogue; intro6C7084 names エレキマン and reserved stimulating-days voice. Native intro root0384D0/seasonal+52 root038504. Portrait92,110/3rows; global22,event buffer/loop unchanged; no nickname insertion. Normal unlock/date/gender/event routes unverified.',voice='Tentative reserved colloquial voice with emphatic oni denial, illumination enthusiasm and elongated reset shout. Human terminology/wording/voice review pending.',evidence='analysis/full_scope_v1/source_tpl/6C7084.tpl; analysis/full_scope_v1/source_tpl/6CB184.tpl; native roots0384D0/038504',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All40 literals including2 unchanged quotes; IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. No name/save/RTC/gameplay edits.',semantic_review=['Setsubun denies being an oni despite pointed head, then denies being a thunder deity despite electricity, contrasting ThunderMan. カミナリ deity sense is attested in Kanjipedia; selection is an inference from this head/oni/electricity context, still human-review pending.','Giri chocolate1 and female Valentine victory-day branch retained; tentative 초조해 preserves nervous ピリピリ rather than inventing shock gameplay.','Hina lamps use bulbs not candles, illuminated carp-streamer wish, Tanabata lights-off/MilkyWay, Christmas lighting removed on25 and loneliest day of1year preserved as character claims. All numerals24/25/1/5/5 unchanged.','NewYearEve emphatic reset concerns unpleasant memories, not a game-save reset instruction; birthday explicitly has no gift. NumberMan4649 approval not reused.'],reference_sources=[dict(url='https://www.kanjipedia.jp/kotoba/0007025300',scope='Dictionary sense2 of カミナリ includes a deity causing thunder; scene interpretation is provisional, not a source assertion about this game.')],units=units)
    out=ROOT/'translations/elecman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('ElecMan40 serialized')

if __name__=='__main__':main()
