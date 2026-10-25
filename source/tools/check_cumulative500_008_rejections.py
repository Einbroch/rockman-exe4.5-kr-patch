"""008 artifact negative controls; never alter on-disk product assets."""
import check_cumulative500_rejections as controls
from cumulative_batch500_008 import verify_product_lineage
controls.STEM='exe45_ko_development_pending500_008_v1'
controls.OUT='analysis/pending500_008_v1/rejection_controls.json'
controls.VERIFY=verify_product_lineage
if __name__=='__main__':controls.main()
