"""249-unit artifact /90name held-page pixel checks, no prior results reused."""
from pathlib import Path
import report_chip_folder_names_batch02 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'batch02':'batch03', 'range(1,61)':'range(1,91)', '==196':'==166',
        'all60':'all90', 'range(9,18)':'range(9,22)', '%60+1':'%90+1',
        '60-name':'90-name', 'not 60 acquired':'not 90 acquired',
        'names60_report_bound':'names90_report_bound', '189-unit':'249-unit',
    }.items():
        if old not in code: raise ValueError('missing90-name report anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'batch03_name_report_binding'}
    exec(compile(code,previous.__file__+' [90-name binding]','exec'),ns)
    ns['main']()


if __name__=='__main__': main()
