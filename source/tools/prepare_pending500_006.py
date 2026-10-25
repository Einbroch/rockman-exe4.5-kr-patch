"""Sixth500 raw/no-variable selection profile, all prior consumers excluded."""
import prepare_pending500_004 as analysis

analysis.BASE='poc/output/exe45_ko_development_pending500_005_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_006_selection_v2'
analysis.PREFLIGHT='analysis/pending_insertion_500_006_preflight_v2'
analysis.LAYOUT='translations/pending_insertion_500_006_layout.json'
analysis.BATCH_ID='pending-insertion-500-006'

if __name__=='__main__':analysis.main()
