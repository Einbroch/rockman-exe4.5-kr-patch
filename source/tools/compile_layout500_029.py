"""Compile selected027500 from immutable source; no ROM/carry injection."""
import re
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet,bdf_glyphs
from cumulative_batch500 import read,frozen_write
from prepare_layout500_029 import OUT as SELECTION
from compile_layout_candidates_024 import canonical_literals,ref
from compare_archive_payloads import payload_of
from tpl_literals import literals,skeleton
from archive_scripts import verify_untouched_scripts
from survey_pet_quick_reflow_024 import replace_for_analysis
from textpet_korean import prepare_plugins,command
from korean_codec import EXTRA_CHARACTER_INDICES,EXTRA_CHARACTER_METRICS
from field_hint_capacity import validate as full_validate
from pet_nickname_capacity_025 import validate as quick_validate
from normal_battle_choice_capacity_026 import validate as choice_validate
from normal_vertical_choice_capacity_026 import validate as vertical_validate
from pet_choice_capacity_026 import validate as pet_choice_validate
from pet_profile_capacity_027_v2 import validate as profile_validate
from profile_provider_bounds_027_v2 import bounds as profile_bounds
from pet_array_capacity_029 import validate as array_validate
from normal_timing_capacity_025 import validate as normal_validate
from pet_nickname_flags_capacity_025_v2 import validate as flags_validate

OUT='analysis/pending_insertion_500_029_compile500_v1'


def main():
    selected=read(SELECTION);cfg=read('project.json')
    if selected['planned_new_units']!=500 or selected['rom_written'] or selected['insertion_ready']:raise ValueError('Source-only500 policy')
    for p,h in selected['dependencies'].items():require_hash(ROOT/p,h)
    sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,selected['source_sha256']);source=sp.read_bytes()
    rp=ROOT/selected['baseline_rom'];require_hash(rp,selected['baseline_sha256']);rom=rp.read_bytes();meta=read(str(rp.with_suffix('.json').relative_to(ROOT)))
    bound=selected['native_nickname_bound'];profile_bounds(source,rom)
    out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False);plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));common=command(out/'plugins')
    by=defaultdict(list)
    for g in selected['groups']:by[g['archive']].append(g)
    records=[];seen=set();chars=set();lf_edits=[]
    for arc,groups in sorted(by.items()):
        src_ref=groups[0]['source_tpl'];require_hash(ROOT/src_ref['path'],src_ref['sha256']);original=(ROOT/src_ref['path']).read_text(encoding='utf-8-sig');row=groups[0]['source_row'];native=payload_of(source,row);units=[];proofs=[]
        for g in groups:
            if g['source_tpl']!=src_ref or g['source_row']!=row:raise ValueError('Archive source agreement')
            subset=[]
            for link in g['drafts']:
                require_hash(ROOT/link['path'],link['sha256']);a=read(link['path']);u=next(u for u in a['units'] if u['id']==link['id'])
                if u['id'] in seen or u['state']!='needs_review' or a['source_archive_sha256']!=sha(native) or a['source_tpl']!=src_ref:raise ValueError('Source/wording/scope identity')
                value=g['explicit_layouts'].get(u['id'],u['translation'])
                if value.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('Wording changed')
                unit=dict(id=u['id'],source=u['source'],translation=value,state=u['state']);subset.append(unit);units.append(unit);seen.add(u['id']);chars.update(value)
                if value.count('\n')!=u['source'].count('\n'):lf_edits.append(dict(id=u['id'],source_lf=u['source'].count('\n'),target_lf=value.count('\n')))
            if {u['id'] for u in subset}!=set(g['ids']):raise ValueError('Whole script literal selection')
            target_one=replace_for_analysis(original,subset);profile=g['profile']
            if profile=='fullbox':proof=full_validate(original,target_one,[g['script']],set(g['ids']),bound,88)
            elif profile=='pet-native-nickname':proof=quick_validate(original,target_one,[g['script']],set(g['ids']),bound)
            elif profile=='pet-flags':proof=flags_validate(original,target_one,[g['script']],set(g['ids']),bound)
            elif profile=='normal-horizontal-choice':proof=choice_validate(original,target_one,[g['script']],set(g['ids']),bound,88)
            elif profile=='normal-vertical-choice':proof=vertical_validate(original,target_one,[g['script']],set(g['ids']),bound,88)
            elif profile=='pet-array-conditional':proof=array_validate(original,target_one,[g['script']],set(g['ids']),bound)
            elif profile=='pet-direct-profile':proof=profile_validate(original,target_one,[g['script']],set(g['ids']),bound)
            elif profile=='pet-fixed-choice':proof=pet_choice_validate(original,target_one,[g['script']],set(g['ids']),bound)
            elif profile in ('normal-pages','normal-within-page-lf-proposal'):proof=normal_validate(original,target_one,[g['script']],set(g['ids']),bound,88)
            else:raise ValueError('Unknown layout profile')
            if proof!=g['geometry']:raise ValueError('Frozen geometry not reproduced')
            proofs.append(dict(profile=profile,script=g['script'],ids=g['ids'],geometry=proof))
        folder=out/arc;folder.mkdir();src_tpl=folder/'source.tpl';target_tpl=folder/'target.tpl';src_tpl.write_text(canonical_literals(original),encoding='utf-8',newline='\n');target=replace_for_analysis(original,units);target_tpl.write_text(canonical_literals(target),encoding='utf-8',newline='\n')
        native_file=folder/(arc+'_native.msg');compiled=folder/(arc+'.msg');reverse=folder/'reverse.tpl';rebuilt=folder/(arc+'_rebuilt.msg')
        run_textpet(common+['Read-Text-Archives',str(src_tpl),'--format','tpl','Write-Text-Archives',str(native_file),'--format','bin'],folder/'native-roundtrip.log')
        if native_file.read_bytes()!=native:raise ValueError('Native whole-payload byte roundtrip '+arc)
        run_textpet(common+['Read-Text-Archives',str(target_tpl),'--format','tpl','Write-Text-Archives',str(compiled),'--format','bin'],folder/'compile.log');payload=compiled.read_bytes()
        if len(payload)>65535:raise ValueError('16bit script offset capacity')
        run_textpet(common+['Read-Text-Archives',str(compiled),'--format','bin','Write-Text-Archives',str(reverse),'--format','tpl'],folder/'reverse.log')
        run_textpet(common+['Read-Text-Archives',str(reverse),'--format','tpl','Write-Text-Archives',str(rebuilt),'--format','bin'],folder/'rebuild.log');exported=reverse.read_text(encoding='utf-8-sig')
        if skeleton(original)!=skeleton(exported) or [(i.key,i.language,i.text) for i in literals(target)]!=[(i.key,i.language,i.text) for i in literals(exported)] or rebuilt.read_bytes()!=payload:raise ValueError('Target roundtrip '+arc)
        count=int(re.search(r'^@size (\d+)$',original,re.M)[1]);untouched=verify_untouched_scripts(native,payload,count,{g['script'] for g in groups})
        records.append(dict(archive=arc,source_sha256=sha(native),source_tpl=src_ref,compiled=ref(compiled),target_tpl=ref(target_tpl),script_count=count,units=units,profiles=proofs,native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,unselected_scripts=untouched,product_admitted=False))
        print('PASS source-only500',arc,len(units),'units',flush=True)
    if seen!=set(selected['selected_ids']) or len(seen)!=500:raise ValueError('Exact500 ID union')
    wanted={c for c in chars if '\uac00'<=c<='\ud7a3'};extra=chars&EXTRA_CHARACTER_INDICES.keys();fp=ROOT/cfg['development_dependencies']['font']['path'];require_hash(fp,cfg['development_dependencies']['font']['sha256']);glyphs=bdf_glyphs(fp,wanted);glyphs.update(bdf_glyphs(fp,extra,{c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}));ef=meta['extension']
    for ch,glyph in glyphs.items():
        index=ef['legacy_index_view']+(ord(ch)-0xAC00 if ch in wanted else EXTRA_CHARACTER_INDICES[ch]);at=ef['normal_font_offset']+index*96
        if rom[at:at+96]!=glyph:raise ValueError('Actual024 glyph supply '+ch)
    deps=[SELECTION,'tools/compile_layout500_029.py','tools/compile_layout_candidates_024.py','tools/normal_timing_capacity_025.py','tools/pet_nickname_flags_capacity_025_v2.py','tools/field_hint_capacity.py','tools/pet_nickname_capacity_025.py','tools/normal_battle_choice_capacity_026.py','tools/normal_vertical_choice_capacity_026.py','tools/pet_choice_capacity_026.py','tools/pet_profile_capacity_027_v2.py','tools/profile_provider_bounds_027_v2.py','tools/pet_array_capacity_029.py','tools/tpl_literals.py']
    frozen_write(out/'verification.json',dict(schema=1,status='EXACT500_SOURCE_ONLY_COMPILE_PASS_NOT_ROM_ADMISSION',passed=True,source_sha256=sha(source),baseline_rom=selected['baseline_rom'],baseline_sha256=sha(rom),selection=ref(ROOT/SELECTION),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},units=500,archive_count=len(records),archives=records,within_page_lf_edits=lf_edits,extended_glyphs_checked=len(glyphs),plugin=plugin,source_and_target_roundtrip=True,unselected_script_bytes_preserved=True,wording_changed=False,product_integrated=False,rom_written=False,insertion_ready=False,runtime_tested=False,release_eligible=False,limits='Exact500 source-only compilation, NOT a playable027 ROM. Full archive binaries intentionally retain unselected original text; inject only after cumulative026 carry merge and source-bound product gates. Opaque preserved conditional/flag behavior, LF proposal, whole write plan/repro and actual final-ROM CPU/GBA font/OBJ/pixels/clear/exit/reentry remain required.'))
    print('PASS exact500 source-only;',len(records),'archives;',len(glyphs),'actual026 glyphs;NO ROM written')


if __name__=='__main__':main()


