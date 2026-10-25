"""Seventh500 selection, middle-dot glyph now explicitly encodable."""
import prepare_pending500_004 as analysis

analysis.BASE='poc/output/exe45_ko_development_pending500_006_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_007_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_007_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_007_layout.json'
analysis.BATCH_ID='pending-insertion-500-007'

if __name__=='__main__':analysis.main()
