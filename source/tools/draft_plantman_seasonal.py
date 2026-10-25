"""Individually authored PlantMan draft; source-pinned nickname and metaphor scope."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['、\n새해 복 많이 받아\n올해도 잘 부탁해','그런데,가가미모치\n위에 귤이\n올려져 있지?','그건 귤이 아니라,\n다이다이라는 등자야','집안이 먼 훗날까지\n대대로 오래오래','번영하기를\n바라는','기도가 담긴\n길한 물건이란다'],
2:['오늘은 절분이야','콩 뿌리기의 대두는\n반드시 불에\n볶은 걸 쓰고,','생콩을\n써서는 안 된단다','왜냐면,생콩이면\n콩을 뿌린 뒤,','시간이 좀 지나면,\n싹이 나 버리기\n때문이야'],
3:['오늘은,\n발렌타인데이구나','발렌타인 하면\n초콜릿이지','초콜릿의 원료는\n카카오라는 나무의\n열매란다'],
4:['오늘은,\n발렌타인데이구나','너의 사랑의 꽃이,\n멋지게 피어나면\n좋겠네・・・훗'],
5:['오늘은 복숭아 절기,\n히나마쓰리 날이네','복숭아꽃은 좋지\n연한 분홍빛의\n작은 꽃・・・','화려하진 않지만,\n일본다운','그윽한\n아름다움이 있어'],
6:['오늘은 5월5일\n단오 절기인,\n어린이날이네・・・','이 풍습은 말이지,\n아주 먼 옛날에,\n중국에서','전해진 거라고\n하더구나・・・'],
7:['오늘은 7월7일,\n칠석날이야','칠석 밤하늘을\n물들이는 은하수는','형형색색의\n꽃다발로도,','견줄 수 없는\n아름다움이 있지・・・'],
8:['오늘은,\n크리스마스이브야','크리스마스 거리는\n마치,형형색색의\n꽃밭 같구나'],
9:['메리 크리스마스\n오늘은 크리스마스야','크리스마스\n장식은 오늘까지야\n조금 쓸쓸하구나'],
10:['오늘은 섣달그믐,\n올해도 얼마 안 남았네','아,올해도 끝인가\n・・・','왠지 애틋하구나'],
11:['、\n생일,\n축하한다!','나무로 비유하면,\n나이테가 1개\n늘었구나・・・','더 크게,\n더 아름답게,\n더 씩씩하게','성장하렴'],
12:['오늘은 학교\n개교 기념일이\n아니었나?'],
17:['오늘은'],18:['「','」'],19:['이란다・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6D0ADC.tpl';require_hash(p,'effe34f68a756bb7396c8bc04275c8f5936776ab75ba8cf51ea6c4a8727db520');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6D0ADC:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6D0ADC'];validate_literal_numerals(units,scope);validate_nickname_suffix(units,'6D0ADC',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6D0ADC',source_archive_sha256='b91a0175b8ad929c797e62ab9c93d8fe20aacbb9a606daeaea94cf9ec9809e62',consumer='normal-dialogue',context='PlantMan seasonal/birthday dialogue; intro6CC808 names プラントマン and flower/life metaphor. Native intro root03850C/seasonal+52 root038540. Portrait92,110/3rows; global22,two nickname prints and event buffer/loop unchanged. Normal unlock/date/name/gender/event routes unverified.',voice='Tentative elegant conversational voice, gentle instruction and restrained chuckle; human terminology/wording/culture review pending.',evidence='analysis/full_scope_v1/source_tpl/6CC808.tpl; analysis/full_scope_v1/source_tpl/6D0ADC.tpl; native roots03850C/038540',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All43 literals including2 unchanged quotes; IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. Nickname1:0/11:0 first-line comma11px unchanged; no name/save/RTC/gameplay edits.',semantic_review=['NewYear kagami-mochi fruit is not mikan but daidai. Draft retains 다이다이 as source fruit name plus 등자 and 대대로 long-lasting family prosperity/prayer/lucky object. Meaning and Japanese name remain, but Japanese homophony is not reproduced in Korean; human adaptation review pending, no NumberMan4649 approval reuse.','Setsubun requires roasted beans rather than raw because raw beans later sprout; plant-centric reason retained, not replaced with generic safety warning.','Cacao tree fruit, love flower, subdued Japanese peach-blossom beauty, Japan May5 Tango/child holiday and reported ancient Chinese origin retain source culture/date/modality.','MilkyWay more beautiful than colorful bouquets, Christmas town like a flower field, year-end wistfulness and birthday tree-ring1 growth metaphor retained.'],units=units)
    out=ROOT/'translations/plantman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('PlantMan43 serialized')

if __name__=='__main__':main()
