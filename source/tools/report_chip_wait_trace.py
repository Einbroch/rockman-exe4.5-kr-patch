"""Locate observed missed wait boundary without changing native scheduling."""
import json
from report_chip_library_matrix import validate
from report_chip_library_stress import read, require
from report_fixedcell_runtime import verify_route
from build_visibility_poc import ROOT, sha


def summarize(events):
    selected = {e['pc']: e for e in events if e['group'] == 2}
    pcs = (0x08000374, 0x08000380, 0x08000344, 0x08000360)
    require(all(pc in selected for pc in pcs), 'missing wait boundary')
    a, b, c, d = [selected[pc] for pc in pcs]
    require(a['clock'] < b['clock'] < c['clock'] < d['clock'], 'event order')
    return {'entry_frame': a['frame'], 'entry_scanline': a['scanline'],
            'wait_non_vblank_clocks': b['clock'] - a['clock'],
            'wait_vblank_clocks': d['clock'] - c['clock'],
            'resume_frame': d['frame'], 'resume_scanline': d['scanline']}


def main():
    build = '403fc8670b32646ebe9a854ae3f3c194095311bd4966af70effd1e161fd9436a'
    rows = []
    for h in (0, 56):
        p = ROOT / f'poc/runtime/chip-wordcopy-wait{h}'
        r = verify_route(p, build, set())
        require(r.get('normal_play_checkpoint_eligible') is False and not (p / 'fixture_failed.txt').exists(), 'diagnostic fault')
        timing = read(p / 'final_timing.json')
        workload = validate(timing, read(p / 'final_stress.json'), h, 7)
        previous = read(ROOT / f'poc/runtime/chip-wordcopy-matrix-cold{h}/final_timing.json')
        previous_workload = validate(previous, read(ROOT / f'poc/runtime/chip-wordcopy-matrix-cold{h}/final_stress.json'), h, 7)
        require(workload['cadence_frames'] == previous_workload['cadence_frames'], 'cadence reproduction changed')
        require(workload['gap_after_group_1based'] == previous_workload['gap_after_group_1based'], 'gap position changed')
        rows.append({'hangul': h, 'state_sha256': r['state_sha256'], 'result_sha256': sha((p / 'result.json').read_bytes()),
                     'trace_tool_sha256_at_run': read(p / 'wait_trace_environment.json')['tool_sha256'],
                     'exact_timing_repeat': timing == previous,
                     'first_group_clock_difference': next(({'group_1based': i+1, 'clock_delta': a['start']['clock']-b['start']['clock']}
                         for i,(a,b) in enumerate(zip(timing['groups'], previous['groups'])) if a != b), None),
                     'wait': summarize(read(p / 'final_wait_trace.json')['events']), 'workload': workload})
    require(rows[0]['state_sha256'] == rows[1]['state_sha256'], 'state mismatch')
    report = {'scope': 'muted Mesen diagnostic, fixed ROM, same state; no scheduling modification',
              'issue': 'CHIP-CACHE-TIMING-001', 'status': 'OPEN',
              'repeatability_limit': 'Full clock traces are not identical to prior runs (first differences 315/304 clocks); cause not established. Cadence and gap position reproduce. Do not claim cycle-identical non-perturbation.',
              'ignored_fields': 'Historical counter/threshold labels were incorrect; raw addresses 0200F9F0/02010210 were read. Neither field is used for this conclusion. Observer now uses address labels.',
              'cause_boundary': '56-cell work returns to native 08000374 during VBlank; it waits out current VBlank then 08000344 waits for next VBlank. Zero-Hangul control arrives before VBlank.',
              'cases': rows}
    (ROOT / 'analysis/exe45_chip_wait_trace_v1.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
