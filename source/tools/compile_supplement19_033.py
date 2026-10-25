"""Compile19 frozen same-word PET proposals from immutable source, not ROM."""
import re
from collections import defaultdict
from build_visibility_poc import ROOT, sha, require_hash, run_textpet, bdf_glyphs
from cumulative_batch500 import read, frozen_write
from prepare_supplement19_033 import OUT as SELECTION
from survey_aggregate_pet_033 import replace_exact
from calendar_aqua_capacity_033 import validate as aqua
from calendar_menu_capacity_032_v2 import validate as menu
from normal_timing_capacity_025 import validate as normal
def normal_adapter(original,target,scripts,selected_ids,bound):
    return normal(original,target,scripts,selected_ids,bound,88)
VALIDATORS=[('calendar-aqua-early-sfx',aqua),('calendar-menu',menu),('normal-pages',normal_adapter)]
from survey_batch500_017_layout import protected_edges
from canonical_literals_031 import canonical_literals
from compare_archive_payloads import payload_of
from tpl_literals import literals, skeleton
from archive_scripts import verify_untouched_scripts
from compile_layout_candidates_024 import ref
from textpet_korean import prepare_plugins, command
from korean_codec import EXTRA_CHARACTER_INDICES, EXTRA_CHARACTER_METRICS
from profile_provider_bounds_027_v2 import bounds as profile_bounds
from chip_profile_bounds_030 import bounds as chip_bounds

OUT = 'analysis/pending_insertion_500_033_compile19_v1'


def main():
    selection = read(SELECTION); cfg = read('project.json')
    for p, h in selection['dependencies'].items():
        require_hash(ROOT/p, h)
    source_path = ROOT/cfg['source_profile']['filename']; require_hash(source_path, selection['source_sha256'])
    source = source_path.read_bytes(); rp = ROOT/selection['baseline_rom']; require_hash(rp, selection['baseline_sha256'])
    rom = rp.read_bytes(); meta = read(rp.with_suffix('.json')); profile_bounds(source, rom); chip_bounds(source, rom)
    out = ROOT/OUT; out.mkdir(parents=True, exist_ok=False)
    plugin = prepare_plugins(out/'plugins', set(EXTRA_CHARACTER_INDICES)); common = command(out/'plugins')
    grouped = defaultdict(list)
    for g in selection['groups']:
        grouped[g['archive']].append(g)
    records = []; seen = set(); chars = set(); lf_edits = []; validators = dict(VALIDATORS)
    for arc, groups in sorted(grouped.items()):
        src = groups[0]['source_tpl']; require_hash(ROOT/src['path'], src['sha256'])
        original = (ROOT/src['path']).read_text(encoding='utf-8-sig'); row = groups[0]['source_row']
        native = payload_of(source, row); source_literals = {u.key: u for u in literals(original)}
        units = []; proofs = []; values = {}
        for g in groups:
            if g['source_tpl'] != src or g['source_row'] != row or g['source_archive_sha256'] != sha(native):
                raise ValueError('033 whole archive source agreement')
            subset = {}
            for link in g['drafts']:
                require_hash(ROOT/link['path'], link['sha256']); asset = read(link['path'])
                u = next(u for u in asset['units'] if u['id'] == link['id'])
                if u['id'] in seen or u['state'] != 'needs_review' or asset['source_archive_sha256'] != sha(native) or asset['source_tpl'] != src or source_literals[u['id']].text != u['source']:
                    raise ValueError('033 canonical/source/identity conflict')
                value = g['explicit_layouts'].get(u['id'], u['translation'])
                if value.replace('\n', ' ') != u['translation'].replace('\n', ' ') or not protected_edges(u['source'], value):
                    raise ValueError('033 canonical prose or padding changed')
                subset[u['id']] = value; values[u['id']] = value; seen.add(u['id']); chars.update(value)
                units.append(dict(id=u['id'], source=u['source'], translation=value, state=u['state']))
                if value != u['translation']:
                    lf_edits.append(dict(id=u['id'], canonical=u['translation'], target=value))
            if set(subset) != set(g['ids']):
                raise ValueError('033 whole-script selected identity')
            geometry = validators[g['profile']](original, replace_exact(original, subset), [g['script']], set(g['ids']), selection['native_nickname_bound'])
            if geometry != g['geometry']:
                raise ValueError('033 current geometry not reproduced')
            proofs.append(dict(profile=g['profile'], script=g['script'], ids=g['ids'], geometry=geometry))
        folder = out/arc; folder.mkdir(); source_tpl = folder/'source.tpl'; target_tpl = folder/'target.tpl'
        target = replace_exact(original, values)
        source_tpl.write_text(canonical_literals(original), encoding='utf-8', newline='\n')
        target_tpl.write_text(canonical_literals(target), encoding='utf-8', newline='\n')
        native_file = folder/(arc+'_native.msg'); compiled = folder/(arc+'.msg')
        reverse = folder/'reverse.tpl'; rebuilt = folder/(arc+'_rebuilt.msg')
        def convert(a, af, b, bf, log):
            run_textpet(common+['Read-Text-Archives', str(a), '--format', af, 'Write-Text-Archives', str(b), '--format', bf], folder/log)
        convert(source_tpl, 'tpl', native_file, 'bin', 'native-roundtrip.log')
        if native_file.read_bytes() != native:
            raise ValueError('033 native whole-payload byte roundtrip '+arc)
        convert(target_tpl, 'tpl', compiled, 'bin', 'compile.log'); payload = compiled.read_bytes()
        if len(payload) > 65535:
            raise ValueError('033 16-bit script offset overflow')
        convert(compiled, 'bin', reverse, 'tpl', 'reverse.log')
        convert(reverse, 'tpl', rebuilt, 'bin', 'rebuild.log'); exported = reverse.read_text(encoding='utf-8-sig')
        if skeleton(original) != skeleton(exported) or [(u.key, u.language, u.text) for u in literals(target)] != [(u.key, u.language, u.text) for u in literals(exported)] or rebuilt.read_bytes() != payload:
            raise ValueError('033 target semantic/control/binary roundtrip '+arc)
        count = int(re.search(r'^@size (\d+)$', original, re.M)[1])
        untouched = verify_untouched_scripts(native, payload, count, {g['script'] for g in groups})
        records.append(dict(archive=arc, source_sha256=sha(native), source_tpl=src, compiled=ref(compiled),
                            target_tpl=ref(target_tpl), script_count=count, units=units, profiles=proofs,
                            native_roundtrip=True, semantic_roundtrip=True, binary_roundtrip=True,
                            unselected_scripts=untouched, product_admitted=False))
        print('PASS033 source-only', arc, len(units), 'units', flush=True)
    if seen != set(selection['selected_ids']) or len(seen) != selection['planned_new_units']:
        raise ValueError('033 exact source-only ID population')
    wanted = {c for c in chars if '\uac00' <= c <= '\ud7a3'}; extra = chars & EXTRA_CHARACTER_INDICES.keys()
    fp = ROOT/cfg['development_dependencies']['font']['path']; require_hash(fp, cfg['development_dependencies']['font']['sha256'])
    glyphs = bdf_glyphs(fp, wanted)
    glyphs.update(bdf_glyphs(fp, extra, {c: EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    ef = meta['extension']
    for ch, glyph in glyphs.items():
        index = ef['legacy_index_view'] + (ord(ch)-0xAC00 if ch in wanted else EXTRA_CHARACTER_INDICES[ch])
        at = ef['normal_font_offset'] + index*96
        if rom[at:at+96] != glyph:
            raise ValueError('033 actual032 glyph supply mismatch '+ch)
    deps = [SELECTION, 'tools/compile_supplement19_033.py', 'tools/survey_aggregate_pet_033.py',
            'tools/canonical_literals_031.py', 'tools/compile_layout_candidates_024.py', 'tools/archive_scripts.py',
            'tools/tpl_literals.py', 'tools/textpet_korean.py', 'tools/profile_provider_bounds_027_v2.py',
            'tools/chip_profile_bounds_030.py'] + ['tools/'+v.__module__+'.py' for _, v in VALIDATORS]
    frozen_write(out/'verification.json', dict(schema=1, status='PARTIAL19_SOURCE_ONLY_COMPILE_PASS_NOT_ROM_ADMISSION', passed=True,
                  source_sha256=sha(source), baseline_rom=selection['baseline_rom'], baseline_sha256=sha(rom),
                  selection=ref(ROOT/SELECTION), dependencies={p: sha((ROOT/p).read_bytes()) for p in deps},
                  units=len(seen), archive_count=len(records), archives=records, within_page_lf_edits=lf_edits,
                  extended_glyphs_checked=len(glyphs), plugin=plugin, source_and_target_roundtrip=True,
                  unselected_script_bytes_preserved=True, wording_changed=False, product_integrated=False,
                  rom_written=False, new_units_applied=0, additional_units_needed=500-253-len(seen),
                  insertion_ready=False, runtime_tested=False, release_eligible=False,
                  limits='19 supplement source-only units in addition to253 prior prepared units, NOT500 or a033ROM. Whole source-only archives intentionally retain unselected Japanese and must not replace cumulative032 archives. Native provider applicability/carry/gates/exactwrites/repro/final-ROM runtime and semantic review remain required.'))
    print('PASS033 partial source-only', len(seen), 'units', len(records), 'archives', len(glyphs), 'actual032 glyphs;NO ROM')


if __name__ == '__main__':
    main()
