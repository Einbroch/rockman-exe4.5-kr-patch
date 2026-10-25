"""Individually authored MetalMan draft, pinned immutable source and nickname boundaries."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['、\n새해 복 많이 받아라','내 올해 목표는\n이 주먹을 한층 더\n갈고닦는 것이다','너도 뭔가\n목표를\n세우는 게 좋겠군'],
2:['오늘은 절분이군','내 주먹이\n도깨비에게도\n통할까・・・','한번 시험해\n보고 싶군'],
3:['오늘은,\n발렌타인데이다・・・','먼저 말해 두지만\n남자의 가치는,','받은 초콜릿의\n개수가 아니다','기죽지 마라'],
4:['오늘은,\n발렌타인데이다・・・','아무에게나\n의리 초콜릿을\n마구 뿌리지 마라','남자는 착각하기\n쉬운 생물이니까'],
5:['오늘은 히나마쓰리다','나와는 상관없는\n축제지만,','축제 기분만이라도\n맛보도록 할까'],
6:['오늘은 5월5일\n단오절이다・・・','분명 어린이날이라\n휴일이었을 거다','오늘은 마음껏\n놀도록 해라'],
7:['오늘은 칠석이군','직녀와 견우는,\n무사히 만날 수\n있을까・・・'],
8:['오늘은 12월24일,\n크리스마스이브다','듣자니 오늘 밤\n산타라는 녀석이\n집에 몰래 들어온다지','하지만 안심해라,\n내가 지켜봐 주마'],
9:['오늘은 12월25일,\n크리스마스다','어제 한밤중에\n수상한 그림자를\n발견했지만,','아쉽게도 놓치고\n말았다・・・미안하다'],
10:['오늘은 12월31일,\n오미소카, 섣달그믐','미소카란,\n한 달의 마지막 날을\n뜻하지・・・','한 해의 마지막 날,\n큰 미소카인 셈이지','좀 배웠느냐?'],
11:['、\n생일 축하한다','나도 기쁘군\n함께 성장해\n가고 싶구나'],
12:['학교의 창립 기념일\n이었지・・・','오늘은 쉬는 날이냐?'],
17:['오늘은'],18:['「','」'],19:['이란다・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/691A64.tpl';require_hash(p,'039711e89b466224d4a84a9c52891b90aa4a4c0bc797842cb15ef3644bbcef8d');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'691A64:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['691A64'];validate_literal_numerals(units,scope);validate_nickname_suffix(units,'691A64',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='691A64',source_archive_sha256='e06df11b3698486af660647df841f64e865c0bc915c899e0ee93bf07b18c0afd',consumer='normal-dialogue',context='MetalMan operator seasonal/birthday conversations. Intro68D3C8 explicitly names メタルマン and fist-training theme. Native60byte Navi group intro root0382B4/seasonal+52 root0382E8. Portrait92,110/3rows; global22,dates,two nickname prints and anniversary buffer/loop preserved. Normal unlock/date/name route unverified.',voice='Source オレ/おまえ/だ/ぞ and restrained fist-training greetings motivate tentative firm informal mentor voice, human review pending.',evidence='analysis/full_scope_v1/source_tpl/68D3C8.tpl; analysis/full_scope_v1/source_tpl/691A64.tpl; native roots0382B4/0382E8',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All39 source literals including2 unchanged quote literals; IDs/text,dates/numerals,newline counts/boundaries,21slots,commands and event controls preserved. Nickname1:0 and11:0 first line remains invariant source comma 、, same11px. No name/save/RTC/gameplay edits.',semantic_review=['Omisoka/Misoka explanation retains Japanese terms (오미소카/미소카) plus Korean 섣달그믐, rather than inventing a Korean etymology. Wording needs human review.','Japanese Setsubun/Hinamatsuri/May5 Tango/Tanabata kept in context; Orihime/Hikoboshi rendered 직녀/견우 as in preceding draft Tanabata story. Culture and voice review pending.','Source obligation-chocolate warning and Santa intruder/escape joke retained. These are draft character statements, not assistant advice.'],units=units)
    out=ROOT/'translations/metalman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('MetalMan39 serialized')

if __name__=='__main__':main()
