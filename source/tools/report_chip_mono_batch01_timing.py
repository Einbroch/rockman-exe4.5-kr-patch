"""Strict exact-ROM workload and caller checks for the 129-unit candidate."""
from pathlib import Path
import report_chip_mono_timing_v2 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_mono_cannon_v2':'exe45_ko_development_chip_mono_batch01_v1',
        'chip-mono-cannon-v2-changing56':'chip-mono-batch01-v1-folder-changing',
        'chip-mono-cannon-v2-{part}-parent':'chip-mono-batch01-v1-{part}-parent-entry',
        'chip-mono-cannon-v2-':'chip-mono-batch01-v1-',
        'exe45_chip_mono_timing_v2.json':'exe45_chip_mono_batch01_timing_v1.json',
        '102 drafts':'129 drafts',
    }.items():
        if old not in code: raise ValueError('missing timing binding anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'batch01_timing_bound'}
    exec(compile(code,previous.__file__+' [129-unit binding]','exec'),namespace)
    namespace['main']()


if __name__=='__main__': main()
