"""Explicit90-script binding of the preserved30-script diagnostic observer."""
from pathlib import Path
from build_visibility_poc import require_hash
import capture_chip_mono_batch as previous


def main():
    path=Path(previous.__file__);require_hash(path,'1e729d00aab12d06c580ff6982918cf21c30247987141aaf63c364837f069f65')
    code=path.read_text(encoding='utf-8')
    for old,new in {
        "r['translated_units']!=30":"r['translated_units']!=90",
        'protected30':'protected90', 'range(1,31)':'range(1,91)',
        '%30+1':'%90+1', "d['reads']>=30":"d['reads']>=90",
        '1..30':'1..90', 'NOT 30 acquired':'NOT 90 acquired',
    }.items():
        if old not in code: raise ValueError('missing90-script anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'mono90_bound','__file__':__file__}
    exec(compile(code,str(path)+' [protected90 binding]','exec'),ns)
    return ns['main']()


if __name__=='__main__': raise SystemExit(main())
