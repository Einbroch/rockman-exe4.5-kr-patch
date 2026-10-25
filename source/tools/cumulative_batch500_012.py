"""Frozen012 remaining268:40 carried archives and8 source-new archives."""
import cumulative_batch500 as merge
PROFILE=merge.PROFILE012
OUT=PROFILE['out']
PREFLIGHT=OUT+'/preflight.json'
def prepare():return merge.prepare(PROFILE)
def entries(source):return merge.entries(source,PROFILE)
def replace_paths(paths):return merge.replace_paths(paths,PROFILE)
def verify_product_lineage(source,rom,meta):return merge.verify_product_lineage(source,rom,meta,PROFILE)
if __name__=='__main__':
    from prepare_cumulative500_007 import main
    main(PROFILE)
