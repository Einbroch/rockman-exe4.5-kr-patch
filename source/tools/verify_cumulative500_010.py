"""010 exact500-ID delta;49 carry archives and20 new original-source archives."""
import verify_cumulative500_007 as verify
from cumulative_batch500_010 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
