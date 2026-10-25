"""Manual128 profile data manager candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7CC6A0':('a36af431705b6dc48ad0798cc9fa1096c494a4143f4c5ca28d7e6d6e4952355c',128,'translations/profile_data_manager_draft_ko.json'),
}
DRAFT={
'7CC6A0':{
0:['저는,\n',' 님의','학교나 직장\n정보를 관리하는\n프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
1:['저는,\n',' 님의','형·오빠의 이름을\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
2:['저는,\n',' 님의','남동생의 이름을\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
3:['저는,\n',' 님의','누나·언니의 이름을\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
4:['저는,\n',' 님의','여동생의 이름을\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
5:['저는,\n',' 님의','친구의 이름을\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
6:['저는,\n',' 님의','좋아하는 음식 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
7:['저는,\n',' 님의','취미 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
8:['저는,\n',' 님의','장래 희망 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
9:['저는,\n',' 님의','좋아하는 사람 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
10:['저는,\n',' 님의','존경하는 사람 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
11:['저는,\n',' 님의','불편한 사람 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
12:['저는,\n',' 님의','좋아하는 TV 프로그램 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
13:['저는,\n',' 님의','잘하는 과목 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
14:['저는,\n',' 님의','어려운 과목 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
15:['저는,\n',' 님의','갖고 싶은 것 정보를\n관리하는 프로그램입니다','현재 기록된\n데이터를 수정하시겠습니까?\n','예 ','아니요'],
20:['수정할 항목을\n선택해 주세요'],
21:['수정할 항목을\n선택해 주세요'],
22:[None,'」에 대해...\n','수정 ','삭제\n','아무것도 안 함'],
23:[None,'」에 대해\n수정하시겠습니까?\n','예 ','아니요'],
24:[None,'」에 대해\n삭제하시겠습니까?\n','예 ','아니요'],
25:[None,'」에 대해\n삭제했습니다'],
75:['유치원'],
76:['형·오빠'],
77:['남동생'],
78:['누나·언니'],
79:['여동생'],
80:['친구'],
81:['좋아하는 음식'],
82:['취미'],
83:['꿈'],
84:['좋아하는 사람'],
85:['존경하는 사람'],
86:['불편한 사람'],
87:['TV 프로그램'],
88:['잘하는 과목'],
89:['어려운 과목'],
90:['갖고 싶은 것'],
91:['학교'],
92:['회사'],
95:['그러시군요...'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v) if t is not None}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('laserman scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        label=75<=s<=92
        if not shown and not label:raise ValueError('actor missing '+x.key)
        portrait=shown[-1] if shown else None;visibility='visible' if shown else 'not-shown-in-script'
        choice=(s<=15 and i in (4,5)) or (s==22 and i in (2,3,4)) or (s in (23,24) and i in (2,3))
        speaker='player-choice' if choice else 'profile-field-label' if label else portrait
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('laserman topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('laserman tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,consumer_status="unresolved-profile-label-consumer" if label else "profile-edit-dialogue-candidate",origin_portrait=portrait,portrait_visibility=visibility,context='Profile data manager introductions0..15, selection/edit/delete20..25 and labels75..92; complete archive read.',variable_context='Player name between0/1 in intros, buffer printString index0 in22..25. 님의 and quoted-item 에 대해 avoid final-consonant dependent particles; composed width/persistence unverified.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='profile-data-manager-dialogue-and-unresolved-labels',context='All128 Japanese literals, including18 mmbn45s labels with unverified consumers; no profile data/save modification.',voice='Polite MrProgGreen; neutral field labels and player choices; candidates not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep16 printPlayerName boundaries, buffered printString index0, all dynamic printSchool..printWish3 commands, selection width7/11, targets/default/cancel/waitHold, trailing spaces/newlines.',semantic_review=['Sibling wording 형·오빠/누나·언니 avoids player-gender inference. Name suffix 님의 preserved without ending-dependent particle.', 'Buffered user string kept between original opening quote and authored closing suffix 에 대해; actual composed width remains unverified.', 'ニガテなヒト drafted 불편한 사람, not necessarily hated person; source スキなヒト drafted 좋아하는 사람, no opposite-sex restriction inferred. Existing7B67C8 candidates differ and require human terminology reconciliation, not automatic overwrite.', '18 labels75..92 have literal meanings drafted but no proven rendering consumer. No label is integration-ready solely because translated.', 'School/work introduction and kindergarten/school/company labels preserved separately. No occupation or school level selected by translator.', 'Selection words edit/delete/do-nothing and confirmation/result are distinct; no default/targets/width/delete action changes.', 'No actual profile opening/editing/deletion/Hangul input/commit/save/reload/runtime screen verification. Static checks not human or runtime approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve laserman draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
