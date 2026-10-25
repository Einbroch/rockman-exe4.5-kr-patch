"""Development-only valid legacy array-cache applicability; no Hangul saves."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read

RUNTIME='analysis/pending_insertion_500_029_initializer_runtime_v1/verification.json'
CPU='analysis/pending_insertion_500_029_array_cpu_v2/cpu.json'

def bounds(source,rom):
    proof=read(RUNTIME);cpu=read(CPU)
    if not proof['passed'] or not cpu['passed'] or sha(source)!=proof['source_sha256'] or sha(source)!=cpu['source_sha256'] or cpu['case_count']!=34276:raise ValueError('029 source array evidence')
    for p,h in proof['dependencies'].items():require_hash(ROOT/p,h)
    require_hash(ROOT/'tools/bench_profile_arrays_029_v2.py',cpu['tool_sha256'])
    tests=read('analysis/pending_insertion_500_029_models_test_v1/result.json')
    if not tests['passed'] or tests['tests']!=29:raise ValueError('029 array model tests')
    for p,h in tests['dependencies'].items():require_hash(ROOT/p,h)
    for r in cpu['native_ranges']+proof['native_ranges']:
        a,n=r['offset'],r['bytes']
        if sha(source[a:a+n])!=r['sha256'] or rom[a:a+n]!=source[a:a+n]:raise ValueError('029 native array contract changed')
    from pet_array_capacity_029 import ARRAY_CAPS
    out={}
    for f in cpu['fields']:
        if ARRAY_CAPS[f['provider']]!=f['cap']:raise ValueError('029 array logical cap drift')
        raw=source[0x3B0D0+16*f['row']:0x3B0E0+16*f['row']]
        if raw[:3]!=bytes([f['count'],f['index'],f['cap']]) or struct.unpack_from('<II',source,0x526D0+8*f['index'])!=(f['cache'],f['size']):raise ValueError('029 exact array descriptor')
        out[f['provider']]=dict(logical_cap=f['cap'],max_native_advance=f['cap']*11,valid_native_record_and_prepared_cache_required=True,automatic_Hangul_records_supported=False)
    if set(out)!=set(ARRAY_CAPS):raise ValueError('029 array provider denominator')
    return out
