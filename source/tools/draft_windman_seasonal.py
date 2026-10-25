"""Individually authored WindMan draft; immutable source identities are serialized."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['후슈・・・\n새해 복 받거라!!','올해도 잘\n부탁하마','연을 날리러\n가지 않겠느냐?','설날에는 역시\n연날리기지','좋은 바람이 부는군!'],
2:['후슈・・・\n오늘은 절분인가・・・','조금 쌀쌀하지만,\n벌써 봄이로군・・・','곧 첫 봄바람이\n불겠지'],
3:['후슈・・・','오늘은 발렌타인\n데이라는 날이지・・・','여성이 좋아하는\n남성에게\n초콜릿을 준다더군','・・・초콜릿이라\n・・・달콤하고도\n묘한 풍습이로군'],
5:['후슈・・・','오늘은 3월3일\n복숭아꽃 명절인\n히나마쓰리로군','오늘은 아마자케를\n마시면서,\n푹 쉬는 게 좋겠군'],
6:['후슈・・・','오늘은 5월5일\n단오 명절이다・・・','잉어 깃발이 바람에\n나부끼는, 내가\n좋아하는 날이다・・・'],
7:['후슈・・・','오늘은7월7일,\n칠석인가・・・','바람 방향이 좋고,\n구름이 끼지 않으면,','은하수를 볼 수\n있겠군・・・'],
8:['후슈・・・','오늘은,\n크리스마스이브라는\n날이라더군・・・','내게는 별로\n익숙하지 않다만・・・','무슨 축제인가?'],
9:['후슈・・・','메리 크리스마스!!','다들 그렇게\n말하기에,\n나도 해 봤다만,','무슨 주문인가?'],
10:['후슈・・・','오늘은 섣달그믐・・・\n올해 마지막 날이다','「마무리가 좋으면\n 모두 좋은 법」','이라는 말까지\n있지 않느냐・・・','너무 들뜨지는\n말거라'],
11:['후슈・・・','오늘은 네\n생일이었지','축하한다・・・','너를 낳아 주신\n부모님께\n감사하거라'],
12:['후슈・・・','오늘은 학교의\n창립 기념일이로군','학교가 쉬어도,\n놀기만 해서는\n안 된다・・・'],
17:['오늘은'],18:['「','」'],19:['이로군・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/66F78C.tpl';require_hash(p,'4fb6eaac8efabe6bf2ae7bf3c5b04050fa93a71883c6ce752f270dc35392819f');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'66F78C:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='66F78C',source_archive_sha256='bc18012be15429b1253d6e546b2ab94755537ecbb3b6104881a8f58117d5ba2f',consumer='normal-dialogue',context='WindMan operator holiday/birthday conversations. Source intro66B8B0 explicitly names WindMan; seasonal root038180 minus52 is its intro in the native60-byte Navi group. Portrait92,110/3rows; original dates and anniversary buffer/loop preserved. Normal unlock route not established.',voice='Source calm elder-like forms たのむぞ/おる/するがいい motivate tentative 하마/하거라/이로군. Candidate voice, not human approved.',evidence='analysis/full_scope_v1/source_tpl/66B8B0.tpl; analysis/full_scope_v1/source_tpl/66F78C.tpl; native root038180',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All46 source literals including two unchanged quotes; source text, numbers, newline counts,21slots, commands/events and anniversary dynamic buffer/loop preserved. No name/save/RTC/gameplay edits.',semantic_review=['66F78C:3:3 source chocolate/okashi(strange/sweets) pun: 달콤하고도 묘한 is a contextual adaptation proposal, not approved wordplay. NumberMan4649 approval does not apply.','Setsubun, peach-blossom Hinamatsuri, Japanese May5 Tango, Tanabata, amazake and first spring wind retained in their original calendar context. No Korean-calendar replacement.','Source NewYear kite custom and year-end proverb translated contextually; wording/voice review pending.'],units=units)
    out=ROOT/'translations/windman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('WindMan46 serialized')

if __name__=='__main__':main()
