"""020 exact500 integrity/reproduction verification wrapper."""
import verify_cumulative500_007 as verify
from cumulative_batch500_020 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
