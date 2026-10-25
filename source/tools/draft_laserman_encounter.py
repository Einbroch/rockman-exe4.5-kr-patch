"""Manual73 LaserMan encounter candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7C9C44':('eeeaa9510dc7c6ae82b96eeb2acd556bbe177ee38850f62bd6e6f71186327b79',73,'translations/laserman_encounter_draft_ko.json'),
}
DRAFT={
'7C9C44':{
1:['나는 레이저맨\n......','아득히 먼 곳에서\n증오의 힘에\n이끌려 왔다...','왜 내가 여기에\n있는지...','왜, 여기서 싸움을\n갈구하는 나날을\n보내고 있는지...','전혀 기억나지 않는다...','하지만, 이 몸에서\n넘쳐흐르는 증오에','모든 것을 맡기고\n싸움에 미쳐 날뛸 때,','나는 본래의\n나를 떠올릴 수\n있는 것이다...','미치게 해 다오...\n증오의 소용돌이 속에서!!'],
2:['즈, 증오로 날뛰는\n엄청난 어둠의 힘이야\n......','온다, 오퍼레이팅 부탁해!!','배틀 오퍼레이션 세트!\n인!!'],
3:['...뭐, 뭐, 뭐야!\n왜 이렇게 막무가내야!','이런 녀석에게 질 수는\n없어!','힘낼게!\n오퍼레이팅, 부탁해!','간다!!'],
4:['거츠맨도 사나이다, 가스!\n걸어온 싸움은,\n받아 준다, 가스!!','해치워 주겠다, 가스!!\n거츠, 거츠, 거츠!'],
5:['증오에 삼켜졌는가\n......\n가엾구나, 레이저맨!','나의 바람의 힘으로,\n그대의 증오까지\n날려 버리겠다!!','후슈우우우!!'],
6:['...옵니다!\n전투 준비를!','...타깃,\n록온!!','미션 스타트!!'],
7:['쳇, 증오만이\n네 존재를\n증명하는 것이라면,','넌 정말로\n불쌍한 녀석이다...','네 증오까지,\n내가 전부,\n불태워 주마...','파이어어어어!!'],
8:['나의 우레의 힘을,\n똑똑히 맛보아라\n......','그 증오로\n뒤틀린 마음을,\n지워 버리겠다!!'],
9:['레이저맨...\n오피셜의 블랙리스트에\n올라 있는','스페셜 S랭크의\n범죄자....','설마, 이런 곳에\n있었을 줄이야...!!','...참!!'],
10:['저, 저는 아무\n관계도 없어요!','이, 이제, 바로\n돌아갈 테니까요!','그아아아아아아아악!!','히, 히이이익\n살려 주세요오오!!'],
11:['증오에 몸을 맡긴\n싸움 방식으로,\n나를 이길 생각은 마라','이 주먹으로 네\n나약한 마음을\n바로잡아 주겠다!!'],
12:['자, 자신이 누군지\n모르는 불안함...\n나, 잘 안다...','하지만, 나 이제는\n불안하지 않다!!','나, 나는 질 수는\n없다!!'],
13:['퓨, 퓨우웃!!','어, 엄청난\n증오의 힘이야, 퓨!','머릿속 물이 탁해져\n오고 있어, 퓨...!','이, 이쪽으로\n오지 마, 퓨우!'],
14:['분노로 날뛰는\n증오의 힘이여','영원한 잠이라는\n안식을 주겠다!'],
15:['이거...\n내 힘만으로는\n못 이길 것 같네...','밤하늘에 반짝이는 별들이여\n내게 힘을 빌려 줘!','간다!!'],
16:['증오의 힘에\n매달리고, 삶에 매달리는\n망령인가...','나의 인술로\n저승으로 보내 주겠다!','카아아앗!!'],
17:['므으음!!','어둠을 두른\n사도의 전사여!!','내 철구의\n녹으로 만들어 주겠다!!'],
18:['너는 나와\n같은 냄새가 나는군...','훗,\n너도 싸움 속에서만,','살아 있다는 실감을\n느낄 수 있는 거지?','서투른 녀석들끼리,\n즐겁게 해 보자고,','...안 그래!!'],
19:['오, 오퍼레이팅\n잘 부탁해요!!','이 녀석은 쉽게\n상대할 수 없어요!!','오, 오고 있어요!!'],
20:['엄청난 힘이군...','이런 녀석에게 내 전격이\n통할까...?','하지만, 할 수밖에 없겠군\n...각오를 다져라...','...간다!!\n100만 볼트!!'],
21:['내 꽃잎을,\n떨어뜨릴 수\n있을까!?'],
22:['증오의 힘인가...','재미있군...\n자, 덤벼라'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text) and int(x.key.split(':')[1])!=0]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('laserman scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('laserman topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('laserman tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=portrait,origin_portrait=portrait,portrait_visibility=visibility,context='LaserMan introduction1 and21 Navi battle responses2..22; complete archive read, unshown speaker0 unresolved and not selected.',variable_context='No dynamic name/item variables. Preserve S rank and literal100 voltage value.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-boss-encounter',context='73 explicitly shown-speaker Japanese literals in scripts1..22. Two unshown-voice literals0 remain awaiting context, not excluded from denominator.',voice='LaserMan hatred/amnesia, Navi reactions and personality candidates; GutsMan 가스/AquaMan 퓨/JunkMan hesitancy inherited. Not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep21-Navi checkNaviAll/unused1/2 continue,1->2 jump,NumberMan->LaserMan->NumberMan portraits,100 voltage and S rank/page controls; preserve two unselected script0 literals.',semantic_review=['No speaker established in script0; preserved in source and pending ledger. No inference promoted to actor fact.', 'LaserMan does not recall why here; surrendering to hatred recalls original self. No invented identity or backstory.', 'JunkMan empathizes with not knowing oneself but is no longer anxious; NapalmMan shares battle-driven feeling of being alive, not identical origin.', 'ProtoMan Official blacklist Special S rank remains intact. ShadowMan sends specter to afterlife; KnightMan iron-ball rust metaphor retained as candidate.', 'NumberMan mid-script scream is LaserMan, then NumberMan begs rescue. ElecMan hundred-man voltage value100 preserved.', 'No normal-play encounter/battle/portrait/save/screen verification; static preservation not runtime or human approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve laserman draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
