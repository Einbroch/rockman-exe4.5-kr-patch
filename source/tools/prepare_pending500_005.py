"""Fifth500 selection profile using the existing raw/no-variable analysis path."""
import prepare_pending500_004 as analysis

analysis.BASE='poc/output/exe45_ko_development_pending500_004_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_005_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_005_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_005_layout.json'
analysis.BATCH_ID='pending-insertion-500-005'

if __name__=='__main__':analysis.main()
