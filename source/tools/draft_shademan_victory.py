"""Manual98 ShadeMan victory/return candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7C90E0':('aaf8c3b36d0123ce59c1947a4fd931bbcb7fee52a8eb320e25b9190ef3469dc4',98,'translations/shademan_victory_return_draft_ko.json'),
}
DRAFT={
'7C90E0':{
0:['네, 네놈...\n이대로 끝날 거라\n생각하지 마라...','어둠의 힘은...\n...무한하다...','키키이이이이!!'],
1:['셰이드맨...\n무서운 나비였어\n......','자, 인터넷12로\n돌아가자!!','오피셜 토너먼트에\n등록해야지!'],
2:['해냈네!\n네 덕분에\n어떻게든 이겼어!!','멋진 오퍼레이션이었어!!','자, 인터넷12로\n돌아가자!','오피셜 토너먼트에\n등록해야지!'],
3:['거츠 거츠!\n해냈다, 가스!!','하, 하지만 꽤\n무서웠다, 가스...','녀석의 공격이\n먼저 맞았다면, 하고\n생각하니 오싹하다, 가스','얼른 인터넷12로\n돌아간다, 가스!!','오피셜 토너먼트,\n반드시 우승한다, 가스!'],
4:['사악한 기운이 걷혔네...','맑은 바람 앞에서는\n어둠의 힘도\n조금의 승산도 없네','자, 인터넷12로\n돌아가겠네','오피셜 토너먼트의\n등록 절차를\n마쳐야 하겠지...'],
5:['임무, 완료...','상대를 잘못 골랐군...\n...셰이드맨','자, 인터넷12로\n돌아갑시다','오피셜 토너먼트의\n출전 등록을\n마쳐야 합니다'],
6:['그러니까, 말했잖아...','괴물은 불에 약하다고!','크크크, 이거 할 만하군...','이 기세로\n오피셜 토너먼트도\n우승해 버리자! 응!','인터넷12로 돌아가서,\n오피셜 토너먼트에\n등록이다아!!','불타오른다아아!!'],
7:['다음에 다시 태어난다면,\n깨끗한 마음을 가지고\n태어나라...','자, 인터넷12로\n돌아가 볼까','오피셜 토너먼트에\n아직 등록하지 않았다'],
8:['임무 완료!!','셰이드맨...\n만만치 않은 상대였다','하지만, 이 브루스에게\n베지 못할 것은 없다!!','자, 인터넷12로\n돌아갑시다!','오피셜 토너먼트의\n등록을 마쳐야\n합니다'],
9:['...사, 살아 있다...','이, 이긴 건가요...\n...제가','다, 다행이다아아아!!','전, 정신이 하나도 없어서\n뭐가 뭔지...','그, 그런 것보다!\n이, 이런 위험한 곳은,\n얼른 나가죠!!','인터넷12에서\n오피셜 토너먼트에\n등록도 해야 해요!','어, 얼른... 네, 네!'],
10:['건곤일척!!\n내 주먹에\n부서지지 않을 것은 없다!!','...인터넷12로\n돌아간다','오피셜 토너먼트에\n등록해야지'],
11:['해, 해냈다!\n나... 나, 나,\n이겼구나!!','난 몇 번이나 질 뻔했다\n하, 하지만 이긴 것은,\n네 덕분!!','나, 정말 기쁘다!','오피셜 토너먼트도\n이 기세로 힘낸다!','앗,\n오피셜 토너먼트의\n등록, 아직이다!','인터넷12로\n돌아가자!!'],
12:['퓨, 퓨우...','이, 이제 끝인가 하고\n생각했어, 퓨...','다리가 아직 떨려, 퓨\n...덜덜','하, 하지만,\n멋진 오퍼레이팅\n이었어, 퓨!!','어, 얼른\n인터넷12로\n돌아가자, 퓨!!','오피셜 토너먼트에\n등록하러 가자, 퓨!','한순간도, 여기에\n있고 싶지 않아, 퓨우!!'],
13:['이것이 대지의 힘!!\n눈부시게 내리쬐는\n태양의 힘이다!!','그러니 어둠의 힘에는\n굴복하지 않는다!!','자, 피곤하겠지,\n인터넷12로\n돌아갈까','오피셜 토너먼트의\n등록을 마치러\n가야겠군'],
14:['이, 이겼네...\n별의 운행이\n좋았던 걸까?','얼른 인터넷12로\n돌아가자','오피셜 토너먼트의\n등록이 기다리고 있어!'],
15:['어둠에 사는 것이\n너뿐이라고 생각하지 마라\n셰이드맨...','나 또한, 어둠의 세계에서\n살아온 나비...','어둠 속 싸움은\n훤히 알고 있다...\n......나무','그럼, 인터넷12로\n돌아갈까...','오피셜 토너먼트의\n등록을 마쳐야\n하겠지...'],
16:['이 세상에 악이 번성한\n적은 없다!!','자, 인터넷12로\n돌아갑시다','셰이드맨 징벌의\n보고와,','오피셜 토너먼트의\n등록을 해야\n하니까요'],
17:['쳇,\n애먹였잖아...','생각보다\n제법 하는 바람에','조금은,\n겁을 먹어 버렸다고...','하지만, 내 상대는\n아니었지!!','이봐, 인터넷12로\n돌아간다!','아직 싸움이 부족해\n오피셜 토너먼트에\n등록하자!!'],
18:['무, 무, 무서웠어요~\n저렇게 무서운 나비는,\n처음이에요...','하, 하지만, 아까\n배틀로 조금\n자신감이 생겼어요','이 정도면, 오피셜\n토너먼트에 나가도,\n좋은 결과를 낼 것 같아요!','얼른 인터넷12에\n등록하러 가는 거예요!'],
19:['...방전,\n모조리 해 버렸군...','인터넷12로 돌아가서,\n오피셜 토너먼트의\n등록을 마치면,','한동안 충전하고 싶은\n기분이다...'],
20:['잠들어라... 셰이드맨','하지만, 네가 꽃을\n피울 일은 없다...','이제, 2번 다시는...','자, 인터넷12로\n돌아갈까...','우리의 화려한 무대,\n오피셜 토너먼트의\n등록을 해야지'],
21:['뭐가 어둠의 힘이냐\n시시한 벌레 녀석...','...이봐,','오피셜 토너먼트라는 곳에는,\n쓰러뜨릴 만한\n녀석들이 나오겠지?','흥, 인터넷12로\n돌아간다...'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('organ scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('organ topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('organ tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=portrait,origin_portrait=portrait,portrait_visibility=visibility,context='ShadeMan last threat0 and21 Navi victory responses1..21, Internet12 return and Official tournament entry reminders; all scripts read.',variable_context='No dynamic name/item values. Destination12 and source2 repetition retained; no numeric formatting conversion or implied automatic registration.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-boss-victory-return',context='All98 Japanese literals in22 scripts; ShadeMan defeat threat,21 Navi post-victory reactions/Internet12 return/entry reminder read.',voice='Preserve relieved/scared/brash/formal/solemn Navi personalities, ShadeMan still threatening; GutsMan 가스/AquaMan 퓨/JunkMan hesitancy inherited candidates. Not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep21-Navi checkNaviAll table, unused1/2 continue, end/page/portrait boundaries and all12 destinations and2 repetition. No registration/return/quest flag added.',semantic_review=['ShadeMan insists darkness is infinite; do not turn post-battle threat into certain final extinction or confirmed revival. Navi victory dialogue remains each speakers belief.', 'Internet12 return for Official tournament registration is an instruction, not automatic completion. KnightMan separate ShadeMan defeat report and registration retained across pages.', 'WindMan cleared miasma continues prior 사악한 기운; FireMan fire weakness claim remains boast not verified battle rule. WoodMan sunlight/earth, StarMan favorable stars and PlantMan flower stage remain imagery.', 'ProtoMan self-praise firm register then polite operator guidance; NumberMan lives/has won and JunkMan gratitude/forgotten entry separated. No human name or player gender inferred.', 'MetalMan けんこんいってき drafted 건곤일척 and ShadowMan ナム drafted 나무 prayer fragment, not tree object. Human wording/presentation review pending; no source spelling repair in protected fields.', 'ShadowMan source オフィシャルトーメント typo maps same tournament context, candidate translated consistently without changing source. PlantMan literal2 kept2 rather than mechanically normalizing numeral to Hangul.', 'No normal-play ShadeMan defeat/Navi routes/Internet12 return/report/tournament entry/save/screen verification. Static preservation not runtime or human approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve organ draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
