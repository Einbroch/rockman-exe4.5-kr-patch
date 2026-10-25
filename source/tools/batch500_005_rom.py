"""Fifth500 immutable input profile; same raw reinsertion contract as004."""
import batch500_004_rom as raw

PREFLIGHT='analysis/pending_insertion_500_005_preflight_v1/preflight.json'
OUT='analysis/pending_insertion_500_005_rom'
BATCH_ID='pending-insertion-500-005'

def entries(source):return raw.entries(source,PREFLIGHT,BATCH_ID)
def prepare():return raw.prepare(PREFLIGHT,OUT,BATCH_ID)
