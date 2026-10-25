"""Exact189-unit workloads and observed normal library/folder caller binding."""
from pathlib import Path
import report_chip_mono_timing_v2 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_mono_cannon_v2':'exe45_ko_development_chip_mono_batch02_v1',
        'chip-mono-cannon-v2-changing56':'chip-mono-batch02-v1-folder-changing',
        'chip-mono-cannon-v2-{part}-parent':'chip-mono-batch02-v1-{part}-parent-entry',
        'chip-mono-cannon-v2-':'chip-mono-batch02-v1-',
        'exe45_chip_mono_timing_v2.json':'exe45_chip_mono_batch02_timing_v1.json',
        '102 drafts':'189 drafts',
        '6de509d736812dab55b6828088c750496e701bf2690763ba14f65f519a4536b6':'91dc85912d2d1e945a866bf187775e1903302be408c58cde0a9debc7bcdc0110',
    }.items():
        if old not in code: raise ValueError('missing189-unit timing anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'batch02_timing_bound'}
    exec(compile(code,previous.__file__+' [189-unit binding]','exec'),namespace)
    namespace['main']()


if __name__=='__main__': main()
