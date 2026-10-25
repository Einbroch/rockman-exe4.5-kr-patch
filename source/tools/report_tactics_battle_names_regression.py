"""New prompt candidate:normal big-font card label regression."""
from pathlib import Path
import report_chip_battle_names_runtime as previous


def main():
    code = Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_battle_names_v1':'exe45_ko_development_tactics_prompts_v1',
        'battle-names-v1-normal-labels':'tactics-prompts-v1-normal-labels',
        'exe45_battle_names_normal_runtime_v1.json':'exe45_tactics_battle_names_regression_v1.json',
    }.items():
        if old not in code: raise ValueError('name regression anchor:'+old)
        code = code.replace(old,new)
    ns = {'__name__':'tactics_battle_names_regression'}
    exec(compile(code,previous.__file__+' [prompt candidate binding]','exec'),ns)
    ns['main']()


if __name__=='__main__':
    main()
