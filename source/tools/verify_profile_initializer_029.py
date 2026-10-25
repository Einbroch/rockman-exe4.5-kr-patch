"""Source-bound real initializer/cache lifetime evidence for development use."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_profile_arrays_029 import ROM,ROM_SHA

OUT='analysis/pending_insertion_500_029_initializer_runtime_v1/verification.json'

def main():
    require_hash(ROOT/ROM,ROM_SHA);rom=(ROOT/ROM).read_bytes();cfg=read('project.json')
    sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    cpu_path='analysis/pending_insertion_500_029_array_cpu_v2/cpu.json';cpu=read(cpu_path)
    if not cpu['passed'] or cpu['case_count']!=34276 or cpu['baseline_sha256']!=ROM_SHA:raise ValueError('029 initializer CPU')
    for region in cpu['native_ranges']:
        a,n=region['offset'],region['bytes']
        if sha(source[a:a+n])!=region['sha256'] or rom[a:a+n]!=source[a:a+n]:raise ValueError('029 CPU applicability')
    parent='poc/runtime/profile-initializer-029-older-bro-v2/'
    normal='poc/runtime/profile-lifetime-029-startup-v1/'
    for root in (parent,normal):
        receipt=read(root+'result.json')
        if not receipt['complete'] or receipt['rom_sha256']!=ROM_SHA:raise ValueError('029 receipt')
        for p,h in receipt['artifacts'].items():require_hash(ROOT/(root+p),h)
    trace=read(parent+'step_039_initializer_trace.json')
    if not trace['seeded'] or not trace['restored'] or trace['after_writes'] or len(trace['reads'])!=1:raise ValueError('029 initialization/lifetime ordering')
    call=trace['reads'][0]
    if call['index']!=3 or call['cache']!=0x020293E0 or call['frame']<=trace['init_frame']:raise ValueError('029 delayed native array consumption')
    lifecycle=read(normal+'step_034_profile_lifecycle.json')['events']
    init=[x for x in lifecycle if x['pc']==0x08038B94]
    if [x['r0'] for x in init]!=list(range(26)) or not any(x['pc']==0x080309EE for x in lifecycle):raise ValueError('029 normal source caller/26 rows')
    ram=(ROOT/(parent+'step_039_gbaExtWorkRam.bin')).read_bytes()
    baseline=(ROOT/(normal+'step_034_gbaExtWorkRam.bin')).read_bytes()
    def region(raw,a,n):return raw[a-0x02000000:a-0x02000000+n]
    for f in cpu['fields']:
        if region(ram,f['cache'],f['size'])!=bytes.fromhex('e406')*f['cap']+b'\xE5':raise ValueError('029 final all-eight native caches')
        n=f['count']*(f['size']+1)
        if region(ram,f['base'],n)!=region(baseline,f['base'],n):raise ValueError('029 restored native userdata differs from normal startup')
    draws=read(parent+'step_039_roll_pet.json')['draws']
    glyphs=[(d['stream']-0x02010AC0,d['glyph_index'],d['offset']) for d in draws if d['frame']>=call['frame'] and 0x02010AC0<=d['stream']<0x02010ACD]
    if glyphs!=[(2*i,234,44*i) for i in range(6)]:raise ValueError('029 final native cache glyph draws')
    native=[]
    for a,n in ((0x309EE,8),(0x38A9E,18),(0x38D9C,16),(0x355B6,64),(0x37F0C,0x48)):
        if rom[a:a+n]!=source[a:a+n]:raise ValueError('029 caller/editor-cap identity')
        native.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n])))
    paths=[cpu_path,parent+'result.json',normal+'result.json','analysis/pending_insertion_500_029_models_test_v1/result.json','tools/verify_profile_initializer_029.py','tools/capture_profile_initializer_029.py','tools/capture_profile_lifetime_029.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_sha256=ROM_SHA,native_cpu_cases=34276,normal_initializer_26_rows=True,all_eight_caches_preserved=True,records_restored_match_normal_startup=True,representative_delayed_RAM_glyphs=6,native_ranges=native,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},product_admitted=False,release_eligible=False,limits=['Controlled valid legacy records and source initializer, not arbitrary imported/corrupt/default/writer values or Hangul records.','Natural startup initializer runs; GutsMan5 body selection is root/table read alias on own Rockman PET host, not natural character/script selection.','Same shared initializer and F90C reader across eight descriptors covered in CPU; actual delayed older-bro GBA draw is one representative, not every selected script/gameplay branch.','Need final029 ROM build/runtime; no new ROM or package created by this verifier.']))
    print('PASS029 natural initializer,26 rows,8 persistent caches,delayed native glyphs; no ROM written')

if __name__=='__main__':main()
