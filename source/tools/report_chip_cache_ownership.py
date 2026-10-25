"""Bounded evidence for prospective tags; does not allocate or approve space."""
import json
from report_fixedcell_runtime import verify_route
from report_chip_library_stress import read, require
from survey_chip_library import source_assets
from build_visibility_poc import ROOT, require_hash, sha


def main():
    build = '403fc8670b32646ebe9a854ae3f3c194095311bd4966af70effd1e161fd9436a'
    m = read(ROOT / 'poc/output/exe45_ko_development_chip_wordcopy_v1.json')
    source = ROOT / read(ROOT / 'project.json')['source_profile']['filename']
    require_hash(source, m['source_sha256'])
    assets = source_assets(source.read_bytes())
    start, end = 0x06008E40, 0x06008EB0
    require(not any(a['destination'] < end and a['end'] > start for a in assets), 'initial asset overlap')
    # Mesen r15 at these Thumb write callbacks includes the pipeline +4.
    stores = {i['address'] + 4 for i in m['chip_library_extension']['machine_code'][0]['instructions'] if i['mnemonic'] in ('stm', 'stmia')}
    require(len(stores) == 8, 'store-site profile changed')
    rows = []
    for name in ('chip-wordcopy-cache-ownership', 'chip-wordcopy-cache-reentry'):
        p = ROOT / 'poc/runtime' / name
        verify_route(p, build, set())
        env = read(p / 'cache_ownership_environment.json')
        require_hash(ROOT / 'tools/capture_chip_cache_ownership.py', env['tool_sha256'])
        require_hash(ROOT / 'tools/capture_chip_library_probe.py', env['survey_tool_sha256'])
        require(env['positive_controls'] and not (p / 'ownership_failed.txt').exists(), 'observation controls failed')
        s = read(p / 'final_chip_survey.json')
        c = read(p / 'final_chip_ko.json')['verified_word_copies']
        require(s['candidate_write_count'] == c * 16, 'unexplained write count')
        require({x['pc'] for x in s['candidate_write_sites']} == stores, 'unknown cache-window writer')
        require(all(x['count'] == c * 2 for x in s['candidate_write_sites']), 'store distribution')
        refs = [x for x in s['candidate_map_tile_histogram'] if x['tile_address'] < end and x['tile_address'] + 32 > start]
        require(not refs, 'tag candidate has active BG references')
        loads = read(p / 'final_library.json')['loads']
        require(loads and all(x['outside_changed_bytes'] == 0 for x in loads), 'missing/invalid entry loader')
        rows.append({'route': name, 'result_sha256': sha((p / 'result.json').read_bytes()),
                     'checked_frames': s['checked_frames'], 'word_copies': c,
                     'explained_write_callbacks': s['candidate_write_count'],
                     'positive_map_write_callbacks': s['control_map_write_count'], 'loads': loads,
                     'candidate_bg_references': refs})
    report = {'rom_sha256': build, 'state': 'candidate-only; no allocation or cache implementation',
              'tag_interval': [start, end], 'bytes': 112, 'initial_assets_checked': len(assets), 'routes': rows,
              'limits': ['Frame-end BG maps cannot exclude transient mid-frame uses.',
                         'Write absence in proposed tags is inferred from all 8000..8FFF write sites/counts matching bounded verified glyph stores, not a separate tag-only watch.',
                         'No global-free claim: later name-entry graphics own this VRAM.',
                         'Conditional icon stress and candidate cache invalidation are not verified here.'],
              'proposed_contract': '56 uint16 tags: zero invalid, Hangul index+1 valid; reset at every 08042778 scene initialization after its asset loads. Publish a tag only after the complete 64-byte glyph copy. Guarded library consumer only.',
              'next': 'Build an explicit experimental cache candidate with reset hook and prove cold/miss/hit/change/reentry/foreign-write invalidation before promotion.'}
    (ROOT / 'analysis/exe45_chip_cache_ownership_v1.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Bounded candidate checks passed:', sum(x['checked_frames'] for x in rows), 'frames; allocation NOT adopted')


if __name__ == '__main__':
    main()
