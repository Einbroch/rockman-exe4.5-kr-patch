"""Manual58 homepage/battle/organ/venue candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7BEB18':('799c2cb2fe40dcc344d9d930f6973c5c3cea28ead168de52136d670cb190c724',21,'translations/homepage_background_b_draft_ko.json'),
'7BF018':('924e44d5c6025fafeb43679f86c5711228c9af1cde816171493f76bf30ba5165',18,'translations/purple_pink_battlers_draft_ko.json'),
'7BF258':('33897e8111b09f667d6d853dad25bc2df4baf039c60911ac99762f3e0a9d4c8c',19,'translations/organ_venue_draft_ko.json'),
}
DRAFT={
'7BEB18':{
10:['배경색 배경색 배경색\n물들여 드릴게요\n당신의 색으로~','저는 홈페이지 꾸미기\n프로그램!','당신 홈페이지의\n배경색,\n바꿔 보실래요?','예  ','아니요','그러시군요...'],
11:['그럼, 어떤 타입으로\n바꿔 드릴까요?','메툴','브루스\n','푸른 하늘','그만두기\n'],
12:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
13:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
14:['네, 기꺼이요~!!','...샤라랑!!','네! 완성됐어요!!'],
15:['그, 그러시군요...'],
},
'7BF018':{
0:['오늘은 일주일에 한 번 있는\n바이러스 배틀 모임이야!','내 바이러스의 실력을\n시험해 보려는데,\n상대해 주지 않을래?','응  ','싫어!','겁쟁이였구나...'],
1:['간다!!','배틀 오퍼레이션, 세트!\n인!!'],
2:['꺄악!\n어떻게 이럴 수가!!'],
3:['뭐, 이 정도지...'],
4:['내 바이러스는\n인터넷에서\n최강이랍니다!!','당신, 괜찮다면,\n내 바이러스들의\n먹이가 되어 주지 않겠어요?','덤벼 봐!  ','못 해!','호호호,\n누구나 먹이가 되는 건\n싫겠지요!!'],
5:['내 귀여운 바이러스들아,\n식사 시간이란다!!','배틀 오퍼레이션, 세트!\n인!!'],
6:['아와와와와...'],
7:['내 바이러스에게\n도전한 용기를 봐서,\n목숨만은 살려 드리겠어요'],
},
'7BF258':{
0:['저는 이 파이프오르간을\n오랫동안 연주해 왔습니다...','수많은 사람들에게\n감동을 선사했지요','하지만, 이제는\n쉰 소리밖에\n나지 않게 되었습니다...','소리도 내지 못하는 악기는\n우스울 뿐입니다','저는 여기서\n조용히 망가져 가기를\n기다리고 있습니다...'],
10:['이 구역은,\n에브리데이 토너먼트\n대회장이다!!','자세한 건,\n저 토너먼트 게시판을\n읽어 봐!'],
11:['우헤헤!!\n에브리데이 토너먼트,\n열기가 뜨겁군...!!'],
12:['어이 어이 어이이이!!\n해치워라아아!! 삭제해라아아!!'],
13:['구헤헤!!\n싸워라 싸워라!!','푸슈라아아아!!'],
14:['난 나비가\n삭제되는 걸\n보는 게 정말 좋아','쿄호호호호호호!!'],
15:['양지의\n에브리데이 토너먼트로는\n자극이 부족해!!','더 자극적인 걸 원해!!'],
16:['혼이 끓어오르는구먼!!\n호가아, 호가아!!'],
17:['제법인데?\n멋졌다고...'],
20:['멋진 솜씨였어!\n또 도전해 줘!!'],
21:['아쉽게 됐군!\n또 도전해 줘!!'],
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
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        choice=(archive=='7BEB18' and ((s==10 and i in (3,4)) or (s==11 and i in (1,2,3,4)))) or (archive=='7BF018' and s in (0,4) and i in (2,3))
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('organ topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('organ tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Homepage BG types3/4/5, two independent virus battle offers/results, ageing organ and rough tournament crowd. Complete local scripts read.',variable_context='No dynamic name/item literals. Source battle globals, BG grid and venue time/flag/animations remain untouched.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-homepage-battle-venue',context='All58 Japanese literals from3 archives. Offers/refusals/results, background choice and clock/flag venue branches read.',voice='GoldProg same BG-service candidate as7BB878; purple Navi casual/pink Navi affected polite; sad organ program polite; rough excited spectators. Candidates not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='BG types3/4/5, spacePx12/24, disableB=true and sound150; battle195/196/global27=673/674, result globals25/26 and flags1806/7701; venue navi flag1929 and hours9/13/16/20, animations24/25 retained.',semantic_review=['Homepage menu Mettaur/Blues/blue sky maps BG3/4/5, not floor patterns. 메툴/브루스 are project wording candidates; repeated service wording kept consistent with7BB878.', 'Weekly virus meeting is described as once a week without numeric weekday. NaviGirlPurple and NormalNaviPink separately control offers195/196 and result scripts2/3 vs6/7; do not infer player gender or actual damage from 먹이/목숨 threat.', 'The organ contrasts former moving performances with current hoarse sound and waiting to break; no repair choice, reward or death event invented.', 'Venue spectator デリれ abbreviated deletion call drafted 삭제해라; Navi deletion is not omitted. オモテ contrast drafted 양지, contrasting tournament venue without inventing an exact area name.', 'Flag1929 checks before four net-time windows9:00-9:59/13:00-13:59/16:00-16:59/20:00-20:59; script17 praise and scripts20/21 results remain separate.', 'Static preservation only; no normal-play BG/menu/battle/time/venue/animation/save/screen verification. Sounds, menu labels, register and literal layout need independent human/runtime review.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve organ draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
