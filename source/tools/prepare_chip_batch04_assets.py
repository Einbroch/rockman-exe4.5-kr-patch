"""Serialize explicit91..120 drafts; never transform prior90 prose."""
import json
from pathlib import Path
import prepare_chip_batch02_assets as previous


def prepare():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    replacements={
        'chip_batch02_draft_seed.json':'chip_batch04_draft_seed.json',
        'range(31,61)':'range(91,121)',
        'library_chip_names_batch01_ko.json':'library_chip_names_batch03_ko.json',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch03_ko.json',
        '[:30]':'[:90]', 'First60':'First120', 'First30':'First90',
        'first30':'first90', 'Prior30':'Prior90', '196':'136',
        'batch01 prose/source/state':'batch03 prose/source/state',
        'library.chip.batch02.':'library.chip.batch04.', 'desc.batch02.':'desc.batch04.',
        'batch02_exact_common_candidates':'batch04_exact_common_candidates',
        'mono-descriptions-batch02':'mono-descriptions-batch04',
        'New60-scope':'New120-scope',
        'prepare_chip_batch02_assets.py':'prepare_chip_batch04_assets.py',
        "'prior_units_preserved':30":"'prior_units_preserved':90",
        'Battle names and other consumers remain native.':'Opt-in battle clone selector follows this exact scope; other name consumers remain native.',
    }
    for old,new in replacements.items():
        if old not in code: raise ValueError('composition anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'batch04_composition'}
    exec(compile(code,previous.__file__+' [prior90 plus explicit30]','exec'),ns)
    return ns['prepare']()


if __name__=='__main__': print(json.dumps(prepare(),ensure_ascii=False,indent=2))
