"""Exact189-unit normal battle MiniBomb binding; no old-ROM evidence reuse."""
from pathlib import Path
import report_chip_mono_battle_v1 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_mono_batch01_v1':'exe45_ko_development_chip_mono_batch02_v1',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch02_ko.json',
        'chip-mono-batch01-v1-battle-tactics-info':'chip-mono-batch02-v1-battle-tactics-info-r2',
        'exe45_chip_mono_battle_runtime_v1.json':'exe45_chip_mono_batch02_battle_minibomb_v1.json',
        'not all30 battle scripts':'not all60 battle scripts',
        '129 drafts':'189 drafts',
    }.items():
        if old not in code: raise ValueError('missing189-unit battle anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'batch02_battle_minibomb_bound'}
    exec(compile(code,previous.__file__+' [189-unit binding]','exec'),namespace)
    namespace['main']()


if __name__=='__main__': main()
