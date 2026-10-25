"""Individually authored plaza NPC95, per-script native portrait bound."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/7A32A8.tpl'
SOURCE_SHA='707c917fcb8925bf21dbab0b40d8da6ab8bffb7e97ef8d4af53688c196b73390'
OUT='translations/plaza_npcs_draft_ko.json'
DRAFT={
0:['휴일에는 항상\n여기서 놀지','쇼핑도 할 수 있고\n편히 쉴 수도 있으니까','지금은 새 칩을\n살까 말까\n고민 중이야'],
1:['자!\n오늘도 마음껏\n놀아 보자!!','이 광장은,\n우리들의 낙원이야!!'],
2:['쇼핑을\n좀 너무 많이 했더니,\n지갑이 위험해','자꾸 필요 없는 것까지\n사 버리는 게, 내\n나쁜 버릇이지'],
10:['나도 말이야\n쇼핑을 엄청 좋아해서,','자꾸 이 녀석과\n어울려 다니며\n이것저것 사게 되거든','그래도 괜찮잖아!\n누구한테 폐 끼치는 것도 아냐!\n내 제니라고!!'],
11:['오늘도 여기\n와 버렸네...','되도록\n돈을 안 쓰겠다고\n생각하면서도,','결국 잔뜩\n쇼핑하고 말지...'],
12:['이야,\n또 이 녀석이랑 함께\n이것저것 사 버렸어','지갑은 텅 비어\n찬바람이 불지만,\n마음은 따끈따끈하다고!!','.','.','.','후회는 없다!!'],
20:['뭐고, 네놈!!\n감히 나한테 친한 척\n말을 걸다니...','각오는\n되어 있겠제!!\n어이이이이!!','.','.','.','...어?\n어라?','뭐, 뭐야? 그\n「싸우자는 거면 받아 주지」\n같은 무서운 눈빛은...','거짓말이에요, 죄송해요\n저, 사실 싸움 같은 건\n정말 못해요','조금\n우쭐해 있었어요\n정말 죄송해요'],
21:['광장 입구 근처의\n그 노란 아가씨,\n귀엽지 않나?','살짝 사투리를\n쓰는 말투까지,\n내 마음에 쏙 든대이!!','근데 내가 이래 보여도\n수줍음을 타서,\n말을 못 걸겠대이!!','꺅!!\n부, 부끄러워!!'],
22:['그 귀여운 아가씨,\n플러그아웃해 버렸네','후...\n서글프대이...'],
23:['자, 사람도 줄었으니,\n나도 슬슬\n플러그아웃하겠대이'],
30:['제기라아아알!!\n또 토너먼트\n첫판에 졌다아아!!','왜냐아아아!!\n평일에도 쉬지 않고\n맹훈련하는데에에!!','재능이 없는 거냐\n나한테는!!'],
31:['슬슬 이 에어리어도\n북적이기 시작할\n시간대네','하아암...\n그나저나 일요일 아침은\n졸려...','그래도 멍하니 있을 순 없지!\n오늘은 기다리고 기다리던\n토너먼트 날이니까!!'],
32:['우오오오오오!!','난 도대체 몇 번 연속\n토너먼트\n첫판에 진 거지!?','어디 보자,\n1, 2, 3...','이젠 셀 수도 없어!!\n왜, 왜\n난 이렇게 약한 거냐아!!','역시 재능이 없는 거냐\n나한테는!!'],
40:['다들\n편히 쉴 광장도 있고,\n숍도 있으니까,','여기 있으면\n하루 종일 전혀\n심심하지 않구먼!!','역시 도시여!!'],
41:['나는, 최근에\n시골에서 이쪽으로\n막 이사 왔어유!','세련된\n도시 여자가\n될 거여!!'],
42:['시골도 시골 나름\n좋은 데가 있긴 한데,','나처럼 젊은 내비한테는,\n역시 도시가\n자극도 있고 좋구먼!'],
50:['아아, 우리는\n프로그램이면서도,\n서로 사랑하고 말았어!!','원래는\n허락되지 않는\n이 사랑...','하지만 괜찮잖아!!\n어쩔 수 없잖아!!\n좋아하는걸!!'],
51:['...어라?\n그런데, 프로그램은\n연애하면 안 되는 건가?','.','.','.','뭐, 됐어','「금지된 사랑」이라는\n느낌이,\n뭔가 더 멋있잖아!!'],
60:['프로그램이라서\n사랑이\n허락되지 않는다면,','나,\n너와 함께\n도망칠래!!','그래, 어디로든!!\n라라라 너와 함께라면~'],
61:['우리의 사랑은\n금지된 사랑!!','뭔가\n멋지지 않아?'],
70:['젊은이들은 모두,\n넷 배틀에\n푹 빠져 있구먼...','나도 가끔\n도전해 보지만,\n늙어서 금방 져 버리지','.','.','.','허허!!\n시 한 수가 떠올랐네!!','「젊은이와\n 배틀을 벌였더니\n 다리가 풀렸네」'],
71:['넷 배틀 초보자는,\n반드시 이 에어리어에 오지','견습 넷 배틀러가 되어,\n토너먼트에\n참가하기 위해서야','.','.','.','흠!!\n시 한 수가 떠올랐네!!','「승리해서\n 언젠가 되고 싶네\n 오피셜이」'],
80:['매주우우!!\n월요일은은은!!\n쓰레기 버리는 날!!','그리하여\n화려하게 등장!!\n주부 내비!!','자,\n쓰레기를 버리겠어!!\n버릴 거야아아!!','으랴아아아!!\n휙이이이!!'],
90:['어머, 안녕하세요','여러모로\n편리한 곳이라 그런지,\n휴일에는 북적이는군요','쇼핑을\n좋아해서\n지루하진 않네요'],
91:['왠지 이 에어리어는,\n열성적인 사람들이\n많다 했더니,','토너먼트\n참가 접수 같은 걸\n하고 있었군요!!','넷 배틀이라니\n야만적이에요!!\n품위 없어요!!'],
110:['토너먼트는\n1개가 아니야...','강한 녀석에게는,\n그 힘에 걸맞은 무대가\n준비되어 있다는 거지...'],
111:['도대체,\n토너먼트는 몇 개나\n열리는 걸까','최상위 내비들이\n모이는 토너먼트라니,\n엄청 대단할 것 같아']
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA);original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    values={f'7A32A8:{s}:{i}':t for s,rows in DRAFT.items() for i,t in enumerate(rows)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=95 or set(values)!={x.key for x in selected}:raise ValueError('plaza95 scope '+str(set(values)^{x.key for x in selected}))
    blocks={int(s):b for s,b in re.findall(r'script (\d+) mmbn45 \{(.*?)(?=\nscript |\Z)',original,re.S)}
    units=[]
    for x in selected:
        s=int(x.key.split(':')[1]);t=values[x.key];portraits=re.findall(r'mugshot = (\w+)',blocks[s])
        if len(portraits)!=1:raise ValueError('unresolved portrait '+x.key)
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('source row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('source numbers/tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=portraits[0],context='Plaza shopping, bully/reversal, tournament disappointment, countryside newcomer, program romance, elderly verse, rubbish day, polite shopper and tournament ambition. Exact native per-script portraits and time branch arguments retained.',variable_context='No variable substitutions. Timed punctuation kept separate, all source page and line boundaries retained. No time/weekday/portrait patching; actual caller and display review pending.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x7A32A8)
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='7A32A8',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue',context='All95 Japanese literals in255-slot plaza NPC archive. Per-script native portraits bound, local dialogue groups read together. Time branches unchanged even script10 targeting1/2 with different portraits; no speculative branch repair.',voice='Per-NPC drafts from source register; HeelNaviBlack bluff followed by polite apology, NaviGirlOrange countryside voice, program romance roles and NormalNaviBrown elderly verse distinguished. Dialect mapping remains a candidate, not approved regional adaptation.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve IDs, numbers1/2/3 and1tournament, native time branches/portraits/commands/point boundaries, source contradictions, romance uncertainty, verse3-row topology and original weekday. No ROM or save writes.',semantic_review=['Kansai-like bluff/dialect20..23 and countryside40..42 use distinct Korean colloquial candidates; this does not assert Japanese regions are Korean regions. Full dialect/localization approval pending.', 'Original haiku-style verse70/71 keeps three lines and meaning; Korean5/7/5 metre and physical/fear double meaning of コシヌけた not claimed. Human cultural/presentation review needed.', 'Program50/51 doubts whether romance is forbidden;60 is conditional if forbidden. No certainty or new rule about programs added.', 'Script21 says yellow girl while nearby portrait group40 is orange. Preserve source yellow reference, no guessed identity or palette correction.', 'Source10 time targets1/2 are unchanged; static portrait binding is for each stored script, not proof of all actual callers or time routes.'],units=units)

def main():
    a=create();path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored plaza NPC95 draft only; ROM unchanged')

if __name__=='__main__':main()
