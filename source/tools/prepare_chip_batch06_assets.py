"""Serialize explicit151..180 drafts; no prior150 prose edits."""
import json
from pathlib import Path
import prepare_chip_batch05_assets as previous


def prepare():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    replacements={
        'chip_batch05_draft_seed.json':'chip_batch06_draft_seed.json',
        'range(121,151)':'range(151,181)',
        'library_chip_names_batch04_ko.json':'library_chip_names_batch05_ko.json',
        'chip_descriptions_batch04_ko.json':'chip_descriptions_batch05_ko.json',
        '[:120]':'[:150]','First150':'First180','First120':'First150',
        'first120':'first150','Prior120':'Prior150',"'106'":"'76'",
        'batch04 prose/source/state':'batch05 prose/source/state',
        'library.chip.batch05.':'library.chip.batch06.','desc.batch05.':'desc.batch06.',
        'batch05_exact_common_candidates':'batch06_exact_common_candidates',
        'mono-descriptions-batch05':'mono-descriptions-batch06',
        'New150-scope':'New180-scope',
        'prepare_chip_batch05_assets.py':'prepare_chip_batch06_assets.py',
        "'prior_units_preserved':120":"'prior_units_preserved':150",
    }
    for old,new in replacements.items():
        if old not in code:raise ValueError('180-unit composition anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'batch06_composition'}
    exec(compile(code,previous.__file__+' [explicit30 prior150]','exec'),ns)
    return ns['prepare']()


if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
