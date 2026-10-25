"""Bind host/CPU candidates and normal native observations; NOT ROM readiness."""
import json,struct,subprocess,sys
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read,verify_route
from extended_dialogue import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    require_hash(product,identity);rom=product.read_bytes()
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    tests=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/test_hangul_keyboard_model.py')],capture_output=True,text=True,encoding='utf8',timeout=30,check=True)
    if 'Ran 11 tests' not in tests.stderr or not tests.stderr.rstrip().endswith('OK'):raise ValueError('model fixtures')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_hangul_input_encoder.py')],timeout=60,check=True)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/prepare_hangul_keyboard_candidates.py')],timeout=30,check=True)
    record_tests=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/test_hangul_record_candidate.py')],capture_output=True,text=True,encoding='utf8',timeout=30,check=True)
    if 'Ran 5 tests' not in record_tests.stderr or not record_tests.stderr.rstrip().endswith('OK'):raise ValueError('candidate record fixtures')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_hangul_record_decoder.py')],timeout=60,check=True)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_native_keyboard_storage.py')],timeout=30,check=True)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/analyze_keyboard_consumers.py')],timeout=30,check=True)
    base=ROOT/'analysis/hangul_keyboard_v1';cpu=read(base/'cpu_encoder/report.json');native=read(base/'native_boundaries.json')
    if not cpu['passed'] or cpu['vectors']!=11187 or not native['passed'] or native['rom_sha256']!=identity:raise ValueError('foundation report scope')
    require_hash(base/'cpu_encoder/helper.bin',cpu['helper_sha256'])
    route=ROOT/'poc/runtime/hangul-keyboard-v1-record-readers-r2';result=read(route/'result.json');verify_route(route,identity,set())
    env=read(route/'record_readers_environment.json');require_hash(ROOT/'tools/capture_keyboard_record_readers.py',env['tool_sha256']);require_hash(ROOT/'tools/capture_keyboard_native.py',env['native_observer_sha256'])
    trace=read(route/'step_015_record_readers.json');row=next(r for r in trace['readers'] if r['pc']==0x08038bb4)
    metadata=bytes.fromhex(row['metadata_hex']);at=row['r6']-0x08000000
    if row['r4']!=0x020010a6 or metadata!=rom[at:at+16] or metadata[0]!=1 or metadata[2]!=4:raise ValueError('observed field metadata')
    field=0x02000950+struct.unpack_from('<H',metadata,14)[0]
    descriptor=0x526d0+metadata[1]*8
    output=struct.unpack_from('<I',rom,descriptor)[0]
    if field!=row['r4'] or output!=field+1:raise ValueError('observed in-place output')
    for a,b in [(0x38b94,0x38c10),(at,at+16),(descriptor,descriptor+8)]:
        if original[a:b]!=rom[a:b]:raise ValueError('native reader metadata changed')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    observed=[]
    for row0 in trace['readers']:
        pc=row0['pc'];offset=pc-0x08000000;ins=next(decoder.disasm(rom[offset:offset+4],pc),None)
        if ins is None or len(ins.bytes)!=2:raise ValueError('observed read instruction')
        observed.append(dict(pc=hex(pc),hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str,hits=row0['hits']))
    names=['hangul_keyboard_model.py','test_hangul_keyboard_model.py','bench_hangul_input_encoder.py','prepare_hangul_keyboard_candidates.py','capture_keyboard_native.py','report_keyboard_native.py','capture_keyboard_record_readers.py','verify_hangul_keyboard_foundation.py']
    artifacts={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in [base/'native_boundaries.json',base/'cpu_encoder/report.json',base/'cpu_encoder/helper.bin',base/'candidates/plan.json',base/'candidates/jamo_big_cells.bin',base/'candidates/layout_preview.png',route/'result.json',route/'step_015_record_readers.json',route/'record_readers_environment.json']}
    report=dict(id='exe45.hangul-keyboard.foundation.v1',passed=True,claim='host composition/editing model, emitted syllable encoder fixture and one native record-reader path only',rom_integrated=False,release_eligible=False,source_sha256=profile['sha256'],current_rom_sha256=identity,models=dict(tests=11,construction_and_undo_syllables=11172,loaded_edit_syllables=11172,unittest_output=tests.stderr),cpu_vectors=cpu['vectors'],observed_reader=dict(metadata_address=hex(row['r6']),metadata_hex=metadata.hex(),record_count=metadata[0],native_logical_limit=metadata[2],stride_formula='2 * native_logical_limit + 2',native_stride=metadata[2]*2+2,field_address=hex(field),output_descriptor_index=metadata[1],output_pointer=hex(output),in_place_copy=True,instructions=observed),tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in names},artifacts=artifacts,limits=['Native ten-byte stride established only for this observed weak-subject entry, not every field/reader/save ABI.','Automatic composer and jamo bank are not ROM-integrated. CPU helper encodes complete L/V/T only.','Host loaded text editing does not decode any native save record.','Forty-selector static layout is a candidate, not an emulator screenshot.','F9FC four-byte glyph codes cannot be written unmodified into the native four-character field.','Custom packed storage, all readers, reserved RAM, native grid renderer hooks and complete persistence compatibility remain unresolved.'])
    decoder=read(base/'cpu_record_decoder/report.json');risks=read(base/'native_storage_risks.json');consumers=read(base/'consumer_inventory.json')
    if not decoder['passed'] or decoder['format_adopted'] or decoder['rom_integrated'] or not risks['passed'] or risks['rom_sha256']!=identity or consumers['current_rom_sha256']!=identity:raise ValueError('new candidate scope')
    require_hash(base/'cpu_record_decoder/helper.bin',decoder['helper_sha256'])
    for key,path in [('tool_sha256','bench_hangul_record_decoder.py'),('codec_tool_sha256','hangul_record_candidate.py')]:require_hash(ROOT/'tools'/path,decoder[key])
    report['claim']='host composition/editing, isolated emitted encoder/candidate decoder, native adverse fixtures, bounded source consumer inventory and one normal native reader path; NOT ROM support'
    report['candidate_record']=dict(format_adopted=False,tests=5,unittest_output=record_tests.stderr,valid_CPU_vectors=decoder['valid_vectors'],rejected_CPU_vectors=decoder['rejected_vectors'])
    report['native_storage_risks']=dict(vectors=risks['vectors'],truncated_syllables=risks['truncated_syllables'],four_character_overflow_bytes=risks['overflow']['bytes_beyond_field'])
    report['named_consumer_inventory']=dict(source_TPL_archives=consumers['tpl_archives_checked'],named_references=consumers['named_command_references'],weak_subject_references=consumers['descriptor_counts']['16'],complete_native_reader_graph=False)
    for n in ['hangul_record_candidate.py','test_hangul_record_candidate.py','bench_hangul_record_decoder.py','bench_native_keyboard_storage.py','analyze_keyboard_consumers.py']:report['tools'][n]=sha((ROOT/'tools'/n).read_bytes())
    for p in [base/'cpu_record_decoder/report.json',base/'cpu_record_decoder/helper.bin',base/'native_storage_risks.json',base/'consumer_inventory.json']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    composer=read(base/'cpu_composer/report.json')
    if not composer['passed'] or composer['rom_integrated'] or composer['state_bytes']!=276:raise ValueError('native composer fixture scope')
    for n,h in composer['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in composer['artifacts'].items():require_hash(base/'cpu_composer'/n,h)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_workspace.py')],timeout=30,check=True)
    workspace=read(base/'workspace.json')
    if not workspace['passed'] or workspace['rom_sha256']!=identity or workspace['candidate']['decision']!='rejected':raise ValueError('workspace observation')
    compact_tests=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/test_hangul_compact_state.py')],capture_output=True,text=True,encoding='utf8',timeout=30,check=True)
    if 'Ran 4 tests' not in compact_tests.stderr or not compact_tests.stderr.rstrip().endswith('OK'):raise ValueError('compact state fixtures')
    report['native_composer_fixture']=dict(state_bytes=276,full_row_key_CPU_vectors=composer['full_row_key_CPU_vectors'],complete_syllable_paths=composer['complete_syllable_paths'],counts=composer['counts'],rom_integrated=False)
    compact=read(base/'cpu_compact/report.json')
    if not compact['passed'] or compact['rom_integrated'] or compact['compact_state_bytes']!=64 or compact['complete_syllable_paths']!=11172:raise ValueError('compact CPU fixture scope')
    require_hash(base/'cpu_composer/report.json',compact['dependency_report_sha256'])
    for n,h in compact['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in compact['artifacts'].items():require_hash(base/'cpu_compact'/n,h)
    report['compact_state_candidate']=dict(bytes=64,host_tests=4,unittest_output=compact_tests.stderr,native_wrapper_implemented=True,native_CPU_counts=compact['counts'],temporary_stack_bytes=compact['stack_bytes_including_nested_calls'],game_memory_adopted=False,precondition='same external immutable baseline throughout editing; caller-owned state and stack')
    report['workspace_observation']=dict(adjacent276_byte_candidate='rejected by positive CPU access evidence',game_RAM_adopted=False)
    report['claim']='standalone native composition/undo, compact64-byte native replay wrapper and record conversion fixtures, bounded native/source observations; NOT ROM Hangul input support'
    report['limits'].append('64-byte native wrapper is a CPU fixture; game state/baseline ownership, stack budget and hooks remain unverified.')
    for n in ['hangul_composer_thumb.py','bench_hangul_composer_thumb.py','capture_keyboard_workspace.py','report_keyboard_workspace.py','hangul_compact_state.py','test_hangul_compact_state.py']:report['tools'][n]=sha((ROOT/'tools'/n).read_bytes())
    for p in [base/'cpu_composer/report.json',base/'cpu_composer/feed.bin',base/'cpu_composer/undo.bin',base/'cpu_composer/transitions.bin',base/'cpu_composer/deletions.bin',base/'workspace.json']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    for n in ['hangul_compact_thumb.py','bench_hangul_compact_thumb.py']:report['tools'][n]=sha((ROOT/'tools'/n).read_bytes())
    for p in [base/'cpu_compact/report.json',base/'cpu_compact/wrapper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_adapter.py')],timeout=30,check=True)
    adapter=read(base/'adapter.json')
    if not adapter['passed'] or adapter['rom_integrated'] or adapter['rom_sha256']!=identity or not adapter['normal_route']['No_returns_to_editor_and_preserves_draft']:raise ValueError('adapter observation scope')
    report['adapter_observation']=dict(normal_native_B_No_Yes=True,descriptor0_copy_bytes=32,entry_SP=adapter['stack_candidate']['editor_entry_sp'],game_RAM_and_stack_adopted=False)
    for n in ['capture_keyboard_adapter.py','report_keyboard_adapter.py']:report['tools'][n]=sha((ROOT/'tools'/n).read_bytes())
    report['artifacts']['analysis/hangul_keyboard_v1/adapter.json']=sha((base/'adapter.json').read_bytes())
    editor=read(base/'cpu_editor_display/report.json')
    from hangul_editor_display import JAMO_INDICES
    if not editor['passed'] or editor['rom_integrated'] or editor['mapping_adopted_in_ROM'] or editor['jamo_mapping']!=JAMO_INDICES or editor['full_uint16_rank_domain']!=65536 or editor['complete_syllable_slot_vectors']!=11172*12 or not editor['native_compact_to_display_integration']:raise ValueError('editor display fixture scope')
    for n,h in editor['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in editor['artifacts'].items():require_hash(base/'cpu_editor_display'/n,h)
    for p,h in editor['dependencies'].items():require_hash(ROOT/p,h)
    require_hash(ROOT/editor['font']['path'],editor['font']['sha256'])
    require_hash(ROOT/'external/fonts/LICENSE-Galmuri.txt',editor['font']['license_sha256'])
    if len((base/'cpu_editor_display/jamo_normal.bin').read_bytes())!=40*96:raise ValueError('normal jamo bank extent')
    report['editor_display_fixture']=dict(counts=editor['counts'],complete_syllable_slot_vectors=editor['complete_syllable_slot_vectors'],output_max_bytes=33,normal_jamo_glyphs=40,existing_comma_preserved=True,ROM_glyph_supply_and_hook=False)
    report['claim']='standalone native composition/compact replay/edit-display/record conversion fixtures and bounded native/source observations; NOT ROM Hangul input support'
    report['limits'].append('Editor output jamo indices are proposed only; current ROM has no such glyph bank and must not consume that output yet.')
    for n in ['hangul_editor_display.py','bench_hangul_editor_display.py']:report['tools'][n]=sha((ROOT/'tools'/n).read_bytes())
    for p in [base/'cpu_editor_display/report.json',base/'cpu_editor_display/helper.bin',base/'cpu_editor_display/jamo_normal.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_glyph_supply.py')],timeout=30,check=True)
    supply=read(base/'glyph_supply.json')
    if not supply['passed'] or supply['current_play_product_promoted'] or supply['font_supply']['input_hooks_installed']:raise ValueError('font-only candidate scope')
    report['glyph_only_ROM_candidate']=dict(product=supply['product'],rom_sha256=supply['rom_sha256'],fixedcell_CPU_vectors=supply['fixedcell_CPU_vectors'],runtime_claim=supply['runtime_claim'],current_play_product_promoted=False)
    for n,h in supply['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for p in [base/'glyph_supply.json',base/'glyph_provider_cpu.json']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_display_cache.py')],timeout=30,check=True)
    cache=read(base/'display_cache.json')
    if not cache['passed'] or cache['rom_integrated'] or cache['rom_sha256']!=identity or cache['copies']!=cache['consumption']['matched_copies']:raise ValueError('display cache observation scope')
    report['display_cache_observation']=dict(copies=cache['copies'],destination=cache['provider']['destination'],slot_stride=cache['provider']['slot_stride'],same_render_consumption=cache['consumption']['same_render'],Hangul_output_observed=False)
    for n,h in cache['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    report['artifacts']['analysis/hangul_keyboard_v1/display_cache.json']=sha((base/'display_cache.json').read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_lifecycle.py')],timeout=30,check=True)
    lifecycle=read(base/'lifecycle.json')
    if not lifecycle['passed'] or lifecycle['rom_integrated'] or lifecycle['rom_sha256']!=identity or not lifecycle['initializer']['observed'] or not lifecycle['original_record']['unchanged_through_edit_and_No']:raise ValueError('lifecycle observation scope')
    report['lifecycle_observation']=dict(initializer_observed=True,original_record_unchanged_through_No=True,nonempty_import_observed=False)
    for n,h in lifecycle['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    report['artifacts']['analysis/hangul_keyboard_v1/lifecycle.json']=sha((base/'lifecycle.json').read_bytes())
    bridge=read(base/'cpu_baseline_bridge/report.json')
    if not bridge['passed'] or bridge['rom_integrated'] or bridge['record_format_adopted'] or bridge['complete_syllable_slot_vectors']!=11172*12 or bridge['native_bridge_to_compact_paths']!=35:raise ValueError('baseline bridge fixture scope')
    require_hash(base/'cpu_baseline_bridge/helper.bin',bridge['helper_sha256'])
    for n,h in bridge['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for p,h in bridge['dependencies'].items():require_hash(ROOT/p,h)
    report['baseline_bridge_fixture']=dict(counts=bridge['counts'],baseline_bytes=20,native_bridge_to_compact_paths=35,game_stack_or_RAM_adopted=False,legacy_handling_complete=False)
    for p in [base/'cpu_baseline_bridge/report.json',base/'cpu_baseline_bridge/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_extended_scope.py')],timeout=30,check=True)
    scope=read(base/'extended_scope.json')
    if not scope['passed'] or scope['rom_integrated'] or scope['current_rom_sha256']!=identity or scope['calendar_input']['capacity']!=10:raise ValueError('extended input scope')
    report['extended_input_scope']=dict(calendar_capacity=10,keylog64_host_tests=4,initial_stack_tops=scope['initial_stack_tops'],native_keylog_wrapper_installed=False)
    for n,h in scope['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    report['artifacts']['analysis/hangul_keyboard_v1/extended_scope.json']=sha((base/'extended_scope.json').read_bytes())
    extended=read(base/'cpu_extended_composer/report.json')
    if not extended['passed'] or extended['rom_integrated'] or extended['state_bytes']!=304 or extended['tenth_cell_syllables']!=11172:raise ValueError('extended backend fixture scope')
    require_hash(base/'cpu_composer/report.json',extended['dependency_report_sha256'])
    for n,h in extended['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in extended['artifacts'].items():require_hash(base/'cpu_extended_composer'/n,h)
    report['ten_cell_backend_fixture']=dict(counts=extended['counts'],temporary_state_bytes=304,game_memory_adopted=False)
    report['limits'].append('Native calendar caller uses capacity10 and flag-selected staging imports; earlier eight-cell/marker0 helpers are not universal adapters. Ten-cell display/record bridges and game key-log hooks remain pending.')
    for p in [base/'cpu_extended_composer/report.json',base/'cpu_extended_composer/feed.bin',base/'cpu_extended_composer/undo.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    keylog=read(base/'cpu_keylog/report.json')
    if not keylog['passed'] or keylog['rom_integrated'] or keylog['state_bytes']!=64 or keylog['baseline_bytes']!=24 or keylog['full_syllable_creation_paths']!=11172 or keylog['loaded_tenth_cell_syllables']!=11172 or not keylog['successful_replay_ranks_and_undo_history_compared']:raise ValueError('keylog CPU fixture scope')
    for n,h in keylog['dependency_reports'].items():require_hash(base/n/'report.json',h)
    for n,h in keylog['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in keylog['artifacts'].items():require_hash(base/'cpu_keylog'/n,h)
    report['keylog_replay_fixture']=dict(counts=keylog['counts'],state_bytes=64,baseline_bytes=24,temporary_stack_bytes=keylog['stack_bytes_including_nested_calls'],native_wrapper_implemented=True,game_memory_or_stack_adopted=False)
    report['limits'].append('Keylog64 replay is a standalone CPU fixture only. Immutable baseline identity is the caller responsibility; no cached ranks or game display/commit/save bridge is installed.')
    for p in [base/'cpu_keylog/report.json',base/'cpu_keylog/wrapper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    ten_display=read(base/'cpu_ten_cell_display/report.json')
    if not ten_display['passed'] or ten_display['rom_integrated'] or ten_display['source_surface_bytes']!=24 or ten_display['output_max_bytes']!=41 or ten_display['complete_syllable_slot_vectors']!=111720 or ten_display['full_syllable_keylog_paths']!=11172 or ten_display['loaded_tenth_cell_syllables']!=11172 or not ten_display['native_readonly_keylog_to_display']:raise ValueError('ten-cell display CPU fixture scope')
    for n,h in ten_display['dependency_reports'].items():require_hash(base/n/'report.json',h)
    for n,h in ten_display['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in ten_display['artifacts'].items():require_hash(base/'cpu_ten_cell_display'/n,h)
    report['ten_cell_display_fixture']=dict(counts=ten_display['counts'],source_surface_bytes=24,output_max_bytes=41,temporary_stack_bytes=ten_display['stack_bytes_including_nested_calls'],native_readonly_keylog_to_display=True,game_hooks_installed=False)
    report['limits'].append('Ten-cell keylog -> display is connected only in CPU fixtures. Actual 41-byte cache provider, cursor/padding/rendering and save integration are pending.')
    for p in [base/'cpu_ten_cell_display/report.json',base/'cpu_ten_cell_display/helper.bin',base/'cpu_ten_cell_display/bridge.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    ten_base=read(base/'cpu_ten_cell_baseline/report.json')
    if not ten_base['passed'] or ten_base['rom_integrated'] or ten_base['record_format_adopted'] or ten_base['baseline_bytes']!=24 or ten_base['complete_syllable_slot_vectors']!=111720 or ten_base['occupied_uint16_rank_domain']!=65536 or ten_base['native_tenth_cell_baseline_to_display_paths']!=11172 or not ten_base['caller_selected_import'] or not ten_base['legacy_marker0_import_preserved']:raise ValueError('ten-cell caller-selected baseline CPU fixture scope')
    for n,h in ten_base['dependency_reports'].items():require_hash(base/n/'report.json',h)
    for n,h in ten_base['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in ten_base['artifacts'].items():require_hash(base/'cpu_ten_cell_baseline'/n,h)
    report['ten_cell_baseline_fixture']=dict(counts=ten_base['counts'],baseline_bytes=24,caller_selected_import=True,legacy_marker0_import_preserved=True,legacy_editing_implemented=False,save_format_adopted=False,game_hooks_installed=False)
    report['limits'].append('Caller-selected baseline24 decoder preserves marker0/1 imports via no-write legacy routing only. Actual Japanese editing, native import, committed save format and game lifetime remain pending.')
    for p in [base/'cpu_ten_cell_baseline/report.json',base/'cpu_ten_cell_baseline/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/analyze_keyboard_legacy_edit.py')],timeout=30,check=True)
    legacy=read(base/'legacy_edit.json')
    if not legacy['passed'] or legacy['rom_integrated'] or legacy['source_sha256']!=profile['sha256'] or legacy['current_rom_sha256']!=identity or not legacy['findings']['marker_ignored_on_import'] or legacy['findings']['import_checks_capacity'] or legacy['mixed_identity_candidate']['structural_tokens']!=484 or legacy['mixed_identity_candidate']['hangul_rank_collisions']!=0:raise ValueError('native legacy edit scope')
    for n,h in legacy['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    report['native_legacy_edit_observation']=dict(counts=legacy['counts'],native_page_cells=[p['cells'] for p in legacy['selector_table']['pages']],unique_native_selector_tokens=legacy['selector_table']['unique_tokens'],original_import_cursor=legacy['findings']['imported_cursor'],mixed_identity_host_contract=True,actual_nonempty_import_observed=False,native_cursor_aware_Hangul_editing_implemented=False)
    report['limits'].append('Original import leaves cursor at start and native editing permits interior deletion/overwrite. Current pure-Hangul tail-only keylog does not preserve opaque legacy cells or these cursor operations and must not be installed as a universal editor.')
    report['artifacts']['analysis/hangul_keyboard_v1/legacy_edit.json']=sha((base/'legacy_edit.json').read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_hangul_mixed_editor.py')],timeout=60,check=True)
    mixed=read(base/'mixed_editor_host.json')
    if not mixed['passed'] or mixed['rom_integrated'] or mixed['tests']!=6 or mixed['syllable_slot_paths']!=111720 or mixed['structural_native_token_capacity_paths']!=4840 or not mixed['partial_anywhere_blocks_confirmation']:raise ValueError('mixed editor host scope')
    for p,h in mixed['dependencies'].items():require_hash(ROOT/p,h)
    for n,h in mixed['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    report['mixed_editor_host_candidate']=dict(tests=6,syllable_slot_paths=111720,native_structural_token_capacity_paths=4840,imported_cursor=0,native_CPU_editor_implemented=False,game_state_ABI_adopted=False)
    report['limits'].append('Cursor-aware mixed editor is implemented only as a host reference candidate. Snapshot history is not the older64-byte keylog ABI; native code, display/save and user presentation review are pending.')
    report['artifacts']['analysis/hangul_keyboard_v1/mixed_editor_host.json']=sha((base/'mixed_editor_host.json').read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_hangul_mixed_state.py')],timeout=60,check=True)
    mixed_state=read(base/'mixed_state_host.json')
    if not mixed_state['passed'] or mixed_state['rom_integrated'] or mixed_state['game_RAM_allocated'] or mixed_state['native_CPU_codec'] or mixed_state['state_bytes']!=588 or mixed_state['tests']!=4 or mixed_state['occupied_word_domain']!=65536:raise ValueError('mixed serialized host scope')
    for p,h in mixed_state['dependencies'].items():require_hash(ROOT/p,h)
    for n,h in mixed_state['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    report['mixed_state_host_candidate']=dict(state_bytes=588,undo_entries=70,undo_entry_bytes=8,tests=4,native_CPU_codec=False,game_RAM_allocated=False)
    report['limits'].append('Mixed state588-byte delta codec is host-only and not mapped to game RAM; previous64-byte overlay cannot contain it. Native bounded editing and memory/lifetime verification remain pending.')
    report['artifacts']['analysis/hangul_keyboard_v1/mixed_state_host.json']=sha((base/'mixed_state_host.json').read_bytes())
    mixed_undo=read(base/'cpu_mixed_undo/report.json')
    if not mixed_undo['passed'] or mixed_undo['rom_integrated'] or not mixed_undo['trusted_canonical_input_required'] or mixed_undo['complete_history_validation'] or not mixed_undo['forged_forward_transition_counterexample_accepted'] or mixed_undo['state_bytes']!=588 or mixed_undo['counts']['full_word_domain']!=65536 or mixed_undo['counts']['syllable_history_undo']!=37506 or mixed_undo['native_token_cursor_paths']!=5324:raise ValueError('mixed undo trusted CPU scope')
    for n,h in mixed_undo['dependency_reports'].items():require_hash(base/n/'report.json',h)
    for n,h in mixed_undo['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in mixed_undo['artifacts'].items():require_hash(base/'cpu_mixed_undo'/n,h)
    report['mixed_undo_CPU_candidate']=dict(counts=mixed_undo['counts'],helper_bytes=mixed_undo['helper_bytes'],stack_bytes=52,trusted_canonical_input_required=True,complete_history_validation=False,game_hooks_installed=False)
    report['limits'].append('Mixed B/undo CPU kernel requires caller-established canonical state. A structurally valid impossible-history counterexample is accepted, so this is NOT a full native decoder and must not process untrusted imported/save state.')
    for p in [base/'cpu_mixed_undo/report.json',base/'cpu_mixed_undo/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    mixed_feed=read(base/'cpu_mixed_feed/report.json')
    if not mixed_feed['passed'] or mixed_feed['rom_integrated'] or mixed_feed['game_RAM_allocated'] or not mixed_feed['trusted_canonical_input_required'] or mixed_feed['complete_history_validation'] or not mixed_feed['forged_history_counterexample_accepted'] or mixed_feed['state_bytes']!=588 or mixed_feed['counts']['row_key_vectors']!=447680 or mixed_feed['counts']['syllable_slot_paths']!=111720 or mixed_feed['counts']['full_word_domain']!=65536 or mixed_feed['counts']['uninterrupted_native_sequences']!=220:raise ValueError('mixed feed trusted CPU scope')
    for n,h in mixed_feed['dependency_reports'].items():require_hash(base/n/'report.json',h)
    for n,h in mixed_feed['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in mixed_feed['artifacts'].items():require_hash(base/'cpu_mixed_feed'/n,h)
    report['mixed_feed_CPU_candidate']=dict(counts=mixed_feed['counts'],helper_bytes=mixed_feed['helper_bytes'],stack_bytes=52,trusted_canonical_input_required=True,complete_history_validation=False,game_hooks_installed=False)
    report['limits'].append('Mixed feed and undo are connected only in CPU fixtures with caller-established canonical state. Historical forgery is not fully rejected; actual cursor/input wiring, memory lifetime, display/save and runtime remain pending.')
    for p in [base/'cpu_mixed_feed/report.json',base/'cpu_mixed_feed/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_hangul_mixed_replay.py')],timeout=60,check=True)
    mixed_replay=read(base/'mixed_replay_host.json')
    layout=mixed_replay['layout_candidate']
    if not mixed_replay['passed'] or mixed_replay['rom_integrated'] or mixed_replay['native_CPU_codec'] or mixed_replay['external_baseline_required'] or mixed_replay['state_bytes']!=76 or mixed_replay['tests']!=5 or mixed_replay['syllable_slot_paths']!=111720 or mixed_replay['occupied_word_domain']!=65536 or layout['actual_game_memory_adopted'] or layout['editor_bytes']!=96 or layout['state_offset']!=20:raise ValueError('mixed replay host/memory scope')
    for p,h in mixed_replay['dependencies'].items():require_hash(ROOT/p,h)
    for n,h in mixed_replay['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    report['mixed_replay_host_candidate']=dict(state_bytes=76,tests=5,external_baseline_required=False,editor_bytes=96,metadata_bytes=20,native_CPU_codec=False,actual_game_memory_adopted=False)
    report['limits'].append('Self-contained mixed replay76 plus preserved UI16 and relocated destination4 numerically fits observed96-byte editor. This is not an adopted game layout; old pointer/padding/flatten/destination consumers still require coordinated replacement.')
    report['artifacts']['analysis/hangul_keyboard_v1/mixed_replay_host.json']=sha((base/'mixed_replay_host.json').read_bytes())
    replay_cpu=read(base/'cpu_mixed_replay/report.json')
    if not replay_cpu['passed'] or replay_cpu['rom_integrated'] or replay_cpu['state_bytes']!=76 or replay_cpu['output_bytes']!=24 or replay_cpu['stack_bytes']!=68 or replay_cpu['temporary_history_bytes']!=0 or not replay_cpu['full_compact_key_stream_validated'] or not replay_cpu['byte_alignment_supported'] or replay_cpu['counts']['row_key_vectors']!=447680 or replay_cpu['counts']['syllable_slot_paths']!=111720 or replay_cpu['counts']['occupied_word_domain']!=65536:raise ValueError('compact replay CPU scope')
    for n,h in replay_cpu['dependency_reports'].items():require_hash(base/n/'report.json',h)
    for p,h in replay_cpu['host_dependency'].items():require_hash(ROOT/p,h)
    for n,h in replay_cpu['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in replay_cpu['artifacts'].items():require_hash(base/'cpu_mixed_replay'/n,h)
    report['mixed_replay_CPU_candidate']=dict(counts=replay_cpu['counts'],helper_bytes=replay_cpu['helper_bytes'],state_bytes=76,output_bytes=24,stack_bytes=68,temporary_history_bytes=0,full_compact_key_stream_validated=True,game_hooks_installed=False)
    report['limits'].append('Compact76 -> mixed current24 decoder validates/replays all packed keys with68-byte stack in CPU fixtures only. Its count/cap/cursor/activeFF surface differs from old pure-Hangul display ABI; actual mixed display, edit handlers and native reader replacement remain pending.')
    for p in [base/'cpu_mixed_replay/report.json',base/'cpu_mixed_replay/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    mixed_display=read(base/'cpu_mixed_display/report.json')
    if not mixed_display['passed'] or mixed_display['rom_integrated'] or mixed_display['surface_bytes']!=24 or mixed_display['max_output_bytes']!=41 or mixed_display['stack_bytes']!=36 or not mixed_display['partial_anywhere_edit_preserved'] or not mixed_display['partial_anywhere_commit_rejected'] or mixed_display['native_replay_display_paths']!=11172 or mixed_display['counts']['occupied_word_domain']!=131072 or mixed_display['counts']['complete_syllable_slot_paths']!=111720 or mixed_display['counts']['native_token_slot_paths']!=4840:raise ValueError('mixed display CPU scope')
    for n,h in mixed_display['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in mixed_display['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in mixed_display['artifacts'].items():require_hash(base/'cpu_mixed_display'/n,h)
    report['mixed_display_CPU_candidate']=dict(counts=mixed_display['counts'],helper_bytes=mixed_display['helper_bytes'],surface_bytes=24,max_output_bytes=41,stack_bytes=36,partial_anywhere_commit_rejected=True,native_replay_display_paths=11172,game_hooks_installed=False)
    report['limits'].append('Mixed current24 -> display bytes is connected to native compact replay only in CPU fixtures. Structural legacy bytes are preserved, not validated for glyph/input membership or raw save safety; actual41-byte cache/cursor/destination wiring and runtime remain pending.')
    for p in [base/'cpu_mixed_display/report.json',base/'cpu_mixed_display/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    keyedit=read(base/'cpu_mixed_keyedit/report.json')
    if not keyedit['passed'] or keyedit['rom_integrated'] or keyedit['state_bytes']!=76 or keyedit['own_stack_bytes']!=128 or keyedit['nested_stack_bytes']!=196 or keyedit['temporary_history_bytes']!=0 or not keyedit['original_and_proposal_replay_validated'] or not keyedit['history_pop_only'] or keyedit['counts']['syllable_final_key_paths']!=11172 or keyedit['counts']['packed_position_key_paths']!=2800 or keyedit['counts']['uninterrupted_actions']!=1000 or keyedit['counts']['native_edit_replay_display_paths']!=11172:raise ValueError('compact keyedit CPU scope')
    for n,h in keyedit['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in keyedit['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in keyedit['artifacts'].items():require_hash(base/'cpu_mixed_keyedit'/n,h)
    report['mixed_keyedit_CPU_candidate']=dict(counts=keyedit['counts'],helper_bytes=keyedit['helper_bytes'],state_bytes=76,nested_stack_bytes=196,history_pop_only=True,game_hooks_installed=False)
    report['limits'].append('Compact accepted-key append/pop validates original and proposed replay; actual CPU edit/replay/display connected only in fixtures. No-history canonical B and movement/native rebase are provided by separate fixture helpers, not this keyedit helper. Game196-byte stack/IRQ budget, hooks and persistence remain unresolved.')
    for p in [base/'cpu_mixed_keyedit/report.json',base/'cpu_mixed_keyedit/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    rebase=read(base/'cpu_mixed_rebase/report.json')
    if not rebase['passed'] or rebase['rom_integrated'] or rebase['state_bytes']!=76 or rebase['own_stack_bytes']!=128 or rebase['nested_stack_bytes']!=196 or rebase['temporary_history_bytes']!=0 or not rebase['canonical_delete_no_history_only'] or not rebase['sealed_partials_preserved'] or not rebase['native_overwrite_not_insert'] or rebase['counts']['canonical_word_slot_paths']!=111910 or rebase['counts']['action_uint16_domain']!=65536 or rebase['counts']['native_capacity_cursor_paths']!=31460 or rebase['counts']['uninterrupted_mixed_actions']!=5000 or rebase['counts']['native_dispatch_calls']<5000:raise ValueError('compact rebase CPU scope')
    for n,h in rebase['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in rebase['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in rebase['artifacts'].items():require_hash(base/'cpu_mixed_rebase'/n,h)
    report['mixed_rebase_CPU_candidate']=dict(counts=rebase['counts'],helper_bytes=rebase['helper_bytes'],dispatch_bytes=rebase['dispatch_bytes'],state_bytes=76,nested_stack_bytes=196,sealed_partials_preserved=True,native_overwrite_not_insert=True,game_hooks_installed=False)
    report['limits'].append('Compact cursor/native/canonical-B rebasing is connected with accepted-key append/pop only in CPU fixtures. Structural native words are not glyph/input/save membership; actual initializer/import, editor/cache/destination replacements, stack/IRQ lifetime and save/fresh-load remain unresolved.')
    for p in [base/'cpu_mixed_rebase/report.json',base/'cpu_mixed_rebase/helper.bin',base/'cpu_mixed_rebase/dispatch.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    legacy_import=read(base/'cpu_mixed_legacy_import/report.json')
    if not legacy_import['passed'] or legacy_import['rom_integrated'] or not legacy_import['caller_selected_legacy_required'] or not legacy_import['legacy_marker_ignored'] or not legacy_import['empty_initialization_supported'] or legacy_import['state_bytes']!=76 or legacy_import['stack_bytes']!=96 or legacy_import['source_sha256']!=profile['sha256'] or legacy_import['counts']['byte_pair_domain']!=65536 or legacy_import['counts']['token_capacity_slot_paths']!=26620 or legacy_import['counts']['original_leaf_comparisons']!=4840 or legacy_import['counts']['native_import_edit_undo_paths']!=4840:raise ValueError('bounded mixed legacy import CPU scope')
    for n,h in legacy_import['dependencies'].items():require_hash(base/n/'report.json',h)
    require_hash(base/'legacy_edit.json',legacy_import['legacy_source_dependency'])
    for n,h in legacy_import['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in legacy_import['artifacts'].items():require_hash(base/'cpu_mixed_legacy_import'/n,h)
    report['mixed_legacy_import_CPU_candidate']=dict(counts=legacy_import['counts'],helper_bytes=legacy_import['helper_bytes'],state_bytes=76,stack_bytes=96,caller_selected_legacy_required=True,game_hooks_installed=False)
    report['limits'].append('Bounded legacy record -> compact76 initializes empty/imported state and connects to native editing only in CPU fixtures. Caller must already select legacy format; no new Hangul record discrimination, real nonempty game import, UI/destination initialization or persistence claim.')
    for p in [base/'cpu_mixed_legacy_import/report.json',base/'cpu_mixed_legacy_import/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    editor_init=read(base/'cpu_editor_init/report.json')
    if not editor_init['passed'] or editor_init['rom_integrated'] or editor_init['actual_game_layout_adopted'] or not editor_init['clear_service_modeled'] or editor_init['source_sha256']!=profile['sha256'] or editor_init['current_rom_sha256']!=identity or editor_init['editor_bytes']!=96 or editor_init['stack_bytes']!=116 or editor_init['counts']['original_initializer_calls']!=10240 or editor_init['counts']['modeled_clear_calls']!=10240 or editor_init['counts']['UI16_native_comparisons']!=10240:raise ValueError('editor initialization contract scope')
    if not editor_init['shim_original_register_ABI_fixture'] or editor_init['shim_nested_stack_bytes']!=140 or editor_init['counts']['shim_calls']!=10479 or editor_init['counts']['shim_rejected']!=239 or editor_init['counts']['shim_original_liveout_comparisons']!=10240:raise ValueError('initializer register shim fixture scope')
    if len(editor_init['direct_initializer_BL_candidate_windows'])!=5:raise ValueError('bounded initializer caller windows')
    for window in editor_init['direct_initializer_BL_candidate_windows']:
        a=int(window['start'],16)-0x08000000;b=int(window['end_exclusive'],16)-0x08000000
        if sha(original[a:b])!=window['sha256'] or sha(rom[a:b])!=window['sha256']:raise ValueError('bounded initializer caller identity')
    for region in editor_init['bounded_consumer_regions']:
        a=int(region['start'],16)-0x08000000;b=int(region['end_exclusive'],16)-0x08000000
        if sha(source.read_bytes()[a:b])!=region['sha256'] or sha(product.read_bytes()[a:b])!=region['sha256']:raise ValueError('bounded editor consumer identity')
    for n,h in editor_init['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in editor_init['artifacts'].items():require_hash(base/'cpu_editor_init'/n,h)
    report['mixed_editor_init_CPU_candidate']=dict(counts=editor_init['counts'],helper_bytes=editor_init['helper_bytes'],editor_bytes=96,stack_bytes=116,shim_bytes=editor_init['shim_bytes'],shim_nested_stack_bytes=140,original_register_liveout_fixture=True,clear_service_modeled=True,bounded_consumer_regions=len(editor_init['bounded_consumer_regions']),direct_BL_candidate_windows=5,actual_game_layout_adopted=False,game_hooks_installed=False)
    report['limits'].append('Editor96 staging and bridge preserve original valid-domain argument/live-out ABI under a modeled clear-service fixture, not a game hook or whole-clear execution. Compatibility r2=editor+32 must not reach old consumers. Five direct BL windows and bounded consumer inventory do not establish complete caller/writer/reference population; real layout/cache/answer compare/commit/stack/IRQ and persistence remain unresolved.')
    for p in [base/'cpu_editor_init/report.json',base/'cpu_editor_init/helper.bin',base/'cpu_editor_init/shim.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    mixed_count=read(base/'cpu_mixed_count/report.json')
    if not mixed_count['passed'] or mixed_count['rom_integrated'] or mixed_count['source_sha256']!=profile['sha256'] or mixed_count['current_rom_sha256']!=identity or mixed_count['own_stack_bytes']!=32 or mixed_count['nested_stack_bytes']!=100 or mixed_count['counts']['original_leaf_comparisons']!=570 or mixed_count['counts']['syllable_history_queries']!=22344 or mixed_count['counts']['native_edit_query_paths']!=11172 or len(mixed_count['direct_count_BL_candidate_windows'])!=4:raise ValueError('logical caret/count CPU candidate')
    for n,h in mixed_count['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in mixed_count['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in mixed_count['artifacts'].items():require_hash(base/'cpu_mixed_count'/n,h)
    if sha(original[0x35620:0x3562C])!=mixed_count['original_leaf_sha256'] or rom[0x35620:0x3562C]!=original[0x35620:0x3562C]:raise ValueError('logical count source leaf')
    for window in mixed_count['direct_count_BL_candidate_windows']:
        a=int(window['start'],16)-0x08000000;b=int(window['end_exclusive'],16)-0x08000000
        if sha(original[a:b])!=window['sha256'] or sha(rom[a:b])!=window['sha256']:raise ValueError('logical count caller identity')
    report['mixed_logical_count_CPU_candidate']=dict(counts=mixed_count['counts'],helper_bytes=mixed_count['helper_bytes'],nested_stack_bytes=100,direct_BL_candidate_windows=4,original_register_ABI=False,game_hooks_installed=False)
    report['limits'].append('Logical caret/count candidate fully replays compact state, matching valid native counts in leaf fixtures. New value/status ABI is not old pointer_count live-outs. Fixed-cell renderer profile advances eight pixels, unlike twelve-pixel dialogue; actual keyboard font selection/cursor integration, caller replacement, cache/commit/save and game stack/IRQ budget remain unresolved.')
    for p in [base/'cpu_mixed_count/report.json',base/'cpu_mixed_count/helper.bin',base/'cpu_mixed_count/edit_dependency.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    field_parser=read(base/'cpu_editfield_parser/report.json')
    if not field_parser['passed'] or field_parser['rom_integrated'] or field_parser['current_play_rom_sha256']!=identity or field_parser['source_sha256']!=profile['sha256'] or not field_parser['transfer_intercepted'] or field_parser['cell_advance']!=8 or field_parser['cell_bytes']!=64 or field_parser['parser_stack_fixture_bytes']!=40 or field_parser['counts']['parser_calls']!=24584 or field_parser['counts']['syllable_provider_paths']!=22344 or field_parser['counts']['full_field_tint_paths']!=160 or field_parser['counts']['maximum_emitted_stream_bytes']!=41 or field_parser['counts']['transfer_interceptions']!=field_parser['counts']['parser_calls']:raise ValueError('native fixed-cell editfield parser scope')
    if field_parser['product_sha256']!=read(base/'glyph_supply.json')['rom_sha256']:raise ValueError('fixed-cell glyph artifact agreement')
    field_product=ROOT/'poc/output/exe45_ko_development_keyboard_glyphs_v1.gba';require_hash(field_product,field_parser['product_sha256']);field_rom=field_product.read_bytes()
    require_hash(field_product.with_suffix('.json'),field_parser['manifest_sha256'])
    require_hash(base/'glyph_provider_cpu.json',field_parser['glyph_provider_report_sha256'])
    for n,h in field_parser['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in field_parser['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in field_parser['artifacts'].items():require_hash(base/'cpu_editfield_parser'/n,h)
    for region in field_parser['bounded_native_code']:
        at=int(region['source_offset'],16)
        if sha(field_rom[at:at+region['bytes']])!=region['sha256']:raise ValueError('native parser code identity')
    report['mixed_display_native_parser_CPU_candidate']=dict(counts=field_parser['counts'],cell_advance=8,cell_bytes=64,maximum_stream_bytes=41,parser_stack_fixture_bytes=40,transfer_intercepted=True,game_hooks_installed=False)
    report['limits'].append('Emitted mixed display reaches exact glyph-only ROM fixed-cell parser/dispatch/copier and E5 padding in CPU fixtures. Native transfer return is modeled: no descriptor0 cache41 ownership, actual keyboard font/cursor route, upload/scanout, editor/save integration or game stack/IRQ proof.')
    for p in [base/'cpu_editfield_parser/report.json',base/'cpu_editfield_parser/display_helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_transfer_lifetime.py')],timeout=60,check=True)
    lifetime=read(base/'transfer_lifetime.json')
    if not lifetime['passed'] or lifetime['rom_integrated'] or lifetime['source_sha256']!=profile['sha256'] or lifetime['rom_sha256']!=identity or lifetime['observed_transfers']!=860 or lifetime['font']!='0x08619EF8' or lifetime['cell_advance']!=8 or lifetime['transfer_bytes']!=1280 or lifetime['render_cells']!=20 or lifetime['queue']['observed_delay_frames']!=1 or not all(lifetime[k] for k in ['original_font_pixels_match','stage_unchanged_at_consume','native_VRAM_pixels_match']):raise ValueError('native editor transfer lifetime observation')
    for region in lifetime['bounded_native_code']:
        at=int(region['source_offset'],16)
        if sha(original[at:at+region['bytes']])!=region['sha256'] or rom[at:at+region['bytes']]!=original[at:at+region['bytes']]:raise ValueError('native transfer code identity')
    for n,h in lifetime['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for p,h in lifetime['artifacts'].items():require_hash(ROOT/p,h);report['artifacts'][p]=h
    report['artifacts']['analysis/hangul_keyboard_v1/transfer_lifetime.json']=sha((base/'transfer_lifetime.json').read_bytes())
    report['native_transfer_lifetime_observation']=dict(transfers=860,font=lifetime['font'],cell_advance=8,render_cells=20,transfer_bytes=1280,delay_frames=1,stage_unchanged_at_consume=True,native_VRAM_pixels_match=True,Hangul_observed=False)
    bridge=read(base/'cpu_cache_bridge/report.json')
    if not bridge['passed'] or bridge['rom_integrated'] or bridge['helper_bytes']!=804 or bridge['own_stack_bytes']!=44 or bridge['nested_stack_bytes']!=112 or bridge['required_cache_extent']!=41 or bridge['counts']!={'calls':852,'rejected':311,'maximum_stream_bytes':41,'packed_history_paths':70}:raise ValueError('compact edit cache CPU bridge')
    for n,h in bridge['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in bridge['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in bridge['artifacts'].items():require_hash(base/'cpu_cache_bridge'/n,h)
    for p in [base/'cpu_cache_bridge/report.json',base/'cpu_cache_bridge/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['mixed_cache_bridge_CPU_candidate']=dict(counts=bridge['counts'],helper_bytes=804,required_cache_extent=41,nested_stack_bytes=112,game_hooks_installed=False)
    report['limits'].append('Actual native Japanese editor mono8 font and next-frame1280-byte pixel transfer observed860 times; not Hangul rendering or complete writer ownership. Compact76 -> bounded41-byte cache bridge is CPU-only; native descriptor32 replacement, cache/source/stack/IRQ ownership, full input/commit/record/save and fresh-load remain unresolved.')
    pipeline=read(base/'cpu_cache_pipeline/report.json')
    if not pipeline['passed'] or pipeline['rom_integrated'] or pipeline['product_sha256']!=field_parser['product_sha256'] or pipeline['source_sha256']!=profile['sha256'] or not pipeline['BIOS_service_modeled'] or pipeline['transfer_intercepted'] or pipeline['render_cells']!=20 or pipeline['transfer_bytes']!=1280 or pipeline['parser_with_enqueue_stack_bytes']!=56 or pipeline['queue_drain_stack_bytes']!=48 or pipeline['counts']!={'renders':639,'native_key_actions':143,'rejected_key_actions':3,'history_pop_actions':70,'queue_saturation_rejections':1,'maximum_stream_bytes':41}:raise ValueError('compact CPU cache/parser/queue pipeline scope')
    for n,h in pipeline['dependencies'].items():require_hash(base/n/'report.json',h)
    require_hash(base/'transfer_lifetime.json',pipeline['transfer_lifetime_report_sha256'])
    require_hash(field_product.with_suffix('.json'),pipeline['manifest_sha256'])
    for n,h in pipeline['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in pipeline['artifacts'].items():require_hash(base/'cpu_cache_pipeline'/n,h)
    for region in pipeline['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or field_rom[a:b]!=original[a:b]:raise ValueError('pipeline native queue/BIOS wrapper identity')
    for p in [base/'cpu_cache_pipeline/report.json',base/'cpu_cache_pipeline/cache.bin',base/'cpu_cache_pipeline/edit.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['mixed_edit_cache_parser_queue_CPU_candidate']=dict(counts=pipeline['counts'],render_cells=20,transfer_bytes=1280,parser_enqueue_stack_bytes=56,queue_drain_stack_bytes=48,BIOS_service_modeled=True,game_hooks_installed=False)
    report['limits'].append('CPU compact edit/cache reaches original20-cell parser, native enqueue/drain and modeled CpuFastSet output. No host rewriting between accepted-key edit and pixel production; not game hook ABI/cache ownership, VBlank/scanout, Hangul keyboard screen or save/fresh-load proof.')
    copy_shim=read(base/'cpu_copy_shim/report.json')
    if not copy_shim['passed'] or copy_shim['rom_integrated'] or copy_shim['source_sha256']!=profile['sha256'] or copy_shim['current_rom_sha256']!=identity or copy_shim['helper_bytes']!=924 or copy_shim['nested_stack_bytes']!=132 or copy_shim['original_provider_with_shim_stack_bytes']!=176 or copy_shim['counts']!={'new_layout_calls':531,'empty_fallbacks':76,'legacy_provider_comparisons':95,'direct_copy_ABI_checks':7,'maximum_stream_bytes':41}:raise ValueError('selective native copy shim scope')
    for n,h in copy_shim['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in copy_shim['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in copy_shim['artifacts'].items():require_hash(base/'cpu_copy_shim'/n,h)
    for region in copy_shim['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('copy shim native source identity')
    literal=copy_shim['fixture_literal'];a=int(literal['source_offset'],16)
    if original[a:a+4]!=bytes.fromhex(literal['expected_hex']) or rom[a:a+4]!=original[a:a+4]:raise ValueError('copy pointer source')
    for p in [base/'cpu_copy_shim/report.json',base/'cpu_copy_shim/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['selective_copy_shim_CPU_candidate']=dict(counts=copy_shim['counts'],helper_bytes=924,nested_stack_bytes=132,provider_nested_stack_bytes=176,game_hooks_installed=False)
    report['limits'].append('Selective descriptor0/slot0 copy shim preserves native provider and direct copy live-outs under CPU fixtures. Gate is not format discrimination; caller must establish new editor layout. One copy-pointer literal changes only in fixture, not ROM. Real cache41 writer/lifetime, full descriptor0 slot population, IRQ/stack, malformed-input UI and save remain unresolved.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_buffer_writers.py')],timeout=60,check=True)
    writers=read(base/'buffer_writers.json')
    if not writers['passed'] or writers['rom_integrated'] or writers['rom_sha256']!=identity or writers['source_sha256']!=profile['sha256'] or writers['providers']!=860 or writers['protected_cache_consumptions']!=860 or writers['protected_stage_intervals']!=860 or writers['observed_protected_writes']!=0 or writers['scoped_regression']['matched_regions']!=36:raise ValueError('bounded native buffer writer observation')
    # Full snapshot identity failed; do not silently promote scoped buffer equality.
    if writers['whole_snapshot_regression']['byte_identical'] or len(writers['whole_snapshot_regression']['different_files'])!=27:raise ValueError('writer observation regression scope changed')
    require_hash(ROOT/'poc/runtime/hangul-keyboard-v1-transfer-lifetime/result.json',writers['baseline_result_sha256'])
    for n,h in writers['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for p,h in writers['artifacts'].items():require_hash(ROOT/p,h);report['artifacts'][p]=h
    for ins in writers['writer_instructions']:
        a=ins['offset'];code=bytes.fromhex(ins['hex'])
        if original[a:a+len(code)]!=code or rom[a:a+len(code)]!=code:raise ValueError('observed writer source')
    report['artifacts']['analysis/hangul_keyboard_v1/buffer_writers.json']=sha((base/'buffer_writers.json').read_bytes())
    report['native_buffer_writer_observation']=dict(providers=860,protected_cache_windows=860,protected_stage_windows=860,protected_writes_observed=0,scoped_snapshot_regions_matched=36,whole_snapshot_byte_identical=False,cache41_capacity_adopted=False,game_hooks_installed=False)
    report['limits'].append('Normal Japanese route writer callbacks calibrated27520 byte-cache stores and275200 word-stage stores, with no protected-interval writes. Tail9 zero/unwritten does not prove global free space/41-byte ownership.36 selected buffer snapshots equal baseline; whole45-snapshot comparison has27 differences with RTC/CPU differences and is NOT a passed byte-identical regression.')
    mixed_record=read(base/'cpu_mixed_record/report.json')
    if not mixed_record['passed'] or mixed_record['rom_integrated'] or mixed_record['format_adopted'] or not mixed_record['caller_selected_new_format_required'] or not mixed_record['native_encoder'] or mixed_record['native_record_importer'] or mixed_record['encoder_bytes']!=408 or mixed_record['nested_stack_bytes']!=96 or mixed_record['max_record_bytes']!=22:raise ValueError('mixed committed record CPU scope')
    if mixed_record['counts']!={'calls':77393,'rejected':54273,'word_domain':65536,'cap10_last_slot_syllables':11172,'host_roundtrips':23120,'pure_candidate_compatibility':72,'maximum_record_bytes':22}:raise ValueError('mixed committed record coverage')
    if mixed_record['source_sha256']!=profile['sha256'] or mixed_record['current_rom_sha256']!=identity or not mixed_record['legacy_counterexample_original_leaf_executed']:raise ValueError('mixed record original importer evidence')
    if sha(original[0x3558C:0x355BE])!=mixed_record['original_import_leaf_sha256'] or rom[0x3558C:0x355BE]!=original[0x3558C:0x355BE]:raise ValueError('mixed record legacy leaf identity')
    ambiguity=mixed_record['legacy_ambiguity_counterexample']
    if ambiguity['record_hex']!='81e500ffffffffffffe5' or ambiguity['new_identity']!='곥' or ambiguity['legacy_identity']!='empty':raise ValueError('legacy discrimination counterexample')
    for n,h in mixed_record['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in mixed_record['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in mixed_record['artifacts'].items():require_hash(base/'cpu_mixed_record'/n,h)
    for p in [base/'cpu_mixed_record/report.json',base/'cpu_mixed_record/encoder.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['mixed_committed_record_CPU_candidate']=dict(counts=mixed_record['counts'],encoder_bytes=408,nested_stack_bytes=96,max_record_bytes=22,native_record_importer=False,original_legacy_ambiguity_executed=True,format_adopted=False,game_hooks_installed=False)
    report['limits'].append('Native mixed fixed-record encoder rejects partial/empty states and preserves pure candidate bytes; actual CPU outputs are imported/redisplayed only by HOST. Original importer executes packed rank229 as empty, so marker alone cannot establish legacy discrimination. Native packed import, caller-selected format integration/migration, normalize bypass, all save consumers and fresh-load remain unresolved.')
    record_import=read(base/'cpu_mixed_record_import/report.json')
    if not record_import['passed'] or record_import['rom_integrated'] or record_import['format_adopted'] or not record_import['caller_selected_new_format_required'] or not record_import['native_record_importer'] or record_import['helper_bytes']!=486 or record_import['nested_stack_bytes']!=124 or record_import['counts']!={'calls':83262,'rejected':60058,'word_domain':65536,'encoder_import_syllables':11172}:raise ValueError('selected mixed record native import scope')
    for n,h in record_import['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in record_import['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in record_import['artifacts'].items():require_hash(base/'cpu_mixed_record_import'/n,h)
    for p in [base/'cpu_mixed_record_import/report.json',base/'cpu_mixed_record_import/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['mixed_selected_record_import_CPU_candidate']=dict(counts=record_import['counts'],helper_bytes=486,nested_stack_bytes=124,native_record_importer=True,format_adopted=False,game_hooks_installed=False)
    report['limits'].append('Additional selected-format importer connects actual CPU encoder output to compact76 for11172 full-cap10 final syllables without HOST rewriting. Earlier encoder report HOST-only importer limit applies to that report, not this new helper. No automatic format detection, original commit/reader replacement, migration, native saves or fresh-process reload claim.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/analyze_keyboard_record_markers.py')],timeout=60,check=True)
    markers=read(base/'record_markers.json')
    if not markers['passed'] or markers['rom_integrated'] or markers['format_discriminator_adopted'] or markers['source_sha256']!=profile['sha256'] or markers['current_rom_sha256']!=identity or markers['metadata_rows']!=26 or markers['counts']!={'reader_calls':14592,'zero_marker_skipped':57,'nonzero_marker_selected':14535}:raise ValueError('bounded marker selector scope')
    if markers['prerequisite_gate_executed'] or markers['RNG_selection_executed'] or markers['observed_snapshot_count']!=9 or markers['observed_markers']!={'0':511,'1':2}:raise ValueError('marker observation scope')
    require_hash(base/'consumer_inventory.json',markers['inventory_sha256'])
    for n,h in markers['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for p,h in markers['artifacts'].items():require_hash(ROOT/p,h);report['artifacts'][p]=h
    for region in markers['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('marker native code identity')
    report['artifacts']['analysis/hangul_keyboard_v1/record_markers.json']=sha((base/'record_markers.json').read_bytes())
    report['bounded_record_marker_analysis']=dict(counts=markers['counts'],observed_markers=markers['observed_markers'],observed_snapshots=9,format_discriminator_adopted=False)
    report['limits'].append('Original record selection loop treats any nonzero marker as occupied across57 slots/26 metadata rows. Nine normal-route snapshots contain511 zero and2 marker1 observations; no reservation of high markers, all legacy writer/save graph or migration proof. Prerequisite gate/RNG/full reader ABI are outside this loop fixture.')
    commit_bridge=read(base/'cpu_commit_bridge/report.json')
    if not commit_bridge['passed'] or commit_bridge['rom_integrated'] or commit_bridge['original_commit_ABI'] or commit_bridge['format_adopted'] or not commit_bridge['caller_selected_new_format_required'] or commit_bridge['helper_bytes']!=944 or commit_bridge['nested_stack_bytes']!=140 or commit_bridge['counts']!={'calls':23202,'rejected':467,'syllable_capacity_paths':22344,'history_paths':140,'maximum_record_bytes':22}:raise ValueError('compact commit bridge CPU scope')
    for n,h in commit_bridge['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in commit_bridge['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in commit_bridge['artifacts'].items():require_hash(base/'cpu_commit_bridge'/n,h)
    for p in [base/'cpu_commit_bridge/report.json',base/'cpu_commit_bridge/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['mixed_compact_commit_CPU_candidate']=dict(counts=commit_bridge['counts'],helper_bytes=944,nested_stack_bytes=140,original_commit_ABI=False,game_hooks_installed=False)
    report['limits'].append('Compact commit bridge executes replay->mixed fixed serialization for22344 cap4/cap10 full-field syllable paths plus140 accepted-history/undo fixtures. No original confirm ABI/UI branch, automatic discrimination, destination/layout adoption, native save or fresh-load integration.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_confirm.py')],timeout=60,check=True)
    native_confirm=read(base/'native_confirm.json')
    if not native_confirm['passed'] or native_confirm['rom_integrated'] or native_confirm['source_sha256']!=profile['sha256'] or native_confirm['rom_sha256']!=identity or native_confirm['handler_entries']!=212 or native_confirm['handler_r5']!='0x0200FC40' or native_confirm['handler_sp']!='0x030076CC' or not native_confirm['original_ignores_commit_return']:raise ValueError('native confirm observation scope')
    if sha(original[0x34F84:0x34FB4])!=native_confirm['handler_sha256'] or rom[0x34F84:0x34FB4]!=original[0x34F84:0x34FB4]:raise ValueError('native confirm handler identity')
    for n,h in native_confirm['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for p,h in native_confirm['artifacts'].items():require_hash(ROOT/p,h);report['artifacts'][p]=h
    report['artifacts']['analysis/hangul_keyboard_v1/native_confirm.json']=sha((base/'native_confirm.json').read_bytes())
    report['native_confirmation_observation']=dict(entries=212,No_record_unchanged=True,Yes_state=20,original_ignores_commit_return=True,Hangul_observed=False)
    confirm_shim=read(base/'cpu_confirm_shim/report.json')
    if not confirm_shim['passed'] or confirm_shim['rom_integrated'] or confirm_shim['format_adopted'] or not confirm_shim['new_layout_required'] or not confirm_shim['native_dialog_and_sound_services_modeled'] or confirm_shim['original_commit_called'] or confirm_shim['source_sha256']!=profile['sha256'] or confirm_shim['current_rom_sha256']!=identity or confirm_shim['original_handler_sha256']!=native_confirm['handler_sha256'] or confirm_shim['helper_bytes']!=152 or confirm_shim['nested_stack_bytes']!=148:raise ValueError('confirmation candidate scope')
    if confirm_shim['counts']!={'calls':12579,'successful_commits':11703,'rejected_commits':616,'busy_passthroughs':256,'cancel_paths':4,'original_passthrough_comparisons':258,'syllable_paths':11172}:raise ValueError('confirmation CPU coverage')
    for n,h in confirm_shim['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in confirm_shim['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in confirm_shim['artifacts'].items():require_hash(base/'cpu_confirm_shim'/n,h)
    for p in [base/'cpu_confirm_shim/report.json',base/'cpu_confirm_shim/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['mixed_confirmation_handler_CPU_candidate']=dict(counts=confirm_shim['counts'],helper_bytes=152,nested_stack_bytes=148,dialog_sound_modeled=True,game_hooks_installed=False)
    report['limits'].append('Native No/Yes observed from unchanged Japanese route. New-layout confirmation handler validates compact and disjoint editor96/record, emits success state14 or rejection state0C in CPU fixtures only. Original dialog/sound service effects modeled; no handler-table/ROM installation, actual Korean rejection UI, temporary display/consumer integration or save/fresh-load evidence.')
    record_display=read(base/'cpu_record_display/report.json')
    if not record_display['passed'] or record_display['rom_integrated'] or record_display['format_adopted'] or not record_display['caller_selected_new_format_required'] or record_display['helper_bytes']!=428 or record_display['nested_stack_bytes']!=80 or record_display['source_sha256']!=profile['sha256'] or record_display['current_rom_sha256']!=identity or record_display['counts']!={'calls':82820,'rejected':59494,'word_domain':65536,'encoder_display_syllables':11172,'maximum_stream_bytes':41}:raise ValueError('selected record display CPU scope')
    if record_display['raw_normalizer_counterexamples']!=[{'identity':'곥','display_hex':'f9fce500e5','raw_copy_hex':'f9fce5','returned_length':2},{'identity':'structural E4/E5 token','display_hex':'e4e5e5','raw_copy_hex':'e4e5','returned_length':1}]:raise ValueError('raw normalizer adverse reproduction')
    if sha(original[0x32AC6:0x32AD8])!=record_display['original_normalizer_sha256'] or rom[0x32AC6:0x32AD8]!=original[0x32AC6:0x32AD8]:raise ValueError('record display raw normalizer identity')
    for n,h in record_display['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in record_display['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in record_display['artifacts'].items():require_hash(base/'cpu_record_display'/n,h)
    for p in [base/'cpu_record_display/report.json',base/'cpu_record_display/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['mixed_record_display_CPU_candidate']=dict(counts=record_display['counts'],helper_bytes=428,nested_stack_bytes=80,raw_normalizer_adverse_cases=2,game_hooks_installed=False)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/analyze_keyboard_record_redisplay.py')],timeout=60,check=True)
    redisplay=read(base/'record_redisplay.json')
    if not redisplay['passed'] or redisplay['rom_integrated'] or redisplay['source_sha256']!=profile['sha256'] or redisplay['current_rom_sha256']!=identity or redisplay['metadata_rows']!=26 or redisplay['first_record_body_aliases']!=16 or redisplay['provider_bounds_insufficient']!=26 or redisplay['packed_record_in_place_expansion_safe']:raise ValueError('bounded redisplay destinations')
    require_hash(base/'consumer_inventory.json',redisplay['inventory_sha256'])
    for n,h in redisplay['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for region in redisplay['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('redisplay native body')
    report['artifacts']['analysis/hangul_keyboard_v1/record_redisplay.json']=sha((base/'record_redisplay.json').read_bytes())
    report['bounded_record_redisplay_analysis']=dict(metadata_rows=26,first_record_body_aliases=16,insufficient_provider_copy_bounds=26,separate_storage_adopted=False)
    report['limits'].append('CPU fixed-record expansion generates complete display streams without table/history. Original rawE5 copier truncates F9FC rank229 and E4/E5 payload in executed fixtures.16 bounded descriptors alias first saved record body; all26 provider bounds cannot copy full Hangul strings. Other10 destinations are not proven free/expanded storage. No original reader/provider replacement, actual dialogue pixels or save/fresh-load integration.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/report_keyboard_redisplay.py')],timeout=60,check=True)
    observed_redisplay=read(base/'native_redisplay.json')
    if not observed_redisplay['passed'] or observed_redisplay['rom_integrated'] or observed_redisplay['source_sha256']!=profile['sha256'] or observed_redisplay['rom_sha256']!=identity or observed_redisplay['adjacent_field']['address']!='0x02014E94':raise ValueError('native redisplay observation scope')
    for n,h in observed_redisplay['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in observed_redisplay['artifacts'].items():require_hash(ROOT/n,h);report['artifacts'][n]=h
    report['artifacts']['analysis/hangul_keyboard_v1/native_redisplay.json']=sha((base/'native_redisplay.json').read_bytes())
    report['native_redisplay_observation']=dict(metadata_refresh_entries=26,descriptor0_providers=860,temporary_adjacent_count='0x02014E94',temporary41_expansion_safe=False,Hangul_observed=False)
    report['limits'].append('Native return refresh selected a record and raw-copied it into its own body. Temporary text+32 is an independently consumed four-byte count: expanding to41bytes overwrites live state. No separate display storage adopted, dialogue glyph insertion evidence, Hangul ROM installation or save/reload.')
    dialogue_record=read(base/'cpu_dialogue_record_copy/report.json')
    if not dialogue_record['passed'] or dialogue_record['rom_integrated'] or dialogue_record['format_adopted'] or not dialogue_record['caller_selected_mixed_format_required'] or dialogue_record['source_sha256']!=profile['sha256'] or dialogue_record['current_rom_sha256']!=identity or dialogue_record['helper_bytes']!=80 or dialogue_record['original_provider_with_helper_stack_bytes']!=104 or dialogue_record['counts']!={'syllables':11172,'selected_calls':11198,'rejected_records':9,'legacy_comparisons':144,'variable_selector_calls':8}:raise ValueError('dialogue record CPU scope')
    for n,h in dialogue_record['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in dialogue_record['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in dialogue_record['artifacts'].items():require_hash(base/'cpu_dialogue_record_copy'/n,h)
    for region in dialogue_record['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('dialogue record native body')
    for p in [base/'cpu_dialogue_record_copy/report.json',base/'cpu_dialogue_record_copy/helper.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['dialogue_record_copy_CPU_candidate']=dict(counts=dialogue_record['counts'],helper_bytes=80,native_provider_stack_bytes=104,temporary_and_record_unchanged=True,game_hooks_installed=False)
    report['limits'].append('Original printStringBuffer handler consumes caller-selected cap4 mixed records directly into its native128-stride cache in CPU fixtures. Only descriptor16/slots0..7 are selected; no automatic format discrimination, full cache writer/lifetime/IRQ proof or natural runtime call. Fixture08300000 is not free ROM; real installation requires long-call/veneer plan. No refreshed-selection storage, actual Korean dialogue pixels or save/reload integration.')
    pipeline=read(base/'cpu_keyboard_to_dialogue/report.json')
    if not pipeline['passed'] or pipeline['rom_integrated'] or pipeline['format_adopted'] or not pipeline['caller_selected_mixed_format_required'] or not pipeline['no_HOST_surface_rewrite_between_CPU_stages'] or pipeline['source_sha256']!=profile['sha256'] or pipeline['current_rom_sha256']!=identity:raise ValueError('keyboard dialogue pipeline scope')
    for name in ('syllable_pipelines','partial_commit_rejections','successful_commits','native_provider_calls'):
        if pipeline['counts'][name]!=11172:raise ValueError('keyboard dialogue pipeline syllable coverage')
    if pipeline['counts']['maximum_stream_bytes']!=17 or pipeline['counts']['CPU_key_actions']<22344:raise ValueError('keyboard dialogue input/display coverage')
    for n,h in pipeline['dependencies'].items():require_hash(base/n/'report.json',h)
    for n,h in pipeline['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in pipeline['artifacts'].items():require_hash(base/'cpu_keyboard_to_dialogue'/n,h)
    for p in [base/'cpu_keyboard_to_dialogue/report.json',base/'cpu_keyboard_to_dialogue/keyedit.bin']:report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['uninterrupted_keyboard_to_dialogue_CPU_candidate']=dict(counts=pipeline['counts'],no_HOST_surface_rewrites=True,game_hooks_installed=False)
    report['limits'].append('CPU jamo inputs/automatic composition/partial rejection/compact commit feed the original dialogue handler without HOST compact/record/stream rewriting. Initial editor/context/keys are fixtures, format is explicitly selected. Not game keypad/UI/confirm, record discriminator adoption, cache lifetime/IRQ, selected-record refresh, glyph pixels or save/reload.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/analyze_keyboard_descriptor_mutators.py')],timeout=60,check=True)
    mutators=read(base/'descriptor_mutators.json')
    if not mutators['passed'] or mutators['rom_integrated'] or mutators['format_discriminator_adopted'] or mutators['source_sha256']!=profile['sha256'] or mutators['current_rom_sha256']!=identity or not mutators['setup_clear_service_modeled'] or mutators['counts']!={'delete_calls':52,'setup_calls':52,'first_record_marker_aliases':16,'nonrecord_preceding_byte_targets':10}:raise ValueError('descriptor mutator scope')
    require_hash(base/'consumer_inventory.json',mutators['inventory_sha256'])
    for n,h in mutators['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for region in mutators['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('descriptor mutator native body')
    report['artifacts']['analysis/hangul_keyboard_v1/descriptor_mutators.json']=sha((base/'descriptor_mutators.json').read_bytes())
    report['bounded_descriptor_mutators']=dict(counts=mutators['counts'],setup_clear_service_modeled=True,automatic_format_discrimination_adopted=False)
    report['limits'].append('Two more native descriptor consumers execute CPU fixtures on source/current26 entries. Delete clears pointer-1 and writes default47; setup stores pointer-1/selector in0200F550 with clear modeled.16 targets are saved record markers,10 are separate cache preceding bytes. Sideband/cache ownership must include these transitions; selector byte is not proven keyboard capacity. Not complete legacy writers/save or runtime reachability.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/analyze_keyboard_setup_import.py')],timeout=60,check=True)
    setup_import=read(base/'setup_import_caller.json')
    if not setup_import['passed'] or setup_import['rom_integrated'] or setup_import['format_discriminator_adopted'] or setup_import['source_sha256']!=profile['sha256'] or setup_import['current_rom_sha256']!=identity or setup_import['counts']!={'calls':64,'legacy_imports':32,'mixed_rank229_imported_empty':32,'dynamic_heading_modeled_calls':4}:raise ValueError('setup/import caller scope')
    for n,h in setup_import['dependencies'].items():require_hash(base/n,h)
    for n,h in setup_import['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for region in setup_import['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('setup/import source body')
    report['artifacts']['analysis/hangul_keyboard_v1/setup_import_caller.json']=sha((base/'setup_import_caller.json').read_bytes())
    report['bounded_setup_to_import_caller']=dict(counts=setup_import['counts'],selector_is_metadata_index=True,clear_and_dynamic_heading_modeled=True,game_hooks_installed=False)
    report['limits'].append('Bounded caller3A1C2..3A1E7 resolves selector as metadata index then executes native initializer and record importer. Source/current coherent descriptors2..17 tested; mixed rank229 imports empty at this caller. Clear96/dynamic heading modeled. Both initializer and import boundaries require coordinated replacement; no auto format adoption or runtime/save claim.')
    reentry=read(base/'cpu_keyboard_reentry/report.json')
    if not reentry['passed'] or reentry['rom_integrated'] or reentry['format_adopted'] or not reentry['caller_selected_mixed_format_required'] or not reentry['no_HOST_rewrite_between_import_and_recommit'] or reentry['source_sha256']!=profile['sha256'] or reentry['current_rom_sha256']!=identity:raise ValueError('reentry CPU scope')
    if reentry['counts']!={'caller_imports':11284,'syllable_reentries':11172,'CPU_recommits':11220,'caller_rejections':64,'adapter_rejections':37} or reentry['caller_stack_bytes']!=140 or reentry['import_adapter_nested_stack_bytes']!=132 or reentry['dynamic_heading_modeled_calls']!=7:raise ValueError('reentry CPU coverage')
    for n,h in reentry['dependencies'].items():require_hash(base/n,h)
    for n,h in reentry['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in reentry['artifacts'].items():require_hash(base/'cpu_keyboard_reentry'/n,h)
    for patch in reentry['fixture_BLs']:
        a=patch['offset']
        if original[a:a+4].hex()!=patch['expected_hex'] or rom[a:a+4]!=original[a:a+4]:raise ValueError('reentry BL immutable source')
    for n in ['report.json',*reentry['artifacts']]:
        p=base/'cpu_keyboard_reentry'/n;report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['native_caller_mixed_reentry_CPU_candidate']=dict(counts=reentry['counts'],caller_stack_bytes=140,no_HOST_import_to_recommit_rewrites=True,game_hooks_installed=False)
    report['limits'].append('Original metadata caller executes new init/import in CPU source clone with two bounded BL replacements. All11172 fullcap4 final syllables reimport/recommit unchanged;16 descriptor rows and malformed/overlap rejection covered. Heading0 modeled; explicit new-format selection only. Original caller ignores rejected import, so UX remains unresolved. No free-space/RAM lifetime/IRQ adoption, actual keypad/glyph pixels, ROM hook or save/reload.')
    actions=read(base/'cpu_keyboard_actions/report.json')
    if not actions['passed'] or actions['rom_integrated'] or actions['actual_game_layout_adopted'] or not actions['no_HOST_compact_rewrites_between_syllable_keys'] or actions['source_sha256']!=profile['sha256'] or actions['current_rom_sha256']!=identity:raise ValueError('keyboard action CPU scope')
    if actions['counts']!={'calls':52647,'accepted_edits':50554,'rejected_consumed':1325,'unhandled':768,'syllable_paths':11172,'CPU_key_actions':37506} or actions['nested_stack_bytes']!=208 or actions['selector_cells']!=90 or actions['active_jamo_cells']!=40:raise ValueError('keyboard action CPU coverage')
    for n,h in actions['dependencies'].items():require_hash(base/n,h)
    for n,h in actions['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in actions['artifacts'].items():require_hash(base/'cpu_keyboard_actions'/n,h)
    caller=actions['native_caller'];a=caller['offset'];b=a+caller['bytes']
    if sha(original[a:b])!=caller['sha256'] or original[a:b].hex()!=caller['expected_hex'] or rom[a:b]!=original[a:b]:raise ValueError('keyboard action native BL/BNE guard')
    for n in ['report.json',*actions['artifacts']]:
        p=base/'cpu_keyboard_actions'/n;report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['native_AB_action_CPU_candidate']=dict(counts=actions['counts'],stack_bytes=208,active_jamo_cells=40,native_BNE_consumption_verified=True,game_hooks_installed=False)
    report['limits'].append('CPU native BL+BNE caller consumes A/B via new editor action adapter:40 candidate jamo selectors, inactive rejection, history/canonical delete, cursor moves,11172 last-slot syllables. Outer frame drawing/navigation not executed. Candidate page0 only; page/Latin/comma/confirm/cancel/sound/rejection feedback still unsupported. No installed hook, RAM lifetime/IRQ adoption, actual Korean keypad pixels or save/reload.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/analyze_keyboard_control_routes.py')],timeout=60,check=True)
    control_routes=read(base/'control_routes.json')
    if not control_routes['passed'] or control_routes['rom_integrated'] or control_routes['source_sha256']!=profile['sha256'] or control_routes['current_rom_sha256']!=identity or control_routes['counts']!={'comparator_calls':6,'command_calls':112,'page_transitions':60,'confirmation_requests':24,'cancel_exits':2}:raise ValueError('native control routes scope')
    for n,h in control_routes['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for region in control_routes['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('control routes native body')
    if len(control_routes['comparison_lists'])!=2 or any(r['bytes']!=1 or r['entry_lengths']!=[0] for r in control_routes['comparison_lists']):raise ValueError('empty native comparison list')
    report['artifacts']['analysis/hangul_keyboard_v1/control_routes.json']=sha((base/'control_routes.json').read_bytes())
    controls=read(base/'cpu_keyboard_controls/report.json')
    if not controls['passed'] or controls['rom_integrated'] or not controls['new_layout_required'] or not controls['services_modeled'] or controls['raw_key_integration'] or not controls['no_HOST_editor_or_record_rewrite_between_request_and_Yes_No'] or controls['source_sha256']!=profile['sha256'] or controls['current_rom_sha256']!=identity:raise ValueError('logical controls CPU scope')
    if controls['counts']!={'controls':11452,'complete_requests':11176,'partial_rejections':4,'empty_requests':4,'cancel_exits':4,'page_changes':144,'Yes_commits':5586,'No_returns':5586} or controls['nested_stack_bytes']!=180 or not controls['page_upload_queue_guard']:raise ValueError('logical control CPU coverage')
    for n,h in controls['dependencies'].items():require_hash(base/n,h)
    for n,h in controls['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in controls['artifacts'].items():require_hash(base/'cpu_keyboard_controls'/n,h)
    for n in ['report.json',*controls['artifacts']]:
        p=base/'cpu_keyboard_controls'/n;report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['logical_page_request_cancel_CPU_candidate']=dict(counts=controls['counts'],stack_bytes=180,native_empty_comparison_list_confirmed=True,raw_key_integration=False,game_hooks_installed=False)
    report['limits'].append('Original input/count/comparator CPU routes establish3-page controls, two-stage Start, empty-only dialog comparison and emptyB cancel. New logical controls dry-run commit in owned stack before dialog10; empty dialog11, partial stays editable.11172 request->alternating Yes/No CPU paths have no HOST rewrites. Page/dialog/sound/busy/choice services modeled. Raw key routing, page glyph/upload, empty-message handler, actual Korean pixels/ROM/save/IRQ budgets remain pending.')
    raw_router=read(base/'cpu_keyboard_raw_router/report.json')
    if not raw_router['passed'] or raw_router['rom_integrated'] or not raw_router['new_layout_required'] or not raw_router['raw_pressed_mask_routing'] or not raw_router['no_HOST_compact_or_record_rewrites_between_CPU_stages'] or not raw_router['services_modeled'] or raw_router['source_sha256']!=profile['sha256'] or raw_router['current_rom_sha256']!=identity:raise ValueError('raw input router CPU scope')
    if raw_router['counts']!={'raw_calls':72235,'consumed':71851,'unhandled':384,'mask_domain_cases':12288,'syllable_pipelines':11172,'CPU_jamo_keys':37506,'Yes_commits':5586,'No_returns':5586} or raw_router['nested_stack_bytes']!=220:raise ValueError('raw router CPU coverage')
    for n,h in raw_router['dependencies'].items():require_hash(base/n,h)
    for n,h in raw_router['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in raw_router['artifacts'].items():require_hash(base/'cpu_keyboard_raw_router'/n,h)
    caller=raw_router['native_caller'];a=caller['offset'];b=a+caller['bytes']
    if sha(original[a:b])!=caller['sha256'] or original[a:b].hex()!=caller['expected_hex'] or rom[a:b]!=original[a:b]:raise ValueError('raw router BL/BNE source guard')
    for n in ['report.json',*raw_router['artifacts']]:
        p=base/'cpu_keyboard_raw_router'/n;report['artifacts'][str(p.relative_to(ROOT)).replace('\\','/')]=sha(p.read_bytes())
    report['raw_button_edit_control_CPU_candidate']=dict(counts=raw_router['counts'],stack_bytes=220,pressed_mask_routing=True,game_hooks_installed=False)
    report['limits'].append('Native BL/BNE source clone executes raw button routing B>A>Start>L>R into editing and page/Start/cancel controls. All1024low10bit masks/4cells/3states and11172last-slot syllable A->twoStart->Yes/No paths verified without HOST compact/record rewrites. Outer frame drawing/navigation, page assets/Latin/space/feedback, empty dialog handler, RAM/IRQ/format adoption, actual Korean UI/ROM/save remain pending; service effects modeled.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/prepare_keyboard_page_graphics.py')],timeout=30,check=True)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_keyboard_page_graphics.py')],timeout=30,check=True)
    page_assets=read(base/'page_graphics/report.json');page_cpu=read(base/'cpu_page_graphics/report.json')
    for item in (page_assets,page_cpu):
        if not item['passed'] or item['rom_integrated'] or item['source_sha256']!=profile['sha256'] or item['current_rom_sha256']!=identity:raise ValueError('page graphics evidence scope')
        for n,h in item['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    if page_assets['candidate']['active_cells']!=40 or page_assets['candidate']['grid_cells']!=90 or page_assets['candidate']['bank_bytes']!=5472 or not page_assets['candidate']['preserved_outside_grid']:raise ValueError('page candidate asset coverage')
    require_hash(base/'candidates/plan.json',page_assets['plan_sha256']);require_hash(base/'candidates/jamo_big_cells.bin',page_assets['jamo_bank_sha256'])
    pal=page_assets['observed_palette'];require_hash(ROOT/pal['path'],pal['sha256'])
    require_hash(ROOT/'poc/runtime/hangul-keyboard-v1-native-edit/result.json',pal['route_result_sha256'])
    for n,h in page_assets['artifacts'].items():require_hash(base/'page_graphics'/n,h)
    require_hash(base/'page_graphics/report.json',page_cpu['asset_report_sha256'])
    if page_cpu['counts']!={'draws':108,'enqueues':72,'drains':36,'saturation_rejections':36,'candidate_page0_draws':12,'candidate_page0_transfers':4,'cursor_calls':1152,'jamo_cursor_alignment_cases':480} or not page_cpu['BIOS_and_display_config_modeled'] or not page_cpu['no_HOST_rewrite_between_draw_enqueue_drain']:raise ValueError('page CPU coverage')
    for region in page_cpu['native_code']:
        start=region['offset'];end=start+region['bytes']
        if sha(original[start:end])!=region['sha256'] or rom[start:end]!=original[start:end]:raise ValueError('page CPU immutable code guard')
    for patch in page_cpu['fixture_writes']:
        start=patch['offset'];length=len(bytes.fromhex(patch['expected_hex']))
        if rom[start:start+length].hex()!=patch['expected_hex'] or original[start:start+length]!=rom[start:start+length]:raise ValueError('page fixture source table guard')
    for folder,names in [('page_graphics',['report.json',*page_assets['artifacts']]),('cpu_page_graphics',['report.json'])]:
        for n in names:
            path=base/folder/n;report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['jamo_page_assets_native_draw_transfer_CPU_candidate']=dict(counts=page_cpu['counts'],active_jamo_cells=40,bank_bytes=5472,grid_pixels_preserved_outside=True,game_hooks_installed=False)
    report['limits'].append('Candidate page0 replaces90left-grid cells with40jamo/50inactive using deterministic BDF tiles and original background; other pages/command labels remain Japanese. Native cursor1152cases aligns40jamo, native IWRAM draw/fill and ROM upload/enqueue/drain execute108pageconditions. BIOS/config modeled; no HOST stage rewrite between draw/enqueue/drain. Offline preview uses observed palette, not an emulator candidate screen. No product install, natural page lifetime/IRQ/save or remaining-input support claim.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_keyboard_page_input_pipeline.py')],timeout=60,check=True)
    page_input=read(base/'cpu_page_input_pipeline/report.json')
    if not page_input['passed'] or page_input['rom_integrated'] or page_input['source_sha256']!=profile['sha256'] or page_input['current_rom_sha256']!=identity or not page_input['raw_input_to_actual_page_uploader'] or not page_input['page_upload_queue_guard'] or not page_input['no_HOST_editor_queue_map_bank_rewrites_between_CPU_stages']:raise ValueError('page input pipeline scope')
    if page_input['counts']!={'input_calls':623,'page_transitions':477,'draws':865,'drains':725,'jamo_actions':50,'backspaces':41,'queue_rejections':37,'unguarded_mismatch_reproduced':1,'pending_transitions':102}:raise ValueError('page input pipeline coverage')
    for n,h in page_input['dependencies'].items():require_hash(base/n,h)
    for n,h in page_input['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in page_input['artifacts'].items():require_hash(base/'cpu_page_input_pipeline'/n,h)
    require_hash(base/'cpu_keyboard_raw_router/helper.bin',page_input['raw_helper_sha256'])
    for patch in page_input['fixture_writes']:
        start=patch['offset'];length=len(bytes.fromhex(patch['expected_hex']))
        if rom[start:start+length].hex()!=patch['expected_hex'] or original[start:start+length]!=rom[start:start+length]:raise ValueError('page input fixture source guard')
    for n in ['report.json',*page_input['artifacts']]:
        path=base/'cpu_page_input_pipeline'/n;report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['raw_button_to_native_page_graphics_CPU_candidate']=dict(counts=page_input['counts'],page_queue_full_atomic_rejection=True,game_hooks_installed=False)
    report['limits'].append('Raw keys now reach original page uploader/draw/clear/queue drain in CPU clone.623button calls include40jamo across page cycles and CPU-filled96pending uploads:97th page request is rejected atomically while input/delete remain usable. An unguarded control variant reproduces page-index/VRAM mismatch. No HOST editor/queue/map/bank writes between stages; BIOS/sound/config/sprite modeled. No installed ROM, outer-frame/edit-field refresh, concurrent IRQ reservation, natural input/scanout, other-page letters or save/persistence claim.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_keyboard_page_input_pipeline.py'),'--editfield'],timeout=90,check=True)
    input_render=read(base/'cpu_input_render_pipeline/report.json')
    if not input_render['passed'] or input_render['rom_integrated'] or input_render['source_sha256']!=profile['sha256'] or input_render['current_rom_sha256']!=identity or not input_render['raw_to_editfield_pixels'] or not input_render['no_HOST_editor_queue_map_bank_rewrites_between_CPU_stages'] or not input_render['page_upload_queue_guard']:raise ValueError('input render pipeline scope')
    if input_render['counts']!={'input_calls':666,'page_transitions':482,'draws':918,'drains':781,'jamo_actions':66,'backspaces':57,'queue_rejections':37,'unguarded_mismatch_reproduced':1,'pending_transitions':101,'caret_actions':6}:raise ValueError('input render pipeline coverage')
    if input_render['refresh_counts']!={'refresh_calls':920,'queued':781,'deferred':139,'latest_after_drain':2} or input_render['guard_interval_cases']!=1140 or input_render['refresh_rejected_editor_cases']!=7 or input_render['refresh_stack_bytes']!=144:raise ValueError('editfield refresh coverage')
    parser_evidence=read(base/'cpu_editfield_parser/report.json')
    if input_render['glyph_rom_sha256']!=parser_evidence['product_sha256']:raise ValueError('input render glyph identity')
    require_hash(ROOT/'poc/output/exe45_ko_development_keyboard_glyphs_v1.gba',input_render['glyph_rom_sha256'])
    for n,h in input_render['dependencies'].items():require_hash(base/n,h)
    for n,h in input_render['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in input_render['artifacts'].items():require_hash(base/'cpu_input_render_pipeline'/n,h)
    require_hash(base/'cpu_keyboard_raw_router/helper.bin',input_render['raw_helper_sha256'])
    for patch in input_render['fixture_writes']:
        start=patch['offset'];length=len(bytes.fromhex(patch['expected_hex']))
        if rom[start:start+length].hex()!=patch['expected_hex'] or original[start:start+length]!=rom[start:start+length]:raise ValueError('input render fixture source guard')
    for n in ['report.json',*input_render['artifacts']]:
        path=base/'cpu_input_render_pipeline'/n;report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['raw_button_to_native_editfield_pixels_CPU_candidate']=dict(counts=input_render['counts'],refresh_counts=input_render['refresh_counts'],guard_interval_cases=1140,rejected_editor_cases=7,refresh_stack_bytes=144,no_HOST_surface_rewrites=True,game_hooks_installed=False)
    report['limits'].append('Raw A/B/caret/page input connects composition/cache bridge to native editfield parser/queue/drain in CPU fixture;781 exact1280byte pixel transfers. Refresh defers139times while staging buffer has queued readers or queue is full;1140interval/overflow boundaries and7invalid editors preserve memory. Native parser r8/r9/r10 restored;144byte nested refresh stack. Retry is harness scheduling after drain, not adopted outer-frame/IRQ lifetime or rejection feedback. BIOS/sound/config/sprite modeled. No installed ROM hooks, actual Korean screen, free RAM/code placement or save/reload claim.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_keyboard_page_input_pipeline.py'),'--editfield','--frame'],timeout=240,check=True)
    frame=read(base/'cpu_keyboard_frame/report.json')
    if not frame['passed'] or frame['rom_integrated'] or not frame['bounded_native_outer_frame'] or not frame['raw_to_editfield_pixels'] or frame['source_sha256']!=profile['sha256'] or frame['current_rom_sha256']!=identity or frame['glyph_rom_sha256']!=input_render['glyph_rom_sha256']:raise ValueError('native frame scope')
    if frame['frame_stack_bytes']!=248 or frame['refresh_stack_bytes']!=144 or frame['guard_interval_cases']!=1140 or frame['refresh_rejected_editor_cases']!=7 or not frame['no_HOST_editor_queue_map_bank_rewrites_between_CPU_stages']:raise ValueError('native frame safety coverage')
    if frame['original_navigation_unreachable_jamo']!=['ㅕ','ㅗ'] or frame['navigation_adapted_cells']!=[[6,2],[8,2]]:raise ValueError('native navigation counterexample/adaptation')
    if frame['counts']['native_frames']!=frame['counts']['input_calls'] or frame['counts']['navigation_cases']!=1440+frame['counts']['physical_navigation_moves'] or frame['counts']['physical_selector_paths']!=40 or frame['counts']['idle_retry_frames']!=2 or frame['counts']['caret_sprite_cases']<100:raise ValueError('native frame navigation/caret/retry coverage')
    for n,h in frame['dependencies'].items():require_hash(base/n,h)
    for n,h in frame['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in frame['artifacts'].items():require_hash(base/'cpu_keyboard_frame'/n,h)
    for region in frame['frame_native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('native frame immutable body')
    for patch in frame['fixture_writes']:
        a=patch['offset'];n=len(bytes.fromhex(patch['expected_hex']))
        if rom[a:a+n].hex()!=patch['expected_hex'] or original[a:a+n]!=rom[a:a+n]:raise ValueError('native frame fixture source')
    for n in ['report.json',*frame['artifacts']]:
        path=base/'cpu_keyboard_frame'/n;report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['bounded_native_input_frame_CPU_candidate']=dict(counts=frame['counts'],refresh_counts=frame['refresh_counts'],frame_stack_bytes=248,physical_selector_paths=40,game_hooks_installed=False)
    report['limits'].append('Native034E34 state12 frame dispatch/input/cursor/navigation/page draw/editfield decoration/refresh executes with coordinated legacy pad/flatten no-ops, caret query adapter and far render veneer in CPU source clone. Original navigation covers3pages/96positions/5direction masks and40jamo reached by uninterrupted direction+A/B sequence without HOST grid/editor positions. Deferred refresh retried via idle native frame.248byte stack is fixture bound only. BIOS/config/sound/sprite modeled; initialization/animation/confirmation/exit/IRQ/code and RAM adoption, actual Korean screen/save pending.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_keyboard_lifecycle.py')],timeout=30,check=True)
    lifecycle=read(base/'cpu_keyboard_lifecycle/report.json')
    if not lifecycle['passed'] or lifecycle['rom_integrated'] or lifecycle['format_adopted'] or lifecycle['source_sha256']!=profile['sha256'] or lifecycle['current_rom_sha256']!=identity:raise ValueError('lifecycle CPU scope')
    if lifecycle['counts']!={'initializations':120,'frames':4620,'entry_frames':2160,'exit_frames':1920,'commits':60,'no_returns':120,'busy_frames':120,'partial_rejections':60,'reentries':60,'cancel_exits':60,'counter_wraps':60} or lifecycle['frame_stack_bytes']!=172 or lifecycle['init_stack_bytes']!=140 or not lifecycle['no_HOST_compact_or_destination_rewrite_between_busy_No_Yes']:raise ValueError('lifecycle coverage')
    for n,h in lifecycle['dependencies'].items():require_hash(base/n,h)
    for n,h in lifecycle['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for region in lifecycle['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('lifecycle native source')
    patch=lifecycle['fixture_confirm_pointer'];a=patch['offset'];n=len(bytes.fromhex(patch['expected_hex']))
    if rom[a:a+n].hex()!=patch['expected_hex'] or original[a:a+n]!=rom[a:a+n]:raise ValueError('lifecycle confirm pointer source')
    path=base/'cpu_keyboard_lifecycle/report.json';report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['native_lifecycle_CPU_candidate']=dict(counts=lifecycle['counts'],frame_stack_bytes=172,init_stack_bytes=140,render_input_modeled=True,game_hooks_installed=False)
    report['limits'].append('Native state0/4/8 entry animation, state16 confirm, state20 success/cancel exit and reentry execute with new editor/confirm pointer in CPU clone.120initializations/4620frames, No120/busy120/partial60 preserve destination, success60/cancel60 differ in completion byte, counter wrap60 checked. Rendering/state12 input/preload services modeled; this does not extend state12 pixel evidence across lifecycle or prove natural game/save entry. Cap10 destination is test-owned, game/save extent and redisplay consumers remain unresolved. No real ROM hook, screen, resource-release/IRQ or persistence claim.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_calendar_record_transfer.py')],timeout=120,check=True)
    calendar_transfer=read(base/'cpu_calendar_record_transfer/report.json')
    if not calendar_transfer['passed'] or calendar_transfer['rom_integrated'] or calendar_transfer['format_adopted'] or not calendar_transfer['selected_new_format_required'] or calendar_transfer['source_sha256']!=profile['sha256'] or calendar_transfer['current_rom_sha256']!=identity:raise ValueError('calendar transfer scope')
    if calendar_transfer['counts']!={'syllable_routes':11172,'original_truncations':43,'marker_loss_cases':11172,'accepted_transfers':11302,'rejections':27,'whole_EWRAM_checks':22501,'atomic_cancel_branches':17,'unguarded_failure_advance_reproduced':1} or calendar_transfer['helper_stack_bytes']!=220 or calendar_transfer['record_width']!=22 or calendar_transfer['pool_slots_fixture_domain']!=[0,1,2]:raise ValueError('calendar transfer coverage')
    for n,h in calendar_transfer['dependencies'].items():require_hash(base/n,h)
    for n,h in calendar_transfer['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in calendar_transfer['artifacts'].items():require_hash(base/'cpu_calendar_record_transfer'/n,h)
    for region in calendar_transfer['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('calendar transfer native source')
    for name in ('fixture_BL','fixture_finalizer'):
        patch=calendar_transfer[name];a=patch['offset'];n=len(bytes.fromhex(patch['expected_hex']))
        if rom[a:a+n].hex()!=patch['expected_hex'] or original[a:a+n]!=rom[a:a+n]:raise ValueError('calendar transfer source write guard')
    for n in ['report.json',*calendar_transfer['artifacts']]:
        path=base/'cpu_calendar_record_transfer'/n;report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['selected_calendar_record_transfer_CPU_candidate']=dict(counts=calendar_transfer['counts'],helper_stack_bytes=220,record_width=22,game_hooks_installed=False)
    report['limits'].append('Selected cap10 new-format calendar success caller transfers fixed22 marker+words+terminator to bounded pool slots0..2. Original rawE5 caller loses marker11172times/truncates43ranks; helper and coordinated success/cancel finalizer prevent partial/stale-data advance, checked22501whole EWRAM cases. Existing persistent field22 can fit candidate width, but calendar pool/provider/default/record/save ownership and legacy format discrimination remain unresolved. No actual saved record conversion, redisplay, natural keypad screen, code/IRQ budget or ROM installation claim.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_calendar_record_display.py')],timeout=120,check=True)
    calendar_display=read(base/'cpu_calendar_record_display/report.json')
    if not calendar_display['passed'] or calendar_display['rom_integrated'] or calendar_display['format_adopted'] or not calendar_display['selected_new_format_required'] or not calendar_display['no_HOST_pool_rewrite_between_detail_count_pixels'] or calendar_display['source_sha256']!=profile['sha256'] or calendar_display['current_rom_sha256']!=identity or calendar_display['glyph_rom_sha256']!=input_render['glyph_rom_sha256']:raise ValueError('calendar display scope')
    if calendar_display['counts']!={'detail_calls':11277,'syllable_routes':11172,'accepted':11263,'rejected':14,'confirmation_counts':11263,'pixel_consumptions':84,'heading_skips':14,'whole_EWRAM_checks':22624,'format_collision_cases':1} or calendar_display['detail_stack_bytes']!=108 or calendar_display['counter_stack_bytes']!=36 or calendar_display['parser_stack_bytes']!=40:raise ValueError('calendar display coverage')
    for n,h in calendar_display['dependencies'].items():require_hash(base/n,h)
    for n,h in calendar_display['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in calendar_display['artifacts'].items():require_hash(base/'cpu_calendar_record_display'/n,h)
    region=calendar_display['native_detail'];a=region['offset'];b=a+region['bytes']
    if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('calendar display native source')
    patch=calendar_display['fixture_BL'];a=patch['offset'];n=len(bytes.fromhex(patch['expected_hex']))
    if rom[a:a+n].hex()!=patch['expected_hex'] or original[a:a+n]!=rom[a:a+n]:raise ValueError('calendar display fixture source')
    for n in ['report.json',*calendar_display['artifacts']]:
        path=base/'cpu_calendar_record_display'/n;report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['selected_calendar_record_display_CPU_candidate']=dict(counts=calendar_display['counts'],detail_stack_bytes=108,heading_sprite_transfer_modeled=True,game_hooks_installed=False)
    report['limits'].append('Selected cap10 calendar name renderer33C94 decodes record field22 into pool F9FC stream; all11172 syllables reach current native confirmation count,84 representative actual fixed parser pixel consumptions (640bytes each),14 invalids skip heading preserving saved-record fixture/pool. Pool never HOST-rewritten between decode/count/parser. Native heading/TPL lookup, sprite/transfer are modeled.81E5 format collision demonstrates that structural marker validation alone cannot choose legacy/new format. No natural row route, actual save migration/reload, scanout/screenshot, pool/IRQ ownership or ROM installation claim.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_calendar_native_registration.py')],timeout=120,check=True)
    registration=read(base/'cpu_calendar_native_registration/report.json')
    if not registration['passed'] or registration['safe_registration'] or registration['rom_integrated'] or registration['source_sha256']!=profile['sha256'] or registration['current_rom_sha256']!=identity:raise ValueError('negative native registration scope')
    if registration['counts']!={'native_registrations':22353,'whole_EWRAM_checks':22353,'binary_routes':11172,'binary_early_terminations':43,'display_routes':11172,'display_early_terminations':43,'display_neighbor_overflows':11129,'legacy_controls':9,'counter_wraps':3}:raise ValueError('native registration counterexample coverage')
    for n,h in registration['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for region in registration['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('native registration source')
    for literal in registration['literals']:
        a=literal['offset']
        if int.from_bytes(original[a:a+4],'little')!=literal['value'] or rom[a:a+4]!=original[a:a+4]:raise ValueError('native registration literal')
    path=base/'cpu_calendar_native_registration/report.json';report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['unsafe_native_calendar_registration_counterexamples']=dict(counts=registration['counts'],safe_registration=False,game_hooks_installed=False)
    report['limits'].append('Unchanged native32EFE..32F24 copy+37366 metadata registration reproduced22353CPU routes. Cap10 marked binary truncates43ranks; F9FC display overflows22byte field into next record for11129ranks (19bytes), truncates43embeddedE5ranks. Both still register and play success sound (sound modeled). Pool canonical/cache coexistence is unresolved; this negative integration PASS is NOT safe commit/save evidence. No game/save files mutated.')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/bench_calendar_bounded_commit.py')],timeout=120,check=True)
    bounded_commit=read(base/'cpu_calendar_bounded_commit/report.json')
    if not bounded_commit['passed'] or bounded_commit['rom_integrated'] or bounded_commit['format_adopted'] or not bounded_commit['explicit_new_session_required'] or not bounded_commit['no_HOST_canonical_pool_rewrite_between_decode_and_registration'] or bounded_commit['source_sha256']!=profile['sha256'] or bounded_commit['current_rom_sha256']!=identity:raise ValueError('bounded canonical commit scope')
    if bounded_commit['counts']!={'routes':22745,'accepted':22703,'rejected':42,'display_decodes':22703,'whole_EWRAM_checks':45448,'syllable_routes':22344,'arena_slots':255,'direct_mode1':5638,'direct_mode2':5586,'counter_wraps':2} or bounded_commit['helper_stack_bytes']!=220 or bounded_commit['adapter_nested_stack_bytes']!=228:raise ValueError('bounded canonical commit coverage')
    for n,h in bounded_commit['dependencies'].items():require_hash(base/n,h)
    for n,h in bounded_commit['tools'].items():require_hash(ROOT/'tools'/n,h);report['tools'][n]=h
    for n,h in bounded_commit['artifacts'].items():require_hash(base/'cpu_calendar_bounded_commit'/n,h)
    for region in bounded_commit['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('bounded commit native source')
    for patch in bounded_commit['fixture_writes']:
        a=patch['offset'];n=len(bytes.fromhex(patch['expected_hex']))
        if rom[a:a+n].hex()!=patch['expected_hex'] or original[a:a+n]!=rom[a:a+n]:raise ValueError('bounded commit source write guard')
    for n in ['report.json',*bounded_commit['artifacts']]:
        path=base/'cpu_calendar_bounded_commit'/n;report['artifacts'][str(path.relative_to(ROOT)).replace('\\','/')]=sha(path.read_bytes())
    report['explicit_canonical_calendar_commit_CPU_candidate']=dict(counts=bounded_commit['counts'],adapter_nested_stack_bytes=228,game_hooks_installed=False)
    report['limits'].append('Explicit NEW cap10 canonical stage->separate display pool->two bounded native registration routes:22745calls/45448whole EWRAM checks,11172syllables both routes,255arena slots,42rejects leave record/cache/canonical/metadata unchanged and skip success. Native37366/3737A/37386 execute, but sound/selector/37440 update modeled; direct selector0 omitted. Stage lifetime, all writers/defaults, persistent legacy discriminator, actual save/reload and ROM placement are unresolved. Not natural screen/save/whole-memory evidence.')
    (base/'foundation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(product,identity);require_hash(source,profile['sha256'])
    print('PASS foundation; native composition and compact replay fixtures only; ROM integration unresolved')

if __name__=='__main__':main()
