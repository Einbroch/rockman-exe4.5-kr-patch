"""Exact-ROM native-name save/reset/fresh-load evidence, not Hangul support."""
import json
from pathlib import Path
from audit_save_keyboard_fonts import ROOT, digest


def validate_reload(result, before, snapshots, saved, after):
    if not result['complete'] or result['return_code'] != 0:
        raise ValueError('fresh process did not complete')
    if result['state_origin'] is not None or result['state_sha256'] is not None:
        raise ValueError('fresh native reload must not use a savestate')
    if len(before) != 14 or not snapshots or any(value != before for value in snapshots):
        raise ValueError('native name record changed across reload')
    if len(saved) != 65536 or after != saved:
        raise ValueError('native SAV missing, wrong size or modified')


def main():
    folder = ROOT / 'poc/runtime/save-keyboard-fonts-v1-save-regression'
    fresh = ROOT / 'poc/runtime/save-keyboard-fonts-v1-fresh-reload-r2'
    out = folder / 'persistence.json'
    if out.exists():
        raise ValueError('preserve prior evidence')
    product = ROOT / 'poc/output/exe45_ko_development_save_keyboard_fonts_v1.gba'
    manifest = json.loads(product.with_suffix('.json').read_text(encoding='utf-8'))
    if digest(product.read_bytes()) != manifest['output_sha256']:
        raise ValueError('ROM identity mismatch')
    result = json.loads((fresh / 'result.json').read_text(encoding='utf-8'))
    if result['rom_sha256'] != manifest['output_sha256']:
        raise ValueError('fresh process used a different ROM')
    deps = json.loads((ROOT / 'project.json').read_text(encoding='utf-8'))['development_dependencies']['runtime_capture']
    if result['emulator_sha256'] != deps['mesen_sha256']:
        raise ValueError('fresh process environment mismatch')
    if digest((ROOT / deps['tool']).read_bytes()) != deps['tool_sha256']:
        raise ValueError('capture tool drift')
    # Independent live read_memory observations before and after Control reset.
    before = bytes.fromhex('019be57ee5000000000000000000')
    snapshots = []
    files = [product.with_suffix('.json'), folder / 'native_commit.sav', folder / 'native_commit.rtc', fresh / 'result.json']
    for step in (2, 3, 6):
        path = fresh / f'step_{step:03d}_gbaExtWorkRam.bin'
        data = path.read_bytes()
        if len(data) != 0x40000 or digest(data) != result['artifacts'][path.name]:
            raise ValueError('fresh snapshot identity/extent')
        snapshots.append(data[0xE50:0xE5E])
        files.extend([path, fresh / f'step_{step:03d}.png'])
    saved = (folder / 'native_commit.sav').read_bytes()
    after_path = ROOT / 'poc/runtime/chip-matrix-saves' / (product.stem + '.sav')
    validate_reload(result, before, snapshots, saved, after_path.read_bytes())
    report = dict(rom_sha256=manifest['output_sha256'], native_name='あ',
                  native_record_address='0x02000E50', native_record_bytes=14,
                  native_record_hex=before.hex(), save_ui_completion_observed=True,
                  control_reset_reload_observed=True, fresh_process_reload_verified=True,
                  fresh_process_used_savestate=False, native_sav_bytes=len(saved),
                  native_sav_sha256=digest(saved), native_sav_unchanged_after_fresh_reload=True,
                  screenshots_assistant_inspected=True, user_saves_touched=False,
                  hangul_input_installed=False, hangul_persistence_verified=False,
                  complete_integrated_request=False, release_eligible=False,
                  artifacts={str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in files},
                  limits=['Only the Japanese one-character native player-name record was tested.',
                          'Fresh process was seeded with the exact game-generated SAV/RTC from this ROM.',
                          'Other record fields, composed Hangul, calendar titles and all consumers remain unverified.',
                          'Control reset and fresh testRunner used distinct pinned emulator environments.'])
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS actual native Japanese name save/reset/fresh-process reload; Hangul support pending')


if __name__ == '__main__':
    main()
