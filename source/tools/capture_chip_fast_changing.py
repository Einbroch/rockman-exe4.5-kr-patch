"""Changing 56-cell test with the original SWI-0C wrapper actually executed."""
import json
from pathlib import Path
import capture_chip_cache_changing as changing
from build_visibility_poc import require_hash, sha


def fast_main():
    matrix = changing.word.matrix
    fixed = matrix.library.fixed
    rom = Path(fixed.value('--rom')).resolve()
    m = json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'))
    require_hash(rom, m['output_sha256'])
    e = m['chip_library_extension']
    if e.get('copy_policy') != 'experimental-native-fast-bios-16-words' or e['machine_code'][0]['literal_values']['copy_helper'] != 0x0800097D:
        raise ValueError('native fast-copy candidate required')
    matrix.PROBE = matrix.replace_once(matrix.PROBE, '0x08000956,0x08000956', '0x0800097C,0x0800097C')
    rc = matrix.main()
    out = Path(fixed.value('--out'))
    (out / 'fast_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'scope': 'actual native SWI-0C wrapper and BIOS; diagnostic changing names'}, indent=2), encoding='utf-8')
    return rc


if __name__ == '__main__':
    changing.word.main = fast_main
    raise SystemExit(changing.main())
