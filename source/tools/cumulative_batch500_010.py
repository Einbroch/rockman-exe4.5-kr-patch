"""Frozen010 mixed profile:49 carried archives and20 source-only new archives."""
import cumulative_batch500 as merge
PROFILE=merge.PROFILE010
PREFLIGHT=PROFILE['out']+'/preflight.json'
OUT=PROFILE['out']
def prepare():return merge.prepare(PROFILE)
def entries(source):return merge.entries(source,PROFILE)
def replace_paths(paths):return merge.replace_paths(paths,PROFILE)
def verify_product_lineage(source,rom,meta):return merge.verify_product_lineage(source,rom,meta,PROFILE)
if __name__=='__main__':
    from prepare_cumulative500_007 import main
    main(PROFILE)
