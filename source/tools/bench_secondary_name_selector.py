"""Cumulative selector CPU fixture including both full name pools."""
from pathlib import Path
import bench_chip_library as previous

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    changes={
        'selected_pool = 0x08000000 + ext["clone_offset"] if private else root':'selected_pool = 0x08000000 + ext["secondary_clone_offset" if root==0x08765B18 else "clone_offset"] if private else root',
        'secondary = script_spans(rom[0x765B18:0x765B18 + 1103], 137)':'secondary = script_spans(rom[ext["secondary_clone_offset"]:ext["secondary_clone_offset"]+ext["secondary_clone"]["clone_bytes"]],137)',
        'selector=(0x08765B18, index, False)':'selector=(0x08765B18, index, True)',
    }
    for old,new in changes.items():
        if old not in code:raise ValueError('secondary name CPU anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'secondary_selector','__file__':__file__}
    exec(compile(code,previous.__file__+' [both pools]','exec'),ns)
    ns['main']()

if __name__=='__main__':main()
