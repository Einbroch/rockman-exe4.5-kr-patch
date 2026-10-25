"""Six-unit source-only scope; v1 evidence remains immutable."""
import prepare_pending500_004 as analysis
import prepare_repartition500 as selector
from prepare_middle_dot015_inputs import prepare as prepare_world
from prepare_middle_dot015_tutorial_inputs import prepare as prepare_tutorial
analysis.BASE='poc/output/exe45_ko_development_pending500_014_v1.gba'
analysis.SELECTION='analysis/pending_insertion_500_015_partial_selection_v2'
analysis.PREFLIGHT='analysis/pending_insertion_500_015_partial_preflight_v2'
analysis.LAYOUT='translations/pending_insertion_500_015_layout.json'
analysis.BATCH_ID='pending-insertion-6-015-partial-source-only'
analysis.TARGET=6
selector.ALLOW_PARTIAL=True
if __name__=='__main__':prepare_world();prepare_tutorial();analysis.main()
