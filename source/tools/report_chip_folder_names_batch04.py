"""Exact311-unit clone, all120 held name masks; diagnostic only."""
from pathlib import Path
import report_chip_folder_names_batch as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_folder_v3':'exe45_ko_development_chip_batch04_v1',
        'library_chip_names_batch01_ko.json':'library_chip_names_batch04_ko.json',
        'range(1,31)':'range(1,121)','==226':'==136',
        'chip-folder-v3-all30-stable':'chip-batch04-v1-names-all120',
        'capture_chip_folder_names_batch.py':'capture_chip_folder_names_batch04.py',
        'for step in (15,16,17)':'for step in range(9,27)',
        '(start+row)%30+1':'(start+row)%120+1',
        'exe45_chip_folder_names_batch_v3.json':'exe45_chip_folder_names_batch04_v1.json',
        '30-name':'120-name','not 30 acquired':'not 120 acquired',
        "out=ROOT/'analysis/":"require({name for page in pages.values() for name in page.values()}==set(names.values()),'all120 stable name masks')\n    out=ROOT/'analysis/",
    }.items():
        if old not in code:raise ValueError('120-name report:'+old)
        code=code.replace(old,new)
    ns={'__name__':'names120_report'}
    exec(compile(code,previous.__file__+' [120 names]','exec'),ns)
    ns['main']()


if __name__=='__main__':main()
