"""Hash-bound source-only023 checkpoint and unchanged product/source audit."""
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from verify_tpi_index import lz77_decompress


def main():
    report_path = 'analysis/pending_insertion_500_023_b0_compile_v3/verification.json'
    report = read(report_path)
    selected = read(report['selection']['path'])
    baseline_path = ROOT / report['baseline_rom']
    require_hash(baseline_path, report['baseline_sha256'])
    meta = read(str(baseline_path.with_suffix('.json').relative_to(ROOT)))
    old = {u['id'] for r in layout_records(meta) for u in r['layout']}
    rows = report['archives']
    ids = [key for r in rows for key in r['selected_ids']]
    expected = [key for g in selected['groups'] for key in g['ids']]
    if (not report['passed'] or len(ids) != 500 or len(set(ids)) != 500
            or set(ids) != set(expected) or set(ids) & old or len(rows) != 21
            or len({r['archive'] for r in rows}) != 21 or meta['translated_units'] != 12122
            or report['rom_written'] or report['insertion_ready'] or report['runtime_tested']):
        raise ValueError('Source-only population/current product state changed')
    refs = [report['selection'], report['prepared_inputs'], report['extraction'], report['baseline_manifest']]
    for r in rows:
        refs.extend(r[k] for k in ('compiled', 'reexport', 'rebuilt', 'translated_tpl'))
    for r in refs:
        require_hash(ROOT / r['path'], r['sha256'])
    source_cfg = read('project.json')['source_profile']
    protected = [(source_cfg['filename'], source_cfg['sha256']),
        ('poc/output/pending500_020_v1.gba', '1e595b2113e446fa74be2c2e0c7737a0bf13bcbd7984114eb1c1df79b4580788'),
        ('poc/output/pending500_021_v1.gba', '76d9cf6626436f4c683a49f9389f72c3c85b01b6d6b43461a466e32976ec7ac4'),
        (report['baseline_rom'], report['baseline_sha256']),
        ('patches/exe45_ko_development_news_mail_20261013.zip', '2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6')]
    preserved = []
    for path, expected_hash in protected:
        require_hash(ROOT / path, expected_hash)
        preserved.append(dict(path=path, sha256=expected_hash, bytes=(ROOT / path).stat().st_size))
    source = (ROOT / source_cfg['filename']).read_bytes()
    alias, used = lz77_decompress(source, 0x7B65EC)
    catalogued, _ = lz77_decompress(source, 0x7A6B84)
    if alias != catalogued or len(alias) != 510 or used != 68:
        raise ValueError('Separately observed decoded alias changed')
    classes = Counter()
    for g in selected['groups']:
        classes[g['technical_class']] += g['units']
    if dict(classes) != report['units_by_technical_class']:
        raise ValueError('Technical limitations changed')
    tools = ['tools/extract_field_b0_hints.py', 'tools/prepare_field_b0_reuse_023.py',
        'tools/verify_field_b0_compile_023.py', 'tools/audit_field_b0_checkpoint_023.py']
    result = dict(schema=1, status='SOURCE_ONLY_023_CHECKPOINT_NO_ROM_CHANGE', passed=True,
        mechanical_report=dict(path=report_path, sha256=sha((ROOT / report_path).read_bytes())),
        tools=[dict(path=p, sha256=sha((ROOT / p).read_bytes())) for p in tools],
        protected_artifacts=preserved, exact_new_source_units=500, new_ids_overlap_current_product=0,
        current_rom=report['baseline_rom'], current_rom_translated_units=12122,
        all_compilation_artifact_hashes_verified=True, units_by_technical_class=dict(classes),
        decoded_alias=dict(source_archive='7B65EC', catalogued_archive='7A6B84', decoded_bytes=len(alias), source_compressed_bytes=used, decoded_sha256=sha(alias), new_text_counted=False, classification='decoded alias only; not a new translation unit'),
        failed_attempts=[dict(path='analysis/pending_insertion_500_023_b0_compile_v1', reason='Verification harness compared path spellings with opposite separators; no ROM write'), dict(path='analysis/pending_insertion_500_023_b0_compile_v2', reason='TextPet used output binary basename translated as archive identity; corrected to original archive basename in v3; no ROM write')],
        new_rom_written=False, new_patch_created=False, insertion_ready=False, release_eligible=False,
        next_required=['Full B0 consumer/descriptor registration and RAM/lifetime proof', 'Capacity and source-preserved branch guards for all selected scripts', 'Aggregate variable-name/chip insertion widths', 'Final ROM cumulative delta/ExpectedWrites/ISA/source integrity and independent rebuild', 'Same-new-ROM normal startup, natural B0 hints and render/clearing/exit/reentry tests'],
        limits='This checkpoint compiles 500 new source identities, not 500 newly written product translations; unchanged022 remains the verified development ROM. No whole-game remaining count, player save edits, Hangul input completion or release approval.')
    frozen_write(ROOT / 'analysis/pending_insertion_500_023_b0_reuse_v1/checkpoint.json', result)
    print('PASS checkpoint: new source500, actual ROM delta0; current022=12122; protected source/020/021/022/ZIP unchanged')


if __name__ == '__main__':
    main()
