"""Serialize new121..150 explicit drafts, preserve all prior120 prose."""
import json
from pathlib import Path
import prepare_chip_batch02_assets as previous


def prepare():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'chip_batch02_draft_seed.json':'chip_batch05_draft_seed.json',
        'range(31,61)':'range(121,151)',
        'library_chip_names_batch01_ko.json':'library_chip_names_batch04_ko.json',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch04_ko.json',
        '[:30]':'[:120]','First60':'First150','First30':'First120',
        'first30':'first120','Prior30':'Prior120','196':'106',
        'batch01 prose/source/state':'batch04 prose/source/state',
        'library.chip.batch02.':'library.chip.batch05.','desc.batch02.':'desc.batch05.',
        'batch02_exact_common_candidates':'batch05_exact_common_candidates',
        'mono-descriptions-batch02':'mono-descriptions-batch05',
        'New60-scope':'New150-scope',
        'prepare_chip_batch02_assets.py':'prepare_chip_batch05_assets.py',
        "'prior_units_preserved':30":"'prior_units_preserved':120",
        'Battle names and other consumers remain native.':'Opt-in battle clone follows this exact scope; other consumers remain native.',
    }.items():
        if old not in code:raise ValueError('150-unit composition anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'batch05_composition'}
    exec(compile(code,previous.__file__+' [explicit30 prior120]','exec'),ns)
    return ns['prepare']()


if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
