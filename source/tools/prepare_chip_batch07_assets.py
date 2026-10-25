"""Serialize14 explicit pairs181..194; preserve prior180 verbatim."""
import json
from pathlib import Path
import prepare_chip_batch02_assets as previous


def prepare():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'chip_batch02_draft_seed.json':'chip_batch07_draft_seed.json',
        'range(31,61)':'range(181,195)',
        'library_chip_names_batch01_ko.json':'library_chip_names_batch06_ko.json',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch06_ko.json',
        '[:30]':'[:180]','First60':'First194','First30':'First180',
        'first30':'first180','Prior30':'Prior180','196':'62',
        'batch01 prose/source/state':'batch06 prose/source/state',
        'library.chip.batch02.':'library.chip.batch07.','desc.batch02.':'desc.batch07.',
        'batch02_exact_common_candidates':'batch07_exact_common_candidates',
        'mono-descriptions-batch02':'mono-descriptions-batch07',
        'New60-scope':'New194-scope',
        'prepare_chip_batch02_assets.py':'prepare_chip_batch07_assets.py',
        "'prior_units_preserved':30":"'prior_units_preserved':180",
        "'new_units':30":"'new_units':14",
        'Battle names and other consumers remain native.':'Opt-in battle clone follows this exact scope; other consumers remain native.',
    }.items():
        if old not in code:raise ValueError('194-unit composition anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'batch07_composition'}
    exec(compile(code,previous.__file__+' [explicit14 prior180]','exec'),ns)
    return ns['prepare']()


if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
