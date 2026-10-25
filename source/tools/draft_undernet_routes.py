"""Individually authored UnderNet battle/shop/registration137; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7B32B0':('2f1da91f470c7feb1f78b24cdb095a161b632cb3c85de5c0fa2baa983db54759',18,'translations/undernet_battlers_a_draft_ko.json'),
'7B3490':('dc100365339ac666c661f99e34b2f81b32182bf43a05e8388a893feb6ddb2165',21,'translations/undernet_shop_draft_ko.json'),
'7B39D0':('e9db7a6ef178b9d2c0cb5a6a0db1d06d9833debfe6babf56fb6d33bccbc1b772',21,'translations/undernet_battlers_b_draft_ko.json'),
'7B469C':('6314a686c064496b7f200787bbd836a201836103d8e239ddbc803f914a54b210',41,'translations/undernet_battlers_c_draft_ko.json'),
'7B4A6C':('c5dbc8a6354a4ae7202129f4b9114ea966bec499f5d91662cbb8308f56db8365',36,'translations/undernet_entry_draft_ko.json'),
}
DRAFT={
'7B32B0':{
0:['구헤헤...\n배틀하지 않겠나...?','좋아!  ','싫어','헤헤헤... 그런가...'],
1:['게헤헤헤','배틀 오퍼레이션!!\n세트으읏!!!','인!!'],
2:['언더의 무서움을\n알려 주려고\n했는데 말이야...','헤헤헤...','너한테는 가르칠 게\n아무것도 없는 모양이군'],
3:['게헤헤... 봤느냐...\n이것이 언더의 무서움이다'],
4:['...배틀...\n...하지 않겠나...','좋아!  ','싫어','그런가...'],
5:['...배틀오페세인!'],
6:['...승부에선 졌지만,\n싸움에선 이겼다...'],
7:['...봤느냐, 언더의 힘!'],
},
'7B3490':{
0:['헤헤헤...\n여기는 지옥의 1번지다','삭제되고 싶지 않다면\n얼른 플러그아웃해라'],
1:['구헤헤헤...'],
70:['키라키라키라라~!!','저는 금색 프로그램!','배틀 칩 게이트에서\n다 써 버린 칩의\n사용 횟수를...','회복시켜 드리겠습니다!!','키라라키라!!'],
221:['또 오세요!'],
222:['저는\n서브 칩 상인입니다만','지금은 품절입니다!\n죄송해요'],
223:['저는\n서브 칩 상인입니다!','좋은 물건이 있답니다~!\n','볼래  ','안 볼래'],
224:['저는\n서브 칩 상인입니다!','오늘은 일주일에 한 번인\n레이디스 데이!!','여자아이에게는 팍팍\n서비스해 드릴게요!','좋은 물건이 있답니다!?\n','볼래  ','안 볼래'],
},
'7B39D0':{
0:['일반 인터넷에서 왔나?','어때, 조금 놀지 않겠나?','응  ','싫어','결국 일반 인터넷 녀석인가...'],
1:['놀아 주마!\n단, 언더의 규칙으로 말이지!','배틀 오퍼레이션, 세트!\n이인!!'],
2:['서, 설마 일반 인터넷에\n이런 녀석이 있었다니!!'],
3:['어떠냐, 재미있었지,\n언더의 놀이가 말이야!!'],
4:['킁킁...\n강한 녀석의 냄새가 나네요','당신, 상당한\n실력자시죠?','냄새로 알 수 있습죠...','저와 겨뤄\n주시지 않겠습니까?','좋아!  ','싫어','군자는 위험한 곳을\n가까이하지 않는다... 이거죠?'],
5:['갑니다요...','배틀 오퍼레이션, 세트!\n인!!'],
6:['제 코는 틀리지\n않았나 봅니다요...'],
7:['이런, 더 강하실 줄\n알았습니다만...','제가 잘못 생각했나\n봅니다요...'],
},
'7B469C':{
0:['더 할 말은 없다...\n나와 싸워라...','덤벼!  ','싫어','겁먹었나...','오히려 그 정도 녀석이라면,\n싸울 가치도 없다!!'],
1:['배틀 오퍼레이션, 세트!\n인!!'],
2:['생각했던 것보다...\n강하군...'],
3:['이 정도인가...','목숨이 아깝다면,\n빨리 언더에서 나가라','그 정도 실력은,\n언더에서 통하지 않는다'],
4:['난 어둠의 힘에\n매료되어 일반 인터넷에서\n온 내비다...','너도 같은 부류인 모양이군','같은 부류끼리,\n나와 배틀해 보지 않겠나?','응!  ','아니','흥... 그렇게 해서는\n언더에서 살아갈 수 없어'],
5:['후오오오옷...\n어둠이여... 내게 힘을!','배틀 오퍼레이션, 세트!\n인!!!'],
6:['어, 어둠의 힘이...\n부족한 건가...!?'],
7:['이것이 어둠의 힘이다!!'],
8:['후슈~...','너... 나와...\n배틀... 한다...','한다!  ','거절한다!','너... 겁쟁이...'],
9:['배틀... 시작한다...\n우아와오와아아...'],
10:['너... 강하다...'],
11:['너... 약하다...'],
12:['으랴앗!!\n나와 싸워라아아아!!'],
13:['저, 졌다고!?\n으아아아앙!!'],
14:['헤헤헤...','당장이라도 몸에서\n불이 날 정도로 뜨겁군...'],
15:['봉주르!!','저와 배틀을\n하시겠습니까?','한다!  ','거절한다!','모처럼 당신을 위해\n블러디 파티를\n열려고 했는데...'],
16:['그럼, 당신을 위한\n블러디 파티를...\n지금 개막하겠습니다...','배틀 오퍼레이션, 세트!\n인!!'],
17:['제법이군요...'],
18:['후후후후후후후...\n블러디 파티가,\n마음에 드셨습니까?'],
},
'7B4A6C':{
0:['자네의 오퍼레이터,\n진짜 실력을\n지닌 모양이군...','어떤가, 주말에\n열리는,','언더 토너먼트에\n나가 보지 않겠나?','등록비로\n2000제니가 들지만 말이야','어쩔 텐가,\n신청하겠나?','예  ','아니요','뭐, 언더의 최강을\n가리는 토너먼트니까...','겁먹는 것도,\n무리는 아니겠지...','각오가 되면\n다시 오게...'],
1:['무슨 일이지?','난 진짜\n실력을 지닌\n오퍼레이터가 아니면,','말할 마음이 안 생겨\n얼른 돌아가라'],
2:['여기는 언더 토너먼트의\n참가 접수장이다','언더 토너먼트에\n신청할 건가?','신청한다면\n등록비로\n2000제니를 받겠다','어쩔 텐가,\n신청하겠나?','예  ','아니요','뭐, 언더의 최강을\n가리는 토너먼트니까...','겁먹는 것도,\n무리는 아니겠지...','각오가 되면\n다시 오게...'],
3:['그럼, 등록비로,\n2000제니를\n받겠다...','잠깐 기다려라...\n언더 토너먼트에...\n...신청... 완료!','좋아, 끝났다','토너먼트는, 주말에\n열린다','목숨을 잃지 않도록\n열심히 해 보게'],
4:['미안하지만 돈이 부족하군\n자네 실력은\n인정하지만,','역시 이 세상은 돈이지...','2000제니를 모아서\n다시 오게'],
5:['오늘의 등록은\n마감됐다...'],
6:['여기는 언더 토너먼트의\n참가 접수장이지만,','주말에는 참가 신청\n접수를 하지 않는다...','신청하려면 월요일부터 금요일\n사이에 오게'],
110:['토너먼트 참가 접수는,\n평일 아침6시부터\n밤12시까지입니다!'],
111:['드르렁~, 드르렁~...\n드르렁~, 드르렁~...'],
},
}

def create(archive):
    source_sha,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,source_sha);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('under scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)}
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if archive=='7B3490' and s==221:portrait='PurpleNavi';visibility='inherited from native223/224 caller';speaker=portrait
        else:
            if not shown:raise ValueError('actor missing '+x.key)
            portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden';speaker=portrait if visibility=='visible' else 'player-choice'
            if archive=='7B3490' and (s,i) in ((223,2),(223,3),(224,4),(224,5)):speaker='player-choice'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('numbers/tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spaces '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,origin_portrait=portrait,portrait_visibility=visibility,context='UnderNet local encounter acceptance/refusal/outcomes, menace/shop/gate-recovery and Under tournament registration; full native source branch read. Each source portrait associated per literal, including visible shop choices.',variable_context='No runtime name/item interpolation; source controls, flags, battle storeGlobal parameters, shop and registration transitions retained. Width/caller/clock review pending.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive=archive,source_tpl=dict(path=source,sha256=source_sha),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-and-choice',context=f'All{count} unselected Japanese literals in255-slot archive; source/payload pinned; no inferred progression repair.',voice='Source-specific rough, compressed, courteous sly and registration voices; portraits not conflated across encounters. Candidate terms from tournament/story/official-entry assets, no new approvals.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep IDs, numeric1/2000/6/12, source line/option spaces, battle/flag/shop arguments, shop7/17, weekday3+navi1, tournament8 vs Official4, weekday0/6 closure, flag1762 and eligibility checks. No ROM/gameplay/save writes.',semantic_review=['ウラ is 언더 and オモテ is 일반 인터넷 in network contrast; candidate wording not a newly approved glossary. ジゴクの1チョウメ keeps numeric1 as 지옥의1번지 metaphor, not a real mapped location.', '7B32B0:5 intentionally compresses native battle call as 배틀오페세인, not normalizing it into a new page.6 keeps ironic 승부 defeat vs 싸움 victory, not reversing actual outcome.', '7B39D0:4/5/6/7 smell and humble slang preserved as separate speech candidate; proverb 군자는 위험한 곳을 가까이하지 않는다 retained rather than invented coward insult.', '7B469C:4 asserts similarity from the speaker perspective, not a confirmed player alignment;12 forced encounter has no added decline.12 and16 share native battle178/656 but have separate outcome scripts; unchanged even if they look duplicated.', 'Shop portrait PurpleNavi remains visible on options; choices are player-choice,221 inherits223/224. Shop7 normal vs17 ladies branch and source stock refusal retained. No discount percentage/weekday invented.', '7B4A6C uses2000zenny, tournament bitmask8 and source multi-flag requirements; do not borrow Official free or1000zenny terms. Entry weekday/time and sleeping111 preserved; no inferred number of wins/bosses added.', 'GoldProg restores chip use counts via callClearBattleChipGateHistory, not HP/new chips/save erasure. Phonetic キラ and ブラッディパーティ/봉주르 remain human-review candidates.', 'Actual gameplay access/clock/shop/battle/registration charge, display/geometry and persistence remain unverified.'],units=units)

def main():
    for archive,(_,count,out) in SOURCES.items():
        a=create(archive);path=ROOT/out
        if path.exists():
            if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation '+out)
        else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {archive} {count} draft only; ROM unchanged')

if __name__=='__main__':main()
