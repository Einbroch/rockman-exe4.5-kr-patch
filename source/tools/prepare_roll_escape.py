"""Serialize six authored Roll drafts, preserving prior eight units verbatim."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from tpl_literals import literals,resolve_units
from archive_scripts import script_spans

def prepare():
    project=json.loads((ROOT/'project.json').read_text());source=ROOT/project['source_profile']['filename']
    require_hash(source,project['source_profile']['sha256']);pool=source.read_bytes()[0x76C944:0x76C944+4473]
    prior_path=ROOT/'translations/megaman_tactics_escape_ko.json';prior=json.loads(prior_path.read_text(encoding='utf-8'))
    if sha(pool)!=prior['source_archive_sha256']:raise ValueError('source pool drift')
    seed_path=ROOT/'translations/roll_escape_draft_seed.json';seed=json.loads(seed_path.read_text(encoding='utf-8'))
    tpl_path=ROOT/'analysis/tpl_baseline/76C944.tpl';text={x.key:x.text for x in literals(tpl_path.read_text(encoding='utf-8-sig'))}
    expected=['76C944:8:0','76C944:8:1','76C944:8:2','76C944:9:3','76C944:10:3','76C944:11:0']
    if seed['policy']!=prior['policy'] or [d['id'] for d in seed['drafts']]!=expected:raise ValueError('draft scope drift')
    spans=script_spans(pool,144)
    return {'schema':1,'policy':prior['policy'],'source_sha256':project['source_profile']['sha256'],
        'archive':'76C944','source_archive_sha256':sha(pool),'consumer':'fixed-cell-mono','scope_variant':'rockman-roll-escape-v1',
        'review':{'wording':'needs_review','layout':'needs_runtime_review','release_eligible':False},'context':seed['context'],
        'provenance':{'prior_asset':str(prior_path.relative_to(ROOT)),'prior_sha256':sha(prior_path.read_bytes()),
            'seed':str(seed_path.relative_to(ROOT)),'seed_sha256':sha(seed_path.read_bytes()),'tpl_sha256':sha(tpl_path.read_bytes()),
            'tool_sha256':sha((ROOT/'tools/prepare_roll_escape.py').read_bytes()),
            'source_scripts':{str(i):{'raw_hex':spans[i].hex(),'sha256':sha(spans[i])} for i in [0,1,2,3,4,5,8,9,10,11]}},
        'units':resolve_units(prior)+[{'id':d['id'],'source':text[d['id']],'translation':d['translation'],'state':'needs_review'} for d in seed['drafts']]}

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
