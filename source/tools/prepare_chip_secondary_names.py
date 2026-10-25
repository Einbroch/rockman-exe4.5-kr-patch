"""Serialize explicit secondary-pool name drafts; never mutate ROM or source."""
import json
import re
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require
from tpl_literals import literals
from archive_scripts import script_spans

def prepare():
    seed_path=ROOT/'translations/chip_secondary_names_draft_seed.json'
    seed=read(seed_path)
    require(seed['policy']=='development-draft; NON-DISTRIBUTION' and seed['review']=='needs_review','draft policy')
    source_hash='588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8'
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,source_hash)
    raw=source.read_bytes()[0x765B18:0x765B18+1103]
    spans=script_spans(raw,137)
    tpl_path=ROOT/'analysis/tpl_baseline/765B18.tpl'
    tpl=tpl_path.read_text(encoding='utf-8-sig');items=literals(tpl)
    expected=[int(x.key.split(':')[1]) for x in items if x.text.strip() and x.text!='????']
    require([e['script'] for e in seed['entries']]==expected,'exact real-text denominator')
    reference_path=ROOT/'../록맨 에그제 3/translations/chip_names_ko.json'
    require_hash(reference_path,'f2b4625131f08d4844fdcf7fbe38ef87d7ebea29b6bfe8d17398e3428ca1a4ae')
    ref=read(reference_path);source_text={x.key:x.text for x in items}
    artifact={'schema':2,'policy':seed['policy'],'source_sha256':source_hash,'archive':'765B18',
              'source_archive_sha256':sha(raw),'source_bytes':1103,'script_count':137,
              'extraction':{'path':'analysis/tpl_baseline/765B18.tpl','sha256':sha(tpl_path.read_bytes())},
              'consumer':'secondary-chip-name-pool; reinsertion pending',
              'context':'Name-only development drafts; eight-cell adopted range, actual secondary consumers need integration/runtime evidence.',
              'review':{'wording':'needs_review','layout':'needs_runtime_review','release_eligible':False},
              'protected_policy':'Keep script count/order, terminal controls, source raw bytes, numeric suffixes, blank and ???? slots; no ROM writes.',
              'reference':{'path':'../록맨 에그제 3/translations/chip_names_ko.json','sha256':sha(reference_path.read_bytes()),'exact_common_candidates':[]},
              'terminology_review':seed['terminology_review'],'units':[],'wordings':[],'source_script_hex':{}}
    for e in seed['entries']:
        i=e['script'];key=f'765B18:{i}:0';name=e['name'];text=source_text[key]
        require(1<=len(name)<=8,'eight-cell adopted range')
        require(re.findall(r'\d+',name)==re.findall(r'\d+',text),'numeric suffix changed')
        for suffix in ('SP','DS'):
            require(text.endswith(suffix)==name.endswith(suffix),'Navi suffix changed')
        if text in ref:
            artifact['reference']['exact_common_candidates'].append({'script':i,'source':text,'candidate':ref[text],'draft':name,'state':'needs_review'})
        wording=f'chip.secondary.names.{i}'
        artifact['units'].append({'id':key,'source':text,'wording_id':wording})
        artifact['wordings'].append({'id':wording,'translation':name,'state':'needs_review'})
        artifact['source_script_hex'][str(i)]=spans[i].hex()
    artifact['composition']={'seed_path':'translations/chip_secondary_names_draft_seed.json','seed_sha256':sha(seed_path.read_bytes()),'tool_path':'tools/prepare_chip_secondary_names.py','tool_sha256':sha((ROOT/'tools/prepare_chip_secondary_names.py').read_bytes()),'new_units':len(seed['entries'])}
    return artifact

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
