"""Audit cumulative save-UI/font ROM; never claim installed keyboard/save ABI."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def audit(product, baseline):
    def load(path):
        data = path.read_bytes()
        manifest = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
        if digest(data) != manifest['output_sha256']:
            raise ValueError('product hash mismatch')
        return data, manifest

    rom, manifest = load(product)
    _, old = load(baseline)
    profile = json.loads((ROOT / 'project.json').read_text(encoding='utf-8'))['source_profile']
    source = (ROOT / profile['filename']).read_bytes()
    if digest(source) != profile['sha256'] or manifest['source_sha256'] != profile['sha256']:
        raise ValueError('immutable source mismatch')
    if manifest['source_sha256'] != old['source_sha256']:
        raise ValueError('baseline source mismatch')
    if manifest['translated_units'] != old['translated_units']:
        raise ValueError('translation scope changed')
    if manifest['translation_assets'] != old['translation_assets']:
        raise ValueError('selected wording/input lineage changed')
    if not manifest['final_diff_audited'] or not manifest['header_unchanged']:
        raise ValueError('primary builder final-write audit missing')
    glyphs = manifest['hangul_keyboard_glyphs']
    # The font extension does not authorize native input/commit code changes.
    native = []
    for start, end in [(0x34FA0, 0x35050), (0x32AC6, 0x32AD8),
                       (0x37366, 0x3739A), (0x33334, 0x33398)]:
        if source[start:end] != rom[start:end]:
            raise ValueError('native keyboard/calendar boundary unexpectedly changed')
        native.append(dict(start=start, end=end, sha256=digest(rom[start:end])))
    return dict(schema=1, product=str(product.relative_to(ROOT)),
                rom_sha256=digest(rom), rom_bytes=len(rom),
                source_sha256=digest(source), baseline_sha256=old['output_sha256'],
                translated_units=manifest['translated_units'],
                selected_assets_identical=True, primary_final_diff_audited=True,
                glyph_supply=glyphs, unchanged_native_boundaries=native,
                automatic_keyboard_installed=False, hangul_save_abi_installed=False,
                runtime_tested=False, complete_integrated_request=False,
                limits=['Static audit only; runtime observations belong to a separate record.',
                        'Existing save UI plus font supply; not automatic Hangul input or persistence.',
                        'Unregistered translation drafts remain outside this ROM.'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rom', required=True)
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = ROOT / args.out
    if out.exists():
        raise ValueError('preserve prior evidence')
    report = audit(ROOT / args.rom, ROOT / args.baseline)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS cumulative save UI/font scope; input and Hangul persistence NOT installed')


if __name__ == '__main__':
    main()
