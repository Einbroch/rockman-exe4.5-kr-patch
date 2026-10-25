"""Individually authored Blues seasonal draft with immutable source bindings."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['새해가 밝았습니다\n새해 복 많이 받으세요','올해도 부디\n잘 부탁드립니다','그런데,\n새해 첫 참배는\n벌써 다녀오셨나요?','괜찮으시면 저도\n가 보고 싶은데\n가도 괜찮을까요?'],
2:['오늘은 절분입니다','콩을 뿌려서\n도깨비를 쫓아내는\n날입니다・・・','바이러스 퇴치와\n비슷하네요・・・'],
3:['오늘은,\n발렌타인데이입니다','초콜릿을,\n받으시면 좋겠네요'],
4:['오늘은,\n발렌타인데이입니다','원래 외국에서\n들어온 풍습\n이지만,','쉽게 고백하지\n못하는 내성적인 분께\n더없이 좋은 기회죠'],
5:['오늘은 3월3일,\n복숭아꽃 절기,\n히나마쓰리 날입니다','우리 같은 남자는\n별로 관련이\n없지만,','히나아라레 정도는\n먹을 수 있겠네요'],
6:['오늘은 5월5일\n단오절이자,\n어린이날입니다'],
7:['오늘은 7월7일,\n칠석입니다','소원 쪽지에는\n어떤 소원을 쓰실\n생각인가요?'],
8:['오늘은,\n크리스마스이브입니다','이맘때가 되면,\n산타클로스로\n자주 오해받습니다','색이 비슷해서\n그렇겠지요'],
9:['메리 크리스마스!\n오늘은 크리스마스죠','25일은 축제가\n끝난 듯한\n쓸쓸함이 있네요'],
10:['오늘은 섣달그믐입니다','내일은 새로운 해가\n시작되겠네요','새해를 맞이할\n준비는\n되어 있으신가요?'],
11:['생일을,\n축하드립니다','앞으로도 잘\n부탁드립니다'],
12:['창립 기념일입니다\n오늘 학교는\n쉬는 날인가요?'],
17:['오늘은'],18:['「','」'],19:['입니다・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/685C68.tpl';require_hash(p,'d0c842e509eeb40e58f152cf111834a27675eb315f9843419e3b835276f87659');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'685C68:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='685C68',source_archive_sha256='f0f6a9a5af8202801fb267770735dbbbe490c2abce6e45469059f3d6b15fab76',consumer='normal-dialogue',context='Blues seasonal/birthday operator conversations. Source intro681AB8 explicitly names ブルース with formal greetings. Native60byte Navi group intro root03823C and seasonal+52/root038270. Portrait92,110/3rows; global22 gender branch and anniversary buffer/loop preserved. Normal unlock/date path unverified.',voice='Polite source ワタシ/です/ございます/よろしいでしょうか motivates courteous Korean operator-address voice; human review pending.',evidence='analysis/full_scope_v1/source_tpl/681AB8.tpl; analysis/full_scope_v1/source_tpl/685C68.tpl; native roots03823C/038270',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All33 source literals including2 unchanged quote literals; IDs/text,dates/numerals,newline counts/boundaries,21slots,commands and event controls preserved. No name/save/RTC/gameplay edits.',semantic_review=['Hatsumode rendered 새해 첫 참배, keeping visit/permission questions. Hina-arare name retained, Momo no Sekku as 복숭아꽃 절기; culture/terminology review pending.','Japanese Tango no Sekku rendered 단오절 with source5월5일 and 어린이날 retained, not a claim about Korean lunar Dano. Culture wording and courteous voice remain needs_review.','Source red color/Santa misunderstanding and25th post-festival loneliness retained without added jokes.'],units=units)
    out=ROOT/'translations/blues_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('Blues33 serialized')

if __name__=='__main__':main()
