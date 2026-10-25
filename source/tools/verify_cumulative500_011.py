"""011 exact500-ID delta, retained scripts and original-source new archives."""
import verify_cumulative500_007 as verify
from cumulative_batch500_011 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
