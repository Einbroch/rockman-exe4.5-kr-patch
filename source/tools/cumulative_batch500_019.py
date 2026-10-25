"""019 single-writer merge;112 retained archives plus21 new archives."""
import cumulative_batch500 as merge
PROFILE=merge.PROFILE019
OUT=PROFILE['out']
PREFLIGHT=OUT+'/preflight.json'
def prepare():return merge.prepare(PROFILE)
def entries(source):return merge.entries(source,PROFILE)
def replace_paths(paths):return merge.replace_paths(paths,PROFILE)
def verify_product_lineage(source,rom,meta):
    link=meta.get('build_argument_manifest')
    if link is None:raise ValueError('019 hash-bound build arguments absent')
    merge.require_hash(merge.ROOT/link['path'],link['sha256'])
    result=merge.verify_product_lineage(source,rom,meta,PROFILE)
    records={r['archive']:r for r in meta['archives']}
    for bound in merge.read(PREFLIGHT)['archives']:
        record=records[bound['archive']]
        if record['layout']!=bound['proof']['layout'] or record.get('nickname_capacity_proof',[])!=bound['proof'].get('nickname_capacity_proof',[]):raise ValueError('019 final layout/capacity differs')
        at=int(bound['archive'],16);size=bound['scope']['source_bytes']
        if rom[at:at+size]!=source[at:at+size]:raise ValueError('019 native source storage changed')
    return result
if __name__=='__main__':
    from prepare_cumulative500_007 import main
    main(PROFILE)
