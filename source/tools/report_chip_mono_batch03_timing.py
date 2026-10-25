"""Exact249-unit workloads and same-ROM native consumer callers."""
from pathlib import Path
import report_chip_mono_batch02_timing as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {'batch02':'batch03','189':'249'}.items():
        if old not in code: raise ValueError('missing timing anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'batch03_timing_binding'}
    exec(compile(code,previous.__file__+' [249-unit binding]','exec'),ns)
    ns['main']()


if __name__=='__main__': main()
