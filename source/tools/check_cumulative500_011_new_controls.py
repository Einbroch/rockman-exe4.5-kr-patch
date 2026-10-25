"""011 source-new archive integrity controls; in memory only."""
import check_cumulative500_010_new_controls as controls
from cumulative_batch500_011 import verify_product_lineage
controls.STEM='exe45_ko_development_pending500_011_v1'
controls.ARCHIVE='6C5F28'
controls.OUT='analysis/pending500_011_v1/new_archive_controls.json'
controls.verify_product_lineage=verify_product_lineage
if __name__=='__main__':controls.main()
