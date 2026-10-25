"""Individually authored KnightMan draft with protected nickname append boundaries."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['새해가 밝았습니다\n복 많이 받으십시오','부디,\n올해도 잘\n부탁드립니다','、','새해라 해서\n빈둥거리기만 하면\n안 됩니다!!','벗이 있는 곳에\n가셔서,','새해 첫 넷배틀을\n해 보시지요!!'],
2:['오늘은 절분입니다!','현실 세계에서는,\n콩을 뿌리지요!?','그럼, 우리도 질세라\n철구 뿌리기라도\n해 볼까요!'],
3:['、\n오늘은,\n발렌타인데이입니다','\n그대 같은 사내라면,','세상의 여성들이\n가만두지 않겠지요','초콜릿을 몇 개나\n받으실지・・・\n기대되는군요!!'],
4:['、\n오늘은,\n발렌타인데이군요','、\n그대가 준 초콜릿에','기뻐하지 않을 사내는\n없을 것입니다!'],
5:['오늘은,\n히나마쓰리 날입니다','기사라면,\n여성을 먼저 배려함은\n기본 중의 기본','저는 언제나\n여성에게 경의를\n표하고 있습니다'],
6:['오늘은 5월5일의\n어린이날입니다','갑옷과 투구나\n5월 인형을\n장식하지요','서양의 갑옷도\n좋지만,','일본의 갑옷은\n실용성도\n뛰어날 뿐 아니라,','그 아름다움은\n예술의 경지이지요'],
7:['오늘은 7월7일,\n칠석입니다!','자, 소원 쪽지에','「훌륭한 기사가\n 될 수 있도록」\n써 보시지요!'],
8:['오늘은 12월24일,\n크리스마스이브지요!','산타클로스 님은\n언제쯤\n오실까요?'],
9:['、\n메리 크리스마스!!','어젯밤은\n즐거우셨습니까?','저도 한번,\n산타클로스 님과','이야기를 나누고\n싶군요!'],
10:['오늘은 섣달그믐이오!','올해도 끝나는군요\n후회 없는1일을\n보내십시오'],
11:['、\n생일을\n축하드립니다!','삼가, 축하의 말씀\n올립니다!!'],
12:['오늘은,\n창립 기념일이\n아니었습니까?'],
17:['오늘은'],18:['「','」'],19:['입니다!!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6BA3AC.tpl';require_hash(p,'66f1acd761c8255f8d19c5007b0f63ce5b9cf0a3e7553ed8af9b741f6f6c2c2a');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6BA3AC:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6BA3AC'];validate_literal_numerals(units,scope);validate_nickname_suffix(units,'6BA3AC',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6BA3AC',source_archive_sha256='778552959e3b0c761eae033fb9053a0293e1830d628683233712c3ecf3b290a0',consumer='normal-dialogue',context='KnightMan seasonal/birthday operator conversations; intro6B5A70 names ナイトマン and loyalty to player. Native intro root03841C/seasonal+52 root038450. Portrait92,110/3rows; global22,two Valentine nickname prints per branch and event loop unchanged. Normal unlock/date/name routes unverified.',voice='Tentative polite chivalrous voice, respectful advice and iron-ball instead of bean scattering joke; human review pending.',evidence='analysis/full_scope_v1/source_tpl/6B5A70.tpl; analysis/full_scope_v1/source_tpl/6BA3AC.tpl; native roots03841C/038450',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All42 literals including3 unchanged punctuation; IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. Seven nickname suffix first lines bound: commas and leading blank unchanged;4:1 sourceから22px becomes comma11px with explicit 그대가 준 초콜릿 on following row. No name/save/RTC/gameplay edits.',semantic_review=['Valentine gift direction remains FROM player: invariant address comma followed by 그대가 준 초콜릿에, not receiver particle 께.3:1 keeps leading newline after nickname. Name consumer/runtime unverified.','Chivalry/women-first respect, Japanese May5 armour/May doll and Japanese armour practical/artistic contrast retained. Japanese calendar not relabeled as Korean holidays.','NewYear first netbattle and iron-ball-scattering joke retained; wish brackets and indented second line preserved. Culture/register/weapon terminology need human review; NumberMan4649 approval not reused.'],units=units)
    out=ROOT/'translations/knightman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('KnightMan42 serialized')

if __name__=='__main__':main()
