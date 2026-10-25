"""Individually authored AquaMan draft; immutable source and nickname boundary bindings."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['새해 복 많이\n받으세요, 퓨!','싱싱하고\n촉촉한 해로\n만들 거야, 퓨!','그러니까,\n올해도 잘 부탁해퓨!'],
2:['오늘은 절분, 퓨!','나도 잔뜩\n콩을 뿌릴래, 퓨~!','도깨비~밖으로퓨~','복은~안으로퓨~','꽤 재밌어, 퓨','、\n너도 해 봐, 퓨!'],
3:['오늘은,\n발렌타인데이야, 퓨','오늘 1일 동안,\n방심 못 해, 퓨!','두근두근퓨・・・'],
4:['오늘은,\n발렌타인데이야, 퓨!','、\n초콜릿은 누구에게\n줄 거야, 퓨?','두근두근퓨・・・'],
5:['3월3일은,\n여자아이의 날, 퓨!','난 남자라서,\n축하 못 받아퓨','조금, 슬퍼퓨'],
6:['오늘은 5월5일\n어린이날!!','히나마쓰리 후2개월!\n드디어 찾아온\n남자아이의 날, 퓨!','오늘은 남자아이가\n주인공이야, 퓨!!'],
7:['오늘은 칠석, 퓨!','전부터\n궁금했는데, 퓨','은하수는,\n헤엄칠 수 있어, 퓨?'],
8:['오늘은,\n크리스마스이브퓨!','만약 내가 현실로\n갈 수 있다면,','머리 분수의\n물을 눈으로 바꿔서,','화이트 크리스마스로\n만들 수 있어, 퓨!'],
9:['메리 크리스마스퓨!','크리스마스트리를\n치우기는 아직\n너무 일러, 퓨!!','크리스마스는\n안 끝났어, 퓨!'],
10:['섣달그믐이야, 퓨!!','올해 1년의 때를\n물로 씻어 내, 퓨!!','나도 이따가,\nPET 안을 대청소\n할 거야, 퓨!!'],
11:['생일을,\n축하해, 퓨!!','오늘은 경사스런\n날이니까, 내','머리 분수의\n물도 평소보다\n조금 많아, 퓨!'],
12:['창립 기념일이야, 퓨','오늘 1일 내내,\n쉬는 거야, 퓨?'],
17:['오늘은'],18:['「','」'],19:['퓨!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/69C9F4.tpl';require_hash(p,'d36bb7fb947c1d38c9beb90878815fc7efbd053c12f6ef94fe065f476c254811');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'69C9F4:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['69C9F4'];validate_literal_numerals(units,scope);validate_nickname_suffix(units,'69C9F4',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='69C9F4',source_archive_sha256='a3964058397d628e176eb99f399848b03d089b3dd05e2dd5eee750cccadc77a8',consumer='normal-dialogue',context='AquaMan seasonal/birthday operator conversations; intro698424 identifies アクアマン and repeated ぴゅ speech. Native60byte Navi group intro03832C/seasonal+52 root038360. Portrait92,110/3rows; global22,two nickname prints and event buffer/loop unchanged. Normal unlock/date/name route unverified.',voice='Tentative cheerful childish voice retaining source-scoped っぴゅ/ぴゅ endings as 퓨. Polite first NewYear greeting retained; catchphrase selection and water wordplay need human review.',evidence='analysis/full_scope_v1/source_tpl/698424.tpl; analysis/full_scope_v1/source_tpl/69C9F4.tpl; native roots03832C/038360',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All43 literals including2 unchanged quotes; IDs/text,numerals,newline counts/boundaries,21slots,commands preserved. Nickname2:5 first line sourceも and4:1 sourceは become invariant comma 、 (same11px); invitation 너도 and addressed chocolate question follow on source-separated rows. No name/save/RTC/gameplay edits.',semantic_review=['Water/fresh/moist NewYear wording and swim-in-Milky-Way joke retained in context. 퓨 catchphrase is a draft transliteration, not a human-approved voice rule.','March3 girl holiday,May5 boy holiday and2months relation retain Japanese source context rather than relabeling dates. Source day/year numerals1 remain explicit.','Source fountain snow/White Christmas story and PET cleaning retained. All wording/culture/layout require review before distribution.'],units=units)
    out=ROOT/'translations/aquaman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('AquaMan43 serialized')

if __name__=='__main__':main()
