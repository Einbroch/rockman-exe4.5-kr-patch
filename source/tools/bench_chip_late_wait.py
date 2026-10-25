"""Execute guarded bridge and native wait instructions with modeled raster edges."""
import argparse
import itertools
import json
from bench_chip_library import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_CPU_ARM_TI925T, REGS
from build_visibility_poc import require_hash, sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rom', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    from pathlib import Path
    rom, out = Path(args.rom), Path(args.out)
    if out.exists():
        raise ValueError('refusing to overwrite evidence')
    m = json.loads(rom.with_suffix('.json').read_text())
    require_hash(rom, m['output_sha256'])
    e = m['chip_library_extension']['late_wait']
    data = rom.read_bytes()
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for address, size in ((0x08000000, (len(data)+4095)&~4095), (0x02000000, 0x40000),
                          (0x03000000, 0x8000), (0x04000000, 0x1000)):
        uc.mem_map(address, size)
    uc.mem_write(0x08000000, data)
    events = []
    served = [0]
    def observed(engine, address, size, user):
        if address == 0x08000374:
            events.append('wait-out')
            # Model the end of VBlank; native function still executes.
            engine.mem_write(0x04000004, b'\0\0')
        elif address == 0x08000344:
            events.append('wait-next')
            engine.mem_write(0x04000004, b'\1\0')
            engine.mem_write(e['counter'], served[0].to_bytes(4, 'little'))
        elif address == e['continuation'] & ~1:
            engine.emu_stop()
    for address in (0x08000374, 0x08000344, e['continuation'] & ~1):
        uc.hook_add(UC_HOOK_CODE, observed, begin=address, end=address)
    total, skipped = 0, 0
    for context, job, menu, phase, blank, counter, threshold in itertools.product(
            (e['context'], e['context']-64), (28,20), (8,0), (4,0), (0,1), (0,1,2), (0,1,2)):
        uc.mem_write(0x02000000, b'\0'*0x40000)
        uc.mem_write(e['context'], (0x0200FD50).to_bytes(4,'little'))
        uc.mem_write(e['context']+0x34, (0x0200F970).to_bytes(4,'little'))
        uc.mem_write(0x0200FD50, bytes([job]))
        uc.mem_write(0x0200F970, bytes([menu,phase]))
        uc.mem_write(e['counter'], counter.to_bytes(4,'little'))
        uc.mem_write(e['threshold'], threshold.to_bytes(4,'little'))
        uc.mem_write(0x04000004, bytes([blank,0]))
        before = [0x1230+n*4 for n in range(15)]
        before[10], before[13], before[14] = context, 0x03007000, 0x080002D7
        for reg, value in zip(REGS, before):
            uc.reg_write(reg, value)
        expected_skip = (context,job,menu,phase,blank,counter,threshold) == (e['context'],28,8,4,1,1,1)
        served[0] = counter if expected_skip else max(counter,threshold,1)
        events.clear()
        uc.emu_start(0x08000001+e['install'], 0, count=1000)
        expected_events = ['wait-next'] if expected_skip else ['wait-out','wait-next']
        after = [uc.reg_read(reg) for reg in REGS]
        if events != expected_events or after[3:14] != before[3:14] or after[14] != e['continuation']:
            raise ValueError(f'wait bridge ABI/decision failed: {context,job,menu,phase,blank,counter,threshold}; {events}; {after}')
        if after[:3] != [e['counter'],0,served[0]] or bytes(uc.mem_read(e['counter'],4)) != b'\0'*4:
            raise ValueError('native wait result/counter reset failed')
        total += 1
        skipped += int(expected_skip)
    report = {'rom_sha256': m['output_sha256'], 'tool_sha256': sha(Path(__file__).read_bytes()),
              'scope': 'synthetic raster/counter edges; bridge and native Thumb wait code execute; no runtime timing claim',
              'vectors': total, 'eligible_skip_vectors': skipped, 'all_guards_and_register_stack_outputs': True}
    out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('PASS late-wait guards/ABI:', total, 'vectors;', skipped, 'eligible skip')


if __name__ == '__main__':
    main()
