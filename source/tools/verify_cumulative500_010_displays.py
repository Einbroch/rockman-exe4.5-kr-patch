"""010 two stable literal displays; waitHold loss probe remains unverified."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_010 import OUT
verify.STEM='exe45_ko_development_pending500_010_v1'
verify.PREFIX='pending500-010-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_010_v1'
verify.CASES=[('new-win','6989B0',1,4,(2,),(92,110)),('carry','6886F0',20,25,(2,),(92,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
