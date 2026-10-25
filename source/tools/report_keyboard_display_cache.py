"""Verify the observed editor provider -> native cache -> parser boundary."""
import json
import struct
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read, verify_route
from extended_dialogue import Cs, CS_ARCH_ARM, CS_MODE_THUMB


def main():
    identity = '5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    route = ROOT / 'poc/runtime/hangul-keyboard-v1-display-cache-r3'
    result = verify_route(route, identity, set())
    rom_path = Path(result['rom_path'])
    require_hash(rom_path, identity)
    rom = rom_path.read_bytes()
    profile = read(ROOT / 'project.json')['source_profile']
    source = ROOT / profile['filename']
    require_hash(source, profile['sha256'])
    original = source.read_bytes()
    env = read(route / 'display_cache_environment.json')
    for name, key in [('capture_keyboard_display_cache.py', 'tool_sha256'),
                      ('capture_keyboard_native.py', 'native_observer_sha256')]:
        require_hash(ROOT / 'tools' / name, env[key])
    if not env['observer_only'] or not env['no_RAM_or_save_injection']:
        raise ValueError('unexpected intervention')
    trace = read(route / 'step_023_display_cache.json')
    copies, consumption = trace['copies'], trace['consumption']
    if not copies or len(copies) != len(consumption):
        raise ValueError('missing provider or consumption')
    consumers = {p['copy']: p for p in consumption}
    if len(consumers) != len(copies):
        raise ValueError('ambiguous copy/consumer correlation')
    for index, row in enumerate(copies, 1):
        if (row['source'], row['destination'], row['length'], row['context'],
                row['slot'], row['result_pointer'], row['next_slot']) != (
                    0x0200FC80, 0x020155F0, 32, 0x0200FBE0, 0, 0x020155F0, 1):
            raise ValueError('observed provider ABI changed')
        src = bytes.fromhex(row['source_hex'])
        if len(src) != 32 or bytes.fromhex(row['after_hex'])[:32] != src:
            raise ValueError('source -> cache byte mismatch')
        # These observed native streams contain no multibyte/control payloads;
        # this comparison is not a general game-text parser.
        end = src.index(0xE5) + 1
        if end != 5 or any(b >= 0xE4 for b in src[:end - 1]):
            raise ValueError('outside observed single-byte stream class')
        consumed = consumers[index]
        expected = ','.join(f'{0x020155F0 + i:08x}:{b:02x}' for i, b in enumerate(src[:end]))
        if (consumed['frame'] != row['frame'] or consumed['pc'] != 0x0300684A
                or consumed['reads'] != expected):
            raise ValueError('cache -> parser read mismatch')
        if row['copy_return_lr'] != 0x03006A4C or row['copy_return_sp'] != row['sp'] - 4:
            raise ValueError('copy return/shim stack changed')
        events = [p for p in trace['slot_writes'] if p['frame'] == row['frame']]
        event_pairs = [(p['pc'], p['value']) for p in events]
        if ((0x03006838, 0) not in event_pairs or (0x03006A58, 1) not in event_pairs
                or (0x030068E2, 0) not in event_pairs):
            raise ValueError('per-render cache counter lifecycle missing')
    iwram = (route / 'step_004_gbaIntWorkRam.bin').read_bytes()
    # Bind resident routines/literals to their exact immutable ROM origin.
    ranges = [(0x6824, 0x6882), (0x68D8, 0x68E8), (0x6A1C, 0x6A78)]
    regions = []
    for start, end in ranges:
        offset = 0x1E8F00 + start
        blob = iwram[start:end]
        if blob != rom[offset:offset + len(blob)] or blob != original[offset:offset + len(blob)]:
            raise ValueError('resident native code/literal provenance')
        regions.append(dict(IWRAM_start=hex(0x03000000 + start), source_offset=hex(offset),
                            bytes=len(blob), sha256=sha(blob)))
    if struct.unpack_from('<III', iwram, 0x6A68) != (0x080526D0, 0x0800094D, 0x020155F0):
        raise ValueError('descriptor/helper/cache literals')
    if struct.unpack_from('<I', iwram, 0x6A74)[0] != 0x0200FBE0:
        raise ValueError('context literal')
    if struct.unpack_from('<II', original, 0x526D0) != (0x0200FC80, 32):
        raise ValueError('descriptor0 source identity')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    code = {i.address: i for i in decoder.disasm(iwram[0x6A1C:0x6A66], 0x03006A1C)}
    if code[0x03006A38].mnemonic != 'lsls' or code[0x03006A38].op_str != 'r2, r2, #7':
        raise ValueError('native slot stride not 128')
    snapshots = []
    for step in result['capture_steps']:
        ram = (route / f'step_{step:03d}_gbaExtWorkRam.bin').read_bytes()
        snapshots.append(dict(step=step, script=ram[0xFA21], mode=ram[0xFC40],
                              words_hex=ram[0xFC60:0xFC70].hex(), record_hex=ram[0x10A6:0x10B0].hex()))
    bystep = {p['step']: p for p in snapshots}
    if (bystep[14]['mode'], bystep[17]['mode'], bystep[21]['script']) != (16, 12, 93):
        raise ValueError('No/Yes route incomplete')
    if not (bystep[5]['words_hex'] == bystep[10]['words_hex'] == bystep[17]['words_hex']
            and bystep[8]['words_hex'] != bystep[10]['words_hex']
            and bystep[21]['record_hex'].startswith('019be5')):
        raise ValueError('edit/delete/No/native commit changed')
    report = dict(
        id='exe45.hangul-keyboard.display-cache-observation.v1', passed=True,
        rom_integrated=False, rom_sha256=identity, source_sha256=profile['sha256'],
        claim='native descriptor0 copy and same-render cache consumption on the observed Japanese editor route',
        route=str(route.relative_to(ROOT)).replace('\\', '/'), copies=len(copies),
        provider=dict(source='0x0200fc80', bound=32, destination='0x020155f0',
                      context='0x0200fbe0', slot=0, slot_stride=128,
                      result_field='+0x24', counter_field='+0x30',
                      entry='0x03006a1c', copy_call='0x03006a4a', copy_return='0x03006a4c'),
        consumption=dict(parser='0x0300684a', matched_copies=len(consumption),
                         same_render=True, bytes_per_observed_stream=5,
                         streams=sorted({p['source_hex'] for p in copies}),
                         counter_reset_before='0x03006838', counter_reset_at_end='0x030068e2'),
        native_regions=regions, snapshots=snapshots,
        tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in
               ['capture_keyboard_display_cache.py', 'report_keyboard_display_cache.py']},
        artifacts={str(p.relative_to(ROOT)).replace('\\', '/'): sha(p.read_bytes()) for p in
                   [route / 'result.json', route / 'display_cache_environment.json',
                    route / 'step_023_display_cache.json']},
        limits=['128-byte stride is verified, not a global allocator/free-RAM or all-slot capacity proof.',
                'The observed parser consumed native single-byte Japanese/space streams, not F9FC Hangul output.',
                'No automatic input/display/record/save hooks installed; existing ROM and user saves preserved.'],
        next='Use this native destination/lifecycle for the coordinated compact-state display bridge; establish initializer/import/confirm baseline and stack before installation.')
    (ROOT / 'analysis/hangul_keyboard_v1/display_cache.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print(f'PASS {len(copies)} descriptor0 copies and same-render parser consumptions; native cache/counter provenance verified')


if __name__ == '__main__':
    main()
