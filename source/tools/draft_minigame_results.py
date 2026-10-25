"""Manual31 minigame result candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'65AAE0':('f2054ed89bd2014c086cff3928e93e8999ab41759253558c4c6aaaac18ee26f0',31,'translations/minigame_result_rewards_draft_ko.json'),
}
DRAFT={
'65AAE0':{
50:['실패해 버렸어\n계산은,\n어렵네...'],
51:['해냈다, 클리어했어!!\n왠지 힘이\n솟아오르는 것 같아!'],
52:['해냈다, 클리어했어!','......\n어라, 문제집 안에서\n뭔가 나왔어...','제니가\n나왔어!\n운이 좋네!!'],
53:['해냈다, 클리어했어!','......\n어라, 문제집 안에서\n뭔가 나왔어...','버그 조각이 ','개\n나왔어!\n운이 좋네!!'],
60:['실패해 버렸어','꽤 만만치 않은\n퍼즐이네...'],
61:['해냈다, 클리어했어!!\n왠지 힘이\n솟아오르는 것 같아!'],
62:['해냈다, 클리어했어!','......\n어라, 편지 사이에서\n뭔가 나왔어...','제니가\n나왔어!\n운이 좋네!!'],
63:['해냈다, 클리어했어!','......\n어라, 편지 사이에서\n뭔가 나왔어...','버그 조각이 ','개\n나왔어!\n운이 좋네!!'],
70:['실패해 버렸어','어려운\n미션이었네...'],
71:['해냈다, 클리어했어!!\n왠지 힘이\n솟아오르는 것 같아!'],
72:['해냈다, 클리어했어!','......\n어라, 무슨 데이터가\n도착한 것 같아...','제니가\n보내져 왔어!\n이번 보상이래!','잘됐다!!'],
73:['해냈다, 클리어했어!','......\n어라, 무슨 데이터가\n도착한 것 같아...','버그 조각이 ','개\n보내져 왔어!\n이번 보상이래!','잘됐다!!'],
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
        portrait=None;visibility='not-shown-in-script'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('laserman topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('laserman tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker="unshown-result-voice",origin_portrait=portrait,portrait_visibility=visibility,context='Results50..73 for minigame0 arithmetic/drill,1 puzzle/letters,2 mission; no mugshot or character identity in archive.',variable_context='Buffer3 amount precedes zenny suffix or follows BugFrag prefix; preserve printBuffer/padLeft and reward command boundaries; unknown actor does not authorize selecting MegaMan portrait.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='minigame-results-and-rewards',context='31 Japanese literals in12 result scripts50..73; source0 placeholder retained pending consumer.',voice='Source friendly plain result voice; speaker identity/caller not established, no character-specific trait added; not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve minigame0/1/2 results calls, flag3585, global5 reward branches0..3, item33 and zenny/bug sentinel4294967295, buffer3/coordinates/waitHold and placeholder0.',semantic_review=['No explicit mugshot or caller-derived actor identity; unshown-result-voice records that limitation. Neutral source style drafted without naming current Navi.', 'ドリル in arithmetic context drafted 문제집 rather than drilling tool; puzzle letters and mission transmitted data remain different reward sources.', 'Strength rising item33 outcome separated from zenny and bug fragment reward branches; no type/amount cap inferred from sentinel.', 'Prefix 버그 조각이 plus buffer3 then 개 preserves amount boundary. Zenny amount first then 제니가 suffix avoids final-consonant dependence.', 'Source0 かりです provisional placeholder not translated and remains awaiting context in denominator.', 'Existing positionText92/110 and box10/12/type1/arrow225/141 suggest distinct result layout; actual rendering capacity and actor reachability unverified.', 'No minigame completion/reward receipt/save/portrait/runtime screen verification; static checks not human or runtime approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve laserman draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
