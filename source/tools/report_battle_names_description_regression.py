"""Exact battle-name candidate:big Hangul labels then mono9x3 description."""
from pathlib import Path
import report_chip_mono_battle_v1 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_mono_batch01_v1':'exe45_ko_development_battle_names_v1',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch03_ko.json',
        'chip-mono-batch01-v1-battle-tactics-info':'battle-names-v1-tactics-info',
        'exe45_chip_mono_battle_runtime_v1.json':'exe45_battle_names_description_regression_v1.json',
        'not all30 battle scripts':'not all90 battle scripts', '129 drafts':'249 drafts',
        'battle chip names remain native Japanese outside current name scope':'separate name report covers normal MiniBomb and diagnostic90; other name consumers remain native',
    }.items():
        if old not in code: raise ValueError('missing cross-font battle anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'battle_names_description_regression'}
    exec(compile(code,previous.__file__+' [big-name to mono-description]','exec'),ns)
    ns['main']()


if __name__=='__main__': main()
