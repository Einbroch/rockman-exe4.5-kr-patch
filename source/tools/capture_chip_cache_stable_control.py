"""Same entry/input and alternating icons; only fixed-name reuse is retained."""
import json
from pathlib import Path
import capture_chip_cache_matrix as cache
from capture_chip_wait_trace import TRACE
from build_visibility_poc import sha


def main():
    matrix = cache.word.matrix
    fixture = matrix.FIXTURE
    fixture = matrix.replace_once(fixture, 'local stressDesc=nil', 'local stressDesc=nil\nlocal stressEpoch=0')
    fixture = matrix.replace_once(fixture, 'stressDesc=timingGroup.descriptor', 'stressEpoch=stressEpoch+1\n stressDesc=timingGroup.descriptor')
    fixture = matrix.replace_once(fixture, 'local off=(address-stressDesc)%4',
        'local off=(address-stressDesc)%4\n if pc==0x0804302C and off==3 and stressEpoch%2==0 then stressReads=stressReads+1;return 0 end')
    matrix.FIXTURE = fixture
    matrix.PROBE += TRACE
    rc = cache.main()
    out = Path(matrix.library.fixed.value('--out'))
    scope = 'DIAGNOSTIC fixed 56 glyphs with alternating 7/0 icons; same-state control for changing names'
    r = json.loads((out / 'result.json').read_text())
    r['scope'] = scope
    (out / 'result.json').write_text(json.dumps(r, indent=2), encoding='utf-8')
    (out / 'stable_control_environment.json').write_text(json.dumps({
        'tool_sha256': sha(Path(__file__).read_bytes()), 'scope': scope,
        'trace_sha256': sha(TRACE.encode())}, indent=2), encoding='utf-8')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
