"""Adapt the frozen factorial observer to actual inline word-copy boundaries."""
import json
from pathlib import Path
import capture_chip_library_matrix as matrix
from build_visibility_poc import require_hash, sha


def main():
    require_hash(Path(matrix.__file__), 'fefaf53bef8e1fac62a1619d29a34f65076b6fb46dda293f4b19587933ef45c4')
    fixed = matrix.library.fixed
    rom = Path(fixed.value('--rom')).resolve()
    m = json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'))
    require_hash(rom, m['output_sha256'])
    e = m['chip_library_extension']
    if e.get('copy_policy') != 'experimental-inline-16-words':
        raise ValueError('word-copy candidate required')
    loads = [i for i in e['machine_code'][0]['instructions'] if i['mnemonic'] in ('ldm', 'ldmia')]
    if len(loads) != 8:
        raise ValueError('word-copy boundaries changed')
    matrix.PROBE = matrix.replace_once(matrix.PROBE,
        '0x08000956,0x08000956', f"{loads[0]['address']},{loads[0]['address']}")
    matrix.PROBE = matrix.replace_once(matrix.PROBE, "c['cpu.r2']~=64 or ", '')
    matrix.PROBE = matrix.PROBE.replace('real BIOS pixel-copy', 'real inline word pixel-copy')
    rc = matrix.main()
    out = Path(fixed.value('--out')).resolve()
    (out / 'wordcopy_matrix_environment.json').write_text(json.dumps({
        'tool_sha256': sha(Path(__file__).read_bytes()), 'matrix_tool_sha256': sha(Path(matrix.__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'copy_entry': loads[0]['address'],
        'scope': 'DIAGNOSTIC read substitutions; actual LDM/STM, not BIOS glyph copies; not normal play'}, indent=2), encoding='utf-8')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
