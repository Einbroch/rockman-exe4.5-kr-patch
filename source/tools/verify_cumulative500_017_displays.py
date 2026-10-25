"""14 changed pages across six archive writers, including explicit layouts."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_017 import OUT
verify.STEM='exe45_ko_development_pending500_017_v1'
verify.PREFIX='pending500-017-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_017_v1'
verify.CASES=[('heel','716DE4',14,141,(2,),(52,110)),('napalm','71A66C',3,36,(2,4,6,8),(52,110)),('fire','76C944',35,144,(2,),(52,110)),('prog','7A152C',21,255,(2,4,6),(52,110)),('proto','7C0F8C',2,255,(2,4),(52,110)),('thunder','7C7188',6,42,(2,4,6),(52,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
