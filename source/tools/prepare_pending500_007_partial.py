"""Next500 source-only preflight, not cumulative-merge or ROM-application evidence."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector

analysis.BASE='poc/output/exe45_ko_development_middle_dot_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_007_partial_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_007_partial_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_007_layout.json'
analysis.BATCH_ID='pending-insertion-500-007-partial-source-only'
selector.ALLOW_PARTIAL=True

if __name__=='__main__':analysis.main()
