"""Actual018 new-archive payload/ID/pointer/source-storage rejection controls."""
import check_cumulative500_010_new_controls as check
from cumulative_batch500_018 import verify_product_lineage
check.verify_product_lineage=verify_product_lineage
check.STEM='exe45_ko_development_pending500_018_v1'
check.ARCHIVE='65E828'
check.OUT='analysis/pending500_018_v1/new_archive_controls.json'
if __name__=='__main__':check.main()
