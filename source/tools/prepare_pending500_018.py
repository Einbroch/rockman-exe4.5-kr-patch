"""Source-only018 compiler gate; no ROM mutation or wording substitution."""
import prepare_pending500_017 as compiler
from prepare_batch500_018_inputs import prepare,SELECTION
compiler.prepare=prepare
compiler.SELECTION=SELECTION
compiler.OUT='analysis/pending_insertion_500_018_preflight_v2'
if __name__=='__main__':compiler.main()
