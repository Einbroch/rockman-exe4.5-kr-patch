"""Individually authored save dialogue271; source-pinned serialization only.

All script rows explicitly authored here, not machine-translated substitutions.
Not connected to the ROM builder. User requests full drafting before insertion.
"""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals,serialize,skeleton
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/6DA21C.tpl'
SOURCE_SHA='39179b397c6bf925a300105542d125be246c9c088cd2db0d7bdd4d06ec1b9775'
OUT='translations/remaining_navi_save_draft_ko.json'
SPEAKERS={30:'WindMan',35:'SearchMan',40:'FireMan',45:'ThunderMan',50:'ProtoMan',60:'MetalMan',65:'JunkMan',70:'AquaMan',75:'WoodMan',80:'StarMan',85:'ShadowMan',90:'KnightMan',95:'NapalmMan',100:'IceMan',105:'ElecMan',110:'PlantMan',115:'Bass'}
DRAFT={
30:['지금까지의 활약을\n저장해 두겠나?\n','예  ','아니요'],
31:['기존 저장 데이터를\n덮어쓰겠네...\n','예  ','아니요'],
32:['저장 중이네...\n전원을 끄지 말게','저장에\n실패한 것 같군...','다시 해 보겠네\n','예  ','아니요'],
33:['저장이 끝났네...'],
34:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없네','다시 해 보겠네\n','예  ','아니요'],
35:['지금까지의 활약을\n저장할까요?\n','예  ','아니요'],
36:['기존 저장 데이터를\n덮어씁니다만,\n괜찮으시겠습니까?','예  ','아니요'],
37:['저장 중입니다...\n전원을 끄지\n마십시오...','저장에\n실패했습니다','다시 한번\n시도할까요?\n','예  ','아니요'],
38:['......\n완료!\n저장이 끝났습니다'],
39:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없습니다','다시 한번\n시도할까요?\n','예  ','아니요'],
40:['지금까지의 활약을\n저장해 둘까?\n','예  ','아니요'],
41:['기존 저장 데이터를\n덮어써 버릴 건데?\n','예  ','아니요'],
42:['저장 중이다\n전원 끄지 마라','저장에\n실패했군...','다시 한번\n해 볼까?\n','예  ','아니요'],
43:['저장이 끝났다'],
44:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없군','다시 한번\n해 볼까?\n','예  ','아니요'],
45:['지금까지의 활약을\n저장하려는 건가...\n','예  ','아니요'],
46:['기존 저장 데이터를\n덮어쓰겠다. 좋겠지?\n','예  ','아니요'],
47:['저장 중이다...\n전원을 끄면\n안 된다...','저장에\n실패한 듯하군...','다시 한번\n해 볼까?\n','예  ','아니요'],
48:['......\n저장이 끝났다'],
49:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없군...','다시 한번\n해 볼까?\n','예  ','아니요'],
50:['지금까지의 활약을\n저장하시겠습니까?\n','예  ','아니요'],
51:['기존 저장 데이터를\n덮어씁니다만,\n괜찮으시겠습니까?','예  ','아니요'],
52:['저장 중입니다...\n전원을 끄지\n마십시오...','저장에\n실패했습니다','다시 한번\n시도할까요?\n','예  ','아니요'],
53:['저장을\n완료했습니다'],
54:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없습니다','다시 한번\n시도할까요?\n','예  ','아니요'],
60:['지금까지의 활약을\n저장해 둘까?\n','예  ','아니요'],
61:['기존 저장 데이터를\n덮어쓰겠다...\n','예  ','아니요'],
62:['저장 중이다...\n전원을 끄지 마라','저장에\n실패한 듯하군...','다시 해 보겠다\n','예  ','아니요'],
63:['저장이 끝났다...'],
64:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없다','다시 해 보겠다\n','예  ','아니요'],
65:['지금까지의 활약을\n저장해 둘까?\n','예  ','아니요'],
66:['기존 저장 데이터를\n덮어쓸 건데,\n괜찮은가?','예  ','아니요'],
67:['저장 중이다...\n전원을 끄지 마라','저장에\n실패했다...','다시 한번\n해 볼까?\n','예  ','아니요'],
68:['...기뻐해라,\n저장이 끝났다'],
69:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없다','다시 한번\n해 볼까?\n','예  ','아니요'],
70:['지금까지의 활약을\n저장할까, 퓨?\n','예  ','아니요'],
71:['기존 저장 데이터를\n덮어쓸 거야, 퓨!\n괜찮아, 퓨?','예  ','아니요'],
72:['저장 중이야, 퓨!\n전원을 끄면\n안 돼, 퓨!','저장에\n실패했어, 퓨','다시 한번\n해 볼까, 퓨?\n','예  ','아니요'],
73:['저장이 끝났어, 퓨!'],
74:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없어, 퓨','다시 한번\n해 볼까, 퓨?\n','예  ','아니요'],
75:['지금까지의 활약을\n저장해 둘까?\n','예  ','아니요'],
76:['기존 저장 데이터를\n덮어쓰겠다...\n','예  ','아니요'],
77:['저장 중이다...\n전원을 끄지 마라...','저장에\n실패한 듯하군...','다시 해 보겠다\n','예  ','아니요'],
78:['저장이 끝났다...'],
79:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없다','다시 해 보겠다\n','예  ','아니요'],
80:['지금까지의 활약을\n저장해 둘까?\n','예  ','아니요'],
81:['기존 저장 데이터를\n덮어써 버릴 거야?\n','예  ','아니요'],
82:['지금 저장 중이니까,\n전원을 끄지 마','저장에\n실패한 것 같아...','다시 해 볼게\n','예  ','아니요'],
83:['저장 끝났어!'],
84:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없어','다시 해 볼게\n','예  ','아니요'],
85:['지금까지의 활약을\n저장해 둘까?\n','예  ','아니요'],
86:['기존 저장 데이터를\n덮어쓰겠다...\n','예  ','아니요'],
87:['저장 중이다...\n전원을 끄지 마라...','저장에\n실패한 듯하군...','다시 해 볼까\n','예  ','아니요'],
88:['저장이 끝났다...'],
89:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없군...','다시 해 볼까\n','예  ','아니요'],
90:['지금까지의 활약을\n저장하시겠습니까?\n','예  ','아니요'],
91:['기존 저장 데이터를\n덮어쓰게 됩니다만\n괜찮으시겠습니까?','예  ','아니요'],
92:['지금 저장 중입니다\n전원을 끄면\n안 됩니다','음! 저장에\n실패한 것 같습니다','다시 한번\n시도할까요?\n','예  ','아니요'],
93:['저장이 끝났습니다!'],
94:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없습니다','다시 한번\n시도할까요?\n','예  ','아니요'],
95:['지금까지의 활약을\n저장해 둘까!?\n','예  ','아니요'],
96:['기존 저장 데이터를\n덮어써 버릴 건데!?\n','예  ','아니요'],
97:['저장 중이야. 절대로\n전원 끄지 마!','저장에\n실패했군...','다시 한번\n해 볼까!?\n','예  ','아니요'],
98:['저장이 끝났다!'],
99:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없군','다시 한번\n해 볼까!?\n','예  ','아니요'],
100:['지금까지의 활약을\n저장할까요?\n','예  ','아니요'],
101:['기존 저장 데이터를\n덮어쓸 건데요,\n괜찮아요?','예  ','아니요'],
102:['지금 저장 중이에요!\n전원을 끄면\n안 돼요!','저장에\n실패했어요...','다시 한번\n해 볼게요!\n','예  ','아니요'],
103:['저장 끝났어요!'],
104:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없어요','다시 한번\n해 볼게요!\n','예  ','아니요'],
105:['지금까지의 활약을\n저장해 둘까?\n','예  ','아니요'],
106:['기존 저장 데이터를\n덮어쓰겠다...\n','예  ','아니요'],
107:['저장 중이다...\n전원을 끄지 마라...','저장에\n실패한 듯하군...','다시 해 볼까\n','예  ','아니요'],
108:['저장이 끝났다...'],
109:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없다','다시 해 볼까\n','예  ','아니요'],
110:['지금까지의 활약을\n저장해 둘까?\n','예  ','아니요'],
111:['기존 저장 데이터를\n덮어써 버릴 텐데?\n','예  ','아니요'],
112:['지금 저장 중이니까,\n전원을 끄면\n안 돼','저장에\n실패한 것 같군...','다시 해 볼게\n','예  ','아니요'],
113:['저장이 끝났어'],
114:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없는 것 같아','다시 해 볼게\n','예  ','아니요'],
115:['...흥,\n저장하려는 건가...\n','예  ','아니요'],
116:['기존 저장 데이터를\n덮어쓰겠다...\n','예  ','아니요'],
117:['저장 중이다...\n전원을 끄지 마라...','저장 실패다...\n다시 하겠나...\n','예  ','아니요'],
118:['저장이 끝났다...'],
119:['데이터가 부정하게\n변경되어 있어서\n저장할 수 없다','다시 하겠나...\n','예  ','아니요']
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA);original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    # Native script0 contains the actual speaker routing; do not infer by storage.
    for base,name in SPEAKERS.items():
        if f'jumpIf{name} = {base}' not in original:raise ValueError('speaker dispatch '+name)
    selected=[x for x in literals(original) if int(x.key.split(':')[1]) in DRAFT]
    if len(selected)!=271 or {x.key for x in selected}!={f'6DA21C:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('save271 population')
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);text=DRAFT[s][i]
        if x.language!='mmbn45' or x.text.count('\n')!=text.count('\n') or x.text.endswith('\n')!=text.endswith('\n'):raise ValueError('source rows '+x.key)
        if re.findall(r'\d+|\[[^\]]+\]',x.text)!=re.findall(r'\d+|\[[^\]]+\]',text):raise ValueError('tokens/numerals')
        units.append(dict(id=x.key,source=x.text,translation=text,state='needs_review',speaker=SPEAKERS[s-s%5],context=f'Native save flow {s-s%5}..{s-s%5+4}; row roles and commands in source TPL'))
    target=original;lookup={x.key:x for x in selected}
    for u in sorted(units,key=lambda u:lookup[u['id']].start,reverse=True):
        x=lookup[u['id']];target=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('protected commands')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x6DA21C)
    archive_sha=sha(payload_of((ROOT/cfg['source_profile']['filename']).read_bytes(),row))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='6DA21C',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=archive_sha,consumer='normal-dialogue',context='Native checkNaviAll source0 explicitly routes17 remaining speaker save flows. All 271 current unselected Japanese literals in this archive; existing69 selected literals/labels unchanged.',voice='Individual source-register drafts; AquaMan 퓨 candidate inherited from aquaman_seasonal_ko.json, IceMan gentle polite register. No new voice approval inferred.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; no ROM builder selection',protected_policy='Source IDs/controls/select defaults/retry/overwrite/power-off warning/invalid-data refusal retained. All source newline counts and trailing rows retained. No prose substitutions, save writes or ROM build.',semantic_review=['Wording and source voice need independent/human review before release. SearchMan completion exclamation 完了 translated as 완료!; original also has save-completed sentence.', 'JunkMan all-katakana robotic source needs presentation decision; Korean prose meaning drafted without claiming equivalent robotic typography.', 'Date/corruption/overwrite warnings remain distinct; drafting does not authorize save operations.'],units=units)

def main():
    a=create()
    # Use the established catalog payload hash, not an arbitrary guessed extent.
    require_hash(ROOT/'analysis/full_scope_save_initialize_v1/literal_backlog.json','5e0a63a4f6b3b2b996db74a453a91c8fb0c1ed43de310bd6f5ff2faa4ee22797')
    b=json.loads((ROOT/'analysis/full_scope_save_initialize_v1/literal_backlog.json').read_text(encoding='utf8'))
    hashes={u['source_payload_sha256'] for u in b['units'] if u['archive']=='6DA21C'}
    if len(hashes)!=1:raise ValueError('archive source hash')
    if a['source_archive_sha256']!=hashes.pop():raise ValueError('catalog/source payload mismatch')
    path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve authored translations; explicit edit required')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored save271 draft only; ROM unchanged')

if __name__=='__main__':main()
