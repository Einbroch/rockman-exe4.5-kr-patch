"""021 source-based500 merge, full-box diagnostic range remains development-only."""
import cumulative_batch500 as merge
PROFILE=merge.PROFILE021
OUT=PROFILE['out']
PREFLIGHT=OUT+'/preflight.json'
def prepare():return merge.prepare(PROFILE)
def entries(source):return merge.entries(source,PROFILE)
def replace_paths(paths):return merge.replace_paths(paths,PROFILE)
def verify_product_lineage(source,rom,meta):
    link=meta.get('build_argument_manifest')
    if link is None:raise ValueError('021 hash-bound build arguments absent')
    merge.require_hash(merge.ROOT/link['path'],link['sha256'])
    result=merge.verify_product_lineage(source,rom,meta,PROFILE)
    records={r['archive']:r for r in meta['archives']}
    for b in merge.read(PREFLIGHT)['archives']:
        r=records[b['archive']]
        if r['layout']!=b['proof']['layout'] or r.get('fullbox_capacity_proof',[])!=b['proof'].get('fullbox_capacity_proof',[]) or r.get('nickname_capacity_proof',[])!=b['proof'].get('nickname_capacity_proof',[]):raise ValueError('021 final geometry proof')
    return result
if __name__=='__main__':
    from prepare_cumulative500_007 import main
    main(PROFILE)
