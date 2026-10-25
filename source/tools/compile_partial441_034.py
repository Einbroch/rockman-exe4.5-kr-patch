"""Compile partial441 from immutable source, prove locked parent-script bytes."""
import re
from collections import defaultdict
from build_visibility_poc import ROOT, sha, require_hash, run_textpet, bdf_glyphs
from cumulative_batch500 import read, frozen_write
from prepare_partial441_034 import OUT as SELECTION
from survey_aggregate_pet_033 import replace_exact
from survey_locked_carry_034 import VALIDATORS as PRIOR_VALIDATORS
from pet_query_choices_034 import validate as query_validate
from pet_list_capacity_034_v2 import validate as list_validate
def list_adapter(original,target,scripts,ids,bound):
    if len(scripts)!=1:raise ValueError('034 list single script scope')
    script=scripts[0]
    def section(tpl):
        arc=re.search(r'^@archive (\\w+)',tpl,re.M).group(1)
        found=re.search(r'^script '+str(script)+r' \\w+ \\{[\\s\\S]*?(?=^script\\s|\\Z)',tpl,re.M)
        if found is None:raise ValueError('034 list script identity')
        return '@archive '+arc+'\\n'+found.group()
    fields=read('analysis/pending_insertion_500_034_list_formatter_cpu_v1/cpu.json')['fields']
    field=next(f for f in fields if f['list_selector'][0]==script)
    return list_validate(section(original),section(target),scripts,ids,bound,field)
VALIDATORS=PRIOR_VALIDATORS+[('pet-query-two-choice',query_validate),('pet-native-list-conditional',list_adapter)]
from survey_batch500_017_layout import protected_edges
from canonical_literals_031 import canonical_literals
from compare_archive_payloads import payload_of
from tpl_literals import literals, skeleton
from archive_scripts import verify_untouched_scripts, script_spans
from compile_layout_candidates_024 import ref
from textpet_korean import prepare_plugins, command
from korean_codec import EXTRA_CHARACTER_INDICES, EXTRA_CHARACTER_METRICS
from profile_provider_bounds_027_v2 import bounds as profile_bounds
from chip_profile_bounds_030 import bounds as chip_bounds

OUT = 'analysis/pending_insertion_500_034_compile441_v1'


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
        locked = {u['id']:u['translation'] for g in groups for u in g['locked_parent_units']}
        parent_tpl = replace_exact(original, locked)
        parent_record = next(r for r in meta['archives'] if r['archive']==arc)
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
            geometry = validators[g['profile']](original, replace_exact(parent_tpl, subset), [g['script']], set(g['geometry_ids']), selection['native_nickname_bound'])
            if geometry != g['geometry']:
                raise ValueError('033 current geometry not reproduced')
            proofs.append(dict(profile=g['profile'], script=g['script'], ids=g['ids'], geometry=geometry))
        folder = out/arc; folder.mkdir(); source_tpl = folder/'source.tpl'; target_tpl = folder/'target.tpl'
        target = replace_exact(parent_tpl, values)
        if any(u.text!=locked[u.key] for u in literals(target) if u.key in locked):raise ValueError('034 locked prior literal/layout changed')
        source_tpl.write_text(canonical_literals(original), encoding='utf-8', newline='\n')
        target_tpl.write_text(canonical_literals(target), encoding='utf-8', newline='\n')
        native_file = folder/(arc+'_native.msg'); compiled = folder/(arc+'.msg')
        reverse = folder/'reverse.tpl'; rebuilt = folder/(arc+'_rebuilt.msg')
        def convert(a, af, b, bf, log):
            run_textpet(common+['Read-Text-Archives', str(a), '--format', af, 'Write-Text-Archives', str(b), '--format', bf], folder/log)
        convert(source_tpl, 'tpl', native_file, 'bin', 'native-roundtrip.log')
        if native_file.read_bytes() != native:
            raise ValueError('033 native whole-payload byte roundtrip '+arc)
        count = int(re.search(r'^@size (\d+)$', original, re.M)[1])
        parent_path=folder/'parent.tpl'; parent_bin=folder/(arc+'_parent.msg')
        parent_path.write_text(canonical_literals(parent_tpl),encoding='utf-8',newline='\n')
        convert(parent_path,'tpl',parent_bin,'bin','parent-compile.log')
        live=rom[parent_record['rom_offset']:parent_record['rom_offset']+parent_record['compiled_bytes']]
        reconstructed=script_spans(parent_bin.read_bytes(),count); actual=script_spans(live,count)
        if any(reconstructed[g['script']]!=actual[g['script']] for g in groups):
            raise ValueError('034 source+locked parent script differs from actual033 '+arc)
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
                            unselected_scripts=untouched, parent_script_bytes_match_actual033=True,
                            locked_parent_units=len(locked), product_admitted=False))
        print('PASS034 source-only', arc, len(units), 'units', flush=True)
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
    deps = [SELECTION, 'tools/compile_partial441_034.py', 'tools/survey_aggregate_pet_033.py',
            'tools/canonical_literals_031.py', 'tools/compile_layout_candidates_024.py', 'tools/archive_scripts.py',
            'tools/tpl_literals.py', 'tools/textpet_korean.py', 'tools/profile_provider_bounds_027_v2.py',
            'tools/chip_profile_bounds_030.py','tools/pet_list_capacity_034_v2.py'] + ['tools/'+v.__module__+'.py' for _, v in VALIDATORS if v.__module__ != '__main__'] + ['tools/normal_timing_capacity_025.py','tools/normal_vertical_choices_033.py','analysis/pending_insertion_500_033_vertical_models_v1/result.json','analysis/pending_insertion_500_033_manager_models_v1/result.json']
    frozen_write(out/'verification.json', dict(schema=1, status='PARTIAL441_SOURCE_PARENT_COMPILE_PASS_NOT500_NOT_ROM_ADMISSION', passed=True,
                  source_sha256=sha(source), baseline_rom=selection['baseline_rom'], baseline_sha256=sha(rom),
                  selection=ref(ROOT/SELECTION), dependencies={p: sha((ROOT/p).read_bytes()) for p in deps},
                  units=len(seen), archive_count=len(records), archives=records, within_page_lf_edits=lf_edits,
                  extended_glyphs_checked=len(glyphs), plugin=plugin, source_and_target_roundtrip=True,
                  unselected_script_bytes_preserved=True, locked_parent_scripts_match_actual033=True, wording_changed=False, product_integrated=False,
                  rom_written=False, new_units_applied=0, additional_units_needed=500-len(seen),
                  insertion_ready=False, runtime_tested=False, release_eligible=False,
                  limits='441 source-only new units, NOT500 or a034ROM. Locked prior literals reconstructed from source and their script bytes match actual033; other archive scripts retain source Japanese and must not replace current033 archives. Full carry merge, mixed-scope invariants, exact500 inputs/build/repro/runtime still required.'))
    print('PASS034 partial source-only', len(seen), 'units', len(records), 'archives', len(glyphs), 'actual033 glyphs;NO ROM')


if __name__ == '__main__':
    main()


