"""Bound exact029 native8-chip F90C/GBA consumption, not ROM admission."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from inspect_profile_chip_pools_030 import OUT as CENSUS,ROM,ROM_SHA

OUT='analysis/pending_insertion_500_030_chip_runtime_v1/verification.json'

def main():
    require_hash(ROOT/ROM,ROM_SHA);meta=read((ROOT/ROM).with_suffix('.json'));cpu_path='analysis/pending_insertion_500_030_chip_cpu_v1/cpu.json';cpu=read(cpu_path);c=read(CENSUS)
    if not cpu['passed'] or cpu['case_count']!=3932 or cpu['baseline_sha256']!=ROM_SHA:raise ValueError('030 native chip CPU baseline')
    require_hash(ROOT/cpu['census']['path'],cpu['census']['sha256']);require_hash(ROOT/'tools/bench_profile_chips_030.py',cpu['tool_sha256'])
    folder='poc/runtime/profile-chip-030-standard1-v1/';r=read(folder+'result.json')
    if not r['complete'] or r['rom_sha256']!=ROM_SHA or r['normal_play_checkpoint_eligible']:raise ValueError('030 diagnostic receipt')
    for p,h in r['artifacts'].items():require_hash(ROOT/(folder+p),h)
    trace=read(folder+'step_003_profile_trace.json')['events'];fixture=next(n for n in c['names'] if n['advance']==88);raw=bytes.fromhex(fixture['raw_hex'])
    if len(trace)!=1 or not trace[0]['restored'] or not bytes.fromhex(trace[0]['hex']).startswith(raw) or trace[0]['cap']!=8 or trace[0]['field']!=c['fields']['printFavStandardChip1']['field']:raise ValueError('030 native copied chip value/restoration')
    event=trace[0];draws=read(folder+'step_003_roll_pet.json')['draws'];actual=[(d['stream']-event['output'],d['glyph_index'],d['offset']) for d in draws if event['output']<=d['stream']<event['output']+len(raw)]
    if actual!=[(i,ch,44*i) for i,ch in enumerate(raw[:-1])]:raise ValueError('030 native RAM glyph stream/advance')
    ram=(ROOT/(folder+'step_005_gbaExtWorkRam.bin')).read_bytes();own=next(a for a in meta['archives'] if a['archive']=='65A608')
    if struct.unpack_from('<I',ram,0xFA50)[0]!=0x08000000+own['rom_offset']:raise ValueError('030 normal PET return')
    paths=[CENSUS,cpu_path,folder+'result.json',folder+'step_003_profile_trace.json',folder+'step_003_roll_pet.json',folder+'step_003.png','tools/verify_profile_chip_030.py','tools/capture_profile_chip_030.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=cpu['source_sha256'],baseline_sha256=ROM_SHA,native_cpu_cases=3932,native_finite_names=393,fixture_chip_id=fixture['chip_id'],actual_RAM_glyphs=8,actual_advance=88,record_restored=True,normal_PET_return=True,screenshot_directly_viewed=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},product_admitted=False,rom_written=False,release_eligible=False,limits=['Own Rockman host with quarantined GutsMan73 root/table aliases. Not natural character/script selection or battle acquisition.','Valid native chip record temporarily seeded at F90C and restored after actual reader; CPU evidence separately covers native source lookup/writer.','Displayed source Japanese page, not newly translated030 output. Chip-name value remains Japanese on this shared native path.','No final030 ROM, full Korean chip serialization, whole-game/persistence or hardware/audio claim.']))
    print('PASS030 native8 chip RAM/GBA glyphs,record restoration,PET return; no ROM written')

if __name__=='__main__':main()
