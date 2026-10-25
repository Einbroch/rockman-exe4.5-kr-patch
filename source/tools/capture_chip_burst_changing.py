"""Run the retained changing workload against the 6+6+4 burst candidate."""
import json
from pathlib import Path
import capture_chip_cache_changing as changing
from build_visibility_poc import require_hash, sha


def burst_main():
    matrix = changing.word.matrix
    fixed = matrix.library.fixed
    rom = Path(fixed.value('--rom')).resolve()
    m = json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'))
    require_hash(rom, m['output_sha256'])
    e = m['chip_library_extension']
    if e.get('copy_variant') != '6+6+4':
        raise ValueError('burst candidate required')
    loads = [i for i in e['machine_code'][0]['instructions'] if i['mnemonic'] in ('ldm', 'ldmia')]
    if len(loads) != 3 or [i['operands'] for i in loads] != ['r0!, {r2, r3, r4, r5, r6, r7}'] * 2 + ['r0!, {r2, r3, r4, r5}']:
        raise ValueError('burst boundaries changed')
    matrix.PROBE = matrix.replace_once(matrix.PROBE, '0x08000956,0x08000956', f"{loads[0]['address']},{loads[0]['address']}")
    matrix.PROBE = matrix.replace_once(matrix.PROBE, "c['cpu.r2']~=64 or ", '')
    rc = matrix.main()
    out = Path(fixed.value('--out'))
    (out / 'burst_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'scope': 'actual 6+6+4 inline transfers; diagnostic changing names'}, indent=2), encoding='utf-8')
    return rc


if __name__ == '__main__':
    changing.word.main = burst_main
    raise SystemExit(changing.main())
