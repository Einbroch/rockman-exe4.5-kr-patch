"""Actual024 self-match catches wrong direction of shared-archive matching."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records

def main():
    meta=read('poc/output/pending500_024_v1.json');records=list(layout_records(meta));results={}
    for policy in ('smallest','largest'):
        matched=set()
        for current in records:
            ids={u['id'] for u in current['layout']}
            candidates=[r for r in records if r['archive']==current['archive'] and {u['id'] for u in r['layout']}<=ids]
            parent=sorted(candidates,key=lambda r:len(r['layout']),reverse=policy=='largest')[0]
            matched.add((parent['archive'],parent['compiled_sha256']))
        missing=[dict(archive=r['archive'],units=len(r['layout']),sha256=r['compiled_sha256']) for r in records if (r['archive'],r['compiled_sha256']) not in matched]
        results[policy]=dict(matched=len(matched),missing=missing)
    if not results['smallest']['missing'] or results['largest']['missing']:raise ValueError('025 consumer identity direction fixture')
    frozen_write(ROOT/'analysis/pending_insertion_500_025_consumer_identity_v1/result.json',dict(passed=True,baseline_metadata_sha256=sha((ROOT/'poc/output/pending500_024_v1.json').read_bytes()),consumer_count=len(records),results=results,rule='current→prior selects largest subset; prior→current selects smallest superset',rom_written=False,rejected_assumption='Smallest-subset matching loses full-body consumers sharing source archive with short bodies.',limits='Consumer identity fixture, not final product or runtime evidence.'))
    print('PASS025 consumer mapping',len(records),'current/prior consumers; bad smallest subset rejected;largest subset complete')

if __name__=='__main__':main()
