"""Verbatim frozen017 draft inputs; carry scope admitted separately."""
from prepare_batch500_016_inputs import prepare as materialize
SELECTION='analysis/pending_insertion_500_017_selection_v1/selection.json'
OUT='analysis/pending_insertion_500_017_inputs_v1'
def prepare():return materialize(SELECTION,OUT,allow_carry=True)
if __name__=='__main__':print('Prepared',len(prepare()),'archives; source wording unchanged')
