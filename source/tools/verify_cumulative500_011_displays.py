"""011 keyWait-only observations; not native battle outcome/caller evidence."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_011 import OUT
verify.STEM='exe45_ko_development_pending500_011_v1'
verify.PREFIX='pending500-011-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_011_v1'
verify.CASES=[('ice','6C5F28',1,5,(2,),(92,110)),('plant','6D1068',3,5,(2,),(92,110)),('carry','6B69A0',22,25,(2,),(92,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
