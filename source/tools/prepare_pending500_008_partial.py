"""008 source-only selection against actual007; never an injectable payload."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector
analysis.BASE='poc/output/exe45_ko_development_pending500_007_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_008_partial_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_008_partial_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_008_layout.json'
analysis.BATCH_ID='pending-insertion-500-008-partial-source-only'
selector.ALLOW_PARTIAL=True
if __name__=='__main__':analysis.main()
