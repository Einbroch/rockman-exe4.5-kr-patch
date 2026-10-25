"""Exclude caller's empty-row bypass from parser-return pairing."""
import json
from pathlib import Path
import capture_chip_other_consumer as base
from build_visibility_poc import sha


def main():
    old="if not a then otherFail('alternate return without entry') end"
    if base.PROBE.count(old)!=1:
        raise ValueError('alternate return observer anchor drift')
    # Native 0803CB62 branches directly here after clearing an empty row.
    base.PROBE=base.PROBE.replace(old,'if not a then return end')
    rc=base.main()
    out=Path(base.library.fixed.value('--out'))
    e=json.loads((out/'other_consumer_environment.json').read_text())
    e['adapter_sha256']=sha(Path(__file__).read_bytes())
    e['excluded_path']='source 0803CB62 -> 0803CB7A clears empty row without calling parser'
    (out/'other_consumer_v2_environment.json').write_text(json.dumps(e,indent=2),encoding='utf-8')
    return rc


if __name__=='__main__':
    raise SystemExit(main())
