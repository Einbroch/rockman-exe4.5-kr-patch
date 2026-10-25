"""Actual native8x1 name parser/copy with selected clone; CPU fixture only."""
from pathlib import Path
import bench_chip_mono_parser as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    replacements={
        "mono=f['mono_provider']":"mono=f",
        "record=next(a for a in m['translation_assets'] if a['archive']=='76937C')":"record=next(a for a in m['translation_assets'] if a['archive']=='765190')",
        "ar=next(r for r in m['archives'] if r['archive']=='76937C');base=ar['rom_offset']":"ar=m['chip_battle_name_extension'];base=ar['clone_offset']",
        '0x08619EF8':'0x08612E38','0x619EF8':'0x612E38',
        'count not in (1728,1920)':'count not in (512,)',
        'for width in (9,10)':'for width in (8,)',
        'width*3*64':'width*64', 'width,3,':'width,1,',
        "lines+['']*(3-len(lines))":"lines+['']*(1-len(lines))",
        "'rows':3":"'rows':1", '9x3/10x3':'8x1', 'at9x3 and10x3':'at8x1',
        'bench_chip_mono_parser.py':'bench_chip_battle_name_parser.py',
        'shared pointer2165C/D2B58 runtime still required':'all90 normal battle selections and other name consumers still unverified',
    }
    for old,new in replacements.items():
        if old not in code: raise ValueError('missing8x1 name fixture anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'battle_name_parser_bound'}
    exec(compile(code,previous.__file__+' [native8x1 name binding]','exec'),ns)
    ns['main']()


if __name__=='__main__': main()
