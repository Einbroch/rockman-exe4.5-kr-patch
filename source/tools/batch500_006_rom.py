"""Sixth500 frozen input profile for the established raw reinsertion contract."""
import batch500_004_rom as raw

PREFLIGHT='analysis/pending_insertion_500_006_preflight_v2/preflight.json'
OUT='analysis/pending_insertion_500_006_rom'
BATCH_ID='pending-insertion-500-006'

def entries(source):return raw.entries(source,PREFLIGHT,BATCH_ID)
def prepare():return raw.prepare(PREFLIGHT,OUT,BATCH_ID)
