"""Freeze024 investigation, preserved artifacts and B1 duplicate evidence."""
import struct
import subprocess
import sys
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from verify_tpi_index import lz77_decompress, parse_tpi


def main():
    cfg = read('project.json')
    source_path = cfg['source_profile']['filename']
    require_hash(ROOT/source_path, cfg['source_profile']['sha256'])
    source = (ROOT/source_path).read_bytes()
    base = 'poc/output/pending500_023_v1.gba'
    require_hash(ROOT/base, '6e6d9104db33fd927714b4a06cd6a1093fd4b6ef6d4f77c6ecd206daa44a39ec')
    rom = (ROOT/base).read_bytes()
    authority = read('analysis/pending500_023_v1/batch_status.json')
    if sha(rom) not in str(authority):
        raise ValueError('023 authority identity')
    expected = (0x08054238, 0x08054294, 0x080542F0)
    if struct.unpack_from('<3I', source, 0x54060) != expected or source[0x54060:0x5434C] != rom[0x54060:0x5434C]:
        raise ValueError('B0/B1 bounded table identity')
    require_hash(ROOT/cfg['text_catalog']['path'], cfg['text_catalog']['sha256'])
    known = {r['offset'] for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    aliases = []
    for navi in range(23):
        p0, p1 = (struct.unpack_from('<I', source, table+navi*4)[0] for table in (0x54238, 0x54294))
        if not p0 or not p1:
            if navi not in (13, 14) or p0 != p1:
                raise ValueError('B0/B1 null slots')
            continue
        off0, off1 = p0-0x08000000, p1-0x08000000
        raw0, used0 = lz77_decompress(source, off0)
        raw1, used1 = lz77_decompress(source, off1)
        if raw0 != raw1 or source[off0:off0+used0] != rom[off0:off0+used0] or source[off1:off1+used1] != rom[off1:off1+used1]:
            raise ValueError('B1 decoded alias or unchanged native storage')
        aliases.append(dict(navi=navi, b0_archive=f'{off0:X}', b1_archive=f'{off1:X}', decoded_bytes=len(raw0), decoded_sha256=sha(raw0), b1_compressed_bytes=used1, b1_compressed_sha256=sha(source[off1:off1+used1]), b1_exact_catalog_row=off1 in known, whole_payload_identical=True, counted_new_units=0))
    if len(aliases) != 21:
        raise ValueError('B1 denominator')
    reports = ['analysis/pending_insertion_500_024_survey_v1/survey.json', 'analysis/pending_insertion_500_024_fullbox_v1/survey.json', 'analysis/pending_insertion_500_024_quick_v1/survey.json', 'analysis/pending_insertion_500_024_quick_reflow_v2/survey.json']
    for p in reports:
        r = read(p)
        if r['baseline_sha256'] != sha(rom) or r['rom_written'] or r['selected500'] is not None:
            raise ValueError('Analysis-only report scope')
    full, quick = read(reports[1]), read(reports[3])
    full_ids = {k for g in full['candidate_groups'] for k in g['ids']}
    quick_ids = {k for g in quick['candidate_groups'] for k in g['ids']}
    if full_ids & quick_ids or len(full_ids) != 187 or len(quick_ids) != 85:
        raise ValueError('Distinct analysis candidates')
    tests = subprocess.run([sys.executable, '-X', 'utf8', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_pet_quick_capacity_024.py', '-v'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if tests.returncode or 'Ran 14 tests' not in tests.stderr:
        raise ValueError(tests.stdout+tests.stderr)
    protected = {source_path: cfg['source_profile']['sha256'], base: sha(rom), 'poc/output/pending500_022_v2.gba': '7363567b1263dac0700e2430da1046e47aa9ba65c8d9c2125b1ab9b3bd2928a1', 'patches/exe45_ko_development_news_mail_20261013.zip': '2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6'}
    for p, h in protected.items():
        require_hash(ROOT/p, h)
    deps = reports+['tools/survey_fullbox_insertions_024.py', 'tools/pet_quick_capacity.py', 'tools/survey_pet_quick_024.py', 'tools/survey_pet_quick_reflow_024.py', 'tools/test_pet_quick_capacity_024.py', 'tools/checkpoint_pending024.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_024_checkpoint_v1/checkpoint.json', dict(schema=1, status='INVESTIGATION_CONTINUES_NO_NEW_ROM', baseline_rom=base, baseline_sha256=sha(rom), verified_translated_units=12622, dependencies={p:sha((ROOT/p).read_bytes()) for p in deps}, preserved_artifacts=protected, b1_aliases=aliases, b1_counted_new_units=0, fullbox_candidate_units=187, quick_proposed_reflow_candidate_units=85, distinct_analysis_candidate_units=272, requested_batch_units=500, selected500=None, test_output=tests.stderr, test_count=14, tests_passed=True, rom_written=False, new_rom_units=0, package_written=False, prose_changed=False, release_eligible=False, next_action='Establish actual LF/clear lifetime and source-bound compiler policy on a representative PET quick paragraph before admitting the proposed85. Analyze msgOpen-before-mugshot source consumers and other unresolved classes for the remainder; do not relax unmodeled command gates to reach500.', limits='These are candidate layout/command checks, not product admission, translated-unit increments, a whole-game remainder count, or runtime validation. Earlier zero-quick report predates analysis-only terminal waitHold modeling; it is historical negative evidence, not a current model invocation. B1 scene is not selected by023 B0 wrapper. Automatic Hangul commit/save/redisplay, date HUD, inherited leading and semantic review remain open.'))
    print('024 checkpoint: source/023/022/ZIP unchanged;21 B1 aliases excluded;272 analysis candidates;14 tests PASS;new ROM0')


if __name__ == '__main__':
    main()
