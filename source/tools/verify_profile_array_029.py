"""Verify bounded native producer/reader GBA trace; no ROM admission."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_profile_arrays_029 import ROM,ROM_SHA

def main():
    require_hash(ROOT/ROM,ROM_SHA)
    cpu='analysis/pending_insertion_500_029_array_cpu_v1/cpu.json'
    survey='analysis/pending_insertion_500_029_layout_v1/survey.json'
    c=read(cpu);s=read(survey)
    if not c['passed'] or c['baseline_sha256']!=ROM_SHA or c['case_count']!=34256:raise ValueError('029 CPU baseline')
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    parent='poc/runtime/profile-array-029-friend-v1/'
    result=read(parent+'result.json')
    if not result['complete'] or result['display_diagnostic']['script']!=18 or result['display_diagnostic']['navi']!=0:raise ValueError('029 runtime route')
    for p,h in result['artifacts'].items():require_hash(ROOT/(parent+p),h)
    trace=read(parent+'step_003_array_trace.json')['events']
    if len(trace)!=1:raise ValueError('029 exact producer/reader event')
    event=trace[0];f=next(x for x in c['fields'] if x['provider']=='printFriend')
    if not event['records_and_flag_restored'] or event['hex']!='E406'*6+'E5' or event['cache']!=f['cache'] or event['output']!=0x02010AC0:raise ValueError('029 copied bytes/restoration')
    if not 0<=event['selected_source']-f['base']-1<f['count']*(f['size']+1) or (event['selected_source']-f['base']-1)%(f['size']+1):raise ValueError('029 actual selected source')
    draws=read(parent+'step_003_roll_pet.json')['draws']
    actual=[(x['stream']-event['output'],x['glyph_index'],x['offset']) for x in draws if event['output']<=x['stream']<event['output']+13]
    if actual!=[(2*i,234,44*i) for i in range(6)]:raise ValueError('029 six RAM glyphs/advance')
    selected=s['selected500']
    if not selected or sum(x['units'] for x in selected)!=500 or any(x['product_admitted'] for x in selected) or s['rom_written']:raise ValueError('029 conditional candidate boundary')
    paths=[cpu,survey,parent+'result.json',parent+'step_003_array_trace.json',parent+'step_003_roll_pet.json',parent+'step_003.png','tools/verify_profile_array_029.py','tools/capture_profile_array_029.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_029_array_runtime_v1/verification.json',dict(schema=1,passed=True,rom_sha256=ROM_SHA,native_cpu_cases=34256,friend_actual_FC0F_cache_F90C_RAM_glyphs=6,visual_inspection='Screenshot viewed: six native small kana followed by original Japanese first page; no translation claimed.',conditional_new_array_literal_candidates=689,conditional_next500_scripts=len(selected),new_units_applied=0,new_rom_built=False,patch_package_created=False,product_admitted=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},limits=['Quarantined root/table aliases to AquaMan18 while preserving own Rockman PET host. Not natural character/caller selection.','Temporarily seeded valid native friend records/enable flag at real source FC0F handler; restored at real F90C reader return. No game save file written.','Only first waited source Japanese page. No second-page hobby cache, natural entry/exit, all eight array GBA paths, translation integration, persistence or Hangul names proved.','Conditional689/exact500 analysis is not500 translated/applied or whole-game remainder. Need caller/lifetime applicability, product gates and final-ROM runtime before adoption.']))
    print('PASS029 bounded friend producer/reader/RAM glyph trace; new applied units=0; ROM unchanged')

if __name__=='__main__':main()
