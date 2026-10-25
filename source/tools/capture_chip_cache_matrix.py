"""Diagnostic 56-cell fixture with cache hits allowed, pixels still checked."""
import json
from pathlib import Path
import capture_chip_wordcopy_matrix as word
from build_visibility_poc import sha


def main():
    fixed = word.matrix.library.fixed
    rom = Path(fixed.value('--rom'))
    m = json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'))
    if m['chip_library_extension'].get('cache', {}).get('tags') != 0x06008E40:
        raise ValueError('cache candidate required')
    word.matrix.PROBE = word.matrix.replace_once(word.matrix.PROBE,
        "if not c then error('copy return without entry') end", 'if not c then return end')
    # The frozen fixture independently compares every row's 56 glyphs to ROM,
    # including hits, after selector return. Do not equate hit with unchecked.
    hangul = fixed.value('--hangul')
    rc = word.main()
    out = Path(fixed.value('--out'))
    d = json.loads((out / 'final_timing.json').read_text())
    s = json.loads((out / 'final_stress.json').read_text())
    valid = rc == 0 and len(d['groups']) > 100 and s['verified_rows'] == len(d['groups']) * 7
    if hangul == '56':
        # With a fixed fixture and no tab changes, all subsequent copies must hit.
        valid = valid and d['groups'][0]['copies'] == 56 and all(g['copies'] == 0 for g in d['groups'][1:])
    if not valid:
        r = json.loads((out / 'result.json').read_text())
        r['complete'] = False
        (out / 'result.json').write_text(json.dumps(r, indent=2), encoding='utf-8')
    (out / 'cache_matrix_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'scope': 'diagnostic fixed cells, first fill and repeat hits; no changing-name timing claim', 'passed': valid}, indent=2), encoding='utf-8')
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
