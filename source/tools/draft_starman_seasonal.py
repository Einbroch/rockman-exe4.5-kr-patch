"""Individually authored StarMan draft; immutable source and explicit cultural context."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['아,\n새해 복 많이 받아!','새해 첫꿈은 좋았어?','1후지산,2매,3가지\n라고 하는데,','방금 그 3가지가\n새해 첫꿈에 나오면\n길한 징조래!'],
2:['오늘은 절분이네!','콩 뿌리기처럼\n소소한 말은 말고,','유성우라도\n내려 줄까!?','농~담이야!'],
3:['오늘은・・・\n발렌타인데이야!','어젯밤에,\n오늘 초콜릿을 많이\n받게 해 달라고,','별똥별에 소원을\n빌어 놨어!'],
4:['오늘은・・・\n발렌타인데이야!','좋아하는 사람에게\n초콜릿을 주려면,','꽤 큰 용기가\n필요하지!!'],
5:['오늘은・・・\n3월3일,히나마쓰리!','히나 인형은,\n참 예쁘지!','나도 그런 기모노,\n입어 보고 싶어!'],
6:['오늘은・・・\n5월5일,어린이날!','재작년보다 얼마나\n키가 컸어?','기둥에 낸 자국으로\n확인해 보는 건 어때?','그런데・・・\n왜 작년이\n아닌 걸까?'],
7:['오늘은,\n칠석이야!','너는 은하수를\n본 적 있어?','그건 굉장해!\n사람의 손으로는\n만들 수 없는','드넓은 하늘의\n빛의 축제!!','분명,감동할 거야'],
8:['아, 오늘은\n크리스마스이브지!','화이트 크리스마스도\n좋지만,','별빛 크리스마스도\n멋지거든!!','겨울 하늘은 공기가\n맑아서,','별이 정말\n아름답게 보여!'],
9:['메리 크리스마스!!','어제 별이 빛난 밤은\n어땠어?','겨울철 대삼각형은\n볼 수 있었을까?','북두칠성도\n아름다워!','・・・아, 맞다!','북극성도\n아름답게\n빛나고 있어!'],
10:['오늘은 12월31일,\n섣달그믐이야!!','올해의 밤하늘은\n오늘이 마지막!','오전0시가 지나면,\n내년의 밤하늘이\n되어 버리니까!'],
11:['생이이이이일\n축하해애애애!!','새 나이를 맞은\n너에게 좋은 일이,\n생기길 바라!!'],
12:['창립 기념일이야!','오늘은 학교,\n쉬는 날이지?'],
17:['오늘은'],18:['「','」'],19:['이야!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6A8ADC.tpl';require_hash(p,'2573ccbd2799ba2ac448b7e37162640884960da843556f5ea8ca7d24b0154081');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6A8ADC:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6A8ADC'];validate_literal_numerals(units,scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6A8ADC',source_archive_sha256='bb9b7965f03aab554b30ef692eac20fa01090bf3881e8ce363efa5d66038f3d1',consumer='normal-dialogue',context='StarMan seasonal/birthday dialogue; intro6A383C names スターマン and sparkle. Native intro root0383A4/seasonal+52 root0383D8. Portrait92,110/3rows; global22,event buffer/loop unchanged; no nickname insertion in this archive. Normal unlock/date/gender/event routes unverified.',voice='Tentative cheerful conversational voice; meteor-shower joke and elongated birthday shout retained. Human wording/culture/voice review pending.',evidence='analysis/full_scope_v1/source_tpl/6A383C.tpl; analysis/full_scope_v1/source_tpl/6A8ADC.tpl; native roots0383A4/0383D8',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All48 literals including2 unchanged quotes; IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. No name/save/RTC/gameplay edits.',semantic_review=['First dream of NewYear keeps ranked1Fuji/2hawk/3eggplant Japanese custom, not three generic lucky objects. Calendar dates remain Japanese source culture.','Height question retains year-before-last and the following explicit why-not-last-year question, not a corrected last-year substitution.','Meteor shower instead of beans is an immediately retracted joke. Milky Way/light festival, winter triangle/Big Dipper/Polaris and midnight year transition retain source meaning. Birthday vowel elongation is a draft voice decision; NumberMan4649 approval not reused.'],units=units)
    out=ROOT/'translations/starman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('StarMan48 serialized')

if __name__=='__main__':main()
