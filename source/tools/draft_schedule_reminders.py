"""Manual schedule reminder drafts; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={'65AFA0':('c71c238d685ea57add2f5adbabbdbefc3e71fb3643a36bff0629757f790876d8',12,'translations/schedule_reminders_draft_ko.json')}
DRAFT={'65AFA0':{
1:[' 시작할\n시간이야!\nTV 앞으로 서두르자!'],
2:['\n약속 시간이야!\n기대되네!'],
3:['밥 먹을 시간이야!'],
4:['슬슬 학원에 갈\n시간이야!\n힘내자!!'],
5:['\n시간이야!'],
6:['그리고,'],
21:[' 시작할\n시간이야!\nTV 앞으로 서두르자!'],
22:['\n약속 시간이야!\n기대되네!'],
23:['밥 먹을 시간이야!'],
24:['슬슬 학원에 갈\n시간이야!\n힘내자!!'],
25:[' 시간이야!'],
26:['그리고,'],
}}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('reminder scope '+archive)
    units=[]
    for x in selected:
        s=int(x.key.split(':')[1]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('reminder topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('reminder tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',
            speaker='MegaMan' if s>=20 else 'unshown-reminder-voice',
            origin_portrait='MegaMan' if s>=20 else None,
            portrait_visibility='shown' if s>=20 else 'not-shown-in-script',
            context='Reminder routes1..6 positioned quick box and21..26 explicit MegaMan: TV, promise, meal, cram school, other, then additional event.',
            variable_context='TV/promise/other names precede the literal via printScheduleBuffer; avoid final-consonant-dependent particle. User schedule/name repertoire and screen demand remain unverified.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename']
    require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='schedule-reminders',
        context='12 Japanese reminder literals; alert0 punctuation remains source. Dispatch0/20 categorizes TV/promise/meal/school/other; scripts6/26 continue multiple events.',
        voice='Friendly plain reminder; MegaMan explicit only21..26, quick-box actor not established; not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Preserve schedule buffering/name insertion/capitalization, event dispatch/check branches, flags3585/3658, sounds155, waits96, quick-box coordinates, mugshots/end/waitHold and leading newline.',
        semantic_review=[
            'School event source explicitly says じゅく; drafted 학원 rather than regular school despite jumpIfSchool API name.',
            'Promise suffix 약속 시간이야 keeps reminder type and anticipation; other suffix 시간이야 avoids unsupported gender/name particle assumptions.',
            'TV title plus 시작할 시간 avoids fixed 이/가; space begins title suffix, original two newlines retained.',
            'Quick-box scripts1..6 have no mugshot. Matching explicit MegaMan scripts21..26 supports parallel function, not actor identity proof for quick-box.',
            'No alarm clock/event firing/multiple-event chain/schedule name rendering or runtime/save verification; layout and wording remain needs_review.'
        ],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve reminder draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
