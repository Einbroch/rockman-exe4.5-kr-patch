"""Frozen500 disjoint scripts into six retained normal-dialogue writers."""
import cumulative_batch500 as merge
PROFILE=merge.PROFILE017
OUT=PROFILE['out']
PREFLIGHT=OUT+'/preflight.json'
def prepare():return merge.prepare(PROFILE)
def entries(source):return merge.entries(source,PROFILE)
def replace_paths(paths):return merge.replace_paths(paths,PROFILE)
def verify_product_lineage(source,rom,meta):
    result=merge.verify_product_lineage(source,rom,meta,PROFILE)
    records={r['archive']:r for r in meta['archives']}
    for bound in merge.read(PREFLIGHT)['archives']:
        record=records[bound['archive']]
        if record['layout']!=bound['proof']['layout']:raise ValueError('017 final per-ID layout differs from compiled explicit layout')
        at=int(bound['archive'],16);size=bound['scope']['source_bytes']
        if rom[at:at+size]!=source[at:at+size]:raise ValueError('017 native source storage changed')
    return result
if __name__=='__main__':
    from prepare_cumulative500_007 import main
    main(PROFILE)
