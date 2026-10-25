"""Exact311-unit normal battle/prompt checks; no prior result inheritance."""
import sys
from pathlib import Path
import report_chip_battle_names_runtime as names
import report_chip_mono_battle_v1 as description
import report_tactics_prompt_runtime as prompt


def main():
    mode=sys.argv.pop(1)
    if mode=='names':
        previous=names; replacements={
            'exe45_ko_development_battle_names_v1':'exe45_ko_development_chip_batch04_v1',
            'battle-names-v1-normal-labels':'chip-batch04-v1-normal-labels',
            'exe45_battle_names_normal_runtime_v1.json':'exe45_chip_batch04_battle_names_normal_v1.json',
            'not90 acquired':'not120 acquired',
        }
    elif mode=='description':
        previous=description;replacements={
            'exe45_ko_development_chip_mono_batch01_v1':'exe45_ko_development_chip_batch04_v1',
            'chip_descriptions_batch01_ko.json':'chip_descriptions_batch04_ko.json',
            'chip-mono-batch01-v1-battle-tactics-info':'chip-batch04-v1-tactics-info',
            'exe45_chip_mono_battle_runtime_v1.json':'exe45_chip_batch04_battle_description_v1.json',
            'not all30 battle scripts':'not all120 battle scripts','129 drafts':'311 drafts',
        }
    elif mode=='prompt':
        previous=prompt;replacements={'exe45_ko_development_tactics_prompts_v1':'exe45_ko_development_chip_batch04_v1'}
    else:raise ValueError('unknown311-unit report mode')
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in replacements.items():
        if old not in code:raise ValueError('battle path binding:'+old)
        code=code.replace(old,new)
    ns={'__name__':'batch04_'+mode}
    exec(compile(code,previous.__file__+' [311-unit '+mode+']','exec'),ns)
    ns['main']()


if __name__=='__main__':main()
