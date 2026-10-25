"""249-unit exact ROM normal battle source29/9x3 binding."""
from pathlib import Path
import report_chip_mono_batch02_battle_minibomb as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {'batch02':'batch03','all60':'all90','189 drafts':'249 drafts','189-unit':'249-unit'}.items():
        if old not in code: raise ValueError('missing battle anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'batch03_battle_binding'}
    exec(compile(code,previous.__file__+' [249-unit binding]','exec'),ns)
    ns['main']()


if __name__=='__main__': main()
