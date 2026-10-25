"""Valid native finite chip stats fields only; Korean chip names still open."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from inspect_profile_chip_pools_030 import OUT as CENSUS
from compare_archive_payloads import payload_of
from verify_tpi_index import parse_tpi

RUNTIME='analysis/pending_insertion_500_030_chip_runtime_v1/verification.json'
CPU='analysis/pending_insertion_500_030_chip_cpu_v1/cpu.json'

def bounds(source,rom):
    c=read(CENSUS);p=read(RUNTIME);cpu=read(CPU);tests=read('analysis/pending_insertion_500_030_models_test_v1/result.json')
    if sha(source)!=c['source_sha256'] or p['source_sha256']!=sha(source) or not p['passed'] or not cpu['passed'] or cpu['case_count']!=3932 or not tests['passed'] or tests['tests']!=20:raise ValueError('030 finite chip evidence')
    for evidence in (c,p,tests):
        for path,h in evidence['dependencies'].items():require_hash(ROOT/path,h)
    require_hash(ROOT/'tools/bench_profile_chips_030.py',cpu['tool_sha256'])
    require_hash(ROOT/cpu['census']['path'],cpu['census']['sha256'])
    for r in cpu['native_ranges']:
        a,n=r['offset'],r['bytes']
        if sha(source[a:a+n])!=r['sha256'] or rom[a:a+n]!=source[a:a+n]:raise ValueError('030 native chip lookup/writer/reader applicability')
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);rows={r['offset']:r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    for at in (0x765190,0x765B18):
        if payload_of(source,rows[at])!=payload_of(rom,rows[at]):raise ValueError('030 shared native chip pool changed')
    from pet_chip_capacity_030 import CHIP_BOUNDS
    if set(CHIP_BOUNDS)!=set(c['fields']) or any(v!=c['maximum_advance'] for v in CHIP_BOUNDS.values()):raise ValueError('030 finite chip width/model mismatch')
    return c['fields']
