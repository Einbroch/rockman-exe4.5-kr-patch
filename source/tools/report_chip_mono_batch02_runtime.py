"""Exact 189-unit ROM binding of source/control/normal/all-script pixel checks."""
from pathlib import Path
from build_visibility_poc import require_hash
import report_chip_mono_batch01_runtime as previous


def main():
    path=Path(previous.__file__);require_hash(path,'0168f03618c16ac63bcd471b9c44ba0ddfb9f0d82ba970bfb6a40717d91c6d93')
    code=path.read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_mono_batch01_v1':'exe45_ko_development_chip_mono_batch02_v1',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch02_ko.json',
        'chip-mono-batch01-v1-':'chip-mono-batch02-v1-',
        'capture_chip_mono_batch.py':'capture_chip_mono_batch02.py',
        'exe45_chip_mono_batch01_runtime_v1.json':'exe45_chip_mono_batch02_runtime_v1.json',
        'range(1,31)':'range(1,61)',
        '==129':'==189',
        '==226':'==196',
        "'draft_units':129":"'draft_units':189",
        "'description_units':30":"'description_units':60",
        "'new_description_units':27":"'new_description_units':30",
        "'unselected_description_scripts':226":"'unselected_description_scripts':196",
        'all30':'all60',
        'protected30':'protected60',
        'bounded30':'bounded60',
        'prove30':'prove60',
    }.items():
        if old not in code: raise ValueError('missing189-unit anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'mono60_runtime_bound'}
    exec(compile(code,str(path)+' [189-unit binding]','exec'),namespace)
    namespace['main']()


if __name__=='__main__': main()
