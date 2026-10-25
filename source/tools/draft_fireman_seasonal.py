"""Individually authored FireMan draft, immutable extracted source identities."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['새해 복 많이\n받아라!!','올해도 뜨겁게\n불타올라 주겠어!','잘 부탁한다!!\n파이어ーーー!!'],
2:['오늘은 절분이었지\n뭐, 그 근처의\n도깨비 따위는,','꼬리를 말고\n도망칠 거야!','뭐, 말아 넣을 꼬리가\n있다면 말이지만!'],
3:['오늘은\n발렌타인데이였지','사실 난 초콜릿이\n좀 꺼려진단 말이지','왜냐면, 내\n불꽃에 녹으니까!','너도 남자라면\n그 정도 열기는\n있어야 한다고!'],
4:['오늘은\n발렌타인데이였지','사실 난 초콜릿이\n좀 꺼려진단 말이지','왜냐면, 내\n불꽃에 녹으니까!','하지만 뭐, 받는 건\n싫지 않다고'],
5:['오늘은 즐거운\n히나마쓰리다!','등롱에 내\n불꽃으로 불을\n붙여 줄까!?','어이!\n임금님 인형!','딸꾹, 이런・・・\n전뇌 아마자케를\n너무 마셨나 보군'],
6:['오늘은 5월5일\n어린이날이군・・・','뭐, 난\n꼬맹이가 아니니\n들뜨지는 않겠지만,','왠지 넷 배틀을\n하고 싶군・・・','무엇보다,\n남자애의 날이니까!!'],
7:['7월7일・・・\n칠석이군!','난 로맨티스트는\n아니니까,','별로 관심은\n없지만・・・','직녀와 견우\n이야기는 꽤\n좋아한다고・・・'],
8:['오늘은,\n크리스마스이브!!','오늘만큼은 격렬한\n배틀은 그만두고,','고요하고 거룩한\n밤을 실컷\n즐겨 보자!'],
9:['인사부터 할까・・・\n메리 크리스마스!','고요하고 거룩한\n밤은 끝났다!','뜨거운 배틀을\n시작하자고!!'],
10:['드디어 왔군・・・\n섣달그믐이다!!','올해 마지막 배틀을\n하자고!!','올해 배틀 마무리!!'],
11:['야, 잠깐・・・\n너, 분명 오늘이\n생일이었지?','축하한다!','좀 쑥스럽지만,\n축하해 주겠어!!','\n버닝!!','버닝!!\n','!'],
12:['오늘은,\n창립 기념일이지?','그런 날은,\n보통 쉬는 날이지?'],
17:['오늘은'],18:['「','」'],19:['이라고!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/67AE2C.tpl';require_hash(p,'f070365660835b10eb2705529fd965061ffac7d847c3a36099a5218006d16ef7');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'67AE2C:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['67AE2C'];validate_nickname_suffix(units,'67AE2C',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='67AE2C',source_archive_sha256='fafc655f894bd17db372edc40aac995818f27cc1efcb785612f123bb2270397e',consumer='normal-dialogue',context='FireMan operator holiday/birthday conversations. Source intro676AE4 explicitly names FireMan; native60-byte Navi group seasonal+52/root0381F8. Portrait92,110/3rows; global22 gender branch,dates,two birthday nickname inserts,anniversary buffer/loop preserved. Normal unlock route unverified.',voice='Source rough enthusiastic ぜ/よぉ/オレ and fire/burning calls motivate tentative energetic informal voice, human review pending.',evidence='analysis/full_scope_v1/source_tpl/676AE4.tpl; analysis/full_scope_v1/source_tpl/67AE2C.tpl; native root0381F8',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All47 source literals including3 unchanged quote/exclamation literals; source IDs/text,numbers,newline counts and leading/trailing newline boundaries,21slots,commands,gender/nickname/event controls preserved. Birthday11:3 leading newline,11:4 trailing newline and11:5 source ! pinned. No name/save/RTC/gameplay edits.',semantic_review=['Japanese Setsubun/Hinamatsuri/May5/Tanabata/amazake and doll/lantern customs retained in context. おだいりさま described as 임금님 인형; culture review pending.','Source seasonal fire/chocolate/tail jokes retained contextually. Silent/Holy Night translated as 고요하고 거룩한 밤, not song lyrics reproduction.','Fire/Burning calls and rough voice remain draft, not approved equipment terminology. Orihime/Hikoboshi rendered 직녀/견우 in this Tanabata story; review pending.'],units=units)
    out=ROOT/'translations/fireman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('FireMan47 serialized')

if __name__=='__main__':main()
