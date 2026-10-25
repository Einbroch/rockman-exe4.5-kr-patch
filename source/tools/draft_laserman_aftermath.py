"""Manual95 LaserMan aftermath candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7CA474':('753d307cdc9bff86960a551fcb3965c65e910cb22127cfa3170329fe9f7e7683',95,'translations/laserman_aftermath_draft_ko.json'),
}
DRAFT={
'7CA474':{
0:['우고오오오...\n나의 증오가...\n사라질 일은 없다...','이 몸이 썩어 문드러져도\n이 증오는...\n사라지지... 않는다!','우오오오오오오옷!!'],
1:['이, 이 앞의 에리어에서...\n네놈을... 기다리고...\n있는 것은...','...압도적인\n...공포','......그리고,\n...삭제다...','결코, 피할 수는\n...없다','와하하하하하하하하하하!!'],
2:['레이저맨...\n무서운 나비였네...','...이 앞에는\n뭐가 있을까...'],
3:['......부르르','배틀에서 이겼는데도...\n몸이 떨려...','레이저맨의 증오라는\n감정은, 지금도 어딘가에\n떠돌고 있나 봐...','그런데, 레이저맨이\n마지막으로 한 말이,\n마음에 걸리네...','이 앞에는...\n...대체'],
4:['이, 이겼다, 가스...','레이저맨,\n무, 무서웠다, 가스','하지만, 가스...\n이 앞에는,\n뭐가 있나, 거츠?','여기까지 왔으니,\n확인하지 않고는,\n돌아갈 수 없다, 가스!!'],
5:['레이저맨,\n가엾은 나비여...','...!!','...강한 사악한 기운이\n느껴진다...','이 앞의 에리어에서\n불어오는 듯하군...','이 앞에는 대체,\n무엇이 있다는 건가...'],
6:['타깃, 삭제...','미션, 컴플리트!','...','삐삣!!','...무슨 일이지!!','지, 지금, 이 앞의 에리어에\n초거대 파워 반응이 있다\n......','대, 대체... 무엇이...?'],
7:['쳇, 증오는\n계속 살아남는 건가...\n근성 하나는 대단하군','...오싹!!','뭐, 뭐야...\n이 살기!!','레이저맨의 것이 아냐\n......','내 불꽃 따위, 순식간에\n꺼져 버릴 듯한...\n압도적인 힘...','이 앞에는 어떤\n괴물이 있는 거지?'],
8:['레이저맨이여...\n모든 것을 잊고\n잠들어라...','그럼... 앞으로 나아갈까...','여기까지 왔다...\n우리에게는 모든 것을\n확인할 사명이 있다','두려워 마라... 간다'],
9:['레이저맨, 삭제...','하지만, 만만치 않은 나비였습니다\n......','여기에 레이저맨이\n숨어 있었다면,','이 앞의 에리어에는\n대체 무엇이...'],
10:['히이, 히이, 히이...','어떻게든 이겼지만...\n그런 녀석을 상대로\n배틀하다가는,','목숨이 몇 개라도\n부족하겠어요!!','얼른, 플러그아웃해요\n이 앞의 에리어에는,\n절대로 가고 싶지 않으니까요'],
11:['증오에 빠진\n힘 따위는,','굳은 신념으로\n단련한 내 주먹에는,\n통하지 않는다!!','앞으로 나아간다!','절대로 벗어날 수 없는\n공포라는 것을\n보러 가자...'],
12:['나, 나에게는,\n믿을 수 있는 오퍼레이터가\n함께 있다...','그, 그러니, 지지 않는다...','나, 나, 너와 함께라면,\n이 앞의 에리어도\n무섭지 않다...'],
13:['어, 엄청난 힘이었어, 퓨\n물살이 조금만 더\n약했다면,','삭제됐을 거야, 퓨...','이런 에리어에서는,\n얼른 나가고 싶어, 퓨...','이 앞에 나아가는 건\n자살행위야, 퓨!!'],
14:['어떠냐... 위대한\n안식의 힘 앞에서는,','증오의 힘 따위는,\n통하지 않는 것이다!!','이 앞에, 아무리\n사악한 힘이\n소용돌이쳐도,','대지의 힘이\n우리를 지켜 주겠지'],
15:['후우, 위험했어!!','어떻게든, 내 머리 위에\n행운의 별이, 빛나\n준 것 같아','이 앞에 나아가려면,\n아주 큰 행운의 별이\n빛나 주지 않으면,','꽤 위험할 것 같네...'],
16:['레이저맨,\n네놈에게 바칠\n애도의 말은 없다...','영원히 명부마도를\n떠돌도록 해라...','그럼...\n이 어둠의 세계의 밑바닥이\n보고 싶어졌군...','...나아간다'],
17:['레이저맨...\n적이지만 대단한\n실력자였소...','자, 앞으로 나아갑시다!','무슨 일이 있든,\n겁먹지 않고 나아간다!!\n기사의 마음가짐이오!'],
18:['닮은 녀석끼리의\n대결은, 내가\n이긴 모양이군!!','레이저맨...\n이름은 기억해 주지!','크크크, 그럼\n보러 가자고...','이 앞에 있겠지\n압도적인 공포라는\n녀석이 말이야!!'],
19:['레이저맨...\n어떤 의미에서는, 저보다도\n차가운 나비였어요...','저는 물질을\n얼리지만...','레이저맨은...\n마음을 얼리는 듯한','그런 냉혹한\n힘을 가지고 있었어요...','그리고, 이 앞의\n에리어에는, 더욱 무서운\n공포가 기다리고 있어요...'],
20:['어떻게든... 버텨 냈군...','조금만 더\n싸움이 길어졌다면\n내 전기는 바닥났겠지...','아슬아슬했군...','과연, 이 앞에서도,\n내 전기가 버틸 수 있을까...?'],
21:['증오에 휩싸인\n추한 꽃으로는','나의 아름다운\n꽃을 떨어뜨릴 수는\n없는 거야...','아마도, 이 앞의\n에리어에는,','더욱, 추한 꽃이\n피어 있겠지...'],
22:['흥... 쓰레기 녀석...','내가 알고 있는\n증오의 힘은\n이 정도가 아니다...','앞으로... 나아간다'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v) if t is not None}
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
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='system-sfx' if s==6 and i in (2,3) else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='LaserMan defeat statements0/1 and21 Navi reactions2..22; SearchMan hidden warning sound is system-sfx.',variable_context='No dynamic variables or numeric literals; no inferred next boss identity or automatic plugout.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-boss-aftermath',context='95 Japanese literals in23 scripts; LaserMan lingering hatred/warning and21 Navi reactions; complete archive read.',voice='Preserve character-specific fear/determination/gratitude/boasts as draft candidates; not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep21-Navi checkNaviAll/unused1/2 continue and all end/page/portrait/sound controls. SearchMan hidden silence and warning sound localized separately, warning sound localized separately.',semantic_review=['LaserMan warns of overwhelming fear/deletion ahead; no next opponent identity invented or definite revival asserted.', 'Roll lingering emotion is her belief; FireMan distinguishes new killing intent from LaserMan. Navi perceptions not verified battle rules.', 'NumberMan asks to plugout, AquaMan warns suicidal danger; no command/choice added. JunkMan trusts operator, KnightMan resolves forward.', 'IceMan contrasts freezing material with freezing hearts; PlantMan ugly/beautiful flower image and Bass stronger hatred retained.', 'SearchMan hidden6:3 warning beep is system-sfx with inherited source SearchMan portrait hidden; 6:2 hidden silence drafted ASCII ellipsis.', 'ShadowMan underworld/demonic path phrase drafted 명부마도; human wording review pending. No source repair/normalization.', 'No normal-play battle aftermath/next area/portrait/sound/save/screen verification; static checks not human or runtime approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve laserman draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
