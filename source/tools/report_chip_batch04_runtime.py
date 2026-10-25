"""Exact311-unit ROM, protected120 descriptions, normal and diagnostic pixels."""
from pathlib import Path
import report_chip_mono_batch01_runtime as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    replacements={
        'exe45_ko_development_chip_mono_batch01_v1':'exe45_ko_development_chip_batch04_v1',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch04_ko.json',
        'chip-mono-batch01-v1-':'chip-batch04-v1-',
        'capture_chip_mono_batch.py':'capture_chip_mono_batch04.py',
        'exe45_chip_mono_batch01_runtime_v1.json':'exe45_chip_batch04_runtime_v1.json',
        'range(1,31)':'range(1,121)','==129':'==311','==226':'==136',
        "'draft_units':129":"'draft_units':311", "'description_units':30":"'description_units':120",
        "'new_description_units':27":"'new_description_units':30", "'unselected_description_scripts':226":"'unselected_description_scripts':136",
        'all30':'all120','protected30':'protected120','bounded30':'bounded120','prove30':'prove120',
    }
    for old,new in replacements.items():
        if old not in code:raise ValueError('311-unit report anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'batch04_runtime_bound'}
    exec(compile(code,previous.__file__+' [311 units]','exec'),ns)
    ns['main']()


if __name__=='__main__':main()
