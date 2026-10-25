"""Scope-bound completion identity, native regressions and current tool pins."""
import json,ast
from pathlib import Path
from report_roll_pet import ROOT,read,sha,require_hash
from report_input_confirmation import static,OUT
from run_input_confirmation import STEM,PREFIX
def main():
    m,rom,_,_,_=static()
    reports={name:read(OUT/path) for name,path in [('confirmation','confirmation_runtime.json'),('PET','pet_regression/runtime.json'),('profile29','normal_subject_regression/profile_runtime.json'),('plugout','plugout_regression/plugout_runtime.json'),('CPU','cpu/report.json')]}
    for name,r in reports.items():
        if not r['passed'] or r.get('rom_sha256',r.get('baseline_rom_sha256'))!=m['output_sha256']:raise ValueError('exact artifact evidence '+name)
    if len(reports['confirmation']['normal_runtime_units'])!=3 or len(reports['PET']['runtime_observed_units'])!=22 or not reports['CPU']['integrated_artifact_final_bytes_checked']:raise ValueError('finite required evidence')
    # Original keyboard record writers are not part of the UI translation.
    src=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    guards=[]
    for lo,hi in [(0x34fa0,0x35050),(0x32ac6,0x32ad8)]:
        if src[lo:hi]!=rom[lo:hi]:raise ValueError('native record writer altered')
        guards.append(dict(start=lo,end=hi,sha256=sha(src[lo:hi])))
    # 32AD8 is a declared common-root literal, not normalization machine code.
    common=next(a for a in m['archives'] if a['archive']=='6368E8')
    if int.from_bytes(rom[0x32ad8:0x32adc],'little')!=0x08000000+common['rom_offset']:raise ValueError('normalizer common-root literal')
    finalstem=STEM+'_r3';fm=read(ROOT/f'poc/output/{finalstem}.json')
    for stem in [STEM+'_repro',STEM+'_r2',STEM+'_r2_repro',finalstem]:
        require_hash(ROOT/f'poc/output/{stem}.gba',m['output_sha256'])
        if (ROOT/f'poc/output/{stem}.gba').read_bytes()!=rom:raise ValueError('complete ROM byte identity')
    actual={p.name:sha(p.read_bytes()) for p in sorted((ROOT/'tools').glob('*.py'))}
    if actual!=fm['build_tools_sha256']:raise ValueError('current Python tool pins drift')
    for p in (ROOT/'tools').glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
    cpu=reports['CPU'];result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],final_stem=finalstem,runtime_stem=STEM,runtime_prefix=PREFIX,runtime_transfer_by_complete_ROM_byte_identity=True,source_sha256=sha(src),selected_literal_units=m['translated_units'],added_literal_units=3,source_ledger_append_header_repro_verified=True,parent13_and254_common_scripts_preserved=True,prior59_archives_fonts_graphics_keyitem39_preserved=True,native_record_writer_guards=guards,normal_native_confirmation_Yes_No_B_verified=True,native_save_success_script=reports['PET']['native_save_success_script'],native_save_sha256=reports['PET']['native_save_sha256'],cold_continue_without_checkpoint=reports['PET']['cold_continue_has_no_loaded_checkpoint'],cpu_vectors=cpu['vectors'],tool_count=len(actual),tool_drift=[],reports={k:sha((OUT/v).read_bytes()) for k,v in [('confirmation','confirmation_runtime.json'),('PET','pet_regression/runtime.json'),('profile29','normal_subject_regression/profile_runtime.json'),('plugout','plugout_regression/plugout_runtime.json'),('CPU','cpu/report.json')]},limits=reports['confirmation']['limits']+['CPU helper624 is synthetic, not normal shop02031000 evidence. Whole game translation incomplete.'])
    (OUT/'final_identity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({k:result[k] for k in ['passed','rom_sha256','selected_literal_units','added_literal_units','tool_count','tool_drift']},indent=2))
if __name__=='__main__':main()
