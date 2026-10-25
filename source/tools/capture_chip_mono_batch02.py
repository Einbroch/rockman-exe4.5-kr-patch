"""Explicit 60-script binding of the pinned 30-script diagnostic observer."""
from pathlib import Path
from build_visibility_poc import require_hash
import capture_chip_mono_batch as previous


def main():
    path=Path(previous.__file__);require_hash(path,'1e729d00aab12d06c580ff6982918cf21c30247987141aaf63c364837f069f65')
    code=path.read_text(encoding='utf-8')
    for old,new in {
        "r['translated_units']!=30":"r['translated_units']!=60",
        'protected30':'protected60',
        'range(1,31)':'range(1,61)',
        '%30+1':'%60+1',
        "d['reads']>=30":"d['reads']>=60",
        '1..30':'1..60',
        'NOT 30 acquired':'NOT 60 acquired',
    }.items():
        if old not in code: raise ValueError('missing60-script anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'mono60_bound','__file__':__file__}
    exec(compile(code,str(path)+' [protected60 binding]','exec'),namespace)
    return namespace['main']()


if __name__=='__main__': raise SystemExit(main())
