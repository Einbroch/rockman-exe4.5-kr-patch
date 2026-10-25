"""Manual54 background/venue/device/battle candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7BB6C8':('dfda65145e923846a0ee1e0e802125cc6119f3f43261522fd4aae060f0b37c32',10,'translations/moth_battler_draft_ko.json'),
'7BB878':('a76c7e7f6003aa6a5ff5895fe01e0c662bf4112788e86ed001f54f6e1af61f17',24,'translations/homepage_background_draft_ko.json'),
'7BBE54':('c3b4c5278d73d291275d385c6139c0952d545f8d9454b6e47cbd3365fa4dc505',3,'translations/water_gun_draft_ko.json'),
'7BC27C':('9c5834a20d0f8a7c1407ba20e4fdad651b4aac422667db4933beeb0b1c1195f8',17,'translations/cold_venue_draft_ko.json'),
}
DRAFT={
'7BB6C8':{
0:['헤이! 난 말이야,\n꽤 강하다고 생각하는데\n잠깐 시험해 보게 해 줄래?','예  ','아니요','거절한다는 건,\n역시 내가 강하다는 거구나!'],
1:['오케이!\n그럼 시작한다!!','나방처럼 날고, 모기처럼 쏜다!','배틀 오퍼레이션, 세트!\n인!!'],
2:['크하아아아아아아앗!\n내 실력이 고작 이 정도였어!?','하하하... 이건 꿈이겠지!'],
3:['역시, 내가 최강!!'],
},
'7BB878':{
0:['즈고오오오오!!','제 탈취력은\n세계 최고!!','아무리 지독한\n냄새라도, 순식간에\n없애 보이겠습니다!!'],
10:['배경색 배경색 배경색\n물들여 드릴게요\n당신의 색으로~','저는 홈페이지 꾸미기\n프로그램!','당신 홈페이지의\n배경색,\n바꿔 보실래요?','예  ','아니요','그러시군요...'],
11:['그럼, 어떤 타입으로\n바꿔 드릴까요?','록맨','벚꽃\n','전뇌','그만두기\n'],
12:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
13:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
14:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
15:['그, 그러시군요...'],
},
'7BBE54':{0:['피슈우~!!','제 물총은\n바늘구멍도 맞힐 만큼\n정확합니다!!','무엇이든 정확히 겨냥합니다!']},
'7BC27C':{
0:['추, 추워...'],
10:['이 구역은,\n에브리데이 토너먼트\n대회장이야!!','자세한 건,\n저 토너먼트 게시판을\n읽어 봐!'],
11:['우와~!!\n배틀은, 정말 재미있네!!','보기만 해도 너무 신나!'],
12:['으으으...\n나도, 나도!!'],
13:['코피가 날 정도로\n흥분되는군!!','우효이!!'],
14:['오늘도 혈관이\n터질 듯한 배틀이\n줄줄이 펼쳐지는구나아아!!','후, 후, 후, 후가아아!!'],
15:['꺄아! 꺄아아!\n배틀 시간이야아!!'],
16:['이 토너먼트의 배틀은,\n전부 참고가 되는군!','실컷 공부해\n가겠어어어어!!'],
17:['너, 정말 강하구나!\n나, 감동했어!'],
20:['꺄아!!\n축하해!!',' 선수,\n또 도전해 줘!!'],
21:['아이고~, 아쉬워!!\n또 도전해 줘!!'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('background scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        choice=(archive=='7BB6C8' and s==0 and i in (1,2)) or (archive=='7BB878' and ((s==10 and i in (3,4)) or (s==11 and i in (1,2,3,4))))
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('background topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('background tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Boastful yellow Navi battle, deodorizing program/homepage BG service, water-gun accuracy and cold program/tournament crowd. All local branches read.',variable_context='7BC27C20 printCurrentNavi suffix separate; BG choices are types not floor colors. Source battle/time/SFX/animation commands untouched.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-homepage-background',context='All Japanese literals from4 archives;54 total. Complete local offers, results, BG and timed venue branches read.',voice='Boastful Navi, polite enthusiastic programs, rhythmic GoldProg, distinct cheering crowd; candidate voices not approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Retain battle188/global27=666/flags1806/7701; BG types0/1/2, grid spacePx12/46, disableB=true, sound150; venue flag1906/time9/13/16/20 and animations/name boundaries.',semantic_review=['ガ/カ source boast is moth/mosquito, not butterfly/bee. Literal comic animal contrast retained as 나방/모기; high-impact wordplay remains human-review candidate.', 'BG options Rockman/Sakura/cyberspace map0/1/2 via callSetHomepageBG; not previously drafted callSetHomepageFloor. Sakura drafted 벚꽃 as theme-label candidate, not a person name; actual motif/label presentation review pending.', 'Source says background color but then chooses named types; preserve both without inventing a palette. HP is homepage from context and native BG command.', 'Deodorizing and water-gun programs boast independently; source does not name appliances. Cold program has only cold line, so no invented refrigerator identity.', 'Blood-vessel/nosebleed spectator exaggerations are source imagery, not battle damage or health instructions; excited sounds require human voice review.', 'No normal-play battles/BG changes/clock/name redisplay/save/grid or screen verification claimed.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve background draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')

if __name__=='__main__':main()
