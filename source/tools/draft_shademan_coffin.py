"""Manual102 ShadeMan coffin encounter candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7C8570':('3fc27d44327bc623efd192c9f709e2a7d5e2287ff85563817d7e0a7c8bda870b',102,'translations/shademan_coffin_encounter_draft_ko.json'),
}
DRAFT={
'7C8570':{
0:['어, 엄청난\n어둠의 에너지가\n느껴져!!','이, 이 관...\n...설마'],
1:['시, 싫어...\n뭐야, 이 기분 나쁜\n관은...','이거, 혹시...'],
2:['...뭐, 뭔가,\n몸이 오싹하다, 가스!','이 관 안에서\n소름 끼치는\n힘이 느껴진다, 가스...'],
3:['...사악한 기운이 느껴지네\n그것도 어지간한\n기운이 아니네...','이 관인가...'],
4:['목표 포착!!','지금까지 느낀 적 없는\n종류의 힘입니다...!','배틀 칩을 준비하십시오!'],
5:['...이 관인가\n고약한 취미로군','얼른\n삭제해 버리자'],
6:['불길한 힘이\n느껴진다...\n...조심해라!!'],
7:['엄청난 힘이\n느껴집니다...','이 감각...\n틀림없는 어둠의 힘!'],
8:['저, 저기...\n이제 돌아가지 않을까요?','오피셜 토너먼트도\n목숨이 있어야 의미가 있죠...','나머지는 오피셜 나비에게\n맡기고...'],
9:['이게 그 관이군','관에서 새어 나오는\n새까만 힘...','이번만큼은,\n각오를 단단히 해야\n할 것 같군...'],
10:['이, 이 관\n안의 나비를\n쓰, 쓰러뜨리면 되는 거지?','괘, 괜찮다,\n네 오퍼레이팅만 있으면\n어떻게든 된다!!'],
11:['퓨, 퓨퓨...','이, 이건...\n괜히 손대지 않는 편이\n좋지 않을까, 퓨?','...무, 무서워, 퓨...'],
12:['어, 엄청난 어둠의 힘\n......','이 관 안에는\n대체 뭐가 들어 있는 거지!?'],
13:['저, 저기, 이건\n좀 위험하지 않아?','나도, 넷 배틀에는\n자신이 있지만...','...이런 힘은,\n느껴 본 적 없어'],
14:['...윽!!\n엄청난 힘이군...','방심하지 마라...\n안의 녀석은 깨어 있다\n......'],
15:['세상의 평화를 어지럽히는\n사악한 나비가 이 안에 있나...','...나오너라!!','이 나이트맨이\n징벌하겠소!!'],
16:['야, 이봐!!','이 통조림 같은 녀석을\n날려 버리면 되는 거지!!','관째로 화장해\n줄까?'],
17:['...이 관,\n무, 무서워요오...','하, 하지만, 관째로\n얼려 버리면...'],
18:['야, 야...\n느껴지나...?','이 주변의\n「자기장」이 심하게\n흐트러지고 있는 게...','대체, 뭐가\n들어 있는 거지...?'],
19:['후...','스스로 관에\n들어가 주다니\n......','묻어 주는 수고를\n덜 수 있겠군!','내 손으로 그 목숨,\n아름답게 흩날려 주지\n......'],
20:['얼른 관에서\n나와라...','아니면, 그대로\n지워 줄까...'],
21:['...내 잠을\n방해하는 어리석은 자여\n......'],
22:['나를 깨운 것을\n......','영원히 끝나지 않는\n무한한 어둠 속에서\n후회하도록 해라...'],
23:['키키이이이이잇!!'],
24:['온다!!','배틀 오퍼레이션 세트,\n인!!'],
25:['시, 싫어어!!','하, 하지만, 여기서 도망치면\n여자 체면이 말이 아니지!!','오퍼레이팅 부탁해!!\n간다아아아앗!'],
26:['우, 우오오오!!','도, 도망칠 수 없겠다, 가스!\n여기서는 싸워서 길을\n뚫는 수밖에... 없다, 가스!','거츠 거츠 거츠 거츠 거츠\n거어어어어어츠!!'],
27:['사악한 기운을 봉하겠네...','바람이여, 휘몰아쳐라!\n내게 힘을!!'],
28:['타깃, 록온\n......','......\n임무, 시작'],
29:['위, 위험한 녀석이\n나타났잖아!!','이, 이까짓 것!','괴물은 예로부터\n불에 약하다고,\n정해져 있다고!!','히트 업,\n파이어맨!!'],
30:['위대한 천둥이여!','어둠을 묻어 버릴\n힘을 내게!!'],
31:['베겠다!!'],
32:['히, 히야아아!','이, 이렇게 된 이상,\n될 대로 돼라!!','이야아아앗!'],
33:['하아아...\n...정신 집중...','심두멸각!!\n주먹이여, 울려라!!'],
34:['가, 간다!!','오, 오퍼레이팅은,\n부탁한다!!'],
35:['퓨우우우!!','와, 왔어, 퓨!!\n왔어, 퓨!!','퓨, 퓨우우우!!'],
36:['무우우웃!!','정말 사악한\n힘이군!!','대지의 힘으로\n정화해 주마!!'],
37:['큭!\n할 수밖에 없나!!','오퍼레이팅 부탁해!!\n간다!!'],
38:['린, 뵤, 토, 샤,\n카이, 진, 레츠, 자이, 젠!!','...간다!!'],
39:['네놈, 내 철구의\n녹으로 만들어 주마!!','분누오오오옷!!'],
40:['나한테 싸움을 걸다니,\n100만 년은 이르다고!!','재도 남지 않도록\n모조리 태워 주마!!'],
41:['어, 얼려 버리면,\n우리 것이에요~!!','후우우우!!'],
42:['내 100만 볼트로,\n네놈에게 영원한\n잠을 선물해 주마!!'],
43:['꽃잎처럼\n흩날려라!!'],
44:['...쓰레기 녀석!!'],
45:['어둠의 심연에\n가라앉혀 주마!!','키이이이잇!!'],
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
        if not shown and s!=21:raise ValueError('actor missing '+x.key)
        portrait=shown[-1] if shown else None;visibility='visible' if events[-1].group(1) else 'hidden'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('organ topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('organ tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='ShadeMan' if s==21 else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Coffin warnings0..20, common hidden voice21/reveal22/scream23, Navi battle lines24..44 and common ShadeMan45 read.',variable_context='No dynamic name/item values. Hidden speaker21 contextually inferred from sleep/waking lines21/22; no portrait and actual scene transition unverified, not inherited active Navi. Numeric100 units retained.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-boss-coffin-encounter',context='All102 Japanese literals in46 scripts.21 Navi warnings and21 battle responses with common ShadeMan branches read.',voice='Preserve Navi fear/bravado/formal/rough distinctions and ShadeMan ominous voice; GutsMan 가스/AquaMan 퓨 inherited draft candidates. Not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve both21-Navi checkNaviAll tables, unused1/2 continue,21 jumps to21 and21 jumps to45, ShadeMan23 jump24, all page/wait/portrait boundaries. Numeral100 in years/volts retained.',semantic_review=['Script21 hidden voice is contextually inferred as ShadeMan from adjacent waking threat22, not previous Navi; original portrait remains None. Source21 ends without explicit jump22, so scene transition and actor assignment remain review candidates.', 'WindMan ショウキ interpreted ominous miasma from coffin context, drafted 사악한 기운 without an invented named status ailment.', 'NapalmMan coffin/canned insult and cremation, PlantMan burial/beautiful scattering and KnightMan iron-ball rust image kept as source rhetoric, not actual new combat effect.', 'Roll woman-pride line preserves speaker gender and motivation; no implication about player gender. FireMan monsters dislike fire is boast, not confirmed game elemental advice.', 'ShadowMan9-phrase chant transliterated 린/뵤/토/샤/카이/진/레츠/자이/젠 and MetalMan 심두멸각 retained as human-review candidates. Not approved named skills or reconstructed spell mechanics.', 'ProtoMan きる drafted 베겠다 in sword-bearing speaker context, not kill switch or forced deletion command. IceMan freezing boast and ElecMan100만 볼트/NapalmMan100만 년 keep numeric values.', 'Source archived encounter context only. Normal-play coffin/hidden voice/reveal/Navi routing/battle/presentation/save verification not performed; language/layout review still pending.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve organ draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
