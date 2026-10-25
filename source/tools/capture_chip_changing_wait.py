"""Keep changing workload fixed while observing the first native wait cycles."""
import json
from pathlib import Path
import capture_chip_cache_changing as changing
from capture_chip_wait_trace import TRACE
from build_visibility_poc import ROOT, require_hash, sha


def main():
    fixed = changing.word.matrix.library.fixed
    rom = Path(fixed.value('--rom'))
    config = json.loads((ROOT / 'project.json').read_text(encoding='utf-8'))
    source = ROOT / config['source_profile']['filename']
    require_hash(source, config['source_profile']['sha256'])
    data = rom.read_bytes()
    if data[0x244:0x388] != source.read_bytes()[0x244:0x388]:
        raise ValueError('native main-loop scope changed')
    changing.word.matrix.PROBE += TRACE
    rc = changing.main()
    out = Path(fixed.value('--out'))
    (out / 'changing_wait_environment.json').write_text(json.dumps({
        'tool_sha256': sha(Path(__file__).read_bytes()),
        'trace_sha256': sha(TRACE.encode()),
        'main_loop_sha256': sha(data[0x244:0x388]),
        'scope': 'read-only wait events; changing read-substitution workload remains diagnostic'
    }, indent=2), encoding='utf-8')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
