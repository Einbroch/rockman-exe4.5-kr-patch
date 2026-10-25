"""Source storage and lookup corruption must fail for the new raw archive."""
import check_cumulative500_010_new_controls as check
from cumulative_batch500_015 import verify_product_lineage
check.verify_product_lineage=verify_product_lineage
check.STEM='exe45_ko_development_pending500_015_v1'
check.ARCHIVE='7C9C44'
check.OUT='analysis/pending500_015_v1/new_archive_controls.json'
if __name__=='__main__':check.main()
