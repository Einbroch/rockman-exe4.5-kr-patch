"""014 ten-unit source-only selection; proposal input is explicit and preserved."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector
from prepare_middle_dot014_inputs import prepare
analysis.BASE='poc/output/exe45_ko_development_pending500_013_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_014_partial_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_014_partial_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_014_layout.json'
analysis.BATCH_ID='pending-insertion-10-014-partial-source-only'
analysis.TARGET=10
selector.ALLOW_PARTIAL=True
if __name__=='__main__':prepare();analysis.main()
