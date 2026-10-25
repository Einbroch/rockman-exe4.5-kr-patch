"""17 literal samples: source-native full boxes and positioned quick boxes."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_018 import OUT
verify.STEM='exe45_ko_development_pending500_018_v1'
verify.PREFIX='pending500-018-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_018_v1'
verify.CASES=[('mail','65B220',20,255,(2,),(92,110)),('result','65E828',1,5,(2,),(92,110)),('reward','661858',31,97,(2,4),(92,110)),('alarm','66651C',24,28,(2,4),(52,110)),('guts','66A160',1,5,(2,4),(92,110)),('aqua','698424',2,4,(2,4,6,8,10,12),(92,110)),('wind','7C9C44',5,23,(2,4,6),(52,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
