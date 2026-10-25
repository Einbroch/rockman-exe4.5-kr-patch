"""012 remaining268 within the established raw normal scope; no source-only injection."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector
analysis.BASE='poc/output/exe45_ko_development_pending500_011_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_012_partial_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_012_partial_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_012_layout.json'
analysis.BATCH_ID='pending-insertion-268-012-partial-source-only'
analysis.TARGET=268
analysis.EXTRA_EXCLUDE={'70904C'}
selector.ALLOW_PARTIAL=True
if __name__=='__main__':analysis.main()
