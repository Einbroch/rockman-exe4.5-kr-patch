"""Manual41 venue/shop/battle candidates, without ROM integration."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7B6E20':('00c9d43e79cc4c648d27c849d0cf5afce5c794a203add00dc0dc441e33b68977',11,'translations/secret_training_draft_ko.json'),
'7B6F9C':('b38307cfbfd6f1d6a1c6966de740d11fdf4efd30d217e6fc6100a03de3d7acab',30,'translations/everyday_venue_draft_ko.json'),
}
DRAFT={
'7B6E20':{
0:['여기는 내 비밀\n특훈 장소야','어때, 나랑\n넷배틀하지 않을래?','좋아!  ','싫어','그래... 조금 아쉽네'],
1:['간다!!','배틀 오퍼레이션!!\n세트!!','인!!'],
2:['멋진 오퍼레이션!!','좋은 배틀이었어\n고마워!!'],
3:['조금 더 연습이\n필요하겠네!'],
},
'7B6F9C':{
0:['뜨끈뜨끈 따끈따끈\n전기레인지---!!','제 일은,\n전기로 요리를\n만드는 것!!','뚝배기, 중화팬, 곰솥\n뭐든 데워 드려요!'],
10:['이 구역은,\n에브리데이 토너먼트\n대회장이야!!','자세한 건,\n저 토너먼트 게시판을\n읽어 봐!'],
11:['에브리데이 토너먼트는\n오늘도 뜨겁다고!!','야호~!!'],
12:['꺄아꺄아!!\n배틀은 최고야!!'],
13:['매일 실력 있는\n내비들의 배틀을 볼 수 있어,\n행복해~!!'],
14:['여기 토너먼트에서\n우승하면,','」,\n받을 수 있대!!'],
15:['우오오...\n피가 끓는군!!'],
16:['이럴 때,\n강한 배틀러의 기술을\n배워 두는 거야!!'],
17:['너, 제법이구나!!\n훌륭한 기술\n이었어!!'],
20:['축하해---!!\n정말 훌륭한\n기술이었어!!',' 선수,\n또 도전해 줘!!'],
21:['아쉬웠겠네~!\n또 도전해 줘!!'],
221:['다시 찾아와 주세요!'],
222:['저는\n서브칩 상인인데요','지금은 품절입니다!\n죄송해요'],
223:['저는\n서브칩 상인입니다!','좋은 물건 있어요~!\n','보기  ','안 보기'],
224:['저는\n서브칩 상인입니다!','오늘은 일주일에 한 번 있는\n레이디스 데이!!','여자분들께는 팍팍\n서비스해 드릴게요!','좋은 물건 있어요!?\n','보기  ','안 보기'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{2 if archive=="7B6F9C" and s==14 and i==1 else i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('venue scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        portrait=shown[-1] if shown else 'PurpleNavi';visibility=('visible' if events[-1].group(1) else 'hidden') if events else 'inherited-from-caller'
        choice=(archive=='7B6E20' and s==0 and i in (2,3)) or (archive=='7B6F9C' and ((s==223 and i in (2,3)) or (s==224 and i in (4,5))))
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('venue topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('venue tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Local secret-training offer/results or electric-stove program, tournament spectators/results and subchip shop. Script221 inherits merchant portrait from223/224.',variable_context='Reward item19 and current-Navi variable boundaries retained; item suffix avoids consonant-dependent Korean particle. Native flags/time/shop/Navi branch untouched.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-and-shop',context='Complete local branches read; all Japanese literals drafted. Unselected quote-only literal14:1 remains original.',voice='Friendly training partner, energetic spectators, enthusiastic program and polite subchip merchant separated; wording remains candidate.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Retain item19, Navi1/weekday3 eligibility, shop8/18, time checks and flags/native battle globals. No changed prices, player gender or event schedule inferred.',semantic_review=['Script14 hearsay reward stays hearsay. Original opening quote is separate unselected literal; closing quote/comma candidate avoids variable particle dependency and requires actual item-render review.', 'Ladies day source is gated by weekday3 and Navi1, not the entered player gender. Service wording does not invent a discount amount; shop18 details remain original.', 'Stove pot types adapted as 뚝배기/중화팬/곰솥 functional cookware candidates. Source sound effects, 에브리데이 토너먼트 and 레이디스 데이 require human voice/term review.', 'Training positive result praises operation, negative requests more practice. Observers learning techniques is not item theft or a new gameplay mechanic.', 'Static protection is not normal-play runtime, shop purchase, clock, reward, save or layout verification.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve venue draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')

if __name__=='__main__':main()
