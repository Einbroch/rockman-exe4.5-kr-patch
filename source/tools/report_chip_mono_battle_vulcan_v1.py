"""Bind strict 9x3 battle checks to normal Vulcan1, not synthetic selection."""
from pathlib import Path
import report_chip_mono_battle_v1 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        "==29)":"==15)",
        "+29*2":"+15*2",
        "'script':29":"'script':15",
        'chip-mono-batch01-v1-battle-tactics-info':'chip-mono-batch01-v1-battle-airshot-info',
        "parents=read(p/'final_mono_parents.json')['calls']":"parents=[c for c in read(p/'final_mono_parents.json')['calls'] if c['stream']==stream]",
        'len(parents)==3':'len(parents)==2',
        'for step in (2,3,4)':'for step in (3,5)',
        'on3 held screens':'on2 held screens',
        'exe45_chip_mono_battle_runtime_v1.json':'exe45_chip_mono_battle_vulcan_runtime_v1.json',
        'MiniBomb':'Vulcan1',
    }.items():
        if old not in code: raise ValueError('missing Vulcan binding anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'battle_vulcan_bound'}
    exec(compile(code,previous.__file__+' [normal Vulcan1 binding]','exec'),namespace)
    namespace['main']()


if __name__=='__main__': main()
