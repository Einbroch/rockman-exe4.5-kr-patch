"""Sixth500 frozen artifact profile, prior payloads and raw pointer delta."""
import verify_pending500_004_rom as verification
from batch500_006_rom import entries,PREFLIGHT

verification.BASE='poc/output/exe45_ko_development_pending500_005_v1.gba'
verification.TOTAL=5837
verification.PRIMARY=270
verification.PREVIOUS_PRIMARY=183
verification.entries=entries
verification.PREFLIGHT=PREFLIGHT

if __name__=='__main__':verification.main()
