"""Quarantined034 new-caption/choice read aliases, no RAM/ROM writes.

List samples stop before list-buffer reads. No caller/editor/save claim.
"""
import struct,sys
from pathlib import Path
import capture_layout500_display_024 as raw
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from compare_archive_payloads import payload_of
from archive_scripts import script_spans

CASES={'list-caption':('65B9E8',40),'query-choice':('65B9E8',41),'mission-caption':('716DE4',100),'trader-caption':('6FE8D4',21)}


def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    name=value('--display-case')
    if name not in CASES:raise ValueError('034 declared display sample')
    arc,script=CASES[name];rp=Path(value('--rom'));meta=read(rp.with_suffix('.json'));require_hash(rp,meta['output_sha256'])
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    manifest=read('analysis/pending_insertion_500_034_carry500_v1/preflight.json');rec=next(r for r in manifest['archives'] if r['archive']==arc)
    if script not in rec['new_scripts'] or not any(r.get('cumulative034') for r in meta['archives'] if r['archive']==arc):raise ValueError('034 actual newly integrated script')
    native=script_spans(payload_of(source,rec['source_row']),rec['script_count'])[script]
    prefix=(bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d') if name in ('list-caption','query-choice') else bytes.fromhex('f1e700') if name=='trader-caption' else bytes.fromhex('e700f400'))
    if not native.startswith(prefix):raise ValueError('034 exact source sample initializer')
    raw.CASES={name:(arc,rec['script_count'],script,prefix)}
    return raw.main()


if __name__=='__main__':raise SystemExit(main())
