"""012 three exact literals, not profile editing/HP reward/mission outcome proof."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_012 import OUT
verify.STEM='exe45_ko_development_pending500_012_v1'
verify.PREFIX='pending500-012-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_012_v1'
verify.CASES=[('prog','7B67C8',17,255,(2,),(52,110)),('shadow','7C714C',0,10,(2,),(52,110)),('carry','776198',17,20,(2,),(52,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
