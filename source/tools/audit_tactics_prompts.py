"""Read-only source audit and exact-candidate native reboot evidence."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from verify_tpi_index import parse_tpi
from archive_scripts import script_spans
from tpl_literals import literals
from report_chip_library_runtime import read, require


def main():
    project = read(ROOT / 'project.json')
    source = ROOT / project['source_profile']['filename']
    expected = '588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8'
    require_hash(source, expected)
    native = source.read_bytes()
    row = next(r for r in parse_tpi(ROOT / 'external/textpet-indexes/exe45.tpi') if r['offset'] == 0x76C944)
    require(not row['compressed'] and not row['size_header'], 'unsupported source pool')
    pool = native[row['offset']:row['offset'] + row['size']]
    require(struct.unpack_from('<H', pool)[0] == 288, '144-script table boundary')
    spans = script_spans(pool, 144)
    texts = {l.key: l.text for l in literals((ROOT / 'analysis/tpl_baseline/76C944.tpl').read_text(encoding='utf-8-sig'))}
    require(texts['76C944:0:0'] == 'どのてきを\nねらう?', 'target prompt source drift')
    require(texts['76C944:1:0'] == 'てきとの\nまあいは?', 'distance prompt source drift')
    roots = [i for i in range(0, len(native)-3, 4) if struct.unpack_from('<I', native, i)[0] == 0x0876C944]
    require(roots == [0x212E8], 'source aligned root set drift')
    route = ROOT / 'poc/runtime/battle-names-v1-native-reboot'
    env = read(route / 'save_environment.json')
    result = read(route / 'result.json')
    require(env['build_sha256'] == '0f40221f833afe835f9c5ad0eb7fac12570b8ca800fc9b5632916aa88742600e', 'reboot candidate drift')
    before, after = env['files_before'], env['files_after']
    key = 'exe45_ko_development_battle_names_v1.sav'
    require(before[key] == after[key], 'own save changed on reboot')
    require(before[key]['sha256'] == '0619f62e766994fb66b231336417961a6453391393f0ba94776dbd74fb5ac59f', 'own native save identity')
    require(all(after.get(k) == v for k, v in before.items() if k.endswith('.sav')), 'other saves changed')
    report = {
        'source_sha256': expected, 'pool': row, 'pool_sha256': sha(pool),
        'script_count': 144, 'aligned_pointer_roots': roots,
        'scripts': [{'script': i, 'sha256': sha(spans[i]), 'text': texts.get(f'76C944:{i}:0')} for i in range(144)],
        'next_scope': {'scripts': [0, 1], 'geometry': [5, 2], 'drafts_not_installed': ['어느 적을\n노릴까?', '적과의\n거리는?']},
        'native_reboot': {'candidate_sha256': env['build_sha256'], 'save': before[key], 'all_existing_sav_preserved': True, 'result_sha256': sha((route/'result.json').read_bytes()), 'terminal_screenshot_sha256': sha((route/'step_011.png').read_bytes())},
        'limits': ['Aligned pointer scan does not exclude computed or unaligned references.', '5x2 path is Navi TACTICS speech, not an enemy-name field.', 'Only scripts0/1 are proposed; escape dialog and other Navi styles remain native.', 'No translated prompt build or runtime proof yet.', 'Reboot screenshot manually inspected: normal PET and native speech; not whole-game or release QA.']
    }
    out = ROOT / 'analysis/exe45_tactics_prompt_source_audit_v1.json'
    require(not out.exists(), 'refuse overwrite')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('144 source scripts audited; root212E8; native candidate reboot SAV preserved')


if __name__ == '__main__':
    main()
