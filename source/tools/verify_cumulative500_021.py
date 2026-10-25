"""021 exact500 integrity/reproduction wrapper."""
import verify_cumulative500_007 as verify
from cumulative_batch500_021 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
