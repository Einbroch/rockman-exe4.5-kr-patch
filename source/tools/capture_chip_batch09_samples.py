"""17 representative compiled descriptions via quarantined CPU-read aliases."""
from pathlib import Path
import capture_chip_mono_batch as previous

SCRIPTS=[121,123,150,180,194,195,196,201,202,205,218,220,227,236,242,251,255]

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    replacements={"r['translated_units']!=30":"r['translated_units']!=251",
                  'protected30':'protected251', 'range(1,31)':repr(SCRIPTS),
                  '%30+1':'%17+1', "d['reads']>=30":"d['reads']>=17",
                  '1..30':'representative17-of251', 'NOT 30 acquired':'NOT 17 acquired'}
    for old,new in replacements.items():
        if old not in code:raise ValueError('sample binding anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'batch09_samples','__file__':__file__}
    exec(compile(code,previous.__file__+' [17 samples of251]','exec'),ns)
    return ns['main']()

if __name__=='__main__':raise SystemExit(main())
