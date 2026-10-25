"""Eleven exact literals: two full-box and two quick-box consumer paths."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_016 import OUT
verify.STEM='exe45_ko_development_pending500_016_v1'
verify.PREFIX='pending500-016-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_016_v1'
verify.CASES=[('meal','65AFA0',23,28,(2,),(52,110)),('thunder-meal','67CB70',23,28,(2,4),(52,110)),('wind-food','66CA84',11,97,(2,4,6,8,10),(92,110)),('fire-dream','677F64',15,97,(2,4,6),(92,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
