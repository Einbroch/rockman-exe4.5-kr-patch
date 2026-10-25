"""Context-authored SearchMan draft; source fields serialized without rewriting."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['새해 복 많이\n받으십시오!','올해도 잘\n부탁드립니다','올해 첫\n미션은\n아직입니까・・・'],
2:['오늘은 절분입니다','도깨비를 제거하는\n미션・・・\n콩을 뿌립시다','목표・・・도깨비!\n록온!!'],
3:['오늘은 발렌타인\n데이군요・・・','、\n초콜릿 획득\n확률은・・・','・・・60퍼센트!','어머님은 계산에\n넣지 않았습니다・・・'],
4:['오늘은 발렌타인\n데이군요・・・','초콜릿을\n줄 대상은,','이미 록온해\n두셨습니까?'],
5:['오늘은 3월3일,\n히나마쓰리입니다','히나 인형은,\n마트료시카 인형처럼\n화려하군요'],
6:['오늘은 5월5일\n어린이날입니다','일본 전통의\n갑옷과 투구를 장식\n・・・・・・','제게는,\n무척 흥미로운\n날입니다・・・'],
7:['오늘은 7월7일,\n칠석입니다','기상 탐색!','오늘 밤 은하수를\n볼 수 있는 확률은\n・・・・・・','・・・55퍼센트!!'],
8:['오늘은,\n크리스마스이브입니다','화이트 크리스마스가\n될 확률은・・・','・・・45퍼센트!','다만 지역에 따라\n차이가 있습니다'],
9:['메리 크리스마스!!','산타클로스는\n나타났습니까?','올해도 이제\n곧 끝나겠군요・・・'],
10:['오늘은 섣달그믐,\n올해의 끝입니다・・・','제야의 종소리를\n들으면서,','엄숙하게 새해를\n맞이합시다・・・'],
11:['생일을,\n축하드립니다','오퍼레이트 실력을\n더욱 갈고닦으십시오'],
12:['오늘은,\n창립 기념일입니다','학교는 쉬는\n날입니까?'],
17:['오늘은'],18:['「','」'],19:['입니다・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/675440.tpl';require_hash(p,'26b77c7badf06979641c3b872f2e2f8d82dd966c435be3e08254c914f93ba90d');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'675440:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['675440'];validate_nickname_suffix(units,'675440',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='675440',source_archive_sha256='aa4125147506b7467818e08c32c0d5e54597da39ad69ce220ce62ec7224f3973',consumer='normal-dialogue',context='SearchMan operator holiday/birthday conversations. Source intro670DF4 explicitly identifies SearchMan; native60-byte Navi group seasonal+52/root0381BC. Source portrait92,110/3rows; global22 branch,60/55/45 literal probabilities, dates and anniversary buffer/loop retained. Normal unlock route unverified.',voice='Source polite military mission/target/lock-on vocabulary motivates tentative formal 합니다/습니까 voice, human review pending.',evidence='analysis/full_scope_v1/source_tpl/670DF4.tpl; analysis/full_scope_v1/source_tpl/675440.tpl; native root0381BC',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All40 source literals including2 unchanged quote literals; source IDs/text,numbers,newline counts,21slots,gender branch,printPlayerNickname and anniversary buffer/loop preserved. Nickname3:1 first line changes source の to invariant 、 (same11px) without adding Hangul particle. No name/save/RTC/gameplay edits.',semantic_review=['Japanese Setsubun/Hinamatsuri and May5 armour custom retained; matryoshka comparison kept. Culture/voice review pending.','Source Weather Search exclamation translated contextually as 기상 탐색!, not an approved equipment/attack name. Mission/target/lock-on voice draft requires review.','Birthday operation-skill wish and source literal likelihoods retained. No actual probability/gameplay calculation is changed.'],units=units)
    out=ROOT/'translations/searchman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('SearchMan40 serialized')

if __name__=='__main__':main()
