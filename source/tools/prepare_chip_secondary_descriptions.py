"""Source-pinned explicit75 secondary descriptions; stdout serialization only."""
import json
import re
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require
from tpl_literals import literals

def prepare():
    seed_path=ROOT/'translations/chip_secondary_descriptions_draft_seed.json';seed=read(seed_path)
    require(seed['policy']=='development-draft; NON-DISTRIBUTION' and seed['review']=='needs_review','draft policy')
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256'])
    raw=source.read_bytes()[0x76BC60:0x76BC60+3255]
    tpl_path=ROOT/'analysis/tpl_baseline/76BC60.tpl';items=literals(tpl_path.read_text(encoding='utf-8-sig'))
    require([e['script'] for e in seed['entries']]==[int(x.key.split(':')[1]) for x in items],'exact75 source denominator')
    artifact={'schema':2,'policy':seed['policy'],'archive':'76BC60','source_sha256':profile['sha256'],'source_archive_sha256':sha(raw),
              'consumer':'fixed-cell-mono','context':'Secondary chip/PA descriptions. Source113 slots75 literals. Three rows and nine visible cells adopted; secondary native consumer runtime pending.',
              'review':{'wording':'needs_review','layout':'needs_runtime_review','release_eligible':False},
              'protected_policy':'Preserve original controls, source line counts/numeric order,38 nonliteral scripts. No authored chip names or source-slot filling.',
              'terminology_review':seed['terminology_review'],'extraction':{'path':'analysis/tpl_baseline/76BC60.tpl','sha256':sha(tpl_path.read_bytes())},'wordings':[],'units':[]}
    texts={x.key:x.text for x in items}
    for e in seed['entries']:
        i=e['script'];key=f'76BC60:{i}:0';text=e['description'];original=texts[key]
        require(all(1<=len(line)<=9 for line in text.split('\n')) and text.count('\n')==original.count('\n'),'source rows/adopted width')
        require(re.findall(r'\d+',text)==re.findall(r'\d+',original),'protected numerals')
        w=f'chip.secondary.desc.{i}'
        artifact['units'].append({'id':key,'source':original,'wording_id':w})
        artifact['wordings'].append({'id':w,'translation':text,'state':'needs_review'})
    artifact['composition']={'seed_path':'translations/chip_secondary_descriptions_draft_seed.json','seed_sha256':sha(seed_path.read_bytes()),'tool_path':'tools/prepare_chip_secondary_descriptions.py','tool_sha256':sha((ROOT/'tools/prepare_chip_secondary_descriptions.py').read_bytes()),'new_units':len(seed['entries'])}
    return artifact

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
