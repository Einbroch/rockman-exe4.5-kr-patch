"""Exact189-unit binding of normal titles/names/mono/foreign reentry checks."""
from pathlib import Path
from build_visibility_poc import ROOT
import report_chip_mono_regressions as previous
from report_chip_mono_cannon_runtime import mono_sentence


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_chip_mono_cannon_v2':'exe45_ko_development_chip_mono_batch02_v1',
        'chip-mono-cannon-v2-':'chip-mono-batch02-v1-',
        'chip-mono-batch02-v1-input-lifetime':'chip-mono-batch02-v1-input-lifetime-r2',
        'chip-mono-batch02-v1-foreign-reentry':'chip-mono-batch02-v1-foreign-reentry-r2',
        "ROOT/f'poc/runtime/chip-mono-batch02-v1-{part}'":"ROOT/(f'poc/runtime/chip-mono-batch02-v1-{part}' + ('-r2' if part in ('input-lifetime','foreign-reentry') else ''))",
        'for step in (4,5)':'for step in (5,6)',
        'chip_descriptions_cannon_poc_ko.json':'chip_descriptions_batch02_ko.json',
        'exe45_chip_mono_regressions_v2.json':'exe45_chip_mono_batch02_regressions_v1.json',
        '102 draft units':'189 draft units',
        'Cannon normal sentence only; other shared consumers and script2/3 pending':'Cannon normal regression; separate all60 diagnostic pixels do not prove60 acquired play; battle/shared-root runtime pending on this189-unit hash',
    }.items():
        if old not in code: raise ValueError('missing189-unit regression anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'batch02_regression_bound'}
    exec(compile(code,previous.__file__+' [189-unit binding]','exec'),namespace)
    def bound_sentence(*args,**kwargs): return mono_sentence(*args,**kwargs,rom_path=ROOT/'poc/output/exe45_ko_development_chip_mono_batch02_v1.gba')
    namespace['mono_sentence']=bound_sentence;namespace['main']()


if __name__=='__main__': main()
