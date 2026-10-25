"""011 source-only selection against actual010; not an injectable payload."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector
analysis.BASE='poc/output/exe45_ko_development_pending500_010_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_011_partial_selection_v2'
analysis.PREFLIGHT='analysis/pending_insertion_500_011_partial_preflight_v2'
analysis.LAYOUT='translations/pending_insertion_500_011_layout.json'
analysis.BATCH_ID='pending-insertion-500-011-partial-source-only'
selector.ALLOW_PARTIAL=True
analysis.EXTRA_EXCLUDE={'70904C'} # Distinct proportional startup consumer, not this cohort.
if __name__=='__main__':analysis.main()
