"""Bind native save/reboot assertions to the exact 129-unit candidate."""
from pathlib import Path
from build_visibility_poc import ROOT
import report_chip_mono_save_v2 as previous
from report_chip_mono_cannon_runtime import mono_sentence


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_mono_cannon_v2':'exe45_ko_development_chip_mono_batch01_v1',
        'chip-mono-cannon-v2-':'chip-mono-batch01-v1-',
        'chip_descriptions_cannon_poc_ko.json':'chip_descriptions_batch01_ko.json',
        'exe45_chip_mono_save_v2.json':'exe45_chip_mono_batch01_save_v1.json',
        '102 drafts':'129 drafts',
    }.items():
        if old not in code: raise ValueError('missing save binding anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'batch01_save_bound'}
    exec(compile(code,previous.__file__+' [129-unit binding]','exec'),namespace)
    def bound_sentence(*args,**kwargs):
        return mono_sentence(*args,**kwargs,rom_path=ROOT/'poc/output/exe45_ko_development_chip_mono_batch01_v1.gba')
    namespace['mono_sentence']=bound_sentence
    namespace['main']()


if __name__=='__main__': main()
