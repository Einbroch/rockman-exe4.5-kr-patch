"""Individually authored WoodMan seasonal draft, source-pinned and non-distribution."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['새해・・・\n복 많이 받아라!','짝짝!','위대한 대지여\n올해도 건강한\n1년을 보내게 하소서','짝짝!','、\n올해도 잘\n부탁한다'],
2:['오늘은 절분이다','그렇다면,\n내일은 입춘인가','달력상으로는,\n벌써 봄이구나','풀과 나무도 새로\n싹트는 좋은 계절이\n찾아올 거다'],
3:['오늘, 2월14일은\n발렌타인데이구나','초콜릿의\n원료는\n카카오 나무의 열매다','초콜릿 먹기 전에\n준 사람과 대지에\n감사하거라'],
4:['오늘, 2월14일은\n발렌타인데이구나','사랑 담은 초콜릿은\n직접 만든 게 좋구나','이런 말을 당일에\n해 봐야 소용없지만'],
5:['오늘은 3월3일,\n복숭아꽃 명절이구나','오늘은 복숭아꽃을\n보며 느긋하게\n쉬고 싶구나'],
6:['오늘은 5월5일\n일본 단오구나・・・','오늘 목욕은\n창포물로 하나?','창포물 목욕은,\n신경통, 류머티즘,\n어깨 결림에 좋다','또 액막이도\n된다니,\n꼭 한번 해 보거라'],
7:['오늘은 7월7일,\n칠석이구나・・・','나도 소원 쪽지에\n소원을 써 볼까\n・・・・・・','조금 살이 빠지길\n・・・이라고'],
8:['오늘은 크리스마스\n이브였구나・・・','아, 안 된다・・・\n그런 눈으로 봐도!!','크리스마스트리는\n되지 않을 거다!'],
9:['메리 크리스마스\n오늘은 크리스마스군','네가 있는 곳에\n산타클로스는\n찾아왔느냐?'],
10:['오늘은 섣달그믐이다','대청소는\n끝냈느냐?','대청소가\n끝났다면,','느긋하게 인터넷에\n가 볼까・・・'],
11:['오늘은 네\n생일이었구나','음, 결코\n잊고 있던 건\n아니다!','축하한다!!'],
12:['창립 기념일이다・・・\n학교는 쉬느냐?'],
17:['오늘은'],18:['「','」'],19:['이다・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6A2184.tpl';require_hash(p,'a3908de7e31d2ee1a7936c06be3bfd643fadadaecb7f843a9d145ca77af52faa');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6A2184:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6A2184'];validate_literal_numerals(units,scope);validate_nickname_suffix(units,'6A2184',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6A2184',source_archive_sha256='5d66c25b2ab48c88810e7dbfdd89b5f01b9c916d322925548a5d09aaa3c470ac',consumer='normal-dialogue',context='WoodMan seasonal/birthday conversations; intro69E088 names ウッドマン and earth blessing. Native intro root038368/seasonal+52 root03839C. Portrait92,110/3rows; global22,nickname and event loop unchanged. Normal unlock/date/name routes unverified.',voice='Tentative reserved, grounded older masculine voice, source hesitations and Christmas tree joke retained; not a human-approved voice rule.',evidence='analysis/full_scope_v1/source_tpl/69E088.tpl; analysis/full_scope_v1/source_tpl/6A2184.tpl; native roots038368/03839C',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All41 literals including2 unchanged quotes; IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. NewYear nickname1:4 first-line comma11px unchanged. No name/save/RTC/gameplay edits.',semantic_review=['NewYear shrine hand claps become 짝짝, not gunshots. Earth blessing and gratitude, seasonal sprouts and Christmas tree refusal retained.','March3 peach festival and May5 Japanese Tango with iris bath retained as source culture, not a Korean calendar substitution. Bath benefit dialogue is game-character speech, not verified medical guidance.','Honmei chocolate from a loved person, birthday forgotten denial and weight-loss wish retain source meaning. Culture/voice/terminology await human review; NumberMan4649 approval not reused.'],units=units)
    out=ROOT/'translations/woodman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('WoodMan41 serialized')

if __name__=='__main__':main()
