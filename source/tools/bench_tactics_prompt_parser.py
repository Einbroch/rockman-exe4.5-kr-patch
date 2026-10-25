"""Actual5x2 mono parser fixture for two TACTICS drafts; bounded CPU only."""
from pathlib import Path
import bench_chip_mono_parser as previous


def main():
    code = Path(previous.__file__).read_text(encoding='utf-8')
    replacements = {
        "a['archive']=='76937C'": "a['archive']=='76C944'",
        "r['archive']=='76937C'": "r['archive']=='76C944'",
        'count not in (1728,1920)': 'count not in (640,)',
        'for width in (9,10)': 'for width in (5,)',
        'width*3*64': 'width*2*64', 'width,3,': 'width,2,',
        "lines+['']*(3-len(lines))": "lines+['']*(2-len(lines))",
        "'rows':3": "'rows':2", '9x3/10x3': '5x2',
        'at9x3 and10x3': 'at5x2',
        'bench_chip_mono_parser.py': 'bench_tactics_prompt_parser.py',
        'shared pointer2165C/D2B58 runtime still required': 'TACTICS question pixels and other Navi voices remain unverified',
    }
    for old, new in replacements.items():
        if old not in code:
            raise ValueError('missing5x2 fixture anchor: '+old)
        code = code.replace(old, new)
    ns = {'__name__':'tactics_parser_bound'}
    exec(compile(code, previous.__file__+' [5x2 mono binding]', 'exec'), ns)
    ns['main']()


if __name__ == '__main__':
    main()
