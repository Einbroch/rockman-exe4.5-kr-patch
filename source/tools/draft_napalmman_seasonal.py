"""Individually authored NapalmMan seasonal draft, not a prose transformation."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['콰아아아앙!','새해 복 많이\n받아라,으랴아!','올해도 마구 쏴\n갈겨 주겠어!','잘 부탁한다!'],
2:['오늘은 절분이다!!\n콩을 뿌리겠어!!','내 콩 뿌리기는,\n좀 과격하다고!','도깨비는 밖으로!\n콰앙!!','복은 안으로!\n쾅쾅!!','속이 후련하군!'],
3:['오늘은,\n발렌타인데이군!','오늘은 남자가\n집중 공략을\n당하는 날이군!','어때,표적이\n되는 기분은?'],
4:['오늘은,\n발렌타인데이군!','네\n초콜릿 바주카로','누구를 집중\n공략할 거냐?'],
5:['오늘은 히나마쓰리군\n여자들의 축제\n라지만,','어떤 축제든\n떠들썩하게 즐겨야\n손해 안 본다고!!'],
6:['오늘은 어린이날이다!','여기저기에\n갑옷과 투구가\n장식돼 있어서,','왠지 남자의 마음을\n설레게 하는 날이야!'],
7:['오늘은 7월7일,\n칠석이다!','밤하늘 은하수의\n별들을 모조리\n쏴 떨어뜨리겠어!'],
8:['오늘은,\n크리스마스이브다!','난 이렇게\n요란하게 꾸민\n축제 따윈・・・','정말 좋아한다고!!'],
9:['오늘은,\n크리스마스다!!','크리스마스라고\n해도,','벌써 슬슬\n새해 기분이\n들고 있지 않냐?'],
10:['오늘은 섣달그믐이군!','제야의 종 대신\n108발의\n네이팜탄을','쏴 울려 줄까?'],
11:['오늘이 네\n생일이었지!','좋아,당장\n생일 기념\n넷 배틀이다!!'],
12:['오늘은 학교\n개교 기념일이\n아니었나?'],
17:['오늘은'],18:['「','」'],19:['이라고!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6C004C.tpl';require_hash(p,'b8fc0f74af82d83016d1c00b711ed5a48ea5ac610f668250ea7a6f1fbb226a8b');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6C004C:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6C004C'];validate_literal_numerals(units,scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6C004C',source_archive_sha256='6a2c9afa4c376d637ee48ac5f86dd1dd275cbc9c392dff8a61cfe44dacc1e1aa',consumer='normal-dialogue',context='NapalmMan seasonal/birthday dialogue; intro6BBAF8 names ナパームマン and establishes impatient destructive voice. Native intro root038458/seasonal+52 root03848C. Portrait92,110/3rows; global22,event buffer/loop unchanged; no nickname insertion. Normal unlock/date/gender/event routes unverified.',voice='Tentative forceful colloquial voice; explosions, chocolate bazooka, target imagery and holiday enthusiasm retained. Human terminology/wording/voice review pending.',evidence='analysis/full_scope_v1/source_tpl/6BBAF8.tpl; analysis/full_scope_v1/source_tpl/6C004C.tpl; native roots038458/03848C',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All38 literals including2 unchanged quotes; IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. No name/save/RTC/gameplay edits.',semantic_review=['Christmas8:1 feigns disdain but8:2 explicitly loves the festival; reversal retained.','NewYear firing boast, Setsubun beans/oni-out/fortune-in explosions, Valentine gender branch and chocolate bazooka remain source meaning, not new gameplay instructions.','July7/7 remains Japanese Tanabata date. NewYearEve108 counts Napalm shots replacing the bell; birthday celebrates by immediate net battle.','NapalmMan/네이팜탄 and onomatopoeia are provisional individual draft decisions; NumberMan4649 approval is not reused.'],units=units)
    out=ROOT/'translations/napalmman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('NapalmMan38 serialized')

if __name__=='__main__':main()
