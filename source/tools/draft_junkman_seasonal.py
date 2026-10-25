"""Individually authored JunkMan draft; preserves source identities and voice transition."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

DRAFT={
1:['아, 아・・・\n해피 뉴 이어!','다, 다행이야,\n제대로 말했어・・・','나, 나 오, 올해도\n힘낼게, 잘 부탁해'],
2:['오, 오늘은 절분이야','도깨비가 무서워・・・\n빨리 콩 뿌려 줘・・・'],
3:['오늘은,\n발렌타인데이구나','나도 초콜릿,\n받아 보고 싶어・・・'],
4:['오늘은,\n발렌타인데이구나','나, 나한테도 줘\n・・・하, 하지만,\n난 내비니까・・・','초콜릿 못 받아・・・\n조금 쓸쓸해'],
5:['오, 오늘은,\n히나마쓰리야・・・','히나 인형,\n나도 갖고 싶어・・・'],
6:['오, 오늘은 어린이날','나, 나 왠지,\n들떠・・・'],
7:['오, 오늘은 칠석','나, 나는 소원 쪽지에','좀 더 또렷하게\n말할 수 있게 해 달란\n소원을 썼어・・・','어때, 나 또렷하게\n말하고 있어?','아, 지금 또렷하게\n말했어・・・'],
8:['오늘은,\n크리스마스이브!','나, 너랑\n함께라서 기뻐','최고의\n크리스마스 선물이야'],
9:['메,메리 크리스마스!','산타클로스,\n나한테는\n안 왔어・・・','그래도 난 네\nPET에 있기만 해도\n충분해'],
10:['오, 오늘은 섣달그믐','제야의 종을 내\n정크 프레스로\n울려 보고 싶어・・・'],
11:['、\n생일,\n축하해','나, 나 언제\n태어났는지 몰라','그래서 네\n생일이,','내 생일만큼이나\n기뻐'],
12:['오늘은 학교의\n창립 기념일이야','오늘은, 함께\n있을 수 있어?'],
17:['오늘은'],18:['「','」'],19:['이야・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/696DD8.tpl';require_hash(p,'622cf5381e7d94bb69db90754efce6479b21da01a48558a0327eeb72ae13ad62');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'696DD8:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['696DD8'];validate_literal_numerals(units,scope);validate_nickname_suffix(units,'696DD8',scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='696DD8',source_archive_sha256='919820b50b476172c3c5b71d386f908e265a53ec42635643eb54aa3447670ba3',consumer='normal-dialogue',context='JunkMan operator seasonal/birthday conversations; intro69303C identifies ジャンクマン, shy first-time Navi and fear of abandonment. Native60byte Navi group intro root0382F0/seasonal+52 root038324. Portrait92,110/3rows; global22,nickname birthday print and anniversary buffer/loop unchanged. Normal unlock/date/name route unverified.',voice='Tentative simple shy informal speech, manually retains source initial hesitations. Source7:3 alone switches to normal orthography/fluent speech and7:4 notices it; no blanket stutter rule applied.',evidence='analysis/full_scope_v1/source_tpl/69303C.tpl; analysis/full_scope_v1/source_tpl/696DD8.tpl; native roots0382F0/038324',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All37 literals including2 unchanged quotes; IDs/text,source numerals,newline counts/boundaries,21slots,commands preserved. Birthday11:0 first line invariant source comma 、 remains11px. No name/save/RTC/gameplay edits.',semantic_review=['696DD8:4:2 チョコ/チョコット pun: literal meaning rendered 초콜릿 못 받아/조금 쓸쓸해; wordplay not reproduced and no approval inferred from NumberMan4649. Needs human wording/adaptation review; non-distribution input only.','696DD8:7:3 fluent question contrasted with surrounding hesitant dialogue, source7:4 realization preserved. Source オデ phonetic personality rendered through simple voice and source-scoped hesitations, not an approved global voice decision.','Japanese Setsubun/Hinamatsuri/Tanabata and bell custom retained. Junk Press name 정크 프레스 is a draft source-backed transliteration, terminology review pending.'],units=units)
    out=ROOT/'translations/junkman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('JunkMan37 serialized')

if __name__=='__main__':main()
