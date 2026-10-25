"""009 artifact negative controls, in memory only."""
import check_cumulative500_rejections as controls
from cumulative_batch500_009 import verify_product_lineage
controls.STEM='exe45_ko_development_pending500_009_v1'
controls.OUT='analysis/pending500_009_v1/rejection_controls.json'
controls.VERIFY=verify_product_lineage
if __name__=='__main__':controls.main()
