"""013 one explicitly deferred normal notification in mixed startup archive."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector
analysis.BASE='poc/output/exe45_ko_development_pending500_012_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_013_partial_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_013_partial_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_013_layout.json'
analysis.BATCH_ID='pending-insertion-1-013-partial-source-only'
analysis.TARGET=1
selector.ALLOW_PARTIAL=True
if __name__=='__main__':analysis.main()
