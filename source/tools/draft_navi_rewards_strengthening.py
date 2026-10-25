"""Manual59 heart/star rewards and strengthening candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7C6BC0':('2738d0f2ea317204f27c00844d32ee42b6597bfe491c54ee32fa0c90d99a43af',21,'translations/roll_heart_rewards_draft_ko.json'),
'7C6D7C':('915ccf51e6dba0464a39e78c14c42faf1086d5d44fdfe35b1a2c253fca59dd1b',7,'translations/thunderman_strengthening_draft_ko.json'),
'7C6E50':('ce8cd62401ff9329ca101522bf5ac49cea01e810071c04d5a12761e945746348',2,'translations/protoman_failed_return_draft_ko.json'),
'7C6E94':('1009aa20e600e0c41f7b409a54b4172fa92889b906a13abef3b71cd9707cd449',8,'translations/woodman_strengthening_draft_ko.json'),
'7C6F90':('7080062a37c4edbeffa15b33d18f68dd297cf5a2d4cbb00122f2f302d063d9e4',21,'translations/starman_star_rewards_draft_ko.json'),
}
DRAFT={
'7C6BC0':{
0:['앗! 하트 발견!!',',\n떨어져 있는 하트 데이터를\n조사했다.','.','.',', 강화 프로그램\n「','」\n획득!!',',\n잘됐네!!'],
1:['앗! 하트 발견!!',',\n떨어져 있는 하트 데이터를\n조사했다.','.','.',',\n「','제니」\n획득!!',',\n잘됐네!!'],
2:['앗! 하트 발견!!',',\n떨어져 있는 하트 데이터를\n조사했다.','.','.',',\n「버그 조각」\n총 ','개 획득!!',',\n잘됐네!!'],
},
'7C6D7C':{
0:['이 근처에서\n미약한 전기가\n느껴진다...',':\n여기 두면 좋겠군...'],
1:['썬더맨,\n',':\n안치했다!!'],
2:['에서 나온\n전기가 썬더맨에게\n흘러들었다!!','포오오오...','전기를 흡수해,\n썬더맨은 강화되었다!'],
},
'7C6E50':{0:['...임무 실패입니다','면목이... 없습니다\n귀환하겠습니다...']},
'7C6E94':{
0:['음, 전뇌 식물이\n자라고 있군...','여기에는 양분이\n있는 것 같군...',':\n여기에 심어 볼까'],
1:[':\n눈 깜짝할 사이에 자라서,\n큰 나무가 되었다!!'],
2:['나무에서 흘러나오는\n음이온이,','우드맨의 몸을\n감쌌다!!','우, 우오오오!!','나무에서 나오는 치유의 힘으로\n우드맨은 강화되었다!'],
},
'7C6F90':{
0:['앗!\n스타가 있었어!!',',\n떨어져 있는 스타 데이터를\n조사했다.','.','.',', 강화 프로그램\n「','」\n획득!!','잘됐네, 운이 좋았어!'],
1:['앗!\n스타가 있었어!!',',\n떨어져 있는 스타 데이터를\n조사했다.','.','.',',\n「','제니」\n획득!!','잘됐네, 운이 좋았어!'],
2:['앗!\n스타가 있었어!!',',\n떨어져 있는 스타 데이터를\n조사했다.','.','.',',\n「버그 조각」\n총 ','개 획득!!','잘됐네, 운이 좋았어!'],
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
        portrait=shown[-1] if shown else None
        visibility=('visible' if events[-1].group(1) else 'hidden') if events else 'not-shown-in-script'
        system=(archive in ('7C6BC0','7C6F90') and i in (1,2,3,4,5)) or (archive=='7C6D7C' and (s==1 or (s==2 and i in (0,2)))) or (archive=='7C6E94' and (s==1 or (s==2 and i in (0,1,3))))
        if not system and (not shown or visibility!='visible'):raise ValueError('actor missing '+x.key)
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('organ topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('organ tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='system-narration' if system else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Roll heart/StarMan star data rewards, ThunderMan/WoodMan strengthening and ProtoMan failed return; all local scripts read.',variable_context='Keep current Navi/nickname/item33/7/6/buffer3 insertion boundaries; comma/colon or invariant 에서 avoids final-consonant particles. Name/item/amount screen widths unresolved.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-system-reward-strengthening',context='All59 Japanese literals from5 archives; three heart and three star reward paths, placement/growth/strengthening and mission failure read.',voice='Cheerful Roll/StarMan, solemn ThunderMan, steady WoodMan, apologetic formal ProtoMan, neutral reward narration. Candidate wording not approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep item33 amount1, item7/item6 labels, zenny/bug amounts4294967295 with buffer3, printCurrentNavi/nickname, 10-frame dot waits, object vs scene animations24/25 and RollHeart/StarDataErase calls.',semantic_review=['Heart/star paths0/1/2 award strengthening program/zenny/bug fragments respectively; no randomized reward type or amount hardcoded. Timed dot literals remain individually authored dots, not removed prose.', 'Roll nickname+comma stays separate; narrator current Navi+comma and item+colon avoid invariant Korean final-consonant particles. Dynamic widths/presentation still require runtime evidence.', 'ThunderMan item7 is placed, electricity flows into him and strengthening grants item33; do not invent the item name or a player menu.', 'WoodMan item6 grows into a tree; minus ions and healing power are fictional source narration preserved without outside health claims. Names 썬더맨/우드맨 and label 강화 프로그램 are review candidates.', 'Reward/strengthening hidden or never-shown system narration is not attributed to the last visible portrait. Prefix0 hints spoken by ThunderMan/WoodMan are distinguished from later narration.', 'ProtoMan failure apologizes and returns; no success reward or new retry choice. All variables/commands remain source-defined.', 'No normal-play collection/reward limits/item placements/growth/strengthening/mission return/name/save/screen verification. Static draft checks are not runtime proof.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve organ draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
