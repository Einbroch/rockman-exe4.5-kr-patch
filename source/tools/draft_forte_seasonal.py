"""Individually authored Forte seasonal draft; silence and native routing preserved."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['새로운 해가\n밝았군・・・','그건 내게,\n새로운 싸움의\n막이 오른다는 뜻이다','・・・・・・'],
2:['절분이다・・・','콩 뿌리기・・・?','흥,인간에게는,\n나도 도깨비와 별로\n다르지 않겠지・・・'],
3:['발렌타인데이다\n・・・・・・','뭘 기다리는 거냐?\n네가 좋아하는\n여자의 초콜릿은','스스로의 힘으로\n빼앗는 것 아니냐?'],
4:['발렌타인데이다\n・・・・・・','좋아하는 남자가\n있다면,','힘으로라도,\n초콜릿을\n건네도록 해라・・・'],
5:['히나마쓰리다・・・','・・・여자아이의\n축제라고?','・・・흥,시시하군!'],
6:['어린이날이다・・・','여기저기 갑옷이\n장식돼 있더군,','보아하니,오늘은\n싸움의 날인 모양이군'],
7:['칠석이다・・・','・・・소원 종이에\n소원을・・・?','난\n소원을 빌지 않는다','자신의 소원은\n자신의 힘으로\n이루기 때문이지'],
8:['크리스마스이브다・・・'],
9:['크리스마스다・・・'],
10:['섣달그믐이다・・・','인간들이 야단을\n떨고 있지만,','흥,오늘로 올해가\n끝나든 내겐\n상관없다・・・'],
11:['흥,오늘은\n네놈의 생일\n이었지・・・'],
12:['개교 기념일\n이었지・・・'],
17:['오늘은'],18:['「','」'],19:['이다・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6D5A9C.tpl';require_hash(p,'05c158cc9a64bd38ace280249110baa33835fadc88d3a4f864c8a31ed97df6c6');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6D5A9C:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6D5A9C'];validate_literal_numerals(units,scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6D5A9C',source_archive_sha256='56a0883fa115c2101bcd78178458caae82213a8ca43889afbc76199e7f933e2a',consumer='normal-dialogue',context='Forte seasonal/birthday dialogue; intro6D2180 rough contempt for human PET and destruction, same-group jack-in6D27A0 explicitly names フォルテ.EXE. Native roots038548 intro/038558 jack-in/03857C seasonal. Portrait92,110/3rows; global22,event buffer/loop unchanged; no nickname insertion. Normal unlock/date/gender/event routes unverified.',voice='Tentative terse rough voice, haughty contempt, self-reliance and exact silence retained. Human terminology/wording/voice review pending.',evidence='analysis/full_scope_v1/source_tpl/6D2180.tpl; analysis/full_scope_v1/source_tpl/6D27A0.tpl; analysis/full_scope_v1/source_tpl/6D5A9C.tpl; native roots038548/038558/03857C',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All33 literals:30 prose,2 unchanged quotes,1 unchanged six-dot silence. IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. No name/save/RTC/gameplay edits.',semantic_review=['NewYear means opening of another battle, not a warm greeting; explicit separate silence1:2 retained as six native dots.','Setsubun oni likeness is accepted from human perspective, unlike ElecMan denial. Valentine stealing/giving chocolate by force remains fictional harsh character speech, not a real-world recommendation.','Armor leads to mistaken battle-day interpretation; Tanabata wishes are achieved by own strength rather than prayer, not softened into wishing success.','Birthday merely recognizes date without adding congratulations or affection; festival contempt/year-end indifference and ellipses retained. NumberMan4649 approval not reused.'],units=units)
    out=ROOT/'translations/forte_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('Forte33 serialized')

if __name__=='__main__':main()
