"""Serialize manually authored contextual drafts against immutable extraction."""
import json
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from tpl_literals import literals

DRAFT={
1:['새해 복\n많이 받으세요','올해도 잘\n부탁드려요','당신이 있어야\n넘버맨도\n있는 거니까요!'],
2:['오늘은 절분이군요','아킨도시티에서는\n굵은 김밥을 통째로','그해의 길한 방향을\n바라보고','베어 먹으면\n좋다고 하더군요','다만 먹는 동안엔\n말을 하면\n안 된다고 해요','참고로 그\n길한 방향은,','그해의 띠를\n바탕으로 정하는\n복을 부르는 방향이죠'],
3:['오늘은\n발렌타인데이군요','초콜릿을 몇 개나\n받으실까요?','많이많이 세게\n해 주세요~'],
4:['오늘은\n발렌타인데이군요','좋아하는 사람에게\n줄 초콜릿은 있나요?','저도 조금은\n두근두근하네요'],
5:['오늘 3월3일은\n히나마쓰리예요・・・','사실 또 다른\n기념일이기도 해요','3월3일은 귀의 날!','숫자3이 귀의\n모양과 닮았죠?','또 3은 일본어\n히후미에서\n미라고 읽어요','3이2개 나란하면\n미미가 되죠','미미는 귀란\n뜻이거든요!','정말 멋지죠!!'],
6:['오늘은 5월5일\n어린이날이에요','오늘은 힘차게 가는\n1일이에요','왜냐면 5월5일・・・\n고고!!','고고!!\n고, 고고・・・\n・・・재미없죠?'],
7:['오늘은 7월7일\n칠석이군요','그런데 일본의\n기념일은 같은 숫자가\n참 많네요・・・','1월1일은 몰라도','3월3일, 5월5일,\n7월7일,10월10일','뭐, 기억하기 쉬워서\n좋긴 하네요'],
8:['그러고 보니 오늘은\n크리스마스이브군요','사실 오늘을 위해\n커다란 양말을\n준비했어요!','산타클로스에게\n희귀 칩을 잔뜩\n받을 거예요!','내일 아침이면\n양말 속에는・・・','후후후후후후후후!!'],
9:['메리 크리스마스!!','・・・안타까운\n소식이 있어요・・・','제게는\n산타 할아버지가\n오지 않으셨어요','산타클로스도 역시\n전뇌 세계까지는\n못 오셨나 봐요','실망이에요・・・'],
10:['오늘은 올해의 끝!','한 해의 마지막엔\n제야의 종이죠!','제야의 종은 108번\n울린다고 해요\n알고 계셨나요?','참고로 108은\n인간이 지닌 번뇌의\n수라고 하더군요'],
11:['해피 버스데이!','생일을\n축하드려요!','또1살 늘었군요','당신의 나이에\n365를 곱해\n보세요','그게 태어난 때부터\n오늘까지의\n날짜 수예요','어때요, 날짜로 보면\n태어난 뒤로','그리 오래 지나진\n않은 것 같지 않나요?','윤년 등이 있으니\n조금은\n오차가 있겠지만요'],
12:['창립 기념일이군요\n오늘은 쉬시나요?'],
17:['오늘은'],18:['「','」'],19:['이군요!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/68BBB4.tpl';require_hash(p,'f1c31d0d24224b4f48ccb6765d6d994c9ff283affaa5003713d6ed48211ebcc7')
    items=literals(p.read_text(encoding='utf-8-sig'));units=[]
    expected={f'68BBB4:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}
    if {x.key for x in items}!=expected:raise ValueError('draft denominator')
    for x in items:
        _,s,i=x.key.split(':');units.append(dict(id=x.key,source=x.text,translation=DRAFT[int(s)][int(i)],state='needs_review'))
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='68BBB4',source_archive_sha256='94f20b8d0059d2dae96914b608e96eb099f494ea7869b4c1954cda0ec5ae7ea6',consumer='normal-dialogue',context='NumberMan operator seasonal greetings. Script1 observed normally after native save/reload/Navi reselection on baseline return-v1. Source12 holiday/birthday conversations share portrait92,110.17/19 are standalone pages;18 dynamic event buffer retains quote delimiters, buffer command, and source layout. Source gender check22 in3 preserved. Other holiday triggers not yet exercised.',voice='Existing NumberMan polite/playful development voice; names and cultural interpretation require review.',evidence='analysis/full_scope_v1/source_tpl/68BBB4.tpl; analysis/numberman_return_v1/runtime.json native_reload_attempt',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All60 literal identities/source fields; all numbers and ordered numerals; line counts; all commands including global22/checks/anniversary loop/buffer/quotes preserved. No save/RTC/event/name changes.',semantic_review=['2 Japanese Setsubun/ehou/futomaki retained as described custom, not replaced by Korean holiday.','5 Japanese mi/mi-mi counting pun explained in Korean; original numbers retained; human cultural/wordplay review pending.','6 Japanese go/5/go-go pun transliterated; not approved under separate4649 decision.','7 Japanese solar-calendar holiday dates retained; not moved to Korean lunar calendar.'],units=units)
    out=ROOT/'translations/numberman_seasonal_ko.json'
    if out.exists():raise ValueError('do not overwrite existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8')
    print('serialized manually authored60 units',sha(out.read_bytes()))

if __name__=='__main__':main()
