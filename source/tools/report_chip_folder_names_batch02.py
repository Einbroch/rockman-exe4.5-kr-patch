"""Exact189-unit clone and all60 name held-page glyph pixels."""
from pathlib import Path
from build_visibility_poc import require_hash
import report_chip_folder_names_batch as previous


def main():
    path=Path(previous.__file__);require_hash(path,'e459ce07e2577f307692c0439337d17d1c406f9433c4ea59059850d7a4d02bfc')
    code=path.read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_folder_v3':'exe45_ko_development_chip_mono_batch02_v1',
        'library_chip_names_batch01_ko.json':'library_chip_names_batch02_ko.json',
        'range(1,31)':'range(1,61)',
        '==226':'==196',
        'chip-folder-v3-all30-stable':'chip-mono-batch02-v1-names-all60',
        'capture_chip_folder_names_batch.py':'capture_chip_folder_names_batch02.py',
        'for step in (15,16,17)':'for step in range(9,18)',
        '(start+row)%30+1':'(start+row)%60+1',
        'exe45_chip_folder_names_batch_v3.json':'exe45_chip_folder_names_batch02_v1.json',
        '30-name':'60-name',
        'not 30 acquired':'not 60 acquired',
        "out=ROOT/'analysis/":"require({name for page in pages.values() for name in page.values()}==set(names.values()),'all60 stable name pixel coverage')\n    out=ROOT/'analysis/",
    }.items():
        if old not in code: raise ValueError('missing60-name report anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'names60_report_bound'}
    exec(compile(code,str(path)+' [189-unit binding]','exec'),namespace)
    namespace['main']()


if __name__=='__main__': main()
