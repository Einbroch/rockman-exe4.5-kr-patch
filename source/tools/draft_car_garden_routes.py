"""Manual64 car/garden dialogue candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7BA26C':('ead3b365109d113235537d38c13e95115b928f40b0b9febff5472e79c882c92d',6,'translations/car_controls_draft_ko.json'),
'7BA660':('8bf0c24db758f98fcdef1d6c3bad2498c7d605afa6c32a4fda9c38d5c26796b7',8,'translations/car_pink_battler_draft_ko.json'),
'7BA7A0':('fb7976ffa06ee4c5d1ee9a4da161bb51b2cb28fb0fea323e8fbf7ff0ceaffe86',23,'translations/car_homepage_patterns_draft_ko.json'),
'7BACD8':('b07c90c78540ae4b75298f8f3e086031a6a75a630ea7e503f95de142dfcb2678',20,'translations/car_rival_battlers_draft_ko.json'),
'7BAEF8':('3dff480810daed58a1ffb3b516673edd5fa6abc550b3a7325035da8e7a26164f',3,'translations/garden_blades_draft_ko.json'),
'7BB31C':('3263a9a68cc010644711601fb3a9dff0ccdc3b63c42970f4f5f6ab80d8c3e606',4,'translations/water_cleaning_draft_ko.json'),
}
DRAFT={
'7BA26C':{
0:['저는 자동차의\n가속 프로그램입니다','저쪽에 있는 건\n브레이크 프로그램입니다','그가 없으면,\n자동차는 멈출 수 없어요'],
1:['저는 자동차의\n브레이크 프로그램입니다','저쪽에 있는 건\n가속 프로그램입니다','그가 없으면,\n자동차는 움직일 수 없어요'],
},
'7BA660':{
0:['저기~ 내 바이러스랑\n배틀하지 않을래?','응  ','싫어!','재미없네...'],
1:['간다!','배틀 오퍼레이션, 세트!\n인!!'],
2:['키, 키익!\n분해!!'],
3:['호~호호호호호!!'],
},
'7BA7A0':{
0:['저는 선루프를\n움직이는 프로그램입니다','제가 없어도\n자동차는 달려요...'],
10:['바닥색 바닥색 바닥색\n물들여 드릴게요\n당신의 색으로~','저는 홈페이지 꾸미기\n프로그램!','당신 홈페이지의\n바닥색, 바꿔 보실래요?','예  ','아니요','그러시군요...'],
11:['그럼, 무슨 색으로\n물들여 드릴까요?','빨강&파랑','흰색&검정\n','무지개','그만두기\n'],
12:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
13:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
14:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
15:['그, 그러시군요...'],
},
'7BACD8':{
0:['난 저쪽 내비보다 강해!\n시험해 볼래?','좋아!  ','싫어!','정말!?\n한번 시험해 보자아!'],
1:['간다아!!','배틀 오퍼레이션, 세트!\n인!!'],
2:['너한테는 졌지만,\n저쪽 내비보다는\n내가 더 강해...!'],
3:['그래그래, 난 강해!!\n그것만큼은 확실한 것 같아!'],
4:['난 저쪽에 있는 내비보다\n강해!!','시험해 볼래?','예  ','아니요','뭐,\n시험할 필요도 없나...'],
5:['시작할까...','배틀 오퍼레이션, 세트!','인!!'],
6:['으으! 제법이군!!','그래도, 나랑 저쪽 내비 중\n누가 더 강하냐고 하면,\n나겠지...'],
7:['흥흥!!','또 내 강함이\n증명돼 버렸군'],
},
'7BAEF8':{0:['슈바슈바!\n슈바바바!!','제가 돌리는\n고속의 칼날로','어떤 잡초든\n단칼에 두 동강 냅니다!!']},
'7BB31C':{0:['촤아아아!!','강력한 물살!\n막힐 걱정 없어요!!','제가 흘려보내지 못할 건\n없습니다!!','구석구석까지\n깨끗하게 씻어 드리죠!!']},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('car scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        choice=(archive=='7BA660' and s==0 and i in (1,2)) or (archive=='7BACD8' and ((s==0 and i in (1,2)) or (s==4 and i in (2,3)))) or (archive=='7BA7A0' and ((s==10 and i in (3,4)) or (s==11 and i in (1,2,3,4))))
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('car topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('car tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Car accelerator/brake/sunroof programs, pink virus owner, rival boastful Navis, homepage patterns, high-speed blades and strong water-stream programs. Complete local branches read.',variable_context='No inserted name/item text. Choices retain native navigation and line endings; source vehicle/battle/floor/SFX commands unchanged.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-homepage-pattern',context='All Japanese literals in6 source archives;64 total. Local offers/results and pattern branches read together.',voice='Polite programs, informal pink virus owner and boastful yellow/purple rivals, rhythmic GoldProg service separated; candidates not approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve battle185/186/187, globals27=663/664/665, flags1806/7701; homepage floor types3/4/5, color order and & joins, disableB=true, grid spacePx24/24, sound150 and page boundaries.',semantic_review=['Accelerator and brake explain each other: missing brake prevents stopping, missing accelerator prevents movement. Sunroof absence still permits driving; not another required control.', 'Rival superiority is their boast, including after losing to the player, not established battle-ranking or new progression requirement.', 'HP is homepage, confirmed by floor text and callSetHomepageFloor. Patterns red&blue/white&black/rainbow map to3/4/5, not previous plain colors0/1/2.', 'Pink anger/laughter and blade/water/GoldProg sounds are candidate localizations requiring voice review. Water source mentions flushing and blockage, but does not name the appliance; no toilet/washer identification invented.', 'All drafting remains needs_review and NON-DISTRIBUTION; no normal-play battles/floor changes/save persistence/grid geometry or device screens verified.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve car draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')

if __name__=='__main__':main()
