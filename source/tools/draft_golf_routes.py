"""Manual69 golf-area dialogue/choices; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7B9104':('d27cc61b289755b695ab6536397f794c0b0369bb1616294b48689d7a8b8ea7c9',3,'translations/golf_lawn_draft_ko.json'),
'7B94AC':('57d02bba2c6b34b2efc7283022e2568ea1d990f6cb72c3e27c6d6b2d970b9847',26,'translations/golf_battlers_draft_ko.json'),
'7B9748':('ff868d885b91bf49a47b80d32fdd9aeec82e67ad3c02ed66a11e21cfacc2040c',16,'translations/golf_course_shop_draft_ko.json'),
'7B9C94':('c2b1db7ed89ff3c5b6c384134c51d4ab6d08425a38a184e77e5deb085ee3835d',24,'translations/golf_homepage_floor_draft_ko.json'),
}
DRAFT={
'7B9104':{0:['저는 골프장의\n잔디를 관리하는\n프로그램입니다','잔디가 너무 자라지 않았는지\n반대로 시들지 않았는지','꽤 신경이 쓰인답니다']},
'7B94AC':{
0:['안녕, 너도 배틀하러 왔어?\n그럼, 나랑 배틀해 볼래?','응!  ','싫어!','뭐야, 실망이네...'],
1:['그럼 간다!!','배틀 오퍼레이션, 세트!\n인!!'],
2:['대단한 기술이야!!\n너 제법이네!!'],
3:['어때, 나 강하지?'],
4:['나랑 배틀하지 않겠나?','지금까지 본 적 없는\n배틀의 세계를 보여 주마','응  ','거절해!','쳇!'],
5:['매혹적인 배틀의 세계로\n안내해 주마!!','배틀 오퍼레이션, 세트!\n인!!'],
6:['뛰는 놈 위에 나는 놈이\n있다는 건가...'],
7:['어떠냐...\n새로운 세계가 보였나?'],
8:['너, 나랑 배틀하고\n싶다고 생각했지?','좋아, 상대해 주마...','응  ','거절해!','쳇, 그런가...'],
9:['처음부터 달려 주마!!','배틀 오퍼레이션, 세트!\n인!!'],
10:['크허억...\n당했군...'],
11:['그런 사교댄스 같은\n싸움 방식으로는, 나를\n이길 수 없다고!!'],
},
'7B9748':{
0:['저는 골프 코스를\n구상하는 프로그램입니다','너무 쉬워도,\n너무 어려워도 안 되죠','신경이 쓰이는 일이에요'],
221:['다시 찾아와 주세요!'],
222:['저는\n서브칩 상인인데요','지금은 품절입니다!\n죄송해요'],
223:['저는\n서브칩 상인입니다!','좋은 물건 있어요~!\n','보기  ','안 보기'],
224:['저는\n서브칩 상인입니다!','오늘은 일주일에 한 번 있는\n레이디스 데이!!','여자분들께는 팍팍\n서비스해 드릴게요!','좋은 물건 있어요!?\n','보기  ','안 보기'],
},
'7B9C94':{
0:['저는 골프장의\n고객 정보를\n관리하는 프로그램입니다','절대로 정보를\n밖에 흘려서는 안 되죠','신경이 쓰이는 일이에요'],
10:['바닥색 바닥색 바닥색\n물들여 드릴게요\n당신의 색으로~','저는 홈페이지 꾸미기\n프로그램!','당신 홈페이지의\n바닥색, 바꿔 보실래요?','예  ','아니요','그러시군요...'],
11:['그럼, 무슨 색으로\n물들여 드릴까요?','파랑','빨강\n','초록','그만두기\n'],
12:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
13:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
14:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
15:['그, 그러시군요...'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('golf scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown and not (archive=='7B9748' and s==221):raise ValueError('actor missing '+x.key)
        portrait=shown[-1] if shown else 'PurpleNavi';visibility=('visible' if events[-1].group(1) else 'hidden') if events else 'inherited-from-caller'
        choice=(archive=='7B94AC' and ((s==0 and i in (1,2)) or (s in (4,8) and i in (2,3)))) or (archive=='7B9748' and ((s==223 and i in (2,3)) or (s==224 and i in (4,5)))) or (archive=='7B9C94' and ((s==10 and i in (3,4)) or (s==11 and i in (1,2,3,4))))
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('golf topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('golf tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Golf lawn/course/customer administrators, three battle offers/results, subchip merchant, and GoldProg homepage-floor color service. Local branches read together.',variable_context='No inserted name/item text. Source choices, shop gates, battle globals and homepage floor calls remain original;221 inherits PurpleNavi from223/224.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-shop-homepage-floor',context='All Japanese literals from4 archives;69 total. Complete local branches read.',voice='Polite programs/merchant, friendly yellow Navi and boastful purple/black heel Navis, GoldProg rhythmic service separated; candidates not approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve battles182/183/184 and globals27=660/661/662, flags1806/7701, weekday3/Navi1, shops8/19, four-way color targets12/13/14/15, spacePx24/12, disableB=true and callSetHomepageFloor types0/1/2, sound150.',semantic_review=['HP means homepage here: source floor-color wording and callSetHomepageFloor establish it, not health restoration.', 'Blue/red/green/cancel choice order and calls0/1/2 retained. Chant ユカイロ and シャラーン translated as rhythmic/sound candidates, not extra operations.', 'HeelNaviPurple upper-above-upper proverb rendered 뛰는 놈 위에 나는 놈; ballroom-dance taunt retained. These are voice candidates, not newly inferred mechanics.', 'Subchip ladies-day source uses shop19, unlike earlier venue shop18. It checks weekday3/Navi1 rather than player gender; exact discount unasserted.', 'Customer information confidentiality and lawn/course difficulty vigilance retained, not invented security or golf instructions.', 'No normal-play battle/shop/color application/save persistence or screen geometry verified; grid-choice and SFX rendering require later runtime checks.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve golf draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')

if __name__=='__main__':main()
