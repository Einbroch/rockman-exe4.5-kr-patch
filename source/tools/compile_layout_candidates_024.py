"""Source-only mechanical compile of024's272 candidates, NOT a product build.

The LF proposal is kept outside the primary writer. No500 selection or ROM is
emitted. Every wording is joined from frozen references, not authored here.
"""
import re
from collections import defaultdict
from build_visibility_poc import ROOT, sha, require_hash, run_textpet, bdf_glyphs
from cumulative_batch500 import read, frozen_write
from compare_archive_payloads import payload_of
from tpl_literals import literals, skeleton, replace_literals, serialize
from archive_scripts import verify_untouched_scripts
from textpet_korean import prepare_plugins, command
from korean_codec import EXTRA_CHARACTER_INDICES, EXTRA_CHARACTER_METRICS
from survey_pet_quick_reflow_024 import replace_for_analysis
from pet_quick_capacity import validate as quick_validate
from field_hint_capacity import validate as full_validate

FULL = 'analysis/pending_insertion_500_024_fullbox_v1/survey.json'
QUICK = 'analysis/pending_insertion_500_024_quick_reflow_v2/survey.json'
CPU = 'analysis/pending_insertion_500_024_native_controls_v1/cpu.json'
OUT = 'analysis/pending_insertion_500_024_compile_v2'


def ref(path):
    return dict(path=str(path.relative_to(ROOT)), sha256=sha(path.read_bytes()))


def canonical_literals(tpl):
    # Representation only: explicit escaped LF for leading blank lines avoids
    # TextPet's triple-quoted reader trimming them. Require full byte identity
    # below; never modify the frozen extraction or literal values themselves.
    before = literals(tpl)
    out = tpl
    for item in reversed(before):
        if item.text:
            out = out[:item.start]+serialize(item.text)+out[item.end:]
    if [(i.key,i.language,i.text) for i in literals(out)] != [(i.key,i.language,i.text) for i in before] or skeleton(tpl) != skeleton(out):
        raise ValueError('Canonical source representation changed content')
    return out


def main():
    cfg = read('project.json')
    source_path = ROOT/cfg['source_profile']['filename']
    require_hash(source_path, cfg['source_profile']['sha256'])
    source = source_path.read_bytes()
    full, quick, cpu = read(FULL), read(QUICK), read(CPU)
    if full['baseline_sha256'] != quick['baseline_sha256'] or not cpu['passed'] or cpu['baseline_sha256'] != full['baseline_sha256']:
        raise ValueError('Baseline/CPU scope')
    rp = ROOT/full['baseline_rom']
    require_hash(rp, full['baseline_sha256'])
    rom = rp.read_bytes()
    meta = read(str(rp.with_suffix('.json').relative_to(ROOT)))
    if meta['output_sha256'] != sha(rom):
        raise ValueError('Baseline metadata')
    out = ROOT/OUT
    if out.exists():
        raise ValueError('Preserve earlier source-only compile')
    out.mkdir(parents=True)
    plugin = prepare_plugins(out/'plugins', set(EXTRA_CHARACTER_INDICES))
    common = command(out/'plugins')
    groups = defaultdict(list)
    for profile, report in (('fullbox', full), ('quick-within-page-lf-proposal', quick)):
        for g in report['candidate_groups']:
            groups[g['archive']].append((profile, g))
    records, seen, chars, lf_edits = [], set(), set(), []
    for arc, selected in sorted(groups.items()):
        refs = {str(g['source_tpl']) for _, g in selected}
        if len(refs) != 1:
            raise ValueError('Source TPL disagreement')
        src_ref = selected[0][1]['source_tpl']
        require_hash(ROOT/src_ref['path'], src_ref['sha256'])
        original = (ROOT/src_ref['path']).read_text(encoding='utf-8-sig')
        row = selected[0][1]['source_row']
        native = payload_of(source, row)
        units, proof = [], []
        for profile, g in selected:
            for link in g['drafts']:
                require_hash(ROOT/link['path'], link['sha256'])
                asset = read(link['path'])
                u = next(u for u in asset['units'] if u['id'] == link['id'])
                if u['id'] in seen or u['state'] != 'needs_review' or asset['source_tpl'] != src_ref or asset['source_archive_sha256'] != sha(native):
                    raise ValueError('Source/wording/ID binding')
                seen.add(u['id'])
                value = g.get('individual_layouts', {}).get(u['id'], u['translation'])
                if profile.startswith('quick'):
                    layout = g['layouts'].get(u['id'])
                    if layout:
                        if layout['before'] != u['translation'] or layout['after'].replace('\n', ' ') != u['translation'].replace('\n', ' '):
                            raise ValueError('Frozen wording projection')
                        value = layout['after']
                    if value.count('\n') != u['source'].count('\n'):
                        lf_edits.append(dict(id=u['id'], source_lf=u['source'].count('\n'), target_lf=value.count('\n')))
                units.append(dict(id=u['id'], source=u['source'], translation=value, state=u['state']))
                chars.update(value)
            subset = [u for u in units if u['id'] in g['ids']]
            if {u['id'] for u in subset} != set(g['ids']):
                raise ValueError('Incomplete script selection')
            target_one = replace_for_analysis(original, subset) if profile.startswith('quick') else replace_literals(original, subset)
            current = quick_validate(original, target_one, [g['script']], set(g['ids'])) if profile.startswith('quick') else full_validate(original, target_one, [g['script']], set(g['ids']), full['native_nickname_applicability_bound'], 88)
            if current != g['geometry']:
                raise ValueError('Frozen geometry no longer reproduced')
            proof.append(dict(profile=profile, script=g['script'], ids=g['ids'], geometry=current))
        target = replace_for_analysis(original, units)
        folder = out/arc
        folder.mkdir()
        source_tpl, target_tpl = folder/'source.tpl', folder/'target.tpl'
        source_tpl.write_text(canonical_literals(original), encoding='utf-8', newline='\n')
        target_tpl.write_text(canonical_literals(target), encoding='utf-8', newline='\n')
        native_file, compiled, reverse, rebuilt = (folder/n for n in (arc+'_native.msg', arc+'.msg', 'reverse.tpl', arc+'_rebuilt.msg'))
        run_textpet(common+['Read-Text-Archives',str(source_tpl),'--format','tpl','Write-Text-Archives',str(native_file),'--format','bin'],folder/'native-roundtrip.log')
        if native_file.read_bytes() != native:
            raise ValueError('Native binary/TPL/binary identity '+arc)
        run_textpet(common+['Read-Text-Archives',str(target_tpl),'--format','tpl','Write-Text-Archives',str(compiled),'--format','bin'],folder/'compile.log')
        payload = compiled.read_bytes()
        if len(payload) > 65535:
            raise ValueError('16bit script pointer range')
        run_textpet(common+['Read-Text-Archives',str(compiled),'--format','bin','Write-Text-Archives',str(reverse),'--format','tpl'],folder/'reverse.log')
        run_textpet(common+['Read-Text-Archives',str(reverse),'--format','tpl','Write-Text-Archives',str(rebuilt),'--format','bin'],folder/'rebuild.log')
        exported = reverse.read_text(encoding='utf-8-sig')
        if skeleton(original) != skeleton(exported) or [(i.key,i.language,i.text) for i in literals(target)] != [(i.key,i.language,i.text) for i in literals(exported)] or rebuilt.read_bytes() != payload:
            raise ValueError('Literal/control/binary roundtrip '+arc)
        count = int(re.search(r'^@size (\d+)$', original, re.M)[1])
        untouched = verify_untouched_scripts(native, payload, count, {g['script'] for _,g in selected})
        records.append(dict(archive=arc, source_payload_sha256=sha(native), source_tpl=src_ref, compiled=ref(compiled), target_tpl=ref(target_tpl), scripts=count, selected_units=len(units), units=units, profiles=proof, native_roundtrip=True, binary_roundtrip=True, controls_preserved=True, unselected_scripts=untouched, product_admitted=False))
        print('PASS source-only', arc, len(units), 'units', flush=True)
    if len(seen) != 272:
        raise ValueError('Exact frozen candidate denominator')
    wanted = {c for c in chars if '\uac00' <= c <= '\ud7a3'}
    extra = chars & EXTRA_CHARACTER_INDICES.keys()
    font_path = ROOT/cfg['development_dependencies']['font']['path']
    require_hash(font_path, cfg['development_dependencies']['font']['sha256'])
    glyphs = bdf_glyphs(font_path, wanted)
    glyphs.update(bdf_glyphs(font_path, extra, {c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    ef = meta['extension']
    for ch, glyph in glyphs.items():
        index = ef['legacy_index_view']+(ord(ch)-0xAC00 if ch in wanted else EXTRA_CHARACTER_INDICES[ch])
        at = ef['normal_font_offset']+index*96
        if rom[at:at+96] != glyph:
            raise ValueError('Actual023 glyph supply '+ch)
    deps = [FULL,QUICK,CPU,'tools/compile_layout_candidates_024.py','tools/survey_pet_quick_reflow_024.py','tools/field_hint_capacity.py','tools/pet_quick_capacity.py','tools/tpl_literals.py']
    frozen_write(out/'verification.json',dict(schema=1,status='PARTIAL272_SOURCE_ONLY_COMPILE_PASS_NOT_ROM_ADMISSION',passed=True,source_sha256=sha(source),baseline_rom=full['baseline_rom'],baseline_sha256=sha(rom),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},units=272,archives=records,within_page_lf_edits=lf_edits,extended_glyphs_checked=len(glyphs),plugin=plugin,selected500=None,wording_changed=False,source_and_target_binary_roundtrip=True,unselected_script_bytes_preserved=True,geometry_model_reproduced=True,product_integrated=False,rom_written=False,insertion_ready=False,runtime_tested=False,release_eligible=False,limits='272 frozen wording candidates only. Source-only complete archive payloads intentionally keep other source literals; not injectable over023 carry translations. Need exact500 selection, explicit proposed-LF source gate, cumulative merge, ExpectedWrites, final product/repro/CPU/GBA pixels/clear/reentry verification. Geometry checks are not semantic approval or normal event reachability.'))
    print('PASS source-only272;',len(records),'archives;',len(glyphs),'actual023 glyphs;NO ROM written')


if __name__ == '__main__':
    main()
