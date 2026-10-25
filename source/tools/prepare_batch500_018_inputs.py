"""Verbatim frozen018 drafts; separate explicit layout and carry admission."""
from prepare_batch500_016_inputs import prepare as materialize
SELECTION='analysis/pending_insertion_500_018_selection_v2/selection.json'
OUT='analysis/pending_insertion_500_018_inputs_v2'
def prepare():return materialize(SELECTION,OUT,allow_carry=True)
if __name__=='__main__':print('Prepared',len(prepare()),'archives; source wording unchanged')
