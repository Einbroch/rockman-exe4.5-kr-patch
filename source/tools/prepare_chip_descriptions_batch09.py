"""Fill actual DarkChip descriptions195/196, reusing existing draft wording."""
import copy
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require
from tpl_literals import literals,resolve_units

def prepare():
    previous=ROOT/'translations/chip_descriptions_batch08_ko.json'
    asset=copy.deepcopy(read(previous))
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,asset['source_sha256'])
    baseline=ROOT/'analysis/tpl_baseline/76937C.tpl'
    texts={x.key:x.text for x in literals(baseline.read_text(encoding='utf-8-sig'))}
    old=resolve_units(asset);reference=next(x for x in asset['units'] if x['id']=='76937C:187:0')
    for i in (195,196):
        key=f'76937C:{i}:0'
        require(texts[key]==reference['source'],'DarkChip source differs')
        asset['units'].append({'id':key,'source':texts[key],'wording_id':reference['wording_id']})
    require(resolve_units(asset)[:249]==old,'prior249 changed')
    asset['scope_variant']='mono-descriptions-batch09'
    asset['context']='251 actual description literals:249 prior plus195/196 generic DarkChip descriptions. No invented names. Exact new-ROM runtime pending.'
    asset['protected_policy']='Preserve5 unselected scripts, source controls/line counts/numerals. Prior249 wordings retained;195/196 reuse existing identical-source draft wording.'
    asset['composition']={'tool_path':'tools/prepare_chip_descriptions_batch09.py','tool_sha256':sha((ROOT/'tools/prepare_chip_descriptions_batch09.py').read_bytes()),'prior_asset_sha256':sha(previous.read_bytes()),'new_units':2,'prior_units_preserved':249,'new_wordings':0,'reuse_wording':reference['wording_id']}
    return asset

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
