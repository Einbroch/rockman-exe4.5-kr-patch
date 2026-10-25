"""Freeze the next500 from the fresh verified017-baseline finite survey."""
import select_batch500_017 as selector
selector.SURVEY='analysis/pending_insertion_500_018_layout_survey_v2/survey.json'
selector.OUT='analysis/pending_insertion_500_018_selection_v2/selection.json'
selector.LAYOUT='translations/pending_insertion_500_018_layout_v2.json'
if __name__=='__main__':selector.main('pending-insertion-500-018-source-only')
