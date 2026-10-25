"""Real clone names1..120 via diagnostic CPU-read aliases only."""
from pathlib import Path
import capture_chip_folder_names_batch03 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {'%90+1':'%120+1','range(1,91)':'range(1,121)','1..90':'1..120'}.items():
        if old not in code:raise ValueError('120-name binding:'+old)
        code=code.replace(old,new)
    ns={'__name__':'names120_bound','__file__':__file__}
    exec(compile(code,previous.__file__+' [120 names]','exec'),ns)
    return ns['main']()


if __name__=='__main__':raise SystemExit(main())
