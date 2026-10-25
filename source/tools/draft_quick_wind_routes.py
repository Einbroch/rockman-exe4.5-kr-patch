"""Manual next quick confirmations/return/jackin/reminders; no ROM/save writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
'66B950':('b4c1579d30499bd0eeae7eabc269a0fa75fdb7103a50f226c1d926bdef034675',44,'translations/quick_menu_confirmation_b_draft_ko.json'),
'66BDE0':('fee47517dde6875e134887cb33cb5162d679d272b7cc683006362b7246239057',2,'translations/quick_wind_return_draft_ko.json'),
'66BEF8':('3e7690d84023e4b42b153e18a7dd8cbdd7e0126fb9c8781872c54ac426037069',1,'translations/windman_jackin_call_draft_ko.json'),
'66BF44':('7f8e98af640df13f3c4b6cdca37d43a6cc4b71f1fdd64c1eee30b5ce833c9847',18,'translations/windman_reminder_draft_ko.json'),
}
DRAFT={
'66B950':{
'1:0':',\n무엇을 하겠느냐?',
'2:0':'토너먼트에\n참가하겠느냐...\n','2:1':'예  ','2:2':'아니오',
'3:0':'인터넷에\n플러그인하겠느냐...\n','3:1':'예  ','3:2':'아니오',
'4:0':'내 장비를\n바꾸겠느냐...\n','4:1':'예  ','4:2':'아니오',
'5:0':'데이터 라이브러리를\n보겠느냐...\n','5:1':'예  ','5:2':'아니오',
'6:0':'메일을 보겠느냐...\n\n','6:1':'예  ','6:2':'아니오',
'7:0':'통신 대전을\n하겠느냐...\n','7:1':'예  ','7:2':'아니오',
'8:0':'저장 화면으로\n들어가겠느냐...?\n','8:1':'예  ','8:2':'아니오',
'10:0':'토너먼트에\n참가하겠느냐...\n','10:1':'예  ','10:2':'아니오',
'11:0':'인터넷에\n플러그인하겠느냐...\n','11:1':'예  ','11:2':'아니오',
'12:0':'내 장비를\n바꾸겠느냐...\n','12:1':'예  ','12:2':'아니오',
'13:0':'데이터 라이브러리를\n보겠느냐...\n','13:1':'예  ','13:2':'아니오',
'14:0':'메일을 보겠느냐...\n\n','14:1':'예  ','14:2':'아니오',
'15:0':'통신 대전을\n하겠느냐...\n','15:1':'예  ','15:2':'아니오',
'16:0':'지금까지의 데이터를\n저장하겠느냐...\n','16:1':'예  ','16:2':'아니오',
'20:0':'\n내 이야기는\n아직 끝나지 않았다',
},
'66BDE0':{
'1:0':'돌아왔다...\n오늘의 전뇌 바람은\n그럭저럭이군...',
'2:0':'크...\n당하고 말았구나...\n바람 방향이 바뀌었나',
},
'66BEF8':{'1:0':'플러그인!\n윈드맨.EXE,\n트랜스미션!!'},
'66BF44':{
'1:0':' 시작할\n시간이다...',
'1:1':'TV를 볼 때는\n될 수 있으면 멀리서\n보는 것이 좋다...',
'2:0':'\n약속 시간이다','2:1':'늦지 않도록\n가야 한다...',
'3:0':',\n식사 시간이다','3:1':'남기지 말고\n먹어야 한다...',
'4:0':'학원에 갈 시간이다\n열심히 배우고\n오거라...',
'5:0':' 일정\n시간이다...\n늦어서는 안 된다',
'6:0':'그리고...',
'21:0':' 시작할\n시간이다...',
'21:1':'TV를 볼 때는\n될 수 있으면 멀리서\n보는 것이 좋다...',
'22:0':'\n약속 시간이다','22:1':'늦지 않도록\n가야 한다...',
'23:0':',\n식사 시간이다','23:1':'남기지 말고\n먹어야 한다...',
'24:0':'학원에 갈 시간이다\n열심히 배우고\n오거라...',
'25:0':' 일정\n시간이다...\n늦어서는 안 된다',
'26:0':'그리고...',
}}
CONTEXT={
'66B950':'Quick menu1/2..8 and10..16 confirmation routes plus interrupted-dialogue20. No mugshot in source;28 choices.',
'66BDE0':'Quick return success/defeat and cyber-wind metaphor; no mugshot shown.',
'66BEF8':'Type3 jackin call explicitly names WindMan.EXE destination. Operator command, not character self-speech.',
'66BF44':'TV/promise/meal/school/other/additional reminders, quick1..6 and explicit WindMan21..26.',
}
NOTES={
'66B950':['Save8 asks to enter save screen;16 asks to save accumulated data. Do not conflate. Menu dispatch, yes target9, no/cancel return1 and20 jump10 retained.', '10..16 alternate path stores global30=120/flag3588/wait1;2..8 does not. Flags3584/3585/3588/3615, tracks127/128,24px option placement and all blank lines/two-space choice padding preserved.', 'No WindMan portrait in this archive; first-person and adjacent source not identity proof. Candidate calm voice only; actual menu/runtime unverified.'],
'66BDE0':['Cyber wind and changed wind direction source imagery retained, not replaced by invented tactical cause. Defeat route wording distinct from ordinary return; actor unknown.'],
'66BEF8':['Preserve literal EXE token, three lines, destination WindMan name, flags3603/3651, wait30/type3 coordinates. Call itself does not show portrait or establish operator identity.'],
'66BF44':['TV distance advice, punctuality, eating without leftovers, sourceじゅく as 학원, learning and extra-event notices kept. No real-world medical advice inferred.', 'Only21..26 explicitly show WindMan; quick1..6 no portrait. Schedule-name+시작할/일정 and nickname comma avoid fixed final-consonant particle.', '0/20 event dispatch and6/26 multiple-event loops, flags3585/3658, sound155/wait96, buffers and options preserved; no clock/input/save/runtime verification.', '66BE58:0:0 sourceかりです inspected but untranslated, unknown placeholder consumer retained in denominator.'],
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
        shown=archive=='66BF44' and s>=20;choice=archive=='66B950' and i in (1,2)
        speaker='player-choice' if choice else 'WindMan' if shown else 'operator-jackin-call' if archive=='66BEF8' else 'unshown-quick-voice'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait='WindMan' if shown else None,portrait_visibility='shown' if shown else 'not-shown-in-script',
            context=CONTEXT[archive],variable_context='Preserve nickname and schedule buffers/command order. Name + 시작할/일정 avoids final-consonant particle. Actual variable widths/caller and runtime display unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='quick-confirmation-return-jackin-reminders',context=CONTEXT[archive],
        voice='Calm elder-like source forms as candidate, not approved. Only66BF44:21..26 explicit WindMan portraits; other quick voices unknown. Jackin call names destination, not speaker.',
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
