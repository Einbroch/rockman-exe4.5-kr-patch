"""022 exact500 (136 raw plus 364 guarded hint) integrity/reproduction wrapper."""
import verify_cumulative500_007 as verify
from cumulative_batch500_022 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
