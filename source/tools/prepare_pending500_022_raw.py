"""Derived raw136 projection of the immutable source-only500 selection."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_pending500_022 import materialize
MANIFEST='translations/pending_insertion_500_022_build_v1.json'
OUT='analysis/pending_insertion_500_022_raw_preflight_v1/preflight.json'

def prepare():
    m=read(MANIFEST)
    if m['policy']!='development-draft; NON-DISTRIBUTION' or m['release_eligible'] is not False or (m['raw_units'],m['hint_units'],m['total_new_units'])!=(136,364,500):raise ValueError('022 development denominator')
    ref=m['source_preflight'];require_hash(ROOT/ref['path'],ref['sha256']);p=read(ref['path']);materialize()
    if p['total_units']!=500 or p['applied_id_intersection']:raise ValueError('022 original source scope')
    b=deepcopy(p);b['archives']=[r for r in b['archives'] if r['archive'] in m['raw_archives']]
    if [r['archive'] for r in b['archives']]!=m['raw_archives'] or sum(r['selected_units'] for r in b['archives'])!=136:raise ValueError('022 raw projection')
    b.update(batch_id='pending-insertion-136-022-raw-source-only',total_units=136,full500_source_preflight=ref)
    frozen_write(ROOT/OUT,b)
    return b

if __name__=='__main__':prepare();print('Prepared raw136 projection; full500 unchanged')
