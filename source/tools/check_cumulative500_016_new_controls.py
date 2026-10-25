"""Five corruption controls for a newly added profile archive, in memory only."""
import check_cumulative500_010_new_controls as check
from cumulative_batch500_016 import verify_product_lineage
check.verify_product_lineage=verify_product_lineage
check.STEM='exe45_ko_development_pending500_016_v1'
check.ARCHIVE='67D708'
check.OUT='analysis/pending500_016_v1/new_archive_controls.json'
if __name__=='__main__':check.main()
