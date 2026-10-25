"""Reuse strict regression assertions, explicitly bind the129-unit ROM/routes."""
from pathlib import Path
from build_visibility_poc import ROOT
import report_chip_mono_regressions as frozen
from report_chip_mono_cannon_runtime import mono_sentence


def main():
    code=Path(frozen.__file__).read_text(encoding='utf-8')
    substitutions={
        'exe45_ko_development_chip_mono_cannon_v2':'exe45_ko_development_chip_mono_batch01_v1',
        'chip-mono-cannon-v2-':'chip-mono-batch01-v1-',
        'chip_descriptions_cannon_poc_ko.json':'chip_descriptions_batch01_ko.json',
        'exe45_chip_mono_regressions_v2.json':'exe45_chip_mono_batch01_regressions_v1.json',
        '102 draft units':'129 draft units',
        'Cannon normal sentence only; other shared consumers and script2/3 pending':
        'Cannon normal regression route; separate all30 diagnostic pixels are not acquired normal play; shared consumers pending',
    }
    for old,new in substitutions.items(): code=code.replace(old,new)
    namespace={'__name__':'batch01_bound_regression'}
    exec(compile(code,frozen.__file__+' [129-unit binding]','exec'),namespace)
    def bound_sentence(*args,**kwargs):
        return mono_sentence(*args,**kwargs,rom_path=ROOT/'poc/output/exe45_ko_development_chip_mono_batch01_v1.gba')
    namespace['mono_sentence']=bound_sentence
    namespace['main']()


if __name__=='__main__': main()
