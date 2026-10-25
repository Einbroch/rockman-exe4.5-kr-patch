"""Explicit sparse draft: prior194 plus actual scripts201..255; no ROM build."""
import json
from pathlib import Path
import prepare_chip_batch02_assets as previous

def prepare():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    changes={
        'chip_batch02_draft_seed.json':'chip_batch08_draft_seed.json',
        'range(31,61)':'range(201,256)',
        'library_chip_names_batch01_ko.json':'library_chip_names_batch07_ko.json',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch07_ko.json',
        '[:30]':'[:194]', 'First60':'Sparse249', 'First30':'Prior194',
        'first30':'prior194', 'Prior30':'Prior194', '196':'7',
        'batch01 prose/source/state':'batch07 prose/source/state',
        'library.chip.batch02.':'library.chip.batch08.', 'desc.batch02.':'desc.batch08.',
        'batch02_exact_common_candidates':'batch08_exact_common_candidates',
        'mono-descriptions-batch02':'mono-descriptions-batch08',
        'New60-scope exact-ROM runtime required.':'Sparse draft only; contiguous battle helper integration and exact-ROM runtime pending.',
        'prepare_chip_batch02_assets.py':'prepare_chip_batch08_assets.py',
        "'prior_units_preserved':30":"'prior_units_preserved':194",
        "'new_units':30":"'new_units':55",
    }
    for old,new in changes.items():
        if old not in code: raise ValueError('sparse composition anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'batch08_composition'}
    exec(compile(code,previous.__file__+' [sparse55 prior194]','exec'),ns)
    return ns['prepare']()

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--part',choices=['names','descriptions'])
    args=parser.parse_args();result=prepare()
    print(json.dumps(result[args.part] if args.part else result,ensure_ascii=False,indent=2))
