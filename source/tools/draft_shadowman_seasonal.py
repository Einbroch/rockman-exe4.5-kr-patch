"""Individually authored ShadowMan seasonal draft, source-pinned/non-distribution."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={
1:['새해가 밝았군,\n복 많이 받게','소인이 말하니,\n어쩐지 우스꽝스러워\n보일지도 모르나,','새해 인사는\n중요하니 말일세\n제대로 해야지・・・'],
2:['오늘은 절분일세・・・','아아, 일본 고래의\n풍습은\n좋은 것이로군・・・','이 전통은\n지켜 나가야\n하겠구먼・・・'],
3:['서양 신부들의\n축제,\n발렌타인데이군・・・','아녀자가 사내에게\n초콜릿을 건네어\n마음을 전한다니','그건 그것대로\n운치가 있구먼・・・'],
5:['오늘은 3월3일,\n복숭아꽃 명절・・・','이런 행사가','현대인이\n잊어 가고 있는','일본의 마음을\n떠올리게 해 주지'],
6:['오늘은 5월5일의\n일본 단오일세・・・','본래\n잉어 깃발은,','잉어가 폭포를 올라\n용이 된다는\n전설에서 유래해,','사내아이의 출세를\n뜻하지・・・','잉어 깃발에는,\n자식을 생각하는','부모의 소망이\n담겨 있는 것이지'],
7:['오늘은,칠석이구먼','오늘 밤에는 하늘을\n올려다보면 좋겠군','요즘에는 하늘을\n보는 기회도\n줄었을 테니 말일세'],
8:['오늘은,\n크리스마스이브군・・・','이브의 밤에는\n산타클로스가\n찾아온다 하던데・・・','서양의 닌자인가?'],
9:['오늘은 크리스마스일세','산타클로스는\n왔던 것인가・・・?','소인도 기척조차\n느끼지 못하다니・・・'],
10:['오늘은 섣달그믐・・・\n올해도 저무는구먼\n・・・・・・','오늘 밤 제야의 종을\n들으며 느긋하게\n새해를 맞고 싶군'],
11:['오늘은 그대의\n생일인가・・・','축하한다고\n말해 두겠네・・・','1살씩 먹을수록\n짊어져야 할 책임이\n늘어나는 법이지・・・','생일이라고\n해서,','들떠 있기만은\n할 수 없네・・・'],
12:['오늘은,\n창립 기념일이군・・・','그대,\n오늘은 쉬는가?'],
17:['오늘은'],18:['「','」'],19:['일세・・・']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/6AE834.tpl';require_hash(p,'30564b461e20e340bf825d3065121d3cbb2a956f8a91d568cb3e2479672ecdfc');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'6AE834:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('complete source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6AE834'];validate_literal_numerals(units,scope)
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6AE834',source_archive_sha256='a6f7058c085d4c5e3a4f482f3c113af6c32b070862d7af76eaa899887e00b464',consumer='normal-dialogue',context='ShadowMan seasonal/birthday conversations; intro6AA1A0 names シャドーマン with archaic せっしゃ/そうろう. Native intro root0383E0/seasonal+52 root038414. Portrait92,110/3rows; script4 native jump3 protected; event loop unchanged; no nickname insertions. Normal unlock/date/branch/event routes unverified.',voice='Tentative archaic 소인/그대/일세/구먼 voice reflecting source historical register and cultural unfamiliarity; wording not human-approved.',evidence='analysis/full_scope_v1/source_tpl/6AA1A0.tpl; analysis/full_scope_v1/source_tpl/6AE834.tpl; native roots0383E0/038414',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='All41 literals including2 unchanged quotes; IDs/source,numerals,newline counts/boundaries,21slots,commands preserved. Nonliteral script4 jump3 remains native bytes. No name/save/RTC/gameplay edits.',semantic_review=['バテレン retains foreign Christian priest meaning as 서양 신부들; not generic Western festival without religious attribution. Santa as Western ninja and undetectable presence keep source joke.','March3 peach festival/May5 Japanese Tango and carp streamers retain Japanese calendar/culture; carp waterfall-to-dragon legend and parents wishing sons success remain connected across six pages.','Birthday responsibility caution and NewYear greeting importance retained. Register/culture/terminology need human review; NumberMan4649 approval not reused.'],units=units)
    out=ROOT/'translations/shadowman_seasonal_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('ShadowMan41 serialized')

if __name__=='__main__':main()
