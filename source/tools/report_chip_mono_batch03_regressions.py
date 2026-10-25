"""Current249-unit normal routes only; no prior candidate result inheritance."""
from pathlib import Path
import report_chip_mono_batch02_regressions as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {'batch02':'batch03','189':'249','all60':'all90','prove60':'prove90'}.items():
        if old not in code: raise ValueError('missing regression anchor: '+old)
        code=code.replace(old,new)
    code=code.replace("'for step in (4,5)':'for step in (5,6)',",
                      "'chip-mono-batch03-v1-library-tabs':'chip-mono-batch03-v1-library-tabs-r2',\n        'for step in (4,5)':'for step in (5,6)',")
    code=code.replace("if part in ('input-lifetime','foreign-reentry')", "if part in ('library-tabs','input-lifetime','foreign-reentry')")
    ns={'__name__':'batch03_regressions_binding'}
    exec(compile(code,previous.__file__+' [249-unit binding]','exec'),ns)
    ns['main']()


if __name__=='__main__': main()
