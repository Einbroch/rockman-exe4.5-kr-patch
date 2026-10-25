"""Manual quick tournament/result and remaining GutsMan reminder drafts; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
'664804':('a18e6f813fa5facb3df4ebd02dae51631af573757bae23a24f10e2f2c4c9af2c',5,'translations/quick_tournament_encouragement_draft_ko.json'),
'664D84':('2b4ee70a2b22f0fbc037c29e9b9e76cda03b8555125ef389001d2fcaccdcd8a4',4,'translations/quick_battle_outcome_draft_ko.json'),
'66651C':('8286cb9ad04ff3ac3ec9f09570327fd24da70450943fd7f4e5209a19d6e1dce1',14,'translations/guts_reminder_remaining_draft_ko.json'),
}
DRAFT={
'664804':{
'1:0':'주말에 열리는\n토너먼트,',
'1:1':'꼭 우승\n하자!!',
'2:0':'드디어, 토너먼트\n날이 왔네...\n힘내자!!',
'3:0':'있잖아, 재밌어 보이는\n아이템이 있나 봐',
'3:1':'키 아이템을\n확인해 보자!',
},
'664D84':{
'1:0':'져 버렸네...\n하지만, 다음엔 이기도록\n힘내자!!',
'2:0':'해냈다~!!\n',
'2:1':',\n멋진 오퍼레이션이야!',
'3:0':'다음에 할 때는,\n완전히 결판내자!',
},
'66651C':{
'1:0':' 시작할\n시간이거스!',
'2:0':'\n약속 시간이거스',
'5:0':'거츠, 거츠!!\n',
'5:1':' 일정\n시간이거스!!!',
'21:0':' 시작할\n시간이거스!',
'21:1':'서두르지 않으면,\n오프닝을\n놓치는거츠!!',
'22:0':'\n약속 시간이거스',
'22:1':'거츠맨도\n기대되는거츠!!',
'23:0':',\n밥 먹을 시간이거스!',
'24:0':'학원에 갈\n시간이거스!!',
'24:1':'공부, 공부\n힘내는거츠!!',
'25:0':'거츠, 거츠!!\n',
'25:1':' 일정\n시간이거스!!!',
'26:0':'그리고...',
}}
CONTEXT={
'664804':'Quick-box weekend/tournament-day encouragement and key-item suggestion; no mugshot in source.',
'664D84':'Quick-box defeat encouragement, victory/operator praise and decisive-rematch message; no mugshot.',
'66651C':'Only remaining14 TV/promise/other quick reminders and explicit GutsMan21..26; prior selected quick entries retained.',
}
NOTES={
'664804':['Absolute victory emphasis and tournament day arrival preserved. Key-item suggestion does not assert possession of a particular item. No named actor inferred from adjacent archive.'],
'664D84':['Defeat encouragement, victory praise and complete settlement on next attempt kept distinct. Script3 external draw/result caller unproven; no route assertion.', 'Nickname follows the victory first literal and precedes comma in second; separate keyWait/clearMsg and trailing newline retained.'],
'66651C':['TV opening urgency, promise anticipation, meal/school/other/additional event distinctions preserved; sourceじゅく translated 학원.', 'Sourceガス/ガッツ distinguished as existing candidate 거스/거츠; literal self-name거츠맨 preserved. Only21..26 have explicit GutsMan portrait; quick1/2/5 unshown.', 'Dispatch0/20, sound155/wait96, flags3585/3658, event6/26 loops, quick coordinates and schedule/nickname options unchanged. No clock/variable/save/runtime verification.', '666430:0:0 sourceかりです remains unresolved original and in untranslated denominator; consumer not established.'],
}
def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    ids={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}
    values={archive+':'+k:v for k,v in DRAFT[archive].items()}
    selected=[x for x in literals(original) if x.key in ids]
    if len(selected)!=count or set(values)!=ids:raise ValueError('remaining scope '+archive)
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('remaining topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('remaining tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('remaining padding '+x.key)
        shown=archive=='66651C' and s>=20
        speaker='GutsMan' if shown else 'unshown-guts-style-reminder' if archive=='66651C' else 'unshown-quick-voice'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait='GutsMan' if shown else None,portrait_visibility='shown' if shown else 'not-shown-in-script',
            context=CONTEXT[archive],variable_context='Preserve nickname and schedule buffers/command order. Name + 시작할/일정 avoids final-consonant particle. Actual variable widths/caller and runtime display unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='quick-tournament-results-guts-reminders',context=CONTEXT[archive],
        voice='Friendly quick-box voice unidentified; GutsMan only explicit portraits21..26. Existing 거스/거츠 suffix candidates retained, not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Keep prior selected literals, commands, flags, buffers, newlines and literal segmentation; no ROM/save writes.',
        semantic_review=NOTES[archive],units=units)
def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve remaining draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
