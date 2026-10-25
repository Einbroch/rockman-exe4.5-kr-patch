"""Explicit120-script diagnostic binding, no progression or text-RAM writes."""
from pathlib import Path
import capture_chip_mono_batch03 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {'!=90':'!=120','protected90':'protected120','range(1,91)':'range(1,121)','%90+1':'%120+1','>=90':'>=120','1..90':'1..120','NOT 90 acquired':'NOT 120 acquired'}.items():
        if old not in code: raise ValueError('120-script binding:'+old)
        code=code.replace(old,new)
    ns={'__name__':'mono120_bound','__file__':__file__}
    exec(compile(code,previous.__file__+' [120 scripts]','exec'),ns)
    return ns['main']()


if __name__=='__main__':raise SystemExit(main())
