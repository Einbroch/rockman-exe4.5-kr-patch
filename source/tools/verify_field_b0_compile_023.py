"""Mechanical source compilation only; never author or admit a product ROM."""
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash, run_textpet, bdf_glyphs, FONT_SHA256
from cumulative_batch500 import read, frozen_write
from verify_tpi_index import lz77_decompress
from tpl_literals import literals, skeleton, replace_literals
from textpet_korean import prepare_plugins, command
from korean_codec import HANGUL_BASE, HANGUL_COUNT, EXTRA_CHARACTER_INDICES, EXTRA_CHARACTER_METRICS
from archive_scripts import verify_untouched_scripts

PREP = 'analysis/pending_insertion_500_023_b0_reuse_v1'
OUT = 'analysis/pending_insertion_500_023_b0_compile_v3'


def ref(path):
    return dict(path=str(path.relative_to(ROOT)), sha256=sha(path.read_bytes()))


def main():
    selection_path = ROOT / PREP / 'selection.json'
    selected = read(str(selection_path.relative_to(ROOT)))
    prepared_path = ROOT / PREP / 'prepared_inputs.json'
    prepared = read(str(prepared_path.relative_to(ROOT)))
    require_hash(ROOT / selected['survey']['path'], selected['survey']['sha256'])
    survey = read(selected['survey']['path'])
    require_hash(ROOT / survey['extraction']['path'], survey['extraction']['sha256'])
    extraction = read(survey['extraction']['path'])
    sources = {r['archive']: r for r in extraction['archives']}
    config = read('project.json')
    source_path = ROOT / config['source_profile']['filename']
    require_hash(source_path, selected['source_sha256'])
    source = source_path.read_bytes()
    baseline_path = ROOT / selected['baseline_rom']
    require_hash(baseline_path, selected['baseline_sha256'])
    baseline = baseline_path.read_bytes()
    meta = read(str(baseline_path.with_suffix('.json').relative_to(ROOT)))
    if (selected['total_new_units'] != 500 or prepared['total_units'] != 500
            or selected['rom_written'] or selected['insertion_ready']
            or selected['release_eligible'] or prepared['insertion_ready']):
        raise ValueError('Source-only selection policy changed')
    work = ROOT / OUT
    work.mkdir(parents=True, exist_ok=False)
    plugins = work / 'plugins'
    plugin_report = prepare_plugins(plugins, set(EXTRA_CHARACTER_INDICES))
    common = command(plugins)
    records, all_ids, chars = [], set(), set()
    for row in prepared['archives']:
        require_hash(ROOT / row['path'], row['sha256'])
        asset = read(row['path'])
        arc = asset['archive']
        src = sources[arc]
        require_hash(ROOT / src['source_tpl']['path'], src['source_tpl']['sha256'])
        if asset['source_tpl'] != src['source_tpl'] or asset['source_archive_sha256'] != src['source_payload_sha256']:
            raise ValueError('New source identity changed')
        link_ref = asset['source_draft_links']['selection']
        if ((ROOT / link_ref['path']).resolve() != selection_path.resolve()
                or link_ref['sha256'] != sha(selection_path.read_bytes())):
            raise ValueError('Selection reference changed')
        groups = [g for g in selected['groups'] if g['archive'] == arc]
        expected_links = [link for g in groups for link in g['links']]
        if asset['source_draft_links']['links'] != expected_links:
            raise ValueError('Canonical wording reference set changed')
        expected_units = {}
        for link in expected_links:
            parent = link['parent']
            require_hash(ROOT / parent['path'], parent['sha256'])
            donor = next(u for u in read(parent['path'])['units'] if u['id'] == parent['unit_id'])
            expected_units[link['id']] = dict(id=link['id'], source=link['source'], translation=donor['translation'], state=donor['state'])
        if {u['id']: u for u in asset['units']} != expected_units:
            raise ValueError('Derived wording projection changed')
        units = asset['units']
        ids = {u['id'] for u in units}
        if len(ids) != row['units'] or all_ids & ids or any(u['state'] != 'needs_review' for u in units):
            raise ValueError('Distinct needs-review population changed')
        all_ids |= ids
        chars |= set(''.join(u['translation'] for u in units))
        offset = int(arc, 16)
        native, consumed = lz77_decompress(source, offset)
        if sha(native) != src['source_payload_sha256'] or consumed != src['compressed_bytes_consumed']:
            raise ValueError('Protected native payload changed')
        if baseline[offset:offset + consumed] != source[offset:offset + consumed]:
            raise ValueError('Baseline compressed source storage changed')
        original = (ROOT / src['source_tpl']['path']).read_text(encoding='utf-8-sig')
        target = replace_literals(original, units)
        folder = work / arc
        folder.mkdir()
        tpl = folder / (arc + '.tpl')
        compiled = folder / (arc + '.msg')
        reexport = folder / 'reexport.tpl'
        rebuilt = folder / 'rebuilt.msg'
        tpl.write_text(target, encoding='utf-8', newline='\n')
        run_textpet(common + ['Read-Text-Archives', str(tpl), '--format', 'tpl', 'Write-Text-Archives', str(compiled), '--format', 'bin'], folder / 'compile.log')
        run_textpet(common + ['Read-Text-Archives', str(compiled), '--format', 'bin', 'Write-Text-Archives', str(reexport), '--format', 'tpl'], folder / 'reexport.log')
        run_textpet(common + ['Read-Text-Archives', str(reexport), '--format', 'tpl', 'Write-Text-Archives', str(rebuilt), '--format', 'bin'], folder / 'rebuild.log')
        exported = reexport.read_text(encoding='utf-8-sig')
        payload = compiled.read_bytes()
        if rebuilt.read_bytes() != payload or skeleton(original) != skeleton(exported):
            raise ValueError('Binary roundtrip or protected controls changed')
        if [(u.key, u.language, u.text) for u in literals(target)] != [(u.key, u.language, u.text) for u in literals(exported)]:
            raise ValueError('Re-extracted complete literal stream changed')
        scripts = {int(k.split(':')[1]) for k in ids}
        kept = verify_untouched_scripts(native, payload, 255, scripts)
        records.append(dict(archive=arc, units=len(ids), selected_ids=sorted(ids), source_bytes=len(native), compiled_bytes=len(payload), growth_bytes=len(payload)-len(native), source_payload_sha256=sha(native), compiled=ref(compiled), reexport=ref(reexport), rebuilt=ref(rebuilt), translated_tpl=ref(tpl), exact_wording_links=True, protected_controls_unchanged=True, unselected_scripts=kept, binary_roundtrip=True))
        print('PASS mechanical', arc, len(ids), len(native), '->', len(payload), flush=True)
    if len(all_ids) != 500:
        raise ValueError('Not exact500')
    font = ROOT / 'external/fonts/Galmuri11.bdf'
    require_hash(font, FONT_SHA256)
    wanted = {ch for ch in chars if HANGUL_BASE <= ord(ch) < HANGUL_BASE + HANGUL_COUNT or ch in EXTRA_CHARACTER_INDICES}
    glyphs = bdf_glyphs(font, wanted, {ch: m['vertical_shift'] for ch, m in EXTRA_CHARACTER_METRICS.items()})
    extension = meta['extension']
    if extension['legacy_index_view'] != 442:
        raise ValueError('Actual font index view changed')
    glyph_report = []
    for ch, glyph in sorted(glyphs.items()):
        index = (EXTRA_CHARACTER_INDICES[ch] if ch in EXTRA_CHARACTER_INDICES else ord(ch) - HANGUL_BASE) + 442
        at = extension['normal_font_offset'] + index * 96
        width_at = extension['advance_offset'] + index * 4
        if baseline[at:at+96] != glyph or int.from_bytes(baseline[width_at:width_at+4], 'little') != 12:
            raise ValueError('Actual baseline glyph/advance mismatch: ' + ch)
        glyph_report.append(dict(character=ch, index=index, offset=at, glyph_sha256=sha(glyph), advance=12))
    # Source-only compilation must not mutate either protected ROM.
    require_hash(source_path, selected['source_sha256'])
    require_hash(baseline_path, selected['baseline_sha256'])
    classes = Counter()
    for g in selected['groups']:
        classes[g['technical_class']] += g['units']
    report = dict(schema=1, status='MECHANICAL_COMPILE_PASS_NOT_ROM_ADMISSION', passed=True, scope='exact selected500 source-bound context-reuse units only', selection=ref(selection_path), prepared_inputs=ref(prepared_path), extraction=survey['extraction'], source_sha256=sha(source), baseline_rom=selected['baseline_rom'], baseline_sha256=sha(baseline), baseline_manifest=ref(baseline_path.with_suffix('.json')), units=500, archives=records, plugin=plugin_report, selected_extended_glyphs_in_actual_baseline=glyph_report, all_literal_streams_and_controls_roundtrip=True, unselected_script_bytes_preserved=True, units_by_technical_class=dict(classes), geometry_pass=False, aggregate_variables_pass=False, reader_registration=False, runtime_tested=False, rom_written=False, insertion_ready=False, release_eligible=False, limits='Mechanical compilation and existing glyph supply only. Canonical LF/wording retained without candidate layout edits. The 500 selected units are NOT inserted or product-admitted. B0 descriptor/reader lifetime, full capacity, branch conditions, variable print aggregation, full source/integrity/cumulative/ISA checks and own-ROM runtime verification remain required.')
    frozen_write(work / 'verification.json', report)
    print('PASS exact500 mechanical compilation;', len(glyph_report), 'extended glyphs checked; NO ROM written')


if __name__ == '__main__':
    main()
