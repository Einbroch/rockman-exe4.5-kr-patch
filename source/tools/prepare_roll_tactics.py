"""Link two new Roll source units to unchanged authored question decisions."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from tpl_literals import literals,resolve_units
from archive_scripts import script_spans

def prepare():
    project=json.loads((ROOT/'project.json').read_text());source=ROOT/project['source_profile']['filename']
    require_hash(source,project['source_profile']['sha256']);pool=source.read_bytes()[0x76C944:0x76C944+4473]
    prior_path=ROOT/'translations/rockman_roll_escape_ko.json';prior=json.loads(prior_path.read_text(encoding='utf-8'))
    prompts_path=ROOT/'translations/megaman_tactics_prompts_ko.json';prompts=json.loads(prompts_path.read_text(encoding='utf-8'))
    if sha(pool)!=prior['source_archive_sha256'] or sha(pool)!=prompts['source_archive_sha256']:raise ValueError('source pool drift')
    links_path=ROOT/'translations/roll_tactics_wording_links.json';links=json.loads(links_path.read_text(encoding='utf-8'))
    if links['policy']!=prior['policy'] or [(d['id'],d['wording_id']) for d in links['selections']]!=[('76C944:6:0','tactics.target'),('76C944:7:0','tactics.distance')]:raise ValueError('scope/decision drift')
    tpl_path=ROOT/'analysis/tpl_baseline/76C944.tpl';text={x.key:x.text for x in literals(tpl_path.read_text(encoding='utf-8-sig'))}
    prior_units=resolve_units(prior);wordings=prompts['wordings'].copy();units=prompts['units'].copy()
    if resolve_units(prompts)!=prior_units[:2]:raise ValueError('prior question wording drift')
    for u in prior_units[2:]:
        wid='carry.'+u['id'];wordings.append({'id':wid,'translation':u['translation'],'state':u['state']})
        units.append({'id':u['id'],'source':u['source'],'wording_id':wid})
    units.extend({'id':d['id'],'source':text[d['id']],'wording_id':d['wording_id']} for d in links['selections'])
    spans=script_spans(pool,144)
    return {'schema':2,'policy':prior['policy'],'source_sha256':project['source_profile']['sha256'],
        'archive':'76C944','source_archive_sha256':sha(pool),'consumer':'fixed-cell-mono','scope_variant':'rockman-roll-tactics-escape-v1',
        'review':{'wording':'needs_review','layout':'needs_runtime_review','release_eligible':False},'context':links['context'],
        'provenance':{'prior_asset':str(prior_path.relative_to(ROOT)),'prior_sha256':sha(prior_path.read_bytes()),
            'prompt_wordings':str(prompts_path.relative_to(ROOT)),'prompt_wordings_sha256':sha(prompts_path.read_bytes()),
            'selections':str(links_path.relative_to(ROOT)),'selections_sha256':sha(links_path.read_bytes()),'tpl_sha256':sha(tpl_path.read_bytes()),
            'tool_sha256':sha((ROOT/'tools/prepare_roll_tactics.py').read_bytes()),
            'source_scripts':{str(i):{'raw_hex':spans[i].hex(),'sha256':sha(spans[i])} for i in range(12)}},
        'wordings':wordings,'units':units}

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
