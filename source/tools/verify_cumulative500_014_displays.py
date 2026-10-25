"""All ten added literals: glyph reads, residency, pixels and clearing."""
import verify_cumulative500_007_displays as verify
from cumulative_batch500_014 import OUT
verify.STEM='exe45_ko_development_pending500_014_v1'
verify.PREFIX='pending500-014-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_014_v1'
verify.CASES=[('stereo','7BDC90',0,255,(2,4,6,8,10),(52,110)),('shop','7B3C30',0,255,(2,),(52,110)),('shadow-one','7B4184',1,255,(2,),(52,110)),('shadow-two','7B4184',2,255,(2,),(52,110)),('shadow-challenge','7B4184',3,255,(2,4),(52,110))]
verify.REQUIRE_CLEARING=True
if __name__=='__main__':verify.main()
