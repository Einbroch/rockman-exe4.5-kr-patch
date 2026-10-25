"""Bind positive native initializer and unchanged-until-commit observations."""
import json
import struct
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read, verify_route


def main():
    identity = '5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    route = ROOT / 'poc/runtime/hangul-keyboard-v1-lifecycle'
    result = verify_route(route, identity, set())
    rom_path = Path(result['rom_path'])
    require_hash(rom_path, identity)
    rom = rom_path.read_bytes()
    profile = read(ROOT / 'project.json')['source_profile']
    source_path = ROOT / profile['filename']
    require_hash(source_path, profile['sha256'])
    source = source_path.read_bytes()
    env = read(route / 'lifecycle_environment.json')
    require_hash(ROOT / 'tools/capture_keyboard_lifecycle.py', env['tool_sha256'])
    require_hash(ROOT / 'tools/capture_keyboard_native.py', env['native_observer_sha256'])
    if not env['observer_only'] or not env['no_RAM_or_save_injection']:
        raise ValueError('unexpected intervention')
    events = read(route / 'step_038_lifecycle.json')['events']
    if [e['pc'] for e in events] != [0x080355B6, 0x080355C4, 0x080355F4, 0x08035000]:
        raise ValueError('outside observed empty-entry initializer/commit class')
    entry, cleared, finished, commit = events
    if (entry['r0'], entry['r1'], entry['r2'], entry['r3'], entry['lr']) != (4, 33, 0x020010A6, 0, 0x08038DA7):
        raise ValueError('initializer ABI')
    if len({e['frame'] for e in events[:3]}) != 1 or bytes.fromhex(cleared['edit_hex']) != bytes(96):
        raise ValueError('initializer clear boundary')
    edit = bytes.fromhex(finished['edit_hex'])
    if edit[4:6] != bytes([4, 33]) or struct.unpack_from('<4I', edit, 16) != (
            0x0200FC60, 0x0200FC60, 0x0200FC60, 0x020010A6):
        raise ValueError('initializer destination/pointers')
    before = entry['record_hex']
    if before != '007e7e7ee50000000000' or any(e['record_hex'] != before for e in events):
        raise ValueError('record changed before commit entry')
    trace = read(route / 'step_038_keyboard.json')
    writes = [w for w in trace['writes'] if 0x020010A6 <= w['address'] < 0x020010B0]
    if not writes or any(w['frame'] < commit['frame'] for w in writes):
        raise ValueError('precommit record write observed')
    native_writes = [w for w in writes if w['frame'] == commit['frame']]
    if [(w['pc'], w['address'], w['value']) for w in native_writes] != [
            (0x0803500C, 0x020010A6, 1), (0x0803501E, 0x020010A7, 0x9B),
            (0x08035026, 0x020010A8, 0xE5)]:
        raise ValueError('native record commit changed')
    snapshots = {}
    for step in result['capture_steps']:
        ram = (route / f'step_{step:03d}_gbaExtWorkRam.bin').read_bytes()
        snapshots[step] = dict(mode=ram[0xFC40], script=ram[0xFA21],
                               words=ram[0xFC60:0xFC70].hex(), record=ram[0x10A6:0x10B0].hex())
    if (snapshots[29]['mode'], snapshots[32]['mode'], snapshots[36]['script']) != (16, 12, 93):
        raise ValueError('No/Yes route')
    if snapshots[20]['words'] != snapshots[25]['words'] or snapshots[25]['words'] != snapshots[32]['words']:
        raise ValueError('B/No draft preservation')
    if any(p['record'] != before for n, p in snapshots.items() if n <= 32):
        raise ValueError('record not immutable over observed edit/No snapshots')
    guards = []
    for a, b in [(0x3558C, 0x3564E), (0x38D8E, 0x38DB2), (0x35000, 0x35032)]:
        if source[a:b] != rom[a:b]:
            raise ValueError('native initializer/caller/commit code changed')
        guards.append(dict(start=hex(a), end=hex(b), sha256=sha(source[a:b])))
    report = dict(id='exe45.hangul-keyboard.lifecycle-observation.v1', passed=True,
                  rom_integrated=False, rom_sha256=identity, source_sha256=profile['sha256'],
                  initializer=dict(entry='0x080355b6', caller='0x08038da2', observed=True,
                                   capacity=4, heading_script=33, destination='0x020010a6',
                                   clear_bytes=96, entry_sp=hex(entry['sp'])),
                  original_record=dict(before=before, marker=0,
                                       unchanged_through_edit_and_No=True,
                                       first_observed_write_frame=commit['frame']),
                  import_observed=False, native_guards=guards, events=events,
                  snapshots=snapshots, observed_record_writes=writes,
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in
                         ['capture_keyboard_lifecycle.py', 'report_keyboard_lifecycle.py']},
                  artifacts={str(p.relative_to(ROOT)).replace('\\', '/'): sha(p.read_bytes()) for p in
                             [route / 'result.json', route / 'lifecycle_environment.json',
                              route / 'step_038_lifecycle.json', route / 'step_038_keyboard.json']},
                  limits=['Normal marker0 weak-subject route only; imported nonempty records and other fields remain unverified.',
                          'Native initializer stack measurement is not the input-handler/IRQ stack budget.',
                          'No Hangul hooks, marker migration, save or fresh-load proof.'],
                  next='Derive immutable baseline on each call from the unmodified record; connect import and coordinated editor/display/commit hooks, then verify actual stack and persistence.')
    (ROOT / 'analysis/hangul_keyboard_v1/lifecycle.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS observed native initialization; original record unchanged through B/No until commit; nonempty import pending')


if __name__ == '__main__':
    main()
