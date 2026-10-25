"""Individually authored PET/Official/news mail120; draft-only serialization."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/6DD9AC.tpl'
SOURCE_SHA='2a6c92f83d7fe1076688de57f7b162b1f23faedb755bc753d8bd6d127caeda9a'
OUT='translations/story_mail_draft_ko.json'
DRAFT={
0:[
'이번에 PET를\n구입해 주셔서,\n감사합니다',
'고객님께서 내비와\n함께, 즐거운 나날을\n보내시기를,',
'I.P.C. 임직원\n일동은 진심으로\n기원합니다',
'자, 오늘부터 고객님도\n어엿한 넷 배틀러의\n일원이 되십니다',
'PET는 바로\n인터넷에\n접속할 수 있도록',
'설정되어 있습니다',
'인터넷에는,\n주말에 열리는',
'넷 배틀 토너먼트의\n참가 접수장이\n마련되어 있습니다',
'참가 접수는,\n월요일부터 금요일의',
'아침6시부터\n밤12시까지입니다',
'참가 신청을 하면,\n주말 토너먼트에\n참가할 수 있습니다',
'토너먼트는,',
'실버 토너먼트,\n골드 토너먼트,\n오피셜 토너먼트',
'이렇게, 3개 토너먼트가\n개최됩니다',
'그중 최고봉인\n오피셜 토너먼트에서\n우승하는 것은',
'모든 넷 배틀러의\n꿈입니다',
'고객님도,\n오피셜 토너먼트\n우승을 목표로,',
'힘내 보시는 건\n어떨까요?',
'즐거운 일이 가득한\n인터넷이지만,',
'주의하셔야 할\n일도 있습니다',
'최근, 다크로이드를\n자칭하는 흉악한 내비가',
'인터넷에 나타난다는\n정보가\n들어오고 있습니다',
'부디 주의하시며,\n쾌적한 넷 배틀러\n생활을 즐기시길 바랍니다'
],
1:[
'모든 오피셜\n넷 배틀러에게 알린다',
'우리가 오래전부터\n추적 중인',
'다크로이드의 흔적을\n인터넷7에서\n발견했으나,',
'다크로이드 자체는\n이미 도주한 뒤였다',
'아마 더 깊은\n에어리어로 이동한 것으로\n보인다',
'더 자세한\n정보가 들어오는 대로\n연락하겠다',
'이상'
],
2:[
'지난 메일에 관해서다,',
'다크로이드가 서버에\n불법 접속을\n시도한 것이 원인으로,',
'민간인에게\n메일이 전송되었을\n우려가 있다',
'자세한 내용은 조사 중이나,\n다크로이드의 정보가\n외부에 유출되지 않도록',
'주의하기 바란다',
'다음으로, 다크로이드의\n정보에 관해서다,',
'언더인터넷에\n잠복하고 있을\n가능성이 높다는',
'정보가 들어왔다',
'우리 오피셜의\n관할 에어리어를 빠져나가\n언더에 들어간 듯하다',
'하지만, 언더는 녀석들\n어둠의 주민들의\n본거지다',
'섣불리 손을 대면,\n뜻밖의 반격을\n당할 수 있다',
'신중하게 수사를\n진행하기 바란다',
'이상'
],
3:[
'다크로이드 1체인,\n셰이드맨이',
'얼마 전 열린\n오피셜 토너먼트의\n우승자의 손에',
'삭제되었다는\n정보가 들어왔다',
'하지만, 녀석들은 어둠의\n힘으로 다시\n되살아날지도 모른다',
'계속해서\n경계해 주기 바란다',
'또한, 또 다른 1체의\n다크로이드가,',
'그 에어리어에\n잠복하고 있을\n가능성이 드러났다',
'그 에어리어 안쪽에는\n어둠의 힘을 끌어당기는\n무언가가 있는 듯하다',
'하지만, 그 에어리어에\n들어가는 것은\n오피셜이라 해도,',
'목숨을 버리러\n가는 것과 같다',
'장관의 지령이\n내려올 때까지 전원 대기',
'이상'
],
8:[
'메일 뉴스1호\n「탭맨을 조심하세요」',
'현재\n인터넷3에서',
'탭맨이라는 내비가\n폭주 중이라는 정보가\n들어오고 있습니다',
'어쩌면\n다크로이드의 소행일\n가능성도 있습니다',
'인적이 없는\n에어리어 구석 등을\n지나실 때는',
'각별히\n주의해 주세요!',
'이 메일은, 전국의\n견습 넷 배틀러에게\n보내 드리고 있습니다'
],
9:[
'메일 뉴스2호\n「다크로이드의 암약!」',
'지난번 전해 드린\n폭주 탭맨은',
'아무래도 어느\n뛰어난 오퍼레이터가\n쓰러뜨려 준 모양입니다!',
'오피셜의\n조사에 따르면\n탭맨은',
'다크로이드에게\n해킹을 당한\n모양입니다...',
'그리고 지금도\n다크로이드의 소행으로\n폭주 중인 내비가',
'인터넷5에\n출몰 중이라는\n정보가 들어왔습니다',
'절대로\n넷 배틀에 도전하는\n일이 없도록 해 주세요!'
],
10:[
'메일 뉴스3호\n「수수께끼의 오퍼레이터!」',
'놀랍게도 이번에도\n폭주하던\n스파크맨을...',
'수수께끼의 오퍼레이터가\n쓰러뜨려 주었다는\n정보가 들어왔습니다!',
'오피셜도 이\n오퍼레이터가 누구인지\n조사 중입니다',
'하지만 이번에는\n인터넷7에서',
'내비가 갈색 테이프에\n휘감기는 사건이\n발생하고 있습니다',
'앞으로도\n경계를 늦추지\n않도록 합시다!'
],
11:[
'메일 뉴스4호\n「오퍼레이터의 정체 공개!」',
'인터넷7에서\n폭주하던\n비디오맨을',
'또다시,\n그 오퍼레이터가\n쓰러뜨려 주었습니다!',
'우리의 조사\n결과,',
'수수께끼의 오퍼레이터의\n정체가\n밝혀졌습니다!!',
'그 오퍼레이터의 이름은\n',
'님!',
'감사합니다,\n',
'님!',
'화제를 바꿔서,\n인터넷9에서,',
'불길을 뿜는 내비가\n출몰하며,\n날뛰고 있다는',
'정보가 들어왔습니다',
'이번에도, 다크로이드의\n해킹으로 인한',
'폭주 사건으로\n보입니다!!',
'부디,\n조심해 주세요!'
],
12:[
'메일 뉴스5호\n「무차별 칼부림 사건 발생」',
'또다시,\n',
'님께서',
'인터넷9에서\n폭주하던',
'버너맨을\n쓰러뜨려 주었다는\n정보가 들어왔습니다',
'1개 사건이\n막 해결되었지만',
'인터넷10에서\n민간 내비가',
'무차별 칼부림을 당하는\n사건이 벌어지고 있습니다',
'다크로이드가 일으키는\n내비 폭주 사건이\n끊이지 않고 있습니다!',
'경계를 늦추지\n않도록 해 주세요!'
],
13:[
'메일 뉴스6호\n「영하의 세계」',
'인터넷10에서\n무차별 칼부림 사건을\n일으키던',
'켄도맨은\n',
'님에 의해\n쓰러졌습니다',
'하지만, 이번에는\n인터넷12에서',
'갑자기 영하의\n냉기가 내비를 덮치는\n사건이 일어났습니다!',
'그 냉기는\n약 -40도!!',
'보통 내비로서는\n견딜 수 없는 온도입니다',
'인터넷12를\n지나실 때는,\n주의해 주세요!'
],
14:[
'님',
'여기는, 오피셜\n센터입니다',
'귀하는, 수많은\n사건을\n해결하셨습니다',
'오피셜 일동은\n매우 감사하게\n생각하고 있습니다',
'이번에, 귀하께서는,\n오피셜 토너먼트의\n예선에 도전하기에 충분한',
'실력을 갖추신 것으로,\n판단되었습니다',
'오피셜 토너먼트의\n예선 접수는,',
'인터넷9에서\n진행하고 있습니다',
'한번 도전해\n보시는 건 어떨까요?'
]
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA);original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    if not all(t in original for t in ('I.P.C.しゃいん','callBeginStoryQuest','flag = 2054','flag = 2169','printPlayerName','flag = 2491')):raise ValueError('mail context changed')
    values={f'6DD9AC:{s}:{i}':t for s,rows in DRAFT.items() for i,t in enumerate(rows)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=120 or set(values)!={x.key for x in selected}:raise ValueError('mail120 scope '+str(set(values)^{x.key for x in selected}))
    units=[]
    for x in selected:
        script=int(x.key.split(':')[1]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('source row topology '+x.key)
        if re.findall(r'\d+|\[[^\]]+\]',t)!=re.findall(r'\d+|\[[^\]]+\]',x.text):raise ValueError('source numbers/tokens '+x.key)
        speaker='I.P.C.-customer-mail' if script==0 else 'Official-bulletin' if script in (1,2,3,14) else 'mail-news-editor'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,context='PET customer guidance0; confidential Official notices1..3; ordered incident news8..13 with source quest flags; Official qualification invitation14',variable_context='printPlayerName unchanged; 님/님께서/님에 의해 avoid final-consonant-dependent particles. Source deliberately unnamed area/revival uncertainty retained. Full native mail consumer/layout review pending'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x6DD9AC)
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6DD9AC',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='mail-text',context='All120 Japanese literals in32-slot mail archive. Complete local letter bodies and serialized news read together; source quest/control semantics retained, no quest execution.',voice='Polite I.P.C./news/customer mail separated from imperative confidential Official bulletins. Existing chip name candidates 탭맨/셰이드맨/스파크맨/비디오맨/버너맨/켄도맨 reused.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep source mail slot IDs, weekday/schedule/time/numbers, source chain order, deliberate unspecified location, possibility rather than certainty, name variables, quest/flag commands and line topology. No ROM/save mutation.',semantic_review=['Boss names inherit chip_secondary_names_ko.json candidates, not new human approval. 다크로이드/언더인터넷/넷 배틀러 need full glossary applicability review.', 'Source3 unspecified area remains 그 에어리어; no inferred location, identity, new causal relation or certain revival added.', 'Script0 morning6/night12 and Monday-Friday preserved; script13 approximate -40 degrees retains minus sign and approximation; times are not converted to different numeric groups.', 'Source news narrative moves from unnamed skilled operator to player-name revelation and later named gratitude. Name-dependent particle endings avoided; variable budgets and actual mail layout unverified.'],units=units)

def main():
    a=create();path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored mail120 draft only; ROM unchanged')

if __name__=='__main__':main()
