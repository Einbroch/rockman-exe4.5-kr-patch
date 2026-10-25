"""Bind captured evidence without upgrading partial runtime coverage to PASS."""
import json
from pathlib import Path
from audit_save_keyboard_fonts import ROOT, digest


def main():
    folder = ROOT / 'poc/runtime/save-keyboard-fonts-v1'
    out = folder / 'runtime_evidence.json'
    if out.exists():
        raise ValueError('preserve prior evidence')
    static = json.loads((folder / 'static_audit.json').read_text(encoding='utf-8'))
    product = ROOT / static['product']
    if digest(product.read_bytes()) != static['rom_sha256']:
        raise ValueError('runtime product drift')
    files = {p.name: dict(bytes=p.stat().st_size, sha256=digest(p.read_bytes()))
             for p in sorted(folder.iterdir()) if p.suffix in ['.png', '.mss', '.md']}
    report = dict(rom_sha256=static['rom_sha256'],
                  rom_sha1='6652EF823624279FF0289E45F6ECA0FCBC1FBF88',
                  launch_id='launch-01m4qrec9zgd07p90vm20nvj4k',
                  live_rom_identity_checked=True, normal_input_only=True,
                  observed=['initial settings', 'native Japanese name input/deletion/confirmation',
                            'profile name redisplay', 'Korean PET menu and selected dialogues',
                            'remaining Japanese initial UI/dialogues/calendar'],
                  automatic_hangul_input_tested=False, native_save_commit_tested=False,
                  fresh_process_native_save_reload_tested=False, release_eligible=False,
                  complete_integrated_request=False, evidence=files,
                  notes='Partial actual-ROM runtime inspection; see README for scope and failed save_state attempt.')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Indexed', len(files), 'evidence files; full keyboard/save request remains incomplete')


if __name__ == '__main__':
    main()
