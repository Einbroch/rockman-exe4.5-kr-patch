"""Fifth500 frozen artifact profile using raw pointer/payload/delta verifier."""
import verify_pending500_004_rom as verification
from batch500_005_rom import entries,PREFLIGHT

verification.BASE='poc/output/exe45_ko_development_pending500_004_v1.gba'
verification.TOTAL=5337
verification.PRIMARY=183
verification.PREVIOUS_PRIMARY=152
verification.entries=entries
verification.PREFLIGHT=PREFLIGHT

if __name__=='__main__':verification.main()
