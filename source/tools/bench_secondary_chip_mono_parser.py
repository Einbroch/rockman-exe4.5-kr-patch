"""Native CPU parser fixture for all75 secondary descriptions, not runtime proof."""
from pathlib import Path
import bench_chip_mono_parser as previous

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {'76937C':'76BC60','bench_chip_mono_parser.py':'bench_secondary_chip_mono_parser.py'}.items():
        if old not in code:raise ValueError('secondary CPU binding:'+old)
        code=code.replace(old,new)
    ns={'__name__':'secondary_mono_fixture'}
    exec(compile(code,previous.__file__+' [secondary75]','exec'),ns)
    ns['main']()

if __name__=='__main__':main()
