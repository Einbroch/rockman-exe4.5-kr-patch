"""Individually authored ThunderMan seasonal draft with pinned source identities."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['새해 복 많이 받아라','올해도 잘\n부탁하마・・・'],
2:['오늘은 절분\n이라는 날이라지・・・','이 나라에서는 콩을\n뿌려서 도깨비를\n쫓아낸다지만,','그럴 필요도 없이\n내 전격으로\n도깨비를 쓰러뜨리마'],
3:['오늘은,\n발렌타인데이로군','널 좋아하는\n여자에게 초콜릿을\n받는 날이었지?','과연 몇 개나\n받을 수 있을까・・・'],
4:['오늘은,\n발렌타인데이로군','초콜릿을\n건네줄 준비는\n되어 있느냐?'],
5:['오늘은 3월3일,\n히나마쓰리인가・・・','이런 풍습은\n소중히 여겨야지'],
6:['오늘은 5월5일\n어린이날이군・・・','이런 풍습은\n소중히 여겨야지'],
7:['오늘은 칠석이다・・・','오늘만큼은\n흐리지 않았으면 하네'],
8:['오늘은\n크리스마스이브로군','올해도 끝나 가는군\n저물어 가는 올해를\n즐겨 보자꾸나'],
9:['메리 크리스마스','크리스마스이브는\n마음껏 즐겼느냐?','새해가,\n바로 코앞이다'],
10:['오늘은 섣달그믐이다','올해 안에 못다 한\n일은 없느냐?','후회 없는 1일을\n보내거라'],
11:['오늘은 네\n생일이었지','축하한다','오늘은 태어난 것에\n감사하는 날이다','살아가는 기쁨을\n되새겨 보거라'],
12:['학교의 창립 기념일\n이로군・・・','오늘은 학교에\n가지 않아도 되느냐?'],
17:['오늘은'],18:['「','」'],19:['이란다・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/680454.tpl';require_hash(p,'702f460ccec4aeed55eeea347d83b7779da7054b2609739969746a10dfb42320');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'680454:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='680454',source_archive_sha256='e91e3c28e603cc99d46e876b4fd46c268de78f0e5575bcc7d5c967a41d7c9251',consumer='normal-dialogue',context='ThunderMan seasonal/birthday conversations; source intro67C4CC identifies speaker. Native60-byte Navi group seasonal+52/root038234. Portrait92,110/3rows; global22 gender branch and anniversary buffer/loop preserved. Normal unlock/date route unverified.',voice='Tentative solemn paternal informal voice based on source ワタシ/おまえ/せんとな/のだぞ and proud introduction, human review pending.',evidence='analysis/full_scope_v1/source_tpl/67C4CC.tpl; analysis/full_scope_v1/source_tpl/680454.tpl; native root038234',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All34 source literals including2 unchanged quotes; IDs/text,source numeral1 and dates,newline counts/boundaries,21slots,commands and event controls preserved. No name/save/RTC/gameplay edits.',semantic_review=['Setsubun/Hinamatsuri/May5/Tanabata retain Japanese holiday context. Culture and solemn paternal voice remain needs_review.','Source end-of-year literal numeral1 retained as 1일; no numeral-policy exemption.'],units=units)
    out=ROOT/'translations/thunderman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('ThunderMan34 serialized')

if __name__=='__main__':main()
