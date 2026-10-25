"""120 names/40 held pages/960 calls, read-only diagnostic aliases."""
from pathlib import Path
import capture_chip_battle_names_all90 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {'%90+1':'%120+1','==720':'==960','1..90':'1..120','not90 acquired':'not120 acquired'}.items():
        if old not in code:raise ValueError('120-name alias anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'battle120_alias','__file__':__file__}
    exec(compile(code,previous.__file__+' [120-name diagnostic]','exec'),ns)
    return ns['main']()


if __name__=='__main__':raise SystemExit(main())
