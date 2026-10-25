"""Manual60 factory/battler/disabled-program candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7BC870':('4c14f483cd866055e2572f76226ebfe1cbb0683f2c336c0e1834540d028dc36f',4,'translations/factory_orders_draft_ko.json'),
'7BCC34':('8d84e6bfb434c16dbddf82bd27ef03a7c88a76da1f0dcadb6f207d75ee65e73f',28,'translations/factory_battlers_draft_ko.json'),
'7BCEBC':('021b1ff7d1c1cc11586540033b72b5fd53b9eff4cb9be3855672ae8a418a4dd8',2,'translations/disabled_program_draft_ko.json'),
'7BD240':('dd7f65d2a3fcc8edf5b4a8a7d72037b709906ae9b281348df2b2f53fe299ef9f',26,'translations/heel_battlers_draft_ko.json'),
}
DRAFT={
'7BC870':{0:['주문! 주문!!','이 공장에서 만든\n철판의 주문을\n받는 게 제 일!','전 세계에서 주문이\n들어와요!!','아아, 바빠!\n오오, 바빠!!']},
'7BCC34':{
0:['너랑 내 바이러스,\n어느 쪽이 더 강할까?','궁금하네...','배틀해 보지 않을래?','좋아  ','싫어!','쳇!\n재미없어!'],
1:['어떤 결과가 나올지,\n기대되네...','배틀 오퍼레이션, 세트!\n인!'],
2:['네가 더 강했구나\n이길 수 있을 줄 알았는데...'],
3:['역시, 내 바이러스가\n더 강했네!!','꺄하하하하하핫!!'],
4:['나와 싸워라!!','좋아  ','싫어!','왜, 왜지...!'],
5:['배틀 오퍼레이션, 세트!\n인!!'],
6:['할 말은 없다...\n내 패배다...'],
7:['할 말은 없다...\n네 패배다...'],
8:['아초아~!!\n호와아아!!\n하초와아아!!','흥, 나랑 배틀해 보지 않겠나?','덤벼!  ','싫어!','도망치는 거냐!!'],
9:['아초아~!!\n호와아아!!\n하초와아아!!'],
10:['호와라와라~!!','젠장!\n제법 좋은 공격을 하는군!'],
11:['하초와아아!!','너, 빈틈투성이야!'],
},
'7BCEBC':{0:['......','꼼짝도 하지 않는다...\n바이러스에 당한 것 같다']},
'7BD240':{
0:['어이, 어이,\n나랑 배틀해 주지 않겠나?','응!  ','싫어!','흥, 겁쟁이 녀석!!'],
1:['간다...','배틀 오퍼레이션, 세트!\n인!!'],
2:['...졌군...'],
3:['꽤 하는데...\n그래도 나만큼은 아니지만'],
4:['너, 강해 보이는구먼!\n나랑 배틀하지 않겠나?','주변 녀석들이랑은,\n배틀하느라 질렸거든!!','어때!?','응  ','거절해!','배틀에서 가장 중요한\n마음이 약해서야,\n말도 안 되는구먼!'],
5:['난 봐주는 법을\n모른다네!','각오하게나아!!','배틀 오퍼레이션, 세트!\n인!!'],
6:['우햐~!\n너, 강하구나아!!'],
7:['좀 지나쳤나?'],
8:['나와 배틀해라...','응  ','거절해!','......'],
9:['.........'],
10:['기 기 기 기 기...'],
11:['카 카 카 카 카...'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('factory heel scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown:raise ValueError('actor missing '+x.key)
        portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
        choice=(archive=='7BCC34' and ((s==0 and i in (3,4)) or (s==4 and i in (1,2)) or (s==8 and i in (2,3)))) or (archive=='7BD240' and ((s in (0,8) and i in (1,2)) or (s==4 and i in (3,4))))
        speaker='player-choice' if choice else 'system-observation' if archive=='7BCEBC' and i==1 else portrait
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('factory heel topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('factory heel tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,origin_portrait=portrait,portrait_visibility=visibility,context='Factory order processing, three battlers per battle archive with separate offers/results, or motionless program observation. Whole local branches read; repeated portrait does not imply shared voice.',variable_context='No inserted names/items. Disabled-program hidden observation is narration, not a choice; punctuation-only silence remains per-ID with6/9-dot rhythm.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-observation',context='All60 catalog Japanese-class literals from4 archives, including source silence marks; not60 unique prose sentences.',voice='Busy polite program, curious girl, terse heel, martial shouts, first rough/second rustic Purple heel and staccato Black heel separated; voices remain candidates.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep battles189..194/globals27=667..672/flags1806/7701, options/targets, page boundaries; disabled program mugshotAnimation0 and portrait hiding retained.',semantic_review=['7BCC34 scripts6/7 switch my loss vs your loss; do not copy the same result into both. Girl compares player with her viruses, not own Navi strength.', '7BD240 first/second Purple Navi share portrait but second source uses オラ/オメー; rustic Korean is a scoped candidate, not a global portrait replacement.', 'Black heel martial syllables in7BCC34 vs repeated staccato in7BD240 kept distinct; no named attack, school or character identity invented.', '7BCEBC silence then hidden observer says motionless/looks virus-struck. It does not prove death or command a repair; system-observation not player-choice.', 'Silence six/nine marks counted by existing Japanese-range catalog because middle dot is in that range. Translate punctuation for display while retaining denominator and original source; not added missing prose.', 'Static protection not normal-play battles/disabled-program route/save/geometry/screen verification; voice/taunts/shout candidates need human review.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve factory heel draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')

if __name__=='__main__':main()
