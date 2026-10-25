"""Current008 artifact profile; exact500 delta from actual007, not ancestry sum."""
import verify_cumulative500_007 as verify
from cumulative_batch500_008 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
