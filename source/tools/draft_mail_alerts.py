"""Manual mail alert drafts; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={'65B220':('48c88004829d329876e21e0dfd48c6ce392e6f3a36bbeebfbb81bf8feb15e301',14,'translations/mail_alerts_draft_ko.json')}
DRAFT={'65B220':{
1:['!!',',\n메일이야!!'],2:['!!',',\n메일이야!!'],3:['!!',',\n메일이야!!'],
4:['!!','메일이야!!'],5:['!!','메일이야!!'],6:['!!','메일이야!!'],7:['!!','메일이야!!'],
20:['!!','메일이야!!'],21:['!!','메일이야!!'],22:['!!','메일이야!!'],23:['!!','메일이야!!'],
24:['!!','메일이야!!'],25:['!!','메일이야!!'],26:['!!','메일이야!!'],
}}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v) if t!='!!'}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('reminder scope '+archive)
    units=[]
    for x in selected:
        s=int(x.key.split(':')[1]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('reminder topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('reminder tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',
            speaker='unshown-mail-alert-voice',
            origin_portrait=None,
            portrait_visibility='not-shown-in-script',
            context='Quick-box mail alerts scripts1..7 and20..26; tournament receive call in2 and distinct mail flags retained; no mugshot.',
            variable_context='Player nickname precedes comma in1..3, no Korean vocative particle added. Nickname width/repertoire/runtime remains unverified.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename']
    require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='mail-alerts',
        context='14 mail arrival literals; 14 punctuation alerts remain source; scripts1..3 insert nickname,4..7 clear mail event flags,20..26 add distinct mail flags.',
        voice='Plain friendly mail notice; no caller-derived speaker identity established, not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Preserve nickname/capitalization, flag3585, clear flags680/681/623..626, tournament receive call, add flags8904..8910, sound155 twice and wait96 twice, quick-box coordinates/waitHold, literal punctuation alerts.',
        semantic_review=[
            'Name plus comma preserves direct address without assuming name ending; no added vocative or actor identity.',
            'Tournament receipt in script2 is not reduced to notification-only behavior; original call and clear flag680 retained.',
            'Mail flags8904..8910 remain independent. Source contains no title or sender; none inferred.',
            'No live arrival/tournament/mail read flag/nickname rendering/quick-box screen/save verification; static draft only.'
        ],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve reminder draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
