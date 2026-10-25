"""New prompt candidate:5x2 TACTICS to9x3 chip-info cross-font regression."""
from pathlib import Path
import report_battle_names_description_regression as previous


def main():
    code = Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_battle_names_v1':'exe45_ko_development_tactics_prompts_v1',
        'battle-names-v1-tactics-info':'tactics-prompts-v1-tactics-info',
        'exe45_battle_names_description_regression_v1.json':'exe45_tactics_description_regression_v1.json',
        '249 drafts':'251 drafts',
        'big-name to mono-description':'TACTICS prompt to mono-description',
    }.items():
        if old not in code: raise ValueError('prompt regression anchor:'+old)
        code = code.replace(old,new)
    ns = {'__name__':'tactics_description_regression'}
    exec(compile(code,previous.__file__+' [prompt candidate binding]','exec'),ns)
    ns['main']()


if __name__=='__main__':
    main()
