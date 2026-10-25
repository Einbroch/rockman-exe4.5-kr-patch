"""Individually authored GutsMan PET prose and labels; serialize source identities."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['뭘 하겠거스?'],
2:['토너먼트에\n참가하겠거스?\n','예  ','아니요'],
3:['인터넷에\n플러그인하겠거스?\n','예  ','아니요'],
4:['거츠맨의 장비를\n바꾸겠거스?\n','예  ','아니요'],
5:['데이터 라이브러리를\n보겠거스?\n','예  ','아니요'],
6:['메일을\n확인하겠거스?\n','예  ','아니요'],
7:['통신 대전을\n하겠거스?\n','예  ','아니요'],
8:['저장 화면에\n들어가겠거스?\n','예  ','아니요'],
10:['토너먼트로\n하겠거스?\n','예  ','아니요'],
11:['인터넷에\n플러그인하겠거스?\n','예  ','아니요'],
12:['거츠맨의 장비를\n바꾸겠거스?\n','예  ','아니요'],
13:['데이터 라이브러리를\n보겠거스?\n','예  ','아니요'],
14:['메일을\n확인하겠거스?\n','예  ','아니요'],
15:['통신 대전을\n하겠거스?\n','예  ','아니요'],
16:['지금까지의 데이터를\n저장하겠거스?\n','예  ','아니요'],
20:['거츠맨의 이야기는,\n아직 안 끝났거스!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/665F3C.tpl';require_hash(p,'7e61d76a8f55d97d703b40e67c3334d2eb4c6b0062358cc22cc31e30d9cccb01');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'665F3C:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='665F3C',source_archive_sha256='45aa744818878d7b67797fcbfc1aefcbc741ca240bc16ff529bfbec67713f719',consumer='normal-dialogue',context='GutsMan PET idle/question/selection/reentry/interruption. Explicit GutsMan equipment/interruption naming, original root038114=08665F3C, intro038110+4. Scripts2..8 initial seven questions,10..16 second dispatch;8 enters save screen,16 saves current data. Portrait92,110, source option row and exact controls retained. No nickname insertion.',voice='Tentative existing GutsMan intro/seasonal/save 거츠/거스 voice; human terminology/wording/voice review pending.',evidence='analysis/full_scope_v1/source_tpl/665F3C.tpl; translations/gutsman_intro_ko.json; native root038114',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All44 literals/22slots. Original IDs/source,numerals,newline boundaries/trailing option row,Yes two trailing spaces,commands/options/select targets/flag3584,3585,3588,3615/global30=120 retained. No RTC/name/save-code/gameplay changes.',semantic_review=['Save-screen navigation8 and save-current-data16 kept distinct. Initial tournament participation2 vs second dispatch tournament choice10 kept distinct.','Interruption says GutsMan has not finished speaking, no invented affection or advice. No live communications or all reentry branches claimed from cancelled initial prompts. NumberMan4649 approval not reused.'],units=units)
    out=ROOT/'translations/gutsman_pet_menu_ko.json'
    if out.exists():raise ValueError('preserve translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('GutsMan PET44 serialized')

if __name__=='__main__':main()
