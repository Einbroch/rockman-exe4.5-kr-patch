"""Select exactly 500 unapplied draft IDs; compile checks only, never write ROM."""
import argparse
import json
import re
from build_visibility_poc import ROOT, sha, require_hash, run_textpet, bdf_glyphs
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from tpl_literals import literals, replace_literals, skeleton
from textpet_korean import prepare_plugins, command
from archive_scripts import verify_untouched_scripts
from korean_codec import encode_character,EXTRA_CHARACTER_INDICES

BASE = 'poc/output/exe45_ko_development_pending500_arrow_v2.gba'
BASE_SHA = 'da920efbbd2b965a5e7bbab75ee88242735a8613777f96fb483daf5bad0bd068'
LAYOUT = 'translations/pending_insertion_500_002_layout.json'
LAYOUT_COUNT=19
EXPECTED_UNITS=500
PLAN = [
    ('translations/batch500_016_destruction_6E01AC_draft_ko.json', {38, 39, 40}, 105),
    ('translations/batch500_015_mission_6DED88_draft_ko.json', set(), 220),
    ('translations/batch500_045_navi_mail_npcs_6DE2C8_draft_ko.json', set(), 15),
    ('translations/batch500_001_equipment_guts_draft_ko.json', set(), 51),
    ('translations/batch500_001_equipment_fire_draft_ko.json', set(), 51),
    ('translations/batch500_001_equipment_proto_draft_ko.json', set(), 51),
    ('translations/batch500_045_navi_mail_npcs_6A5578_draft_ko.json', set(), 7),
]


def prepare(out):
    if out.exists():
        raise ValueError('Existing artifacts are immutable; choose a new output directory')
    cfg = json.loads((ROOT / 'project.json').read_text(encoding='utf8'))
    source_path = ROOT / cfg['source_profile']['filename']
    require_hash(source_path, cfg['source_profile']['sha256'])
    require_hash(ROOT / BASE, BASE_SHA)
    source = source_path.read_bytes()
    meta_path = (ROOT / BASE).with_suffix('.json')
    meta = json.loads(meta_path.read_text(encoding='utf8'))
    if meta['output_sha256'] != BASE_SHA:
        raise ValueError('Baseline metadata mismatch')
    from prepare_repartition500 import layout_records
    records = list(layout_records(meta))
    applied = set()
    for record in records:
        keys = {x['id'] for x in record['layout']}
        if len(keys) != record['translated_units']:
            raise ValueError('Applied population cannot be derived from metadata')
        applied.update(keys)
    require_hash(ROOT / cfg['text_catalog']['path'], cfg['text_catalog']['sha256'])
    rows = parse_tpi(ROOT / cfg['text_catalog']['path'])
    layout_spec = json.loads((ROOT / LAYOUT).read_text(encoding='utf8'))
    if layout_spec['release_eligible'] is not False or len(layout_spec['layouts']) != LAYOUT_COUNT:
        raise ValueError('Individual layout policy/population mismatch')
    used_layouts = set()
    selected, entries, wanted = set(), [], set()
    for path, excluded_scripts, expected_count in PLAN:
        draft_path = ROOT / path
        d = json.loads(draft_path.read_text(encoding='utf8'))
        a = d['archive']
        if d['source_sha256'] != sha(source) or d['review']['release_eligible'] is not False:
            raise ValueError('Source or draft policy mismatch: ' + a)
        require_hash(ROOT / d['source_tpl']['path'], d['source_tpl']['sha256'])
        tpl = (ROOT / d['source_tpl']['path']).read_text(encoding='utf-8-sig')
        original = {x.key: x.text for x in literals(tpl)}
        units = [dict(x) for x in d['units'] if int(x['id'].split(':')[1]) not in excluded_scripts]
        for x in units:
            if x['id'] in layout_spec['layouts']:
                value = layout_spec['layouts'][x['id']]
                if value.replace('\n',' ') != x['translation'].replace('\n',' ') or value.count('\n') != x['translation'].count('\n'):
                    raise ValueError('Layout changes protected wording/topology: ' + x['id'])
                x['translation'] = value
                used_layouts.add(x['id'])
        if len(units) != expected_count:
            raise ValueError('Batch count mismatch: ' + a)
        scripts = {int(x['id'].split(':')[1]) for x in units}
        japanese_ids = {x.key for x in literals(tpl)
            if int(x.key.split(':')[1]) in scripts and re.search(r'[\u3040-\u30ff\u3400-\u9fff]', x.text)}
        if japanese_ids != {x['id'] for x in units}:
            raise ValueError('Selection fragments Japanese script population: ' + a)
        for x in units:
            if x['id'] in applied or x['id'] in selected or original.get(x['id']) != x['source']:
                raise ValueError('Duplicate/applied ID or protected source mismatch: ' + x['id'])
            if x['state'] != 'needs_review':
                raise ValueError('Unexpected review state: ' + x['id'])
            if re.findall(r'\d+', x['source']) != re.findall(r'\d+', x['translation']):
                raise ValueError('Protected numeric text mismatch: ' + x['id'])
            if x['source'].count('\n') != x['translation'].count('\n'):
                raise ValueError('Protected line topology mismatch: ' + x['id'])
            selected.add(x['id'])
            wanted.update(ch for ch in x['translation'] if '\uac00' <= ch <= '\ud7a3')
        row = next(r for r in rows if r['offset'] == int(a, 16))
        native = payload_of(source, row)
        if sha(native) != d['source_archive_sha256']:
            raise ValueError('Source archive payload mismatch: ' + a)
        entries.append((path, d, tpl, units, scripts, row, native))
    if len(selected) != EXPECTED_UNITS:
        raise ValueError(f'Expected exactly {EXPECTED_UNITS} unique unapplied IDs')
    if used_layouts != set(layout_spec['layouts']):
        raise ValueError('Unused or unknown layout IDs')
    out.mkdir(parents=True)
    plugins = out / 'plugins'
    extra_chars={ch for _,_,_,units,_,_,_ in entries for u in units for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES}
    plugin = prepare_plugins(plugins, extra_chars)
    codes = {}
    for line in (plugins / 'exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            if len(v) == 1:
                codes[v] = bytes.fromhex(k)
    font = cfg['development_dependencies']['font']
    require_hash(ROOT / font['path'], font['sha256'])
    glyphs = bdf_glyphs(ROOT / font['path'], wanted)
    common, results, candidates = command(plugins), [], []
    for path, d, tpl, units, scripts, row, native in entries:
        a = d['archive']
        work = out / a
        work.mkdir()
        (work / 'compiled').mkdir()
        languages = {x.key:x.language for x in literals(tpl)}
        from pending500_002_pages import replace as page_replace,remap_layout
        translated,mapping,page_proof = page_replace(tpl,units)
        original_path, target = work / 'source.tpl', work / 'translated.tpl'
        original_path.write_text(tpl, encoding='utf8')
        target.write_text(translated, encoding='utf8')
        source_bin, compiled = work / 'source.msg', work / 'compiled' / (a + '.msg')
        reverse, rebuilt = work / 'reverse.tpl', work / 'rebuilt.msg'
        run_textpet(common + ['Read-Text-Archives', str(original_path), '--format', 'tpl',
            'Write-Text-Archives', str(source_bin), '--format', 'bin'], work / 'source_compile.log')
        if source_bin.read_bytes() != native:
            raise ValueError('Native unchanged roundtrip failed: ' + a)
        layout = []
        selected_fragment_ids={key for x in units for key in mapping[x['id']]}
        fragment_original={key:x['id'] for x in units for key in mapping[x['id']]}
        for x in literals(translated):
            if x.key not in selected_fragment_ids:continue
            original_id=fragment_original[x.key]
            language = x.language
            widths = []
            for line in x.text.split('\n'):
                width = 0
                for ch in line:
                    if ch not in codes:
                        raise ValueError('Unmapped character: ' + original_id + repr(ch))
                    if '\uac00' <= ch <= '\ud7a3' and codes[ch] != encode_character(ch):
                        raise ValueError('Hangul mapping mismatch')
                    width += 8 if language == 'mmbn45s' else 12 if '\uac00' <= ch <= '\ud7a3' or ch in EXTRA_CHARACTER_INDICES else 8 if ch == ' ' else 11
                widths.append(width)
            layout.append(dict(id=x.key,language=language,line_advance_pixels=widths))
            # Preliminary mail-window comparison only; equipment/NPC geometry is NOT adopted here.
            guide=int(original_id.split(':')[1]) in (60,61,62) and d['archive'] in ('6E1554','6E1CC0','6E21B0')
            limit = 88 if language == 'mmbn45s' else 132 if guide or d['archive']=='6A5578' else 152
            max_rows=1 if language=='mmbn45s' else 2 if guide else 3
            if len(widths) > max_rows or max(widths) > limit or language == 'mmbn45' and len(widths) == 3 and widths[2] > 132:
                candidates.append(dict(id=original_id, fragment_id=x.key,widths=widths,
                    classification='provisional fixed-cell/mail comparison; actual consumer geometry unresolved'))
        run_textpet(common + ['Read-Text-Archives', str(target), '--format', 'tpl',
            'Write-Text-Archives', str(compiled), '--format', 'bin'], work / 'compile.log')
        raw = compiled.read_bytes()
        run_textpet(common + ['Read-Text-Archives', str(compiled), '--format', 'bin',
            'Write-Text-Archives', str(reverse), '--format', 'tpl'], work / 'reverse.log')
        back = reverse.read_text(encoding='utf-8-sig')
        if skeleton(back) != skeleton(translated):
            raise ValueError('Protected command skeleton mismatch: ' + a)
        if [(x.key,x.text) for x in literals(back)] != [(x.key,x.text) for x in literals(translated)]:
            raise ValueError('Semantic roundtrip failed: ' + a)
        run_textpet(common + ['Read-Text-Archives', str(reverse), '--format', 'tpl',
            'Write-Text-Archives', str(rebuilt), '--format', 'bin'], work / 'rebuild.log')
        if rebuilt.read_bytes() != raw:
            raise ValueError('Binary roundtrip failed: ' + a)
        count = int(re.search(r'^@size\s+(\d+)', tpl, re.M).group(1))
        verify_untouched_scripts(native, raw, count, scripts)
        if len(raw) > 65535:
            raise ValueError('Archive exceeds 16-bit extent: ' + a)
        layout=remap_layout(layout,mapping,[x['id'] for x in units])
        results.append(dict(archive=a,draft_path=path,draft_sha256=sha((ROOT/path).read_bytes()),
            source_tpl=d['source_tpl'],source_payload_sha256=sha(native),selected_ids=[x['id'] for x in units],
            selected_units=len(units),scripts=sorted(scripts),script_count=count,source_bytes=len(native),
            compiled_bytes=len(raw),compiled_sha256=sha(raw),source_pointers=row['pointers'],
            source_native_roundtrip=True,protected_controls_unchanged=True,semantic_roundtrip=True,
            binary_roundtrip=True,unselected_scripts_unchanged=True,layout=layout,
            explicit_page_proof=page_proof,consumer_geometry_verified=False,variable_widths_verified=False,loader_capacity_verified=False))
        print('Preflight', a, len(units), 'native', len(native), 'compiled', len(raw), flush=True)
    require_hash(source_path, cfg['source_profile']['sha256'])
    require_hash(ROOT / BASE, BASE_SHA)
    report = dict(schema=1,batch_id='pending-insertion-500-002',policy='development-draft; NON-DISTRIBUTION',
        source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,
        baseline_metadata_sha256=sha(meta_path.read_bytes()),total_units=EXPECTED_UNITS,unique_ids=EXPECTED_UNITS,
        applied_id_intersection=0,existing_drafts_reused_without_wording_changes=True,newly_translated_units=0,
        archives=results,font_source=font,font_glyphs=len(glyphs),hangul_mapping_complete=True,plugin=plugin,
        layout_candidates=candidates,rom_applied_units=0,rom_written=False,runtime_tested=False,
        release_eligible=False,stage='source/encoding/compile preflight; geometry/variables/loaders/integration pending')
    report['individual_layout'] = dict(path=LAYOUT,sha256=sha((ROOT / LAYOUT).read_bytes()),affected_ids=sorted(used_layouts))
    report['artifacts'] = {str(p.relative_to(out)):sha(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file()}
    (out / 'preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(EXPECTED_UNITS,'unapplied IDs checked; candidates',len(candidates),'ROM unchanged',flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out',default='analysis/pending_insertion_500_002')
    a = p.parse_args()
    prepare(ROOT / a.out)
