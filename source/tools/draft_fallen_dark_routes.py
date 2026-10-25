"""Manual21 fallen Navi/dark Heel battles candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7BF8C0':('0c604fe2760775ed28e334db6707242d476f9d2c03c8fa6a0a99e0c0eb6722e2',3,'translations/fallen_navi_draft_ko.json'),
'7BFC50':('d8d2d52a21b0304840298aa14fa78ce96265d4d80ae7da3f7cdfd7557dd5849b',18,'translations/dark_heel_battlers_draft_ko.json'),
}
DRAFT={
'7BF8C0':{0:['......','응답이 없다...','아주 오래전에\n여기서 숨이 끊어진 것 같다...']},
'7BFC50':{
0:['여기까지 왔다는 건,\n꽤 강하다는 거겠지...','나와 싸워 보겠나?','덤벼!  ','싫어','겁을 먹었나...'],
1:['배틀 오퍼레이션, 세트!\n인!!'],
2:['쳇!\n생각보다 강하군...'],
3:['고작 그 정도인가...'],
4:['내 어둠의 힘...\n시험해 보겠나...?','그래  ','싫어','어둠의 힘은 무섭지?\n헤헤헤!!'],
5:['코오오오오...','어둠의 힘이여...\n지금이야말로 깨어나라!!','배틀 오퍼레이션, 세트!\n인!!!'],
6:['내 어둠의 힘이\n통하지 않다니...','어, 어째서...!?'],
7:['하하아!!\n어둠의 힘을 뼈저리게 느꼈나!'],
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
        choice=archive=='7BFC50' and ((s==0 and i in (2,3)) or (s==4 and i in (1,2)))
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('organ topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('organ tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else ('system-observation' if archive=='7BF8C0' and i in (1,2) else portrait),origin_portrait=portrait,portrait_visibility=visibility,context='Fallen Navi silence/hidden observation or two HeelNaviBlack battle offers/results. Complete local scripts read.',variable_context='No dynamic name/item literals. Source animation0, portrait visibility, battle globals and option widths8/9 remain untouched.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-observation-choice-battle',context='All21 Japanese literals from2 archives. Silence/observation and both offers/refusals/results read.',voice='Unresponsive Navi silence, neutral hidden observations and rough dark HeelNaviBlack. Candidates not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Retain mugshotAnimation0 and hidden observation boundaries; battle197/198/global27=675/676, result globals25/26 and flags1806/7701; option widths9/8 and trailing two spaces.',semantic_review=['7BF8C0 visible silence is not spoken translated narration. Hidden no-response and long-ago-expired observations retain uncertainty ようだ; source explicitly differs from disabled program7BCEBC.', 'Both7BFC50 portraits are HeelNaviBlack, but separate battles197/198 with result scripts2/3 and6/7. Dark power rhetoric not a new player ability, reward or changed battle mechanic.', 'ヤミのチカラ drafted 어둠의 힘; no invented named technique or dark chip. Threats and defeat boast are speaker rhetoric, not actual player damage/save deletion.', 'Static preservation only; no normal-play encounter/battle/results/menu/save/screen verification. Wording and presentation remain review candidates.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve organ draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
