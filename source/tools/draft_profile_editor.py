"""Source-bound profile dialogue candidates; no keyboard hook or ROM mutation."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

DRAFT={
16:['저는,\n',' 님의','개인정보를\n관리하는 프로그램입니다','이름이나 직업\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
17:['그럼, 설정 화면을\n열겠습니다'],
20:['학교명? 회사명?\n입력 전'],
21:['형·오빠 이름\n입력 전'],
22:['남동생 이름\n입력 전'],
23:['누나·언니 이름\n입력 전'],
24:['여동생 이름\n입력 전'],
25:['친구 이름\n입력 전'],
26:['좋아하는 음식\n입력 전'],
27:['취미\n입력 전'],
28:['장래 희망\n입력 전'],
29:['좋아하는 이성\n입력 전'],
30:['존경하는 사람\n입력 전'],
31:['싫어하는 사람\n입력 전'],
32:['좋아하는 TV\n입력 전'],
33:['잘하는 과목\n입력 전'],
34:['어려운 과목\n입력 전'],
35:['갖고 싶은 것\n입력 전'],
40:['그러시군요...'],
}
OUT='translations/profile_editor_draft_ko.json'

def create():
    archive='7B67C8';source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    digest='c0586d04b0d9a46fde65a0ad2f01db2be30cdc12b62afcc7fd85c150d34eaccd'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT.items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=24 or set(values)!={x.key for x in selected}:raise ValueError('profile scope')
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('profile topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('profile tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if s==16 and i in (4,5) else 'MrProgGreen',origin_portrait='MrProgGreen',portrait_visibility='visible',context='Profile administrator and edit acceptance/refusal; scripts20..35 are source input-before labels, not proven normal runtime dialogue.',variable_context='Script16 printPlayerName splits literals0/1. Name-dependent total line width and Korean keyboard persistence remain unverified.',consumer_status='unresolved-input-before-label' if 20<=s<=35 else 'dialogue-candidate'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='profile-dialogue-and-unresolved-input-before-labels',context='All24 Japanese literals; scripts0..15 global21/flags512/7701 retained, script17 startProfileEdit and script16 targets17/40 unchanged.',voice='Polite MrProgGreen; profile labels remain neutral candidates.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve names, variable/control boundaries, profile/save behavior, option single trailing space and source question marks. No runtime reachability claim for input-before labels.',semantic_review=['Script16 source has player-name suffix サマ の. Korean split uses name + 님의 without assuming a name-ending particle; actual composed width pending.', 'Source アニ/アネ does not identify player gender. 형·오빠 and 누나·언니 are explicit candidate alternatives, not a gender inference; sibling wording needs human review.', 'Scripts20..35 literal meaning is translated, but input-before labels may be internal placeholders. Their consumer remains unresolved and they are not silently excluded or integration-ready.', 'TV remains TV, school/company question marks remain uncertain alternatives; no broadcast title, employment setting or user data invented.', 'Text translation does not implement Hangul composition, commit, save/reload or prove profile edit runtime.'],units=units)

def main():
    a=create();p=ROOT/OUT
    if p.exists():
        if json.loads(p.read_text(encoding='utf8'))!=a:raise ValueError('preserve profile candidate')
    else:p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored profile24; unresolved consumers retained; ROM unchanged')

if __name__=='__main__':main()
