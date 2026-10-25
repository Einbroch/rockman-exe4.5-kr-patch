"""Bind current-ROM normal selection to observed script4, never predicted slots."""
from pathlib import Path
import report_chip_mono_battle_v1 as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    replacements={
        'exe45_ko_development_chip_mono_batch01_v1':'exe45_ko_development_chip_mono_batch02_v1',
        'chip_descriptions_batch01_ko.json':'chip_descriptions_batch02_ko.json',
        'chip-mono-batch01-v1-battle-tactics-info':'chip-mono-batch02-v1-battle-vulcan-wide-info',
        'exe45_chip_mono_battle_runtime_v1.json':'exe45_chip_mono_batch02_battle_hicannon_v1.json',
        '==29)':'==4)', '+29*2':'+4*2', "'script':29":"'script':4",
        "parents=read(p/'final_mono_parents.json')['calls']":"parents=[c for c in read(p/'final_mono_parents.json')['calls'] if c['stream']==stream]",
        'len(parents)==3':'len(parents)==2', 'for step in (2,3,4)':'for step in (3,5)',
        'on3 held screens':'on2 held screens', 'MiniBomb':'HiCannon',
        'not all30 battle scripts':'not all60 battle scripts', '129 drafts':'189 drafts',
        'colors={};x,y=objects[0]':"calibration=next(i for i,(font,index) in enumerate(glyphs) if font==0x08619EF8 and set(v for row in unpack_pixels(expected[i]) for v in row)=={1,3,4});colors={};x,y=objects[calibration]",
        'unpack_pixels(expected[0])':'unpack_pixels(expected[calibration])',
        'Native source ASCII3':'Native source glyph', 'native ASCII3 calibrates':'native source glyph calibrates',
    }
    for old,new in replacements.items():
        if old not in code: raise ValueError('missing battle binding anchor: '+old)
        code=code.replace(old,new)
    namespace={'__name__':'batch02_battle_hicannon_bound'}
    exec(compile(code,previous.__file__+' [189-unit observed script4]','exec'),namespace)
    namespace['main']()


if __name__=='__main__': main()
