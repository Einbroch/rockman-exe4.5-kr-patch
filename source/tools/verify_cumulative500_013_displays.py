"""013 exact added notification glyphs and full-box keyWait rendering."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_013 import OUT
verify.STEM='exe45_ko_development_pending500_013_v1'
verify.PREFIX='pending500-013-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_013_v1'
verify.CASES=[('notification','70904C',10,120,(2,),(52,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
