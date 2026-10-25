"""Manual132 Bass victory candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7CB850':('f066fcbd31bc5edd0388ec44883c536667061a382cf058be9e2f3631ca77237e',132,'translations/bass_victory_draft_ko.json'),
}
DRAFT={
'7CB850':{
0:['누오오오...\n왜...인가...','이 내가...\n...패배할 리가...','...크윽...\n구오오오오오오옷!!'],
1:['나는... 멸망하지 않는다!!','구오오오오오오오옷!!'],
2:['하아, 하아...','네 오퍼레이팅\n덕분에... 이겼어...','나 1명의 힘만으로는\n도저히 이길 수 없었을\n거야...','...고마워!!','...자, 돌아가자!'],
3:['나, 나... 이긴 거야?','다행이다~...','어, 어라...\n안심하고 나니까...','어라... 눈물이...','흑, 흑...','필사적으로 오퍼레이팅해\n줬잖아...','네 마음,\n전해졌어...\n...흑...흑','고마워...흑...','...얼른 PET으로\n네가 있는 곳으로...\n돌아가고 싶어...'],
4:['우, 우오오오오, 가스!!','해냈다, 가스!!\n이겼다, 가스!!\n멋진 오퍼레이팅이다, 가스!!','...하, 하지만...','사, 살아 있는 기분이\n전혀 안 든다, 가스...','지금까지 나비로 살면서\n가장 강한 적이었다, 가스\n......'],
5:['무서운 나비였네...','사악한 기운은 사라졌다...\n하지만, 언제든','부활할지도 모르지...\n하지만, 그때는,','다시 내가\n쓰러뜨려 주겠네...','...물론,\n그대와 함께 말이네!','그럼, 돌아갈까!'],
6:['타깃, 삭제...','미션, 컴플리트!','이번 배틀은\n제가 지금까지\n경험한 것 중','가장 가혹한\n배틀이었습니다...','하지만, 만약\n녀석이 되살아난다고 해도,\n이제 괜찮습니다','녀석의 데이터는 전부\n기억했습니다','...그리고 무엇보다,\n당신이 있으니까요','자, 귀환합시다'],
7:['이, 이번만큼은\n다, 다 타 버렸군...','완전연소다...','솔직히, 절대로\n못 이길 줄 알았어','하지만, 네\n오퍼레이팅과 호흡을\n맞추다 보니','몸 깊숙한 곳에서\n부글부글 힘이\n솟아올랐거든...','이 정도면 이길지도 모른다는\n생각이 들기 시작했어...','내가 이긴 건\n네 덕분이야,\n...고맙다','뭐, 뭐야, 그 눈빛은!!\n부끄럽잖아!','도, 돌아간다, 어이!!\n아까 같은 꼴은\n두 번 다시 사양이야!'],
8:['심판의 벼락 앞에\n거악은 사라졌다...','하지만, 언젠가 다시,\n녀석 같은 존재가\n나타나겠지...','그래도, 그때 역시,\n너와 함께\n맞서고 싶군','자, 돌아가자...'],
9:['...삭제 완료','훌륭한...\n오퍼레이팅이었습니다','이번 승리는\n당신의 것입니다...','당신과 함께\n싸울 수 있다는 것을\n자랑스럽게 생각합니다...','자, 돌아갑시다,\n새로운 임무가\n기다리고 있습니다!'],
10:['하, 하와와와와와와...','저, 제가, 이긴 건가요?','승리 확률,\n0、00001퍼센트의\n배틀에서...','......기적','하지만, 왜... 아!\n확률을 계산했을\n때에...','제 데이터만\n넣었네요!','최강의\n불확정 요소,\n당신의 존재를!','우리 나비는,\n오퍼레이터와의\n호흡에 따라서는,','계산으로는 산출할 수 없는\n무한한 힘을\n만들어 내는군요...','그렇다면, 당신을\n단련하면, 저는 더욱\n강해질 수 있다는 거네요','바로, 돌아가서\n산수 공부를 해요!','저를 위해서라도,\n열심히 해 줘야겠어요!!'],
11:['엄청난 힘을 가진\n나비였다...','녀석의 힘 앞에서\n내 주먹이 얼마나\n작아 보였던지...','이번에는, 네\n도움으로, 어떻게든\n이길 수 있었지만...','나는 아직도\n수련이 부족하다...','네가 안심하고\n지켜볼 수 있도록\n1부터 다시 시작한다!'],
12:['나, 나, 이겼다...\n네 덕분...','나, 네 나비여서\n다행이다...','더 가까이에서\n네 얼굴...\n보고 싶다...'],
13:['퓨퓨퓨...','이제, 끝인가 하고\n생각했어, 퓨...','그러니까, 앞으로 가기는\n싫다고 했잖아, 퓨\n큰일을 겪었어, 퓨!!','그 보답으로는...\nPET으로 돌아가면,','엄청, 예뻐해\n줘야 해, 퓨!!','알겠지, 퓨!!'],
14:['해냈군...\n이제, 녀석의 기척은 없어...','위대한 대지에\n감사해야겠군...','물론, 너에게도... 말이지','...그래, 대지에\n감사하는 뜻으로','플러그아웃해서\n밖에 나무 1그루라도\n심으러 가지 않겠나'],
15:['태양의 홍염 같은\n힘을 가진 녀석이었네','왜, 내가\n그런 괴물 같은 녀석에게\n이겼을까...?','...알았어!!','너야!\n네가 나에게는\n행운의 별인 거야!','그것도, 초특대급으로!','너와 함께 있으면,\n좋은 일이 있을 것 같아!\n앞으로도, 잘 부탁해!','...그렇게 싫다는\n표정 짓지 마!','PET으로 돌아가면,\n또 매일\n점을 봐 줄 테니까!','응, 응!!'],
16:['...포르테\n어둠으로 돌아갔나...','하지만, 네놈은\n이 정도로 사라질\n나비는 아니겠지...','언젠가 다시,\n맞붙게 되겠지...','...새로운 의뢰가\n있을지도 모르니... 돌아간다!!'],
17:['전뇌 세계에 이 정도의\n강자가 있었다니\n놀랍군...','사악한 자가 아니었다면,\n부하로 삼았을 텐데','참으로, 아쉽군...','나도 더욱\n수련을 쌓아,','더욱 큰 힘을\n손에 넣겠소!!','자, 갑시다!!'],
18:['하아하아하아...\n보, 보았냐... 내, 내가...\n내가... 이겼다아아아','갸하하하하하하하하!!','콜록!!','쳇, 조, 조금\n상처를 입은\n모양이군...','...상처를 치료하자고?','그런 건 필요 없어!','그것보다...\n더 싸우게 해 줘!!','나도 녀석도,\n싸움 속에서만\n자신을 달랠 수 있지...','자, 다음 상대는\n누구냐!!'],
19:['주, 죽는 줄...\n...알았어요...','하, 하지만,\n그렇게 대단한 나비에게\n이기다니...','...저, 감격했어요!','저, 더욱더\n강해질 거예요!!','얼른 돌아가서\n연습할 거예요!!'],
20:['머, 멋진 오퍼레이팅...\n네... 덕분에\n이길 수 있었다...','...하, 하지만...\n이, 이제... 텅 비었어...','꼬마전구 1개도\n켤 수 없어...','어, 얼른... 돌아가자...','전기 속성 칩을\n배부르게 인스톨하고\n싶은 기분이군...'],
21:['강함...\n그것은 곧,\n아름다움...','그는 아마,\n나의 아름다움에\n넋을 잃었을 거야','......으윽','여, 여기는... 너무 어두워\n얼른, PET으로 돌아가\n햇빛을 쬐고 싶군...'],
22:['결국은 그림자인가...','그림자가 아무리\n허세를 부려도\n오리지널에게는 못 이긴다...','이 세계에는...\n내 투쟁 본능을\n만족시킬 녀석이 없는 건가!'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
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
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Bass0/1 defeat threat and21 Navi2..22 postbattle reactions; complete archive read. Same Bass portrait scene roles kept distinct.',variable_context='Preserve literals1 and0、00001 probability; no automatic PET return/plugout/training or item command added.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-bass-victory',context='All132 Japanese literals in23 scripts, defeated challenger0/1 and21 player Navi reactions2..22.',voice='Gratitude/fear/relief/bravado/formality source-specific candidates; not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep21-Navi checkNaviAll/unused1/2 continue, all page/portrait/end controls, numerical1/0、00001 and source fields.',semantic_review=['Bass0/1 denies extinction. Player Bass22 calls defeated opponent shadow and self original; same portrait not proof same individual.', 'NumberMan probability omitted operator, own-data-only reasoning and unbounded combination strength preserved; no numerical game-rule claim.', 'WindMan/ShadowMan possible revival and SearchMan hypothetical revival remain uncertainty, not confirmed extinction or actual respawn.', 'Roll tears and PET return, JunkMan closeness and AquaMan asking affection keep operator relationship, no gender/romance invented.', 'WoodMan tree planting1, MetalMan restarting1 and ElecMan miniature bulb1 preserved. Return/plant/training/chip wishes not executable actions.', 'StarMan solar prominence drafted 홍염 and operator lucky star image. NapalmMan rejects wound treatment and self-soothing battle preserved as character speech.', 'No normal-play victory/actor identity/21 routes/PET return/save/screen verification. Static preservation not runtime or human approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve laserman draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
