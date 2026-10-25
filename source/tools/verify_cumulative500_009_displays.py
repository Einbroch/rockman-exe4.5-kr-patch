"""009 four new literal pages, exact wait/font/OBJ/clearing evidence."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_009 import OUT
verify.STEM='exe45_ko_development_pending500_009_v1'
verify.PREFIX='pending500-009-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_009_v1'
verify.CASES=[('prog','71551C',37,62,(2,4),(52,110)),('item','68BAAC',3,5,(2,4),(92,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
