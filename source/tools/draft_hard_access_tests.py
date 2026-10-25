"""Manual hard-mode access-test122 drafts; source-bound, no ROM changes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7B5328':('6c6179624780460aefe85703e1fbd89cf66abaad3a019bf69fc71e8abaab279e',55,'translations/hard_access_tests_a_draft_ko.json'),
'7B5CC0':('b3f58953673d0fe4c3c22d040b03b5ac78a77f4bac850948b1a9da2744d5dacf',67,'translations/hard_access_tests_b_draft_ko.json'),
}
DRAFT={
'7B5328':{
0:['이 앞에 가실\n생각이신가요?','제가 당신의\n학력을 확인하겠습니다','제가 납득할 만한\n학력을 지니셨다면,\n지나가게 해 드리죠','하시겠습니까?','예  ','아니요','그럼 시작하겠습니다!!'],
1:['제, 제법이시군요...','좋습니다...\n길을 열어 드리죠'],
2:['아직 공부가\n부족하시군요!','더 공부하고 다시 오세요!'],
3:['그러신가요...'],
5:['여기를 지나가고 싶다면,\n네 오퍼레이터의\n실력을 보여라...','내비의 성능이\n아무리 좋아도, 오퍼레이터가\n못하면 소용없다...','네 오퍼레이터에게\n나를 오퍼레이팅하게 하겠다','내 주먹이 떨릴 만큼\n오퍼레이팅할 수 있는\n오퍼레이터라면,','이 길을 지나가게 해 주마','...하겠나?','예  ','아니요','오퍼레이터,\n준비는 됐겠지!\n시작한다!!'],
6:['...훌륭한\n오퍼레이팅이었다...','오랜만에 주먹이\n떨렸군...'],
7:['오퍼레이터여,\n실력을 갈고닦은 뒤\n다시 오도록 해라'],
8:['...그런가'],
10:['...이 앞에\n가고 싶은 모양이군...','네게 이 앞에\n갈 자격이 있는지\n시험해 주겠다','시험을 통과하지 못하면,\n여길 지나가게 할 순 없다','시험을 받겠나?','예  ','아니요','그럼, 시험 내용을\n설명하겠다','지금부터 인터넷7에\n바이러스를 발생시키겠다...','제한 시간 안에\n그 바이러스들을\n모두 저격해라','그걸 해낸다면,\n시험에 합격한 것으로 하겠다','단, 지금부터 임무가\n끝날 때까지,','한 번이라도 플러그아웃하면,\n이번 시험은 실패로 하겠다','...이상이다'],
11:['그런가...'],
12:['시험 내용을\n확인하러 왔군...','그럼, 시험 내용을\n설명하겠다','지금부터 인터넷7에\n바이러스를 발생시키겠다...','제한 시간 안에\n그 바이러스들을\n모두 저격해라','그걸 해낸다면,\n시험에 합격한 것으로 하겠다','단, 지금부터 임무가\n끝날 때까지,','한 번이라도 플러그아웃하면,\n이번 시험은 실패로 하겠다','...이상이다'],
13:['바이러스를 쓰러뜨리고 왔군\n좋아, 시험 합격이다','지나가도 좋다...'],
14:['바이러스 저격에\n실패했군...','다시 도전하겠나?','예  ','아니요','좋다, 다시\n인터넷7로 돌아가라'],
15:['실력을 쌓은 뒤,\n다시 도전하도록 해라'],
},
'7B5CC0':{
0:['여기를 지나가고 싶으세요?','그렇다면, 오퍼레이터님\n저를 도와주셨으면 해요!','지금, 얼어붙은\n바이러스를 퇴치하고\n있는데요,','저 1명만으로는 좀처럼\n잘 안 돼요','만약 오퍼레이터님의\n도움으로 바이러스를\n쓰러뜨릴 수 있다면,','길을 열어 드릴게요!','도와주실 건가요?','예  ','아니요','그럼 부탁드릴게요!'],
1:['해냈어요!!\n덕분에 바이러스를\n쓰러뜨릴 수 있었어요!','그럼 약속대로,\n길을 열어 드릴게요!!','고마워요!!'],
2:['부우우...','안 됐어요!!\n그렇게 해서는,\n여길 지나가게 할 수 없어요!!'],
3:['그런 말씀은,\n하지 말아 주세요~'],
10:['...너,\n여기를 지나가고 싶은가!?','난 마음에 든 녀석에게만\n길을 열어 주는 주의다','여길 지나가고 싶다면\n내가 말한 대로 해서,\n내 마음에 들어 봐!!','어때, 하겠나?','예  ','아니요','헤헤헤, 뭘\n시켜 볼까...','그렇지...\n좋아, 이렇게 하자','언더인터넷2에\n지금부터 내가 바이러스를\n뿌릴 테니까','그 바이러스들을\n제한 시간 안에\n모두 날려 버려라','콰앙 하고 말이야!!','내 네이팜 프로그램을\n빌려주마...','그리고 1가지 더, 내가 뿌린\n바이러스를 모두\n날려 버릴 때까지,','절대로 플러그아웃하지 마라','바이러스가 무서워\n인터넷도 못 돌아다니는\n겁쟁이는 싫어하니까','한 번이라도 플러그아웃하면\n여길 지나가게 하지 않겠다','아무튼\n화끈하게 해 보라고!'],
11:['그런가, 그럼 다른 길을\n찾아보도록 해!'],
12:['뭐야? 뭘 해야 하는지\n벌써 잊었나?','할 수 없군, 다시\n말해 주마!','언더인터넷2에\n지금부터 내가 바이러스를\n뿌릴 테니까','그 바이러스들을\n제한 시간 안에\n모두 날려 버려라!','그리고 1가지 더, 내가 뿌린\n바이러스를 모두\n날려 버릴 때까지,','절대로 플러그아웃하지 마라','바이러스가 무서워\n인터넷도 못 돌아다니는\n겁쟁이는 싫어하니까','한 번이라도 플러그아웃하면\n여길 지나가게 하지 않겠다','아무튼\n화끈하게 해 보라고!'],
13:['언더인터넷2에서\n네가 바이러스를\n날려 버리는 걸 봤다','너, 제법 소질이\n있잖아!!','마음에 들었다...\n자, 지나가라!!'],
14:['뭐야, 실패했잖아\n그래서는 이 길을\n내줄 수 없다고!?','한 번 더 갔다 올 건가?','예  ','아니요','그럼 얼른 갔다 와라!!'],
15:['그런가, 그럼 다른 길을\n찾아보도록 해!'],
20:['이 앞에 가고 싶은가?','그럼, 이 앞에 갈\n자격이 있는지,\n시험해 주겠다...','단, 시험할 상대는\n네가 아니라,\n네 오퍼레이터다...','오퍼레이터여,\n나를 오퍼레이팅해서,\n바람을 일으켜 보아라!!','내가 감탄할 만한\n바람을 일으킬 수 있다면\n여길 지나가게 해 주마','어떠냐...?','예  ','아니요','그런가, 그럼 바로\n시작하자...','간다!!'],
21:['으, 으음음음...!!\n제법이지 않느냐','나를 감탄하게 하다니,\n훌륭한 녀석이군...','자, 지나가도 좋다...'],
22:['그 정도 실력으로는\n나를 감탄하게 할 바람을\n일으킬 수 없다...'],
23:['...음, 그런가...'],
},
}

def create(archive):
    source_sha,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,source_sha);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('hard access scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden';speaker=portrait if visibility=='visible' else 'player-choice'
        if archive=='7B5CC0' and s==14 and i in (2,3):speaker='player-choice'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('numbers/tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spaces '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,origin_portrait=portrait,portrait_visibility=visibility,context='Source hard=true passage tests: NumberMan academic/MetalMan operation/SearchMan sniping or IceMan extermination/NapalmMan explosive/WindMan operation. Initial, reminders, success/failure/refusal/retry read together.',variable_context='No variable names/items; source numeral1/7/2, portraits/options/flags/hard-mode calls and page boundaries retained. Caller/runtime/layout review pending.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive=archive,source_tpl=dict(path=source,sha256=source_sha),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-and-choice',context=f'All{count} unselected Japanese literals in255-slot archive. Complete local branches read, hard-mode start calls preserved. Source text/ROM payload pinned.',voice='NumberMan polite testing, MetalMan terse strength, SearchMan tactical, IceMan polite help, NapalmMan rough showmanship, WindMan commanding admiration separated. Candidates not human-approved new voices.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve source IDs, numeral1/7/2, flags5507/5571/5140/6403/6217/4958, hard=true minigame calls, acceptance/refusal/retry and plugout failure. No gameplay/save/ROM mutation.',semantic_review=['SearchMan Internet7 is not earlier Internet2; NapalmMan UnderInternet2 is not normal Internet2. Unspecified time limits remain unspecified; both require all viruses and any plugout means failure.', 'MetalMan and WindMan test the operator by operating the speaker, not fighting their own Navi. Fist tremble and admiration keep separate source metaphors; no imagined puzzle instructions added.', 'NumberMan academic test is source がくりょく candidate 학력; not a graduation credential gate. Functional wording and consistency require human review.', 'IceMan success promises passage after extermination and failure refuses; polite childlike source voice inherits the earlier candidate but hard=true remains separately tracked.', 'NapalmMan retry14 options have visible portrait; they are player choices, not lines spoken by him. Script12 reminder omits lending-program line as source does; no borrowed command/reward inserted.', 'No human terminology/voice approval or actual gameplay access/clock/minigame/save/geometry verification claimed.'],units=units)

def main():
    for archive,(_,count,out) in SOURCES.items():
        a=create(archive);path=ROOT/out
        if path.exists():
            if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation '+out)
        else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {archive} {count} draft only; ROM unchanged')

if __name__=='__main__':main()
