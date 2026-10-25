"""Manual73 Bass encounter candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7CAF40':('fe245cacc8563907812065f23d0d61f99902ff6c98696ba75638321ccea6ff42',73,'translations/bass_encounter_draft_ko.json'),
}
DRAFT={
'7CAF40':{
1:['어, 엄청난 힘이\n다가오고 있어...!!'],
2:['모, 몸이 떨려...\n뭐, 뭐야...?','누, 누구야!?'],
3:['가... 가가앗...\n무, 무슨 일이\n일어나나, 가스...'],
4:['이 폭풍 같은\n사악한 기운... 누구냐!!'],
5:['타깃, 접근 중!!','뭐, 뭐야, 이 힘은...\n센서가 고장 났나!?'],
6:['이, 이거다...\n아까 느꼈던\n엄청난 힘...'],
7:['자, 자기장이 일그러진다...\n이 정도의 힘을\n느끼는 것은','...처음이다'],
8:['뭐, 무엇이 다가오고\n있다는 건가!!','이에 비하면...\n레이저맨의 힘 따위는\n어린아이 수준...!!','...옵니다!!'],
9:['...덜덜...\n어, 엄청난 힘의\n덩어리가 다가옵니다!','그럴 수가... 전뇌 세계에\n이 정도의 힘이\n집중되는 것은,','...이론상, 불가능해요!!'],
10:['...오싹!!','이, 이 심장이\n움츠러드는 듯한\n감각...','내가, 내가\n공포를 느끼고\n있다는 건가...'],
11:['모, 몸이...\n갈기갈기 찢어질 것 같다...','대, 대체 무슨 일이!?'],
12:['...공기가 떨려, 퓨\n머, 머리의 수조에\n금이 갈 것 같아, 퓨...'],
13:['누오오오오옷!!','누구냐!!\n모습을 보여라!'],
14:['뭐, 뭐, 뭐, 뭐, 뭐야!?'],
15:['이 힘...\n역시, 네놈인가...'],
16:['누우우웃!!\n이 얼마나 엄청난 힘인가!!','누구냐!!\n모습을 보여라!!'],
17:['아, 알고 있다...\n이 힘...','아, 아니, 하지만...\n내가 아는 녀석보다도\n훨씬... 크다!!'],
18:['...아, 아아...'],
19:['뭐, 뭐야...\n이 엄청난 에너지는!?','여, 여기는,\n원자력 발전소\n안인가?'],
20:['이, 이 힘은...\n설마... 그럴 리가...'],
21:['크크크크크...'],
23:['오, 온다!!'],
24:['오, 온다!!'],
25:['오, 온다, 가스!!'],
26:['조심해라!!\n온다!!'],
27:['전투 배치!!\n...옵니다!!'],
28:['쳇!!\n문답무용이라는 건가!','도망칠 수 없다!\n맞서 싸운다!!'],
29:['움츠러들지 마라!!\n앞으로 나선다!!'],
30:['거대한 힘에도\n약점은 있을 것이다...!!','...하앗!!'],
31:['어, 어떻게 계산해도\n도망칠 수 없어요!!','하지만, 싸워서\n이길 확률은...','......\n0、00001퍼센트!','이, 이제 할 수밖에 없어요!'],
32:['겁먹고 적에게\n등을 돌리는 것은\n내 성미에 맞지 않는다!!','설령, 패하더라도\n앞으로 나설 뿐!!'],
33:['나, 나... 반드시\n이긴다...!!'],
34:['다, 다리가 굳어서\n움직이지 않아, 퓨...','이, 이렇게 된 이상,\n할 수밖에 없어, 퓨!!'],
35:['...괜찮다,\n위대한 대지가\n우리 편이 되어 준다...','준비됐나!?\n온다!!'],
36:['오, 온다!!','마, 마치 거대한\n혜성 같아...!'],
37:['네놈을 상대하려면,\n나도 목숨을\n버려야 하겠군...','나무 하치만 대보살!!'],
38:['나이트맨,\n상대해 드리겠소!!','간다!!'],
39:['쳇!!','가진 칩을 전부\n준비해 둬라!!','총력전이다!!'],
40:['...오, 오고 있어요!!','오퍼레이팅,\n부탁해요!!'],
41:['큭, 이렇게 된 이상,\n있는 전력을 전부\n쏟아부어 주마!!'],
42:['어설픈 각오로는\n이길 상대가 아닌 것 같군\n......','보도록 해라!!\n플랜트맨, 목숨을 건\n꽃보라를!'],
43:['흥, 그림자 녀석...','우쭐대지 마라!!'],
44:['...자,\n네놈의 피로,\n나를 적셔 다오!'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text) and int(x.key.split(':')[1]) not in (0,22)]
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
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Two21 Navi reactions1..21/23..43 plus explicitly shown Bass44. Unshown0/22 voice remains pending.',variable_context='Preserve NumberMan source0、00001 probability tokens/separator; no numerical conversion or next-opponent identity inference.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-bass-encounter',context='73 shown-speaker literals in43 scripts. Four unshown voice literals0/22 remain pending, not excluded.',voice='Fear/distinct Navi responses, Bass player routes21/43 and explicitly shown challenger44 kept separately; inherited candidates not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep two21-Navi checkNaviAll tables/unused1/2 continue, targets22/44, unusual27/28->22 jumps, NumberMan probability0、00001 and pages/portraits.',semantic_review=['Hidden0/22 voice may be linked to Bass44 but not independently established; preserve originals pending context rather than infer speaker.', 'Player Bass21/43 differs from challenger44 scene role; same portrait name does not prove same actor identity. Bass43 calls opponent shadow.', 'NumberMan impossibility then0、00001 percent victory estimate retained as dramatic claim, not battle probability verified by code. Original separator retained for numeric safety.', 'ThunderMan magnetic-field distortion and ElecMan nuclear power plant question remain imagery, not real map location.', 'ShadowMan prayer ナムハチマンダイボサツ drafted 나무 하치만 대보살; specific religious reference not generalized, human wording review pending.', 'SearchMan27/FireMan28 target22 preserved exactly despite other second reactions targeting44. No control-flow repair or implied dialogue order change.', 'No normal-play encounter/actor identity/branch/jump/battle/save/screen verification; static checks not human or runtime approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve laserman draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
