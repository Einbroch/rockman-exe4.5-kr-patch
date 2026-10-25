"""009 exact500 delta from actual008 and complete cumulative integrity checks."""
import verify_cumulative500_007 as verify
from cumulative_batch500_009 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
