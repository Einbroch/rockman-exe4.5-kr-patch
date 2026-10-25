"""009 source-only selection against actual008; not an injectable payload."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector
analysis.BASE='poc/output/exe45_ko_development_pending500_008_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_009_partial_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_009_partial_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_009_layout.json'
analysis.BATCH_ID='pending-insertion-500-009-partial-source-only'
selector.ALLOW_PARTIAL=True
if __name__=='__main__':analysis.main()
