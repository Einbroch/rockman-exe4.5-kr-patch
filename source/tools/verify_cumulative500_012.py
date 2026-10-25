"""012 exact268-ID delta, retained scripts and new-source archives."""
import verify_cumulative500_007 as verify
from cumulative_batch500_012 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
