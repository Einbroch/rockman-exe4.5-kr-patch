"""Exact311-unit120-name battle BG/font/pixel evidence, not acquisition."""
from pathlib import Path
import report_chip_battle_names_all90 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'exe45_ko_development_battle_names_v1':'exe45_ko_development_chip_batch04_v1',
        'battle-names-v1-all90':'chip-batch04-v1-battle-names-all120-r2',
        'capture_chip_battle_names_all90.py':'capture_chip_batch04_battle_names_all120.py',
        'range(1,91)':'range(1,121)','==720':'==960','range(1,31)':'range(1,41)',
        '90name':'120name','90/90':'120/120',
        'no90-chip':'no120-chip',"'calls':720":"'calls':960",
        'exe45_battle_names_all90_runtime_v1.json':'exe45_chip_batch04_battle_names_all120_v1.json',
        'all90 actual':'all120 actual','on30 held':'on40 held',
        'report_chip_battle_names_all90.py':'report_chip_batch04_battle_names_all120.py',
    }.items():
        if old not in code:raise ValueError('120-name report anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'battle120_report'}
    exec(compile(code,previous.__file__+' [311-unit120 names]','exec'),ns)
    ns['main']()


if __name__=='__main__':main()
