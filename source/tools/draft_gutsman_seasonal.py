"""Manual contextual draft; serialization never rewrites source identities."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['거츠, 거츠!\n새해 복,\n많이 받으거스!','올해도 거츠 넘치게\n힘내겠거스!!'],
2:['거츠, 거츠!','오늘은 절분,\n콩 뿌리기거스!!','거츠 머신건으로\n콩을 뿌리겠거스!','거츠츠츠츠츠!!','바이러스는 밖으로거스\n칩은 집 안으로거스!'],
3:['거츠, 거츠!','드디어 왔거스!\n발렌타인데이거스!','오늘만큼은,\n거츠맨도 긴장\n하거스!!','초콜릿을 받으면\n좋겠거스!'],
4:['거츠, 거츠!','드디어 왔거스!\n발렌타인데이거스!','거츠맨도\n초콜릿이\n갖고 싶거스~!!'],
5:['거츠, 거츠!','오늘은3월3일\n히나마쓰리거스!','오늘의 주인공은\n여자아이거스!','그러니 거츠맨은,\n얌전히 있겠거스\n・・・・・・'],
6:['거츠, 거츠, 거츠!','5월5일 어린이날은\n단오 명절이자\n남자애의 날이거스!!','오늘은 날뛰겠거스!\n거츠거츠!!'],
7:['거츠, 거츠!','오늘은 칠석이거스!\n종이쪽지에 소원을\n적어서,','대나무 가지에\n매다는 거스!','반드시 소원이\n이뤄질 거스!!'],
8:['거츠, 거츠!','메리 크리스마스거스!','정확히 말하면,\n메리 크리스마스이브\n이거스!','오늘 밤은,\n파티하거스?','거츠맨도\n진수성찬을\n먹고 싶거스!'],
9:['메리 크리스마스거스!','하지만 이브가 끝나면\n바로 새해 기분이\n들거스・・・','연말이거스'],
10:['거츠, 거츠!','오늘은 섣달그믐이거스','대청소하는 날이거스!','오늘은 어느 집이나\n바쁘거스・・・','그러니,\n집에서 얌전히\n있겠거스!!'],
11:['거츠, 거츠!','생일을,\n축하하거스!!','앞으로도 거츠맨과\n친하게 지내주거스'],
12:['거츠, 거츠!','오늘은,\n창립 기념일이거스!','오늘은 느긋하게\n놀겠거스!!','그런데 학교는\n쉬는 거스?'],
17:['오늘은'],18:['「','」'],19:['이거스!!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/66A234.tpl';require_hash(p,'6331e0437b9a25ce18eb62ac3dd44f0229dc45653c7c9fa1f153d16cd92f0c2e');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'66A234:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='66A234',source_archive_sha256='9b548394870d71a7f4db521f21c026c6be3568eb8c930de276a7c81153dc9e71',consumer='normal-dialogue',context='GutsMan operator holiday/birthday conversations. Source intro665EB8 speaker explicitly GutsMan at seasonal root038144 minus52. Native portrait92,110/3rows. global22 branch, original solar-calendar holiday dates and anniversary dynamic event buffer/loop retained.',voice='Existing four_navi_save_ko GutsMan drafts use 거츠 / 거스; retained contextual candidate voice, needs human review.',evidence='analysis/full_scope_v1/source_tpl/66A234.tpl; translations/four_navi_save_ko.json; native root038144',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All49 literals including source-identical quotes; source text, numbers, newline counts, commands/events/gender branch/anniversary buffer preserved. No name/save/RTC/gameplay edits.',semantic_review=['Japanese Setsubun/Tango/Hinamatsuri/Tanabata customs retained, not replacement by Korean calendar dates.','GutsMan virus/chip bean-throwing wordplay and machinegun exclamation translated in context; review pending.'],units=units)
    out=ROOT/'translations/gutsman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('GutsMan49 serialized')

if __name__=='__main__':main()
