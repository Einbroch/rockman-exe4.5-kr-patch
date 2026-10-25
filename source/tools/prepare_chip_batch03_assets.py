"""Compose source61..90 explicit drafts, retaining the previous60 verbatim."""
import json
from pathlib import Path
import prepare_chip_batch02_assets as previous


def prepare():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    replacements={
        'chip_batch02_draft_seed.json':'chip_batch03_draft_seed.json',
        'range(31,61)':'range(61,91)',
        'library_chip_names_batch01_ko.json':'library_chip_names_batch02_ko.json',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch02_ko.json',
        "[:30]":"[:60]", 'First60':'First90', 'First30':'First60',
        'first30':'first60', 'Prior30':'Prior60',
        '196':'166', 'batch01 prose/source/state':'batch02 prose/source/state',
        'library.chip.batch02.':'library.chip.batch03.', 'desc.batch02.':'desc.batch03.',
        'batch02_exact_common_candidates':'batch03_exact_common_candidates',
        'mono-descriptions-batch02':'mono-descriptions-batch03',
        'New60-scope':'New90-scope',
        'prepare_chip_batch02_assets.py':'prepare_chip_batch03_assets.py',
        "'prior_units_preserved':30":"'prior_units_preserved':60",
    }
    for old,new in replacements.items():
        if old not in code: raise ValueError('missing composition anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'batch03_composition'}
    exec(compile(code,previous.__file__+' [new30 prior60 binding]','exec'),ns)
    return ns['prepare']()


if __name__=='__main__': print(json.dumps(prepare(),ensure_ascii=False,indent=2))
