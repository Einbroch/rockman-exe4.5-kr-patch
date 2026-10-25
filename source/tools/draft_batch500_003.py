"""Batch500-003: explicit manual menu484/training15/jackin1 drafts; no ROM/save writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
'670E9C':('d678d9add1eff3b216f408654ffd47b7b03b57e9f7b19f8138a8ea08a8c3fb88',44,'translations/batch500_003_menu_670E9C_draft_ko.json'),
'676BA8':('59580c1422727350014322dd371f4d642971b29603200e8501f08ce326eef127',44,'translations/batch500_003_menu_676BA8_draft_ko.json'),
'67C578':('5183f7749d84a8f6964508f12732816127581e70719398b762c0b69546a89680',44,'translations/batch500_003_menu_67C578_draft_ko.json'),
'681B3C':('4a5dfbcb1bb750809d4fdc35224671c28bccc522d31402e0f16001f955c9ef6a',44,'translations/batch500_003_menu_681B3C_draft_ko.json'),
'68D454':('c5a048b58065b139c0cf8b9e05fe28d3295edf7a33e31234a636b0c7da8396b3',44,'translations/batch500_003_menu_68D454_draft_ko.json'),
'6930F8':('a3e50069f521320fe88924864d9808ef0f4bf3ed11b21e0071bc5004215591a9',44,'translations/batch500_003_menu_6930F8_draft_ko.json'),
'698508':('4096b78ed3958dcd87b32eb5890ebdee17474fdfa0f16bc95905bba996706474',44,'translations/batch500_003_menu_698508_draft_ko.json'),
'69E12C':('60ddf0c2fcc3cbaa1eae3b5ca805d8b58dbafa4e96fbc742295e28fa09cdc53b',44,'translations/batch500_003_menu_69E12C_draft_ko.json'),
'6A38E8':('506416d97ef9c88e2b22c9b67e7aa535353101205e058590ad5d81e242c5e29d',44,'translations/batch500_003_menu_6A38E8_draft_ko.json'),
'6AA214':('e0ff7acfd66b3fab71757372624f7f391082435a937dd553ef25983fa1beec0c',44,'translations/batch500_003_menu_6AA214_draft_ko.json'),
'6B5B1C':('6f54060050082235db1cfb7b3375105f7d6c0348cfcf6c316aac748053ff4e9b',44,'translations/batch500_003_menu_6B5B1C_draft_ko.json'),
'6713B8':('59d744b9c41b39e59e8e3fefbff0a7d36bb5165ffcba4d73e582c90d0e59e450',15,'translations/batch500_003_training_results_draft_ko.json'),
'671638':('3269e6118f3450aa3ee7707180657eefa48fec276c77a72b29ec42c3d09aafe4',1,'translations/batch500_003_search_jackin_draft_ko.json'),
}
MENUS=tuple(SOURCES)[:11]
EXCLUDED={'6713B8':{'6713B8:0:0'}}
# Explicit menu option candidates matched to every inspected stable choice ID.
# No source-string replacement or speaker prose generation.
CHOICES={
'2:1':'예  ','2:2':'아니오','3:1':'예  ','3:2':'아니오',
'4:1':'예  ','4:2':'아니오','5:1':'예  ','5:2':'아니오',
'6:1':'예  ','6:2':'아니오','7:1':'예  ','7:2':'아니오',
'8:1':'예  ','8:2':'아니오','10:1':'예  ','10:2':'아니오',
'11:1':'예  ','11:2':'아니오','12:1':'예  ','12:2':'아니오',
'13:1':'예  ','13:2':'아니오','14:1':'예  ','14:2':'아니오',
'15:1':'예  ','15:2':'아니오','16:1':'예  ','16:2':'아니오',
}
DRAFT={
'670E9C':{
'1:0':',\n무엇을 하시겠습니까?',
'2:0':'토너먼트에\n참가하시겠습니까?\n',
'3:0':'인터넷에\n플러그인하시겠습니까?\n',
'4:0':'제 장비를\n변경하시겠습니까?\n',
'5:0':'데이터 라이브러리를\n확인하시겠습니까?\n',
'6:0':'메일을\n확인하시겠습니까?\n',
'7:0':'통신 대전을\n하시겠습니까?\n',
'8:0':'저장 화면으로\n들어가시겠습니까?\n',
'10:0':'토너먼트에\n참가하시겠습니까?\n',
'11:0':'인터넷에\n플러그인하시겠습니까?\n',
'12:0':'제 장비를\n변경하시겠습니까?\n',
'13:0':'데이터 라이브러리를\n확인하시겠습니까?\n',
'14:0':'메일을\n확인하시겠습니까?\n',
'15:0':'통신 대전을\n하시겠습니까?\n',
'16:0':'지금까지의 데이터를\n저장하시겠습니까?\n',
'20:0':'끝까지 듣지 않으면\n중요한 정보를\n놓칠지도 모릅니다',
},
'676BA8':{
'1:0':'여어, 뭘 할 거야?',
'2:0':'토너먼트에\n참가할 거야?\n',
'3:0':'인터넷에\n플러그인할 거야?\n',
'4:0':'이 몸의 장비를\n바꿀 거야?\n',
'5:0':'데이터 라이브러리를\n볼 거야?\n',
'6:0':'메일을\n확인할 거야?\n',
'7:0':'통신 대전을\n할 거야?\n',
'8:0':'저장 화면으로 들어갈 거야?\n\n',
'10:0':'토너먼트에\n참가할 거야?\n',
'11:0':'인터넷에\n플러그인할 거야?\n',
'12:0':'이 몸의 장비를\n바꿀 거야?\n',
'13:0':'데이터 라이브러리를\n볼 거야?\n',
'14:0':'메일을\n확인할 거야?\n',
'15:0':'통신 대전을\n할 거야?\n',
'16:0':'지금까지의 데이터를\n저장할까?\n',
'20:0':'내 이야기를\n끝까지\n못 듣겠다는 거야!?',
},
'67C578':{
'1:0':',\n무엇을 하겠느냐?',
'2:0':'토너먼트에\n참가하겠느냐?\n',
'3:0':'인터넷에\n플러그인하겠느냐?\n',
'4:0':'내 장비를\n바꾸겠느냐?\n',
'5:0':'데이터 라이브러리를\n확인하겠느냐?\n',
'6:0':'메일을 보겠느냐?\n\n',
'7:0':'통신 대전을\n하겠느냐?\n',
'8:0':'저장 화면에 들어가겠느냐?\n\n',
'10:0':'토너먼트에\n참가하겠느냐?\n',
'11:0':'인터넷에\n플러그인하겠느냐?\n',
'12:0':'내 장비를\n바꾸겠느냐?\n',
'13:0':'데이터 라이브러리를\n확인하겠느냐?\n',
'14:0':'메일을 보겠느냐?\n\n',
'15:0':'통신 대전을\n하겠느냐?\n',
'16:0':'지금까지의 데이터를\n기록하겠느냐?\n',
'20:0':'너는 먼저,\n남의 이야기를 끝까지\n듣는 법부터 배워야겠구나',
},
'681B3C':{
'1:0':',\n무엇을 하시겠습니까?',
'2:0':'토너먼트에\n참가하시겠습니까?\n',
'3:0':'인터넷에\n플러그인하시겠습니까?\n',
'4:0':'제 장비를\n변경하시겠습니까?\n',
'5:0':'데이터 라이브러리를\n보시겠습니까?\n',
'6:0':'메일을\n확인하시겠습니까?\n',
'7:0':'통신 대전을\n하시겠습니까?\n',
'8:0':'저장 화면으로\n들어가시겠습니까?\n',
'10:0':'토너먼트에\n참가하시겠습니까?\n',
'11:0':'인터넷에\n플러그인하시겠습니까?\n',
'12:0':'제 장비를\n변경하시겠습니까?\n',
'13:0':'데이터 라이브러리를\n보시겠습니까?\n',
'14:0':'메일을\n확인하시겠습니까?\n',
'15:0':'통신 대전을\n하시겠습니까?\n',
'16:0':'지금까지의 데이터를\n저장하겠습니다\n',
'20:0':'실례지만,\n제 이야기는\n아직 끝나지 않았습니다',
},
'68D454':{
'1:0':'...무엇을 할까?',
'2:0':'...토너먼트에\n참가하겠나?\n',
'3:0':'...인터넷에\n플러그인하겠나?\n',
'4:0':'...내 장비를\n바꾸겠나?\n',
'5:0':'...데이터 라이브러리를\n보겠나?\n',
'6:0':'...메일을\n확인하겠나?\n',
'7:0':'...통신 대전을\n하겠나?\n',
'8:0':'저장 화면에 들어가겠나?\n\n',
'10:0':'...토너먼트에\n참가하겠나?\n',
'11:0':'...인터넷에\n플러그인하겠나?\n',
'12:0':'...내 장비를\n바꾸겠나?\n',
'13:0':'...데이터 라이브러리를\n보겠나?\n',
'14:0':'...메일을\n확인하겠나?\n',
'15:0':'...통신 대전을\n하겠나?\n',
'16:0':'...지금까지의 데이터를\n저장하겠나?\n',
'20:0':'남의 이야기는\n끝까지 듣는 편이\n좋다고 생각한다...',
},
'6930F8':{
'1:0':',\n무, 무엇을 하겠나?',
'2:0':'토너먼트에\n참가하겠나...?\n',
'3:0':'인터넷에\n플러그인하겠나?\n',
'4:0':'내 장비를\n바꾸겠나...?\n',
'5:0':'데이터 라이브러리를\n보겠나...?\n',
'6:0':'메일을\n확인하겠나?\n',
'7:0':'통신 대전을\n하겠나...?\n',
'8:0':'저장 화면으로\n들어가겠나?\n',
'10:0':'토너먼트에\n참가하겠나...?\n',
'11:0':'인터넷에\n플러그인하겠나?\n',
'12:0':'내 장비를\n바꾸겠나...?\n',
'13:0':'데이터 라이브러리를\n보겠나...?\n',
'14:0':'메일을\n확인하겠나?\n',
'15:0':'통신 대전을\n하겠나...?\n',
'16:0':'지금까지의 데이터를\n저장하겠나...?\n',
'20:0':',\n나, 나는 아직\n말하고 있다...',
},
'698508':{
'1:0':"뭘 할 거야, 퓨~?",
'2:0':"토너먼트에\n참가할 거야, 퓨?\n",
'3:0':"인터넷에\n플러그인할 거야, 퓨?\n",
'4:0':"내 장비를\n바꿀 거야, 퓨?\n",
'5:0':"데이터 라이브러리를\n볼 거야, 퓨?\n",
'6:0':"메일을\n확인할 거야, 퓨?\n",
'7:0':"통신 대전을\n할 거야, 퓨?\n",
'8:0':"저장 화면으로\n들어갈 거야, 퓨?\n",
'10:0':"토너먼트에\n참가할 거야, 퓨?\n",
'11:0':"인터넷에\n플러그인할 거야, 퓨?\n",
'12:0':"내 장비를\n바꿀 거야, 퓨?\n",
'13:0':"데이터 라이브러리를\n볼 거야, 퓨?\n",
'14:0':"메일을\n확인할 거야, 퓨?\n",
'15:0':"통신 대전을\n할 거야, 퓨?\n",
'16:0':"지금까지의 데이터를\n저장할 거야, 퓨?\n",
'20:0':"아, 아, 아직\n이야기 중이야, 퓨",
},
'69E12C':{
'1:0':',\n무엇을 하겠느냐?',
'2:0':'토너먼트에\n참가하겠느냐?\n',
'3:0':'인터넷에\n플러그인하겠느냐?\n',
'4:0':'내 장비를\n바꾸겠느냐?\n',
'5:0':'데이터 라이브러리를\n확인하겠느냐?\n',
'6:0':'메일을 보겠느냐?\n\n',
'7:0':'통신 대전을\n하겠느냐?\n',
'8:0':'저장 화면으로\n들어가겠느냐?\n',
'10:0':'토너먼트에\n참가하겠느냐?\n',
'11:0':'인터넷에\n플러그인하겠느냐?\n',
'12:0':'내 장비를\n바꾸겠느냐?\n',
'13:0':'데이터 라이브러리를\n확인하겠느냐?\n',
'14:0':'메일을 보겠느냐?\n\n',
'15:0':'통신 대전을\n하겠느냐?\n',
'16:0':'지금까지의 데이터를\n저장하겠느냐?\n',
'20:0':'성급한 녀석이구나...\n좀 더 침착하게\n행동해야 한다',
},
'6A38E8':{
'1:0':'자, 뭘 할까?',
'2:0':'토너먼트에\n참가할래?\n',
'3:0':'인터넷에\n플러그인할까?\n',
'4:0':'내 장비를\n바꿀까?\n',
'5:0':'데이터 라이브러리를\n볼까?\n',
'6:0':'메일을 확인할까?\n\n',
'7:0':'통신 대전을\n할까?\n',
'8:0':'저장 화면으로 들어갈래?\n\n',
'10:0':'토너먼트에\n참가할래?\n',
'11:0':'인터넷에\n플러그인할까?\n',
'12:0':'내 장비를\n바꿀까?\n',
'13:0':'데이터 라이브러리를\n볼까?\n',
'14:0':'메일을 확인할까?\n\n',
'15:0':'통신 대전을\n할까?\n',
'16:0':'지금까지의 데이터를\n저장할까?\n',
'20:0':'내 이야기는\n아직 안 끝났어!\n흥!',
},
'6AA214':{
'1:0':'...자,\n무엇을 하겠느냐?',
'2:0':'토너먼트에\n참가하겠느냐...?\n',
'3:0':'인터넷에\n플러그인하겠느냐?\n',
'4:0':'내 장비를\n바꾸겠느냐?\n',
'5:0':'데이터 라이브러리를\n보겠느냐?\n',
'6:0':'메일을\n확인하겠느냐?\n',
'7:0':'통신 대전을\n하겠느냐?\n',
'8:0':'저장 화면에 들어가겠느냐?\n\n',
'10:0':'토너먼트에\n참가하겠느냐...?\n',
'11:0':'인터넷에\n플러그인하겠느냐?\n',
'12:0':'내 장비를\n바꾸겠느냐?\n',
'13:0':'데이터 라이브러리를\n보겠느냐?\n',
'14:0':'메일을\n확인하겠느냐?\n',
'15:0':'통신 대전을\n하겠느냐?\n',
'16:0':'지금까지의 데이터를\n기록하겠느냐?\n',
'20:0':'남의 말을 끝까지\n듣지 못하다니,\n닌자로서 실격이다...',
},
'6B5B1C':{
'1:0':',\n무엇을 하시겠습니까?',
'2:0':'토너먼트에\n참가하시겠습니까?\n',
'3:0':'인터넷에\n플러그인하겠습니다만?\n',
'4:0':'제 장비를\n변경하시겠습니까?\n',
'5:0':'데이터 라이브러리를\n보시겠습니까?\n',
'6:0':'메일을\n확인하겠습니다만?\n',
'7:0':'통신 대전을\n하시겠습니까?\n',
'8:0':'저장 화면으로\n들어가시겠습니까?\n',
'10:0':'토너먼트에\n참가하시겠습니까?\n',
'11:0':'인터넷에\n플러그인하겠습니다만?\n',
'12:0':'제 장비를\n변경하시겠습니까?\n',
'13:0':'데이터 라이브러리를\n보시겠습니까?\n',
'14:0':'메일을\n확인하겠습니다만?\n',
'15:0':'통신 대전을\n하시겠습니까?\n',
'16:0':'지금까지의 데이터를\n저장하겠습니다만?\n',
'20:0':'조금 더 침착하게\n남의 이야기를\n들어 보시겠습니까?',
},
'6713B8':{
'70:0':',\n죄송합니다\n이럴 리가 없는데...',
'71:0':'미션 완료',
'71:1':'이번 훈련에서,\n뭔가 깨달음을 얻은\n느낌입니다...',
'71:2':'한층 더\n성장할 수 있었던 것\n같습니다',
'72:0':'미션 완료',
'72:1':'이번 훈련에서,\n뭔가 깨달음을 얻은\n느낌입니다...',
'72:2':'...방금 군에서\n무언가가\n전송되었습니다!',
'72:3':'이번 훈련에\n성공한 보상이라고\n합니다...',
'72:4':'제니를\n획득했습니다',
'73:0':'미션 완료',
'73:1':'이번 훈련에서,\n뭔가 깨달음을 얻은\n느낌입니다...',
'73:2':'...방금 군에서\n무언가가\n전송되었습니다!',
'73:3':'이번 훈련에\n성공한 보상이라고\n합니다...',
'73:4':'버그 조각',
'73:5':'개를\n획득했습니다!',
},
'671638':{'1:0':'플러그인!\n서치맨.EXE,\n트랜스미션!!'},
}
CONTEXT={a:'Quick menu1/2..8/10..16 confirmations and interrupted dialogue20; full literal population and canonical control differences inspected; no portrait.' for a in MENUS}
CONTEXT.update({'6713B8':'Minigame2 result dispatch global5=0/1/2/3; apology, completion, growth item33, military-transmitted zenny/bug-frag rewards. No portrait; placeholder0 unresolved.',
'671638':'Type3 operator jackin call explicitly names SearchMan.EXE destination; not character self-speech.'})
def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    ids={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}-EXCLUDED.get(archive,set())
    authored={**DRAFT[archive],**CHOICES} if archive in MENUS else DRAFT[archive]
    values={archive+':'+k:v for k,v in authored.items()}
    selected=[x for x in literals(original) if x.key in ids]
    if len(selected)!=count or set(values)!=ids:raise ValueError('batch scope '+archive)
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('batch topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('batch tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('batch padding '+x.key)
        choice=archive in MENUS and f'{s}:{i}' in CHOICES
        speaker='player-choice' if choice else 'operator-jackin-call' if archive=='671638' else 'unshown-quick-voice'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait=None,portrait_visibility='not-shown-in-script',context=CONTEXT[archive],
            variable_context='Nickname punctuation and source literal/page boundaries unchanged; reward amount buffer3 not hardcoded. EXE destination preserved. Runtime/layout unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    notes=['Batch500-003 exact500 stable literals: menu484 (308 choices/176 prose), training15, jackin1. Not500 unique sentences.',
        'All needs_review/non-distribution; no ROM/save writes, independent wording approval or runtime proof.',
        'Menu baseline670E9C read in full; all menu literals inspected, all command skeleton tokens compared against baseline. Differences only nickname insertion and textSpeed0; preserved per archive, not normalized. Training and jackin full scripts read.']
    if archive in MENUS:
        notes+=['Keep two menu dispatch groups;2..8 vs10..16 global30=120/flag3588/wait1; yes9/no return1,20 jump10; flags3584/3585/3588/3615, tracks127/128, default/cancel/24px/blank lines/choice padding.',
            'Save8 is entry to save screen,16 accumulated-data saving (681B3C source statement remains statement). No save/menu action executed.',
            'Source polite/direct/elder-like/robotic/shy speech and voiced suffix candidate retained per literal. No named actor inferred from adjacency. Nickname followed by comma avoids final-consonant-dependent vocative.',
            '6B5B1C:10 omits source参加 but dispatcher and corresponding2 establish tournament participation; Korean restores implicit predicate as development interpretation requiring semantic review.']
        if archive=='698508':
            notes+=['Sourceっぴゅ retained as 퓨 draft candidate, consistent with prior AquaMan candidate; not official voice approval.']
    elif archive=='6713B8':
        notes+=['0:0かりです excluded from authored scope only, kept in original/catalog/untranslated denominator. Not filler to reach500.',
            'Global5 result dispatch minigame2, item33 growth, 군 military transfer and reward purpose preserved; zenny/bug-frag values remain buffer3 and sentinel4294967295 command arguments unchanged.',
            'No inferred SearchMan portrait; actor unknown despite military register. Bug-frag label/count suffix split preserved.']
    else:
        notes+=['Three-line call, literalEXE token, SearchMan destination, type3/flags3603/3651/wait30 retained; command speaker identity unconfirmed.']
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='batch500-quick-menu-training-jackin',
        context=CONTEXT[archive],voice='Source-conditioned manual candidates, no named quick actor attribution; not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Source fields/IDs/TPL/payload, commands, variables, newline/padding and unselected placeholders immutable; no ROM/save writes.',
        batch_id='batch500-003',semantic_review=notes,units=units)
def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
