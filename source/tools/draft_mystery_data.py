"""Individually authored mystery-data90; variable-bound fragments, draft only."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/778CC0.tpl'
SOURCE_SHA='323446b9e727ab21188093e9fb2d0d6dad091e2fbe58638c80a51273b319d317'
OUT='translations/mystery_data_draft_ko.json'
# Explicit per-entry drafting; None protects the source-only opening quote18:0.
DRAFT={
0:[',\n미스터리 데이터\n조사했다.','.','.'],
3:['서브 칩\n「','」\n효과 발휘!!',', 배틀 칩\n「','」\n획득!!'],
6:[',\n미스터리 데이터\n조사했다.','.','.'],
7:['잠겨 있다!\n열려면, 「','」\n필요'],
9:[', 배틀 칩\n「','」\n획득!!'],
10:[',\n미스터리 데이터\n조사했다.','.','.'],
13:['서브 칩\n「','」\n효과 발휘!!',', 서브 칩\n「','」\n획득!!'],
16:[',\n미스터리 데이터\n조사했다.','.','.'],
18:[None,'」\n소지 한도라 더 못 가진다'],
19:[', 서브 칩\n「','」\n획득!!'],
20:[',\n미스터리 데이터\n조사했다.','.','.'],
23:['서브 칩\n「','」\n효과 발휘!!',',\n「','제니」\n획득!!'],
26:[',\n미스터리 데이터\n조사했다.','.','.'],
29:[',\n「','제니」\n획득!!'],
30:[',\n미스터리 데이터\n조사했다.','.','.'],
33:['서브 칩\n「','」\n효과 발휘!!',',\n「','」\n획득!!'],
36:[',\n미스터리 데이터\n조사했다.','.','.'],
39:[',\n「','」\n획득!!'],
40:[',\n미스터리 데이터\n조사했다.','.','.'],
43:['서브 칩\n「','」\n효과 발휘!!',',\n「버그 조각」\n총 ','개 획득!!'],
46:[',\n미스터리 데이터\n조사했다.','.','.'],
48:['「버그 조각」은\n소지 한도라 더 못 가진다'],
49:[',\n「버그 조각」\n총 ','개 획득!!'],
56:[',\n미스터리 데이터\n조사했다.','.','.','서브 칩\n「','」\n효과 발휘!!','미스터리 데이터에\n숨어 있던 바이러스 데이터가\n삭제되었다!'],
59:['놀랍게도 미스터리 데이터는\n바이러스였다!!'],
66:[',\n미스터리 데이터\n조사했다.','.','.','서브 칩\n「','」\n효과 발휘!!','미스터리 데이터에\n숨어 있던 바이러스 데이터가\n삭제되었다!'],
69:['놀랍게도 미스터리 데이터는\n바이러스였다!!'],
70:[',\n미스터리 데이터\n조사했다.','.','.'],
73:['서브 칩\n「','」\n효과 발휘!!',', 강화 프로그램\n「','」\n획득!!'],
76:[',\n미스터리 데이터\n조사했다.','.','.'],
79:[', 강화 프로그램\n「','」\n획득!!']
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA);original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    if not all(t in original for t in ('printCurrentNavi','printChip','printItem','printBuffer','callEnableMysteryDataBufferCheck','flag = 7690','flag = 7691','startRandomBattle','jumpIfNone = 18','jumpIfNone = 48')):raise ValueError('mystery context changed')
    values={f'778CC0:{s}:{i}':t for s,rows in DRAFT.items() for i,t in enumerate(rows) if t is not None}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=90 or set(values)!={x.key for x in selected}:raise ValueError('mystery90 scope '+str(set(values)^{x.key for x in selected}))
    units=[]
    for x in selected:
        t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('source row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('source numbers/tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='system-mystery-data',context='Native mystery data search/reward, locked item44 requirement, capacity refusal, item42 trap-removal vs random battle, and chip/subchip/zenny/item/bugfrag/program branches',variable_context='printCurrentNavi/printItem/printChip/printBuffer order and numeric IDs unchanged; comma and noun-form labels avoid variable-final-consonant particles. Invariant 버그 조각은 is a fixed literal, not a variable. Real name/amount budgets pending.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x778CC0)
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='778CC0',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-system',context='All90 unselected Japanese literals in80-slot mystery-data archive. Payload/TPL pinned; native reward, scene/object animation, trap and capacity branches preserved. Source-only quote18:0 kept unselected.',voice='Concise source-backed system narration; 미스터리 데이터/서브 칩/제니/버그 조각 candidates inherited from existing keyitem and mission assets. All entries manually authored, not a bulk source-string replacement.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve source IDs, variables/amount/padding, flags7690/7691, scene/object animation, timed10-frame literal boundaries, unlock requirement, capacity refusal and trap battle transitions. No gameplay/ROM/save writes.',semantic_review=['Name-independent noun-form investigation/acquisition avoids 은/는/이/가 selection from variable names. Final wording/presentation human review pending.', 'Search wording 조사했다 preserves source past tense and separate timed dots; later result branches express discovered reward/trap. Command timing is not modified or asserted runtime verified.', 'Item44 key requirement and item42 trap suppression remain separate; dynamic item names are not hardcoded guesses.', 'Trap-free branches56/66 keep 바이러스 데이터 삭제, while59/69 keep 바이러스였다 and native battle command. No safety outcome falsely promised.', 'Capacity failure18/48 is not acquisition; source-only quote remains protected. All consumer variable combinations and actual screens unverified.'],units=units)

def main():
    a=create();path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored mystery-data90 draft only; ROM unchanged')

if __name__=='__main__':main()
