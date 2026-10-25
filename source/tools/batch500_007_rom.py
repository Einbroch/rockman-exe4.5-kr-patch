"""Unadopted untouched-only proposal; NOT the cumulative007 product adapter.

Its preflight was not produced. The adopted single-writer product path is
cumulative_batch500.py; source-only partial payloads must never enter here.
"""
import batch500_004_rom as raw

PREFLIGHT='analysis/pending_insertion_500_007_preflight_v1/preflight.json'
OUT='analysis/pending_insertion_500_007_rom'
BATCH_ID='pending-insertion-500-007'

def entries(source):return raw.entries(source,PREFLIGHT,BATCH_ID)
def prepare():return raw.prepare(PREFLIGHT,OUT,BATCH_ID)
