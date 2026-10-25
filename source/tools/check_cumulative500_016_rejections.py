"""Previous compiled ID/layout/payload corruption still rejected after new500."""
import check_cumulative500_rejections as check
from cumulative_batch500_016 import verify_product_lineage
check.VERIFY=verify_product_lineage
check.STEM='exe45_ko_development_pending500_016_v1'
check.OUT='analysis/pending500_016_v1/rejection_controls.json'
if __name__=='__main__':check.main()
