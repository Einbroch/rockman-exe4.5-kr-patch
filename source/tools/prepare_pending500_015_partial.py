"""Two-unit source-only preflight; no ROM mutation or product flag."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector
from prepare_middle_dot015_inputs import prepare
analysis.BASE='poc/output/exe45_ko_development_pending500_014_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_015_partial_selection_v1'
analysis.PREFLIGHT='analysis/pending_insertion_500_015_partial_preflight_v1'
analysis.LAYOUT='translations/pending_insertion_500_015_layout.json'
analysis.BATCH_ID='pending-insertion-2-015-partial-source-only'
analysis.TARGET=2
selector.ALLOW_PARTIAL=True
if __name__=='__main__':prepare();analysis.main()
