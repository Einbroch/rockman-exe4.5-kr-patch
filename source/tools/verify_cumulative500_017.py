"""Exact500 new-ID delta; unchanged prior scripts/metrics and final writes."""
import verify_cumulative500_007 as verify
from cumulative_batch500_017 import entries,verify_product_lineage
verify.ROM_LINEAGE=verify_product_lineage
verify.ENTRIES=entries
if __name__=='__main__':verify.main()
