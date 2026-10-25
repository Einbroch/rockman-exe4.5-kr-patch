"""Verify font-only product candidate; do not promote keyboard runtime support."""
import json
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from hangul_editor_display import JAMO_INDICES
from hangul_composer_thumb import KEYS
from report_fixedcell_runtime import read,verify_route

def main():
    stem='exe45_ko_development_keyboard_glyphs_v1'
    product=ROOT/f'poc/output/{stem}.gba';manifest=product.with_suffix('.json');m=read(manifest)
    require_hash(product,m['output_sha256']);rom=product.read_bytes()
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    if m['source_sha256']!=profile['sha256'] or not m['final_diff_audited'] or not m['header_unchanged']:raise ValueError('product applicability')
    for n in ['build_keyitem_full_rom.py','build_roll_pet.py','build_development_patch.py','fixedcell_extension.py','hangul_editor_display.py','hangul_composer_thumb.py']:require_hash(ROOT/'tools'/n,m['build_tools_sha256'][n])
    k=m['hangul_keyboard_glyphs']
    if k['mapping']!=JAMO_INDICES or k['fixed_order']!=[',']+list(KEYS) or k['input_hooks_installed'] or not k['final_placement_verified']:raise ValueError('glyph contract')
    font=m['font'];require_hash(ROOT/font['path'],font['sha256']);require_hash(ROOT/font['license'],font['license_sha256'])
    normal=bdf_glyphs(ROOT/font['path'],set(KEYS));bank=b''.join(normal[ch] for ch in KEYS)
    if rom[k['normal_jamo_offset']:k['normal_jamo_offset']+len(bank)]!=bank:raise ValueError('final normal jamo font')
    cpu_path=ROOT/'analysis/hangul_keyboard_v1/glyph_provider_cpu.json';cpu=read(cpu_path)
    require_hash(ROOT/'tools/bench_fixedcell_mono_provider.py',cpu['tool_sha256'])
    if cpu['rom_sha256']!=m['output_sha256'] or not cpu['status'].startswith('PASS') or not cpu['native_copier_executed'] or cpu['keyboard_extra_characters']!=k['fixed_order'] or cpu['keyboard_extra_vectors']!=328:raise ValueError('CPU provider claim')
    boot=ROOT/'poc/runtime/hangul-keyboard-glyphs-v1-boot-menu';verify_route(boot,m['output_sha256'],set())
    # Default path must retain the established cumulative product byte-for-byte.
    old='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    regression=ROOT/'poc/output/exe45_ko_development_input_heading_v1_regression_r3.gba';require_hash(regression,old)
    require_hash(ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba',old)
    for start,end in [(0x34e34,0x34e62),(0x35000,0x35032),(0x353b0,0x35582),(0x3558c,0x3564e),(0x526d0,0x526d8)]:
        if original[start:end]!=rom[start:end]:raise ValueError('native editor changed by font-only option')
    report=dict(id='exe45.hangul-keyboard.glyph-supply.v1',passed=True,policy='development glyph-supply candidate; NON-DISTRIBUTION',product=str(product.relative_to(ROOT)).replace('\\','/'),rom_sha256=m['output_sha256'],bytes=len(rom),source_sha256=profile['sha256'],default_regression_rom_sha256=old,font_supply=k,normal_jamo_final_pixels_verified=True,fixedcell_CPU_vectors=cpu['vectors'],fixedcell_extra_CPU_vectors=cpu['keyboard_extra_vectors'],runtime_claim='Cold boot through title screen observed; no jamo selection/rendering or keyboard input/save claim',boot_route=str(boot.relative_to(ROOT)).replace('\\','/'),current_play_product_promoted=False,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['report_keyboard_glyph_supply.py','bench_fixedcell_mono_provider.py','build_keyitem_full_rom.py','build_roll_pet.py','build_development_patch.py','fixedcell_extension.py']},artifacts={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in [manifest,cpu_path,boot/'result.json',regression.with_suffix('.json')]},limits=['Generated glyph banks and final CPU provider code are incorporated in this exact ROM; automatic composer/display hooks are not.','Font asset placement and CPU pixel consumption do not prove game lookup/load/render lifetime; actual jamo screen test remains pending.','Title screenshot inspected; no human approval of keyboard arrangement/readability or save compatibility.','Established input-heading ROM remains the current play baseline until keyboard integration/runtime verification.'])
    out=ROOT/'analysis/hangul_keyboard_v1/glyph_supply.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS font-only ROM candidate, native copier CPU, cold-title route, byte-identical default regression')

if __name__=='__main__':main()
