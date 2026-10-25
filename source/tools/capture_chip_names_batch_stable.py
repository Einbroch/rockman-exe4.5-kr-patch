"""Hold each diagnostic seven-name page 30 updates for scanout inspection."""
import json
from pathlib import Path
import capture_chip_names_batch as batch
from build_visibility_poc import sha


def main():
    fixed = batch.normal.variant.cache.word.base.library.fixed
    original = batch.normal.main

    def held_main():
        old = '(batchEpoch-1)*7'
        if fixed.PROBE.count(old) != 1:
            raise ValueError('batch index anchor drift')
        fixed.PROBE = fixed.PROBE.replace(old,'math.floor((batchEpoch-1)/30)*7')
        return original()

    batch.normal.main = held_main
    rc = batch.main()
    out = Path(fixed.value('--out'))
    e = json.loads((out / 'batch_environment.json').read_text())
    e.update({'adapter_sha256':sha(Path(__file__).read_bytes()),'hold_updates':30,
              'scope':e['scope']+'; each seven-name page held for 30 updates'})
    (out / 'stable_batch_environment.json').write_text(json.dumps(e,indent=2),encoding='utf-8')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
