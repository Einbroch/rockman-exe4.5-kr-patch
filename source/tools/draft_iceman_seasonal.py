"""Individually authored IceMan draft with explicit nickname/cultural boundaries."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['새해 복 많이\n받으세요~!','올해도,잘\n부탁드려요!'],
2:['도깨비는~밖으로!\n복은~안으로!','오늘은 절분이에요~','콩 뿌리기는,\n재밌어요~'],
3:['오늘은 설레고 쑥스런\n발렌타인데이예요!','、\n초콜릿은 몇 개나\n받을 수 있을까요?'],
4:['오늘은 설레고 쑥스런\n발렌타인데이예요!','초콜릿을,\n진짜 좋아하는 분께,\n드릴 건가요?'],
5:['오늘은 3월3일,\n복숭아 절기인\n히나마쓰리예요!','히나마쓰리가\n끝난 뒤에도,','히나 인형을\n계속 장식해\n두면,','시집을\n늦게 가게 된다고\n하더라고요!'],
6:['오늘은 5월5일\n어린이날이에요~!','3월3일이\n여자아이의 날이면,','5월5일은\n남자아이의 날이에요!'],
7:['오늘은,\n대나무 잎 사각사각\n칠석이에요!!','은하수는 마치,\n다이아몬드 더스트\n처럼 아름다워요~'],
8:['오늘은 12월24일,\n크리스마스이브예요!','B 소리 말고,\nV 소리예요!','눈이 내리면\n좋겠어요~!'],
9:['오늘은 12월25일,\n크리스마스예요!','크리스마스 선물은\n뭘 받았나요?'],
10:['오늘은 12월31일,\n섣달그믐이에요!','시간 참 빠르네요,\n오늘로 올해도 끝나요','내년도 좋은 해가\n되면 좋겠어요!','해넘이 소바는,\n냉중화면이\n좋겠어요~'],
11:['、\n생일을\n축하드려요!!','정말\n경사스러워요!'],
12:['오늘이,\n개교 기념일\n맞았지요?'],
17:['오늘은'],18:['「','」'],19:['이에요!!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6C5A88.tpl';require_hash(p,'a3aa5fc7530aa4c65550de1072cf22f09ba408b216f7039942114da0f330aaae');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6C5A88:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6C5A88'];validate_literal_numerals(units,scope);validate_nickname_suffix(units,'6C5A88',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6C5A88',source_archive_sha256='16cd9b1e7ce2355d2b3dc5f91659ea0c92edbad47dfe4b569d196e22a1e7fc63',consumer='normal-dialogue',context='IceMan seasonal/birthday dialogue; intro6C167C names アイスマン with polite childish speech. Native intro root038494/seasonal+52 root0384C8. Portrait92,110/3rows; global22,two nickname prints and event buffer/loop unchanged. Normal unlock/date/name/gender/event routes unverified.',voice='Tentative gentle polite voice, elongated~ endings retained locally. Human wording/terminology/culture review pending.',evidence='analysis/full_scope_v1/source_tpl/6C167C.tpl; analysis/full_scope_v1/source_tpl/6C5A88.tpl; native roots038494/0384C8',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All34 literals including2 unchanged quotes; IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. Nickname3:1/11:0 first-line comma11px unchanged; no name/save/RTC/gameplay edits.',semantic_review=['Christmas8:1 distinguishes Japanese イブ(B) from イヴ(V). Draft B/V sound explanation preserves the contrast rather than identical Korean 이브 twice; wording requires human review, not reuse of NumberMan4649 approval.','March3 peach festival and Hina dolls left displayed causing late marriage remain reported source folklore, not a factual endorsement or Korean custom substitution. May5 gender contrast and all dates retained.','Tanabata bamboo-leaf rustling and MilkyWay compared to diamond dust retained. NewYearEve prefers chilled Chinese noodles to year-crossing soba; not silently corrected to hot soba or Korean naengmyeon.'],units=units)
    out=ROOT/'translations/iceman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('IceMan34 serialized')

if __name__=='__main__':main()
