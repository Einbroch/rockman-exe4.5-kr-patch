#!/usr/bin/env python3
"""Primary immutable-source build for adopted dialogue and fixed-cell archives.

Version025 of the primary path; frozen024 composition remains before025.
Only source-pinned archives in the development registry may be selected.
Untouched archives keep their source storage, pointers, and compression bytes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from archive_scripts import verify_untouched_scripts
from build_visibility_poc import ROOT, bdf_glyphs, require_hash, run_textpet, sha
from compare_archive_payloads import payload_of
from extended_dialogue import HANGUL_COUNT, construct
from fixedcell_font import bdf_cells
from fixedcell_extension import construct as construct_fixedcell
from chip_library_extension import compile_clone, construct as construct_chip_library
from chip_battle_name_extension import construct as construct_battle_names
from pet_graphics_font import construct as construct_pet_graphics
from folder_labels import title as construct_equipment_title,validate_header_path,HEADER_SCOPE,HEADER_ROOT
from equipment_labels import validate as validate_equipment_labels,SCOPE as EQUIPMENT_SCOPE,ROOTS as EQUIPMENT_ROOTS,HEADER_WIDTH as EQUIPMENT_HEADER_WIDTH
from equipment_guides import construct as construct_equipment_guides,SCOPE as GUIDE_SCOPE
from lz10_literals import encode as encode_lz10, decode as decode_lz10
from korean_codec import EXTRA_CHARACTER_INDICES, EXTRA_CHARACTER_METRICS, encode_character
from textpet_korean import command, prepare_plugins
from tpl_literals import literals, replace_literals, resolve_units, skeleton, serialize
from verify_tpi_index import parse_tpi, lz77_decompress


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_numberman_return_decision(asset: dict) -> None:
    if asset.get('scope_variant')!='numberman-return-prose-v1':return
    unit=next(u for u in asset['units'] if u['id']=='6872B8:2:4')
    decision=next((d for d in asset.get('decisions',[]) if d['id']==unit.get('semantic_decision')),None)
    if not decision or decision.get('approved') is not True or decision.get('scope')!='6872B8:2:4 only' or unit['source']!='あらためて\n4649おねがいします' or unit['translation']!='다시 한번\n잘 부탁드려요':
        raise ValueError('NumberMan4649 semantic decision missing or changed')


def selected_scope(scope: dict, asset: dict) -> dict:
    variant=asset.get('scope_variant')
    if variant is None:
        return scope
    if variant in ('official-mail-v1','news-mail-v1'):
        from first_mail import specifications,validate_selected
        spec=specifications('news' if variant=='news-mail-v1' else True).get(asset['archive'])
        if spec is None or scope['literal_scripts']!=spec['scripts']:raise ValueError('official mail scope not registered')
        validate_selected(asset)
        return scope
    if variant=='full-mail-header-v1':
        from first_mail import FULL_HEADER_SCRIPTS,validate_selected
        validate_selected(asset)
        if asset['archive']!='6DD63C':raise ValueError('full mail header archive')
        return dict(scope,literal_scripts=FULL_HEADER_SCRIPTS,literal_ids=[u['id'] for u in asset['units']],
            max_literal_rows=1,max_line_advance=88,context=asset['context'])
    if variant=='mission-mail-header-v1':
        from mission_mail_header import validate,SCRIPTS
        validate(asset)
        if asset['archive']!='6DD864' or scope['literal_scripts']!=SCRIPTS:raise ValueError('mission header archive/scope')
        return dict(scope,literal_ids=[u['id'] for u in asset['units']])
    variants=scope.get('variants',{})
    if variant=='save-initialize-v1':
        from save_initialize import validate,SCRIPTS
        old=validate(asset);base=selected_scope(scope,old)
        profiles=base['literal_profiles']+[dict(scripts=SCRIPTS,consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=3,max_line_advance=132)]
        return dict(base,literal_scripts=sorted(set(base['literal_scripts']+SCRIPTS)),literal_ids=[u['id'] for u in asset['units']],literal_profiles=profiles,context=asset['context'])
    if variant=='calendar-date-save-v1':
        from calendar_date_save import validate,SCRIPTS
        validate(asset)
        base=selected_scope(scope,dict(asset,scope_variant='input-remaining-v1',parent_asset={'path':'translations/input_heading_ko.json','sha256':'3aeea8e1b6d5956e0ba2d6a635d6b2932e45c82223bd7cc46eddf7334107e884','carry_units':17},units=asset['units'][:38]))
        profiles=base['literal_profiles']+[dict(scripts=SCRIPTS,consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=3,max_line_advance=132)]
        return dict(base,literal_scripts=sorted(set(base['literal_scripts']+SCRIPTS)),literal_ids=[u['id'] for u in asset['units']],literal_profiles=profiles,protected_numeral_ids=base['protected_numeral_ids']+['6368E8:91:1'],literal_tokens={'6368E8:91:1':{'[z]':'99'}},context=asset['context'])
    if variant=='input-remaining-v1':
        from input_remaining import validate,SCRIPTS
        validate(asset)
        base=variants['input-heading-v1']
        profiles=[dict(p) for p in base['literal_profiles']]
        profiles.append(dict(scripts=[s for s in SCRIPTS if s!=11],consumer='fixed-cell-mono',literal_language='mmbn45s',max_literal_rows=1,max_line_advance=80))
        profiles.append(dict(scripts=[11],consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=3,max_line_advance=132))
        return dict(scope,**dict(base,literal_scripts=sorted(set(base['literal_scripts']+SCRIPTS)),literal_ids=base['literal_ids']+[f'6368E8:{s}:0' for s in SCRIPTS],literal_profiles=profiles,context=asset['context']))
    if variant not in variants:
        raise ValueError('unregistered archive scope variant')
    if variant=='roll-gutsman-plugout-v1':
        parent=ROOT/'translations/roll_plugout_ko.json'
        require_hash(parent,'cd2cbfb2f2569b19afa8bc5908271b870469bd64a692d1207ba227d827f65421')
        carried=resolve_units(read_json(parent));indexed={u['id']:u for u in resolve_units(asset)}
        if any(indexed.get(u['id'])!=u for u in carried):raise ValueError('Roll plugout parent wording/source/state changed')
    if variant in ('gutsman-profile-answers-v1','gutsman-profile-wishlist-v1'):
        wishlist=variant=='gutsman-profile-wishlist-v1';carry=150 if wishlist else 110
        path='translations/gutsman_profile_answers_ko.json' if wishlist else 'translations/gutsman_profile_family_checked_ko.json'
        digest='e04a02a87e2ca4d5d86caa686965df2abde660ff4a14e93cc9e57fc9705a9b1f' if wishlist else 'b721d8274af3d1b7e5afe84ae8cfbd2023998234014d31f5ab68e86c9a8b0eeb'
        require_hash(ROOT/path,digest)
        carried=resolve_units(read_json(ROOT/path));indexed={u['id']:u for u in resolve_units(asset)}
        if len(carried)!=carry or asset.get('parent_asset')!={'path':path,'sha256':digest,'carry_units':carry} or any(indexed.get(u['id'])!=u for u in carried):raise ValueError('GutsMan answers parent changed')
        for first,last in [('667044:11:3','667044:11:4'),('667044:88:0','667044:88:1')]:
            a,b=indexed[first]['translation'],indexed[last]['translation']
            if not a.endswith('\n') or a.count('\n')!=1 or b.count('\n')!=1 or b.split('\n')[0]!='、':raise ValueError('GutsMan joined nickname page must retain three-row layout')
    if variant in ('gutsman-profile-questions-v1','gutsman-profile-family-v1'):
        family=variant=='gutsman-profile-family-v1'
        path='translations/gutsman_profile_questions_ko.json' if family else 'translations/gutsman_profile_ko.json'
        parent=ROOT/path
        digest='18d06a397c5708015b30ddb820a5a4b207d8fca369ddedd1ec3d284f0a6a68bb' if family else 'b69d6a1f553ce743c04c44c96112f700bd1725fae7240700397a9b51d54458c5'
        require_hash(parent,digest)
        carried=resolve_units(read_json(parent));indexed={u['id']:u for u in resolve_units(asset)}
        if asset.get('parent_asset')!={'path':path,'sha256':digest,'carry_units':81 if family else 40} or any(indexed.get(u['id'])!=u for u in carried):raise ValueError('GutsMan profile parent wording/source/state changed')
        # These source-pinned pages join two literals around a second-row
        # nickname. Per-literal3-row validation alone does not bound the page.
        for first,last in [('667044:11:3','667044:11:4'),('667044:88:0','667044:88:1')]:
            a,b=indexed[first]['translation'],indexed[last]['translation']
            if not a.endswith('\n') or a.count('\n')!=1 or b.count('\n')!=1 or b.split('\n')[0]!='、':raise ValueError('GutsMan joined nickname page must retain three-row layout')
    override=variants[variant]
    if set(override)-{'literal_scripts','literal_ids','literal_profiles','context','reward_variable_profile','chipquest_variable_profile','schedule_variable_profile','nickname_suffix_scripts','nickname_suffix_profiles','nickname_aggregate_profiles','standalone_choice_rows','choice_groups','vertical_choice_rows','grid_choice_rows','protected_numeral_ids'} or not override.get('literal_scripts'):
        raise ValueError('scope variant may only select pinned script inventory/context')
    return dict(scope,**override)


def literal_scope(scope: dict, key: str) -> dict:
    """Source-pinned mixed archives retain separate language/geometry paths."""
    script=int(key.split(':')[1]); matches=[]
    for p in scope.get('literal_profiles',[]):
        if (set(p)-{'scripts','consumer','literal_language','max_literal_rows','max_line_advance'}
                or not p.get('scripts') or not set(p['scripts'])<=set(scope['literal_scripts'])
                or p.get('consumer') not in ('normal-dialogue','fixed-cell-big','fixed-cell-mono')
                or p.get('literal_language') not in ('mmbn45','mmbn45s')
                or p.get('max_literal_rows',0)<=0 or p.get('max_line_advance',0)<=0):
            raise ValueError('invalid mixed literal profile')
        if script in p['scripts']:matches.append(p)
    if len(matches)>1:raise ValueError('overlapping mixed literal profiles')
    return dict(scope,**{k:v for k,v in matches[0].items() if k!='scripts'}) if matches else scope


def translate_literal_scope(original: str, units: list[dict], scope: dict) -> str:
    grouped={}
    if scope.get('pending500_002_pages') or scope.get('pending500_003_equipment_layout'):
        from pending500_002_pages import replace as replace_pages
        return replace_pages(original,units)[0]
    if scope.get('full_mail_raw_rom'):
        from full_mail_body import replace
        return replace(original,units)
    if scope.get('literal_ids') and '6368E8:96:0' in scope['literal_ids']:
        from save_initialize import replace as replace_initialize
        return replace_initialize(original,units)
    if scope.get('literal_ids') and '6368E8:91:0' in scope['literal_ids']:
        from calendar_date_save import replace as replace_date_save
        return replace_date_save(original,units)
    if scope.get('literal_ids') and '6368E8:11:0' in scope['literal_ids'] and '6368E8:33:0' in scope['literal_ids']:
        from input_remaining import replace as replace_remaining
        return replace_remaining(original,units)
    if scope.get('literal_ids') and '6368E8:33:0' in scope['literal_ids']:
        from input_heading import replace as replace_heading
        return replace_heading(original,units)
    if scope.get('literal_ids') and '6368E8:10:0' in scope['literal_ids']:
        from input_confirmation import replace as replace_confirmation
        return replace_confirmation(original,units)
    if scope.get('literal_ids') and '6368E8:80:0' in scope['literal_ids']:
        from possessions_statistics import replace as replace_statistics
        return replace_statistics(original,units)
    if scope.get('nickname_aggregate_profiles'):
        from gutsman_calendar_inventory import replace as replace_inventory
        return replace_inventory(original,units)
    if {u['id'] for u in units}=={'6368E8:0:0','6368E8:60:0','6368E8:62:0','6368E8:63:0','6368E8:73:0','6368E8:74:0','6368E8:75:0',*[f'6368E8:{i}:0'for i in range(119,124)]}:
        from calendar_frequency_names import replace as replace_frequency
        return replace_frequency(original,units)
    if {u['id'] for u in units}=={'6368E8:0:0','6368E8:60:0','6368E8:62:0','6368E8:63:0','6368E8:73:0','6368E8:74:0','6368E8:75:0'}:
        from calendar_anniversary_confirmation import replace as replace_anniversary_presets,PARENTS
        parent,digest,count,_=PARENTS['6368E8']
        return replace_anniversary_presets(original,dict(archive='6368E8',parent_asset=dict(path=parent,sha256=digest,carry_units=count),units=units))
    if {u['id'] for u in units}=={'6368E8:0:0','6368E8:60:0','6368E8:62:0','6368E8:63:0','6368E8:73:0'}:
        from calendar_anniversary_labels import replace as replace_anniversary_labels
        return replace_anniversary_labels(original,units)
    if scope.get('literal_scripts')==[0,60,62,63] and scope.get('literal_ids')==['6368E8:0:0','6368E8:60:0','6368E8:62:0','6368E8:63:0']:
        from calendar_presets import replace as replace_presets
        return replace_presets(original,units)
    if {u['id'] for u in units}=={'6368E8:0:0','6368E8:60:0'}:
        from calendar_types_model import replace_types_literals
        return replace_types_literals(original,units)
    if {u['id'] for u in units}=={'6368E8:0:0'}:
        from calendar_menu_model import replace_menu_literal
        return replace_menu_literal(original,units)
    for u in units:
        p=literal_scope(scope,u['id'])
        language=p.get('literal_language','mmbn45s' if p['consumer']=='fixed-cell-big' else 'mmbn45')
        grouped.setdefault(language,[]).append(u)
    target=original
    trailing={}
    for group in scope.get('grid_choice_rows',[]):
        for literal,count in group.get('trailing_literal_spaces',{}).items():
            key=f"715064:{group['script']}:{literal}"
            # Only the source-pinned NumberMan grid permits this exception.
            if key not in ('715064:13:1','715064:13:3') or count!=1 or scope.get('literal_scripts')!=list(range(16)) or not all(u['id'].startswith('715064:') for u in units):
                raise ValueError('unregistered trailing grid padding')
            trailing[key]=count
    for language,subset in grouped.items():target=replace_literals(target,subset,language=language,trailing_spaces=trailing)
    # TextPet alpha3 LF serialization can lose an unselected literal's leading
    # empty line. Explicit escapes retain the same decoded text/E8 boundary;
    # source/semantic/binary and unselected-script byte checks still apply.
    for item in reversed(literals(target)):
        if item.text.startswith('\n'):target=target[:item.start]+serialize(item.text)+target[item.end:]
    before={x.key:x for x in literals(original)};after={x.key:x for x in literals(target)}
    selected={u['id'] for u in units}
    if any(before[k].text!=after[k].text or before[k].language!=after[k].language for k in before if k not in selected):
        raise ValueError('unselected mixed literal changed')
    return target


def validate_literal_numerals(units: list[dict], scope: dict) -> None:
    for unit in units:
        if scope.get('preserve_literal_numerals') or unit['id'] in scope.get('protected_numeral_ids',[]):
            if re.findall(r'\d+',unit['source'])!=re.findall(r'\d+',unit['translation']):
                raise ValueError(f"protected literal numeral changed: {unit['id']}")
            if unit['id'] in scope.get('protected_numeral_ids',[]) and re.findall(r'\d+~\d+',unit['source'])!=re.findall(r'\d+~\d+',unit['translation']):
                raise ValueError(f"protected literal range changed: {unit['id']}")


def validate_characters(tpl: str, table_path: Path, scope: dict, selected_ids: set[str]) -> list[dict]:
    codes = {}
    token_codes = {}
    for line in table_path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if len(value) == 1:
                codes[value] = bytes.fromhex(key)
            elif value.startswith('[') and value.endswith(']'):
                token_codes[value] = bytes.fromhex(key)
    measured = []
    for item in literals(tpl):
        if item.key not in selected_ids:
            continue
        profile=literal_scope(scope,item.key)
        widths = []
        for line in item.text.split("\n"):
            width = 0
            allowed_tokens=scope.get('literal_tokens',{}).get(item.key,{})
            for token,hexcode in allowed_tokens.items():
                if token_codes.get(token)!=bytes.fromhex(hexcode):raise ValueError('pinned literal token mapping')
            pattern='|'.join(re.escape(t) for t in allowed_tokens)
            chars=re.findall('(?:'+pattern+')|.' if pattern else '.',line)
            for ch in chars:
                if ch in allowed_tokens:
                    if profile['consumer']!='normal-dialogue':raise ValueError('token consumer not adopted')
                    width+=11
                    continue
                if profile["consumer"] in ("fixed-cell-big", "fixed-cell-mono"):
                    if ch in EXTRA_CHARACTER_INDICES:
                        raise ValueError("extra-character glyphs not adopted for this fixed-cell provider")
                    if ch not in codes or (0xAC00 <= ord(ch) <= 0xD7A3 and codes[ch] != encode_character(ch)):
                        raise ValueError(f"unmapped fixed-cell character: {ch!r}")
                    width += 8
                    continue
                if 0xAC00 <= ord(ch) <= 0xD7A3 or ch in EXTRA_CHARACTER_INDICES:
                    if codes.get(ch) != encode_character(ch):
                        raise ValueError(f"extended character mismatch: {ch!r}")
                    width += 12
                else:
                    if ch not in codes:
                        raise ValueError(f"unmapped character in {item.key}: {ch!r}")
                    width += 8 if ch == " " else 11
            widths.append(width)
        if len(widths) > profile["max_literal_rows"] or max(widths, default=0) > profile["max_line_advance"]:
            raise ValueError(f"scene layout needs review: {item.key}: {widths}")
        record = {"id": item.key, "line_advance_pixels": widths}
        measured.append(record)
    groups = [{"script": i, "literals": [0, 1, 2], "prompt_rows": 3} for i in scope.get("choice_scripts", [])]
    groups.extend(scope.get("choice_groups", []))
    indexed = {r["id"]: r for r in measured}
    archive = literals(tpl)[0].key.split(":")[0]
    for group in groups:
        script = group["script"]
        prompt, yes, no = [indexed[f"{archive}:{script}:{i}"] for i in group["literals"]]
        if len(prompt["line_advance_pixels"]) != group["prompt_rows"] or prompt["line_advance_pixels"][-1] != 0:
            raise ValueError("choice prompt no longer leaves its selection row open")
        # Unchanged commands: spacePx(24), option, space(1), yes,
        # option, space(1), no. The normal font's space width is 8.
        row_advance = 24 + 8 + yes["line_advance_pixels"][0] + 8 + no["line_advance_pixels"][0]
        if row_advance > scope["max_line_advance"]:
            raise ValueError(f"choice row exceeds adopted display extent: script {script}")
        prompt["choice_row_advance_pixels"] = row_advance
        prompt["choice_runtime_check_required"] = True
    for group in scope.get('standalone_choice_rows',[]):
        yes,no=[indexed[f"{archive}:{group['script']}:{i}"] for i in group['literals']]
        if len(yes['line_advance_pixels'])!=1 or len(no['line_advance_pixels'])!=1:raise ValueError('standalone choice row count changed')
        advance=group['prefix_pixels']+8+yes['line_advance_pixels'][0]+8+no['line_advance_pixels'][0]
        if advance>scope['max_line_advance']:raise ValueError('standalone choice row exceeds adopted display extent')
        yes.update(choice_row_advance_pixels=advance,choice_runtime_check_required=True)
    for group in scope.get('vertical_choice_rows',[]):
        labels=[indexed[f"{archive}:{group['script']}:{i}"] for i in group['literals']]
        for label in labels:
            if len(label['line_advance_pixels'])!=2 or label['line_advance_pixels'][1]!=0:
                raise ValueError('vertical option trailing row boundary changed')
            if 8+label['line_advance_pixels'][0]>11*group['native_width']:
                raise ValueError('vertical option exceeds native centered slot')
            label.update(vertical_option_slot_pixels=11*group['native_width'],choice_runtime_check_required=True)
    for group in scope.get('grid_choice_rows',[]):
        labels=[indexed[f"{archive}:{group['script']}:{i}"] for i in group['literals']]
        pads=group.get('leading_literal_spaces',0)
        text={x.key:x.text for x in literals(tpl)}
        if pads and any(len(text[f"{archive}:{group['script']}:{i}"])-len(text[f"{archive}:{group['script']}:{i}"].lstrip(' '))!=pads for i in group['literals']):
            raise ValueError('grid label leading padding changed')
        if len(labels)!=4:raise ValueError('grid requires four choices')
        for i,label in enumerate(labels):
            widths=label['line_advance_pixels']
            if len(widths)!=(2 if i%2 else 1) or (i%2 and widths[-1]!=0):
                raise ValueError('grid option row boundaries changed')
        for i in [0,2]:
            width=16+sum(x['line_advance_pixels'][0] for x in labels[i:i+2])
            if width>scope['max_line_advance']:raise ValueError('grid choice row overflow')
            labels[i].update(grid_choice_row_pixels=width,choice_runtime_check_required=True)
    return measured


def validate_nickname_suffix(units: list[dict], archive: str, scope: dict) -> None:
    for profile in scope.get('nickname_suffix_profiles',[]):
        if set(profile)!={'script','literal','source_first_line','first_line'} or profile['script'] not in scope['literal_scripts']:raise ValueError('invalid pinned nickname suffix profile')
        unit=next(u for u in units if u['id']==f"{archive}:{profile['script']}:{profile['literal']}")
        source_line=unit['source'].split('\n')[0];target_line=unit['translation'].split('\n')[0]
        if source_line!=profile['source_first_line'] or target_line!=profile['first_line']:raise ValueError('dynamic nickname suffix differs from pinned food translation')
        def advance(line):return sum(8 if c==' ' else 12 if '\uac00'<=c<='\ud7a3' or c in EXTRA_CHARACTER_INDICES else 11 for c in line)
        if advance(target_line)>advance(source_line):raise ValueError('dynamic nickname suffix width grows')
    for script in scope.get('nickname_suffix_scripts',[scope['nickname_suffix_script']] if 'nickname_suffix_script' in scope else []):
        unit=next(u for u in units if u['id']==f"{archive}:{script}:{scope.get('nickname_suffix_literal',0)}")
        # Source first-line punctuation follows a dynamic nickname. Keeping
        # these exact bytes avoids adding width or Korean particle dependence.
        source_line=unit['source'].split('\n')[0];target_line=unit['translation'].split('\n')[0]
        if 'nickname_suffix_first_line' in scope:
            if source_line!=scope.get('nickname_suffix_source_first_line') or target_line!=scope['nickname_suffix_first_line']:raise ValueError('dynamic nickname suffix differs from pinned topic translation')
            def advance(line):return sum(8 if c==' ' else 12 if '\uac00'<=c<='\ud7a3' or c in EXTRA_CHARACTER_INDICES else 11 for c in line)
            if advance(target_line)>advance(source_line):raise ValueError('dynamic nickname suffix width grows')
        elif target_line!=source_line:raise ValueError('dynamic nickname suffix first-line bytes must remain source-identical')

def compile_archive(source: bytes, row: dict, asset: dict, scope: dict, common: list[str],
                    plugins: Path, work: Path) -> tuple[bytes, dict]:
    archive = asset["archive"]
    native_payload = payload_of(source, row)
    if sha(native_payload) != asset["source_archive_sha256"]:
        raise ValueError(f"protected source payload changed: {archive}")
    work.mkdir()
    (work / "compiled").mkdir()
    native_file = work / f"{archive}.msg"
    native_file.write_bytes(native_payload)
    source_tpl = work / "source.tpl"
    run_textpet(common + ["Read-Text-Archives", str(native_file), "--format", "bin",
                         "Write-Text-Archives", str(source_tpl), "--format", "tpl"], work / "extract.log")
    original = source_tpl.read_text(encoding="utf-8-sig")
    fullbox_proof=[]
    if scope.get('fullbox_capacity_profiles'):
        from fullbox_capacity import validate as validate_fullbox
        fullbox_proof=validate_fullbox(original,translate_literal_scope(original,resolve_units(asset),scope),scope['fullbox_capacity_profiles'],set(scope['literal_ids']))
    for profile in scope.get('nickname_aggregate_profiles',[]):
        if archive!='665698' or asset.get('scope_variant')!='calendar-inventory-v1':raise ValueError('unregistered aggregate consumer')
        from gutsman_calendar_inventory import template
        template(resolve_units(asset),profile,original)
    native_rebuilt = work / "native-rebuilt.msg"
    run_textpet(common + ["Read-Text-Archives", str(source_tpl), "--format", "tpl",
                         "Write-Text-Archives", str(native_rebuilt), "--format", "bin"], work / "native-rebuild.log")
    if native_rebuilt.read_bytes() != native_payload:
        raise ValueError(f"native archive roundtrip failed: {archive}")
    units = resolve_units(asset)
    validate_nickname_suffix(units,archive,scope)
    validate_literal_numerals(units,scope)
    selected_ids = {u["id"] for u in units}
    if scope["complete_literal_scope"]:
        expected_ids = {x.key for x in literals(original)}
    else:
        if not scope.get("literal_scripts") or "script_count" not in scope:
            raise ValueError("partial archive scope requires an explicit script denominator")
        expected_ids = {x.key for x in literals(original) if int(x.key.split(":")[1]) in scope["literal_scripts"]}
        if 'literal_ids' in scope:
            pinned=set(scope['literal_ids'])
            if (len(pinned)!=len(scope['literal_ids']) or not pinned<=expected_ids
                    or {int(k.split(':')[1]) for k in pinned}!=set(scope['literal_scripts'])):
                raise ValueError('invalid partial literal denominator')
            expected_ids=pinned
    if expected_ids != selected_ids:
        raise ValueError(f"selected archive literal denominator changed: {archive}")
    translated = translate_literal_scope(original,units,scope)
    field_hint_proof=None
    if scope.get('field_hint_capacity_profile'):
        from field_hint_capacity import validate_source as validate_field_hint
        field_hint_proof=validate_field_hint(source,archive,original,translated,scope)
    nickname_capacity_proof=None
    if scope.get('nickname_capacity_profiles'):
        from nickname_capacity import validate as validate_nickname_capacity
        nickname_capacity_proof=validate_nickname_capacity(source,original,translated,scope['nickname_capacity_profiles'],selected_ids)
    page_mapping=None;page_proof=None
    if scope.get('pending500_002_pages') or scope.get('pending500_003_equipment_layout'):
        if archive not in ('6DED88','6E1554','6E1CC0','6E21B0'):raise ValueError('Unregistered explicit pages')
        from pending500_002_pages import replace as replace_pages
        page_target,page_mapping,page_proof=replace_pages(original,units)
        if page_target!=translated:raise ValueError('Page selection mismatch')
        fragment_ids={k for original_id in selected_ids for k in page_mapping[original_id]}
        layout = validate_characters(translated, plugins / "exe45-utf8.tbl", scope, fragment_ids)
    else:layout = validate_characters(translated, plugins / "exe45-utf8.tbl", scope, selected_ids)
    if scope.get('mail_arrow_row3_limit'):
        if archive not in ('6DE3E0','6DF988','6E01AC','6DED88','6DE2C8') or scope['mail_arrow_row3_limit']!=132:raise ValueError('unregistered mail arrow extent')
        for r in layout:
            if len(r['line_advance_pixels'])==3 and r['line_advance_pixels'][2]>132:raise ValueError('mail row3 arrow overlap '+r['id'])
    mail_proof=None
    if scope.get('full_mail_raw_rom'):
        from full_mail_body import validate
        mail_proof=validate(source,asset,original,translated,layout)
    if scope.get('schedule_variable_profile'):
        from roll_schedule_time_model import validate
        validate(units,scope,original,translated,layout)
    reward_proof=None
    if archive=='6DE3E0' and scope.get('mission_reward_profile'):
        from mission_reward_model import validate as validate_mission_reward
        reward_proof=validate_mission_reward(source,units,layout)
    if scope.get('reward_variable_profile'):
        if scope['reward_variable_profile']=='numberman-minigame-buffer3-v1':
            from numberman_reward_model import validate_layout
        else:
            from roll_reward_model import validate_layout
        reward_proof=validate_layout(source,layout,scope)
    if scope.get('chipquest_variable_profile'):
        if scope['chipquest_variable_profile']=='gutsman-chip104-native-and-ko-v1':
            from gutsman_chipquest_model import validate_layout
        else:
            from roll_chipquest_model import validate_layout
        validate_layout(source,units,layout,scope)
    if "dynamic_name_script" in scope:
        key = f"{archive}:{scope['dynamic_name_script']}:0"
        before = next(x for x in literals(original) if x.key == key)
        after = next(x for x in layout if x["id"] == key)
        # Variable bytes/command are unchanged; prefix demand must not grow.
        original_advance = sum(8 if ch == " " else 11 for ch in before.text)
        if after["line_advance_pixels"][0] > original_advance:
            raise ValueError("dynamic-name prefix growth needs a full variable-width model")
        after["dynamic_suffix_unchanged"] = True
        after["source_prefix_advance_pixels"] = original_advance
    translated_file = work / "translated.tpl"
    equipment_proof=None
    if scope.get('equipment_aggregate_profile'):
        if archive not in ('6E1554','6E1CC0','6E21B0'):raise ValueError('Unregistered equipment aggregate')
        from batch500_003_rom import validate_aggregate
        equipment_proof=validate_aggregate(source,asset,layout)
    translated_file.write_text(translated, encoding="utf-8", newline="\n")
    compiled, reverse, rebuilt = work / "compiled" / f"{archive}.msg", work / "reverse.tpl", work / "rebuilt.msg"
    run_textpet(common + ["Read-Text-Archives", str(translated_file), "--format", "tpl",
                         "Write-Text-Archives", str(compiled), "--format", "bin"], work / "compile.log")
    payload = compiled.read_bytes()
    if len(payload) > 0xFFFF:
        raise ValueError("16-bit archive script-offset range exceeded")
    run_textpet(common + ["Read-Text-Archives", str(compiled), "--format", "bin",
                         "Write-Text-Archives", str(reverse), "--format", "tpl"], work / "reverse.log")
    reexport = reverse.read_text(encoding="utf-8-sig")
    if ([(x.key, x.text) for x in literals(translated)] != [(x.key, x.text) for x in literals(reexport)]
            or skeleton(translated) != skeleton(reexport)):
        raise ValueError(f"translated text or protected controls failed semantic roundtrip: {archive}")
    run_textpet(common + ["Read-Text-Archives", str(reverse), "--format", "tpl",
                         "Write-Text-Archives", str(rebuilt), "--format", "bin"], work / "rebuild.log")
    if rebuilt.read_bytes() != payload:
        raise ValueError("translated archive failed binary roundtrip")
    sharing=None
    quantity_proof=None
    if archive=='709408' and scope.get('keyitem_raw_rom'):
        from keyitem_rom_data import validate_payload
        quantity_proof=validate_payload(source,native_payload,payload,original,translated,units,layout)
    elif archive=='709408':
        from keyitem_empty import compact,validate_source
        validate_source(source,native_payload)
        if units!=[dict(id='709408:32:0',source='キーアイテムが\n1つもない・・・',translation='키 아이템이\n1개도 없다・・・',state='needs_review')]:raise ValueError('keyitem empty exact selection')
        payload,sharing=compact(native_payload,payload)
    preserved = (verify_untouched_scripts(native_payload, payload, scope["script_count"], set(scope["literal_scripts"]))
                 if not scope["complete_literal_scope"] and sharing is None else [])
    if page_mapping:
        from pending500_002_pages import remap_layout
        layout=remap_layout(layout,page_mapping,[u['id'] for u in units])
    return payload, {**({'field_hint_capacity_proof':field_hint_proof} if field_hint_proof is not None else {}),**({'fullbox_capacity_proof':fullbox_proof} if fullbox_proof else {}),**({'nickname_capacity_proof':nickname_capacity_proof} if nickname_capacity_proof is not None else {}),"archive": archive, "source_bytes": len(native_payload), "source_sha256": sha(native_payload),
                     "explicit_page_layout":page_proof,
                     "equipment_aggregate_proof":equipment_proof,
                     "compiled_bytes": len(payload), "compiled_sha256": sha(payload), "translated_units": len(units),
                     "native_roundtrip": True, "semantic_roundtrip": True, "binary_roundtrip": True,
                       "protected_controls_unchanged": True, "layout": layout, "reward_variable_proof":reward_proof,"native_storage_sharing":sharing,"quantity_aggregate_proof":quantity_proof,
                       "mail_player_name_proof":mail_proof,
                       "textpet_roundtrip_stage":"before native storage sharing" if sharing else "final payload",
                       "post_sharing_native_resolved_equivalence":True if sharing else None,
                     "unselected_script_bytes_preserved": preserved}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--translations", action="append", help="repeat for explicit archive selection; defaults to registry")
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fixedcell-visibility", action="store_true",
                    help="NON-DISTRIBUTION diagnostic: temporarily replace four used big-font slots")
    ap.add_argument("--chip-library", action="store_true",
                    help="NON-DISTRIBUTION: private seven-row library chip-name draft")
    ap.add_argument("--chip-word-copy", action="store_true",
                    help="experimental aligned word-copy candidate; requires --chip-library")
    ap.add_argument("--chip-cache", action="store_true", help="experimental per-cell tags; requires --chip-word-copy")
    ap.add_argument('--chip-burst-copy', action='store_true', help='experimental 6+6+4 word bursts; requires --chip-word-copy')
    ap.add_argument('--chip-fast-copy', action='store_true', help='experimental native fast BIOS copy; requires --chip-word-copy')
    ap.add_argument('--chip-stack-renderer', action='store_true', help='experimental private IWRAM stack execution; requires --chip-burst-copy')
    ap.add_argument('--chip-library-late-wait', action='store_true', help='experimental active-library late VBlank wait; requires --chip-cache')
    ap.add_argument('--chip-name-translations', help='explicit non-distribution library name asset; requires --chip-library')
    ap.add_argument('--chip-folder', action='store_true', help='experimental separate seven-row folder consumer; requires library cache/burst and excludes stack/fast')
    ap.add_argument('--chip-folder-owner-guard', action='store_true', help='require confirmed folder context/job/menu/phase for private rendering and tag reset')
    ap.add_argument('--mono-font-poc', action='store_true', help='NON-DISTRIBUTION optional mono F9FC provider; no description translation')
    ap.add_argument('--hangul-keyboard-glyphs',action='store_true',help='NON-DISTRIBUTION jamo supply only; automatic keyboard hooks not installed')
    ap.add_argument('--native-keyboard-labels',action='store_true',help='Korean native kana command graphics only; no Hangul input hooks')
    ap.add_argument('--navi-card-graphics',action='store_true',help='21 same-slot native Navi card-name graphics')
    ap.add_argument('--chip-battle-names', action='store_true', help='NON-DISTRIBUTION caller-gated reuse of selected names in native8x1 battle cards')
    ap.add_argument('--chip-secondary-name-translations',help='explicit secondary names; guarded library/folder only, not battle')
    ap.add_argument('--pet-menu-graphics',action='store_true',help='NON-DISTRIBUTION source-preserving seven PET OBJ labels')
    ap.add_argument('--calendar-frequency-graphics',action='store_true',help='NON-DISTRIBUTION five same-slot calendar OBJ labels')
    ap.add_argument('--calendar-presets-poc',action='store_true',help='NON-DISTRIBUTION bounded preset names/confirmation counter experiment')
    ap.add_argument('--save-title-graphics',action='store_true',help='NON-DISTRIBUTION same-slot save OBJ title')
    ap.add_argument('--title-menu-graphics',action='store_true',help='Same-slot Korean new-game and continue OBJ labels')
    ap.add_argument('--title-weekend-menu',action='store_true',help='Same-slot Korean all three title labels including weekend tournament')
    ap.add_argument('--folder-labels',action='store_true',help='NON-DISTRIBUTION equipment title and isolated chip-folder header clone')
    ap.add_argument('--equipment-labels',action='store_true',help='NON-DISTRIBUTION three shared equipment menu literals; requires folder-labels')
    ap.add_argument('--equipment-guides',action='store_true',help='NON-DISTRIBUTION source-pool-specific three equipment guides; requires equipment-labels')
    ap.add_argument('--roll-equipment-guides',action='store_true',help='NON-DISTRIBUTION separate Navi1 equipment guide clone; requires equipment-guides')
    ap.add_argument('--equipment-weapons',action='store_true',help='NON-DISTRIBUTION additional33 shared weapon names; requires equipment-labels')
    ap.add_argument('--equipment-attack-caption',action='store_true',help='NON-DISTRIBUTION original-slot compressed buster attack label; requires equipment-labels')
    ap.add_argument('--roll-dialogue-chip-name',action='store_true',help='NON-DISTRIBUTION exact Roll13 printChip104 normal-buffer name reuse')
    ap.add_argument('--gutsman-dialogue-chip-name',action='store_true',help='NON-DISTRIBUTION additional exact Guts13 name selector guard')
    ap.add_argument('--keyitem-rom-translations',help='NON-DISTRIBUTION full39 raw-ROM clone; requires retained bounded709408')
    ap.add_argument('--mail-rom-reader',action='store_true',help='NON-DISTRIBUTION guarded mail ROM-reader capacity PoC; retained bounded RAM archive required')
    ap.add_argument('--full-mail-body',help='Explicit full120 raw mail clone; retained77 compressed RAM archive required')
    ap.add_argument('--pending-batch500',action='store_true')
    ap.add_argument('--pending-batch500-002',action='store_true')
    ap.add_argument('--pending-batch500-003',action='store_true')
    ap.add_argument('--pending-batch500-004',action='store_true')
    ap.add_argument('--pending-batch500-005',action='store_true')
    ap.add_argument('--pending-batch500-006',action='store_true')
    ap.add_argument('--pending-batch500-007',action='store_true')
    ap.add_argument('--pending-batch500-008',action='store_true')
    ap.add_argument('--pending-batch500-009',action='store_true')
    ap.add_argument('--pending-batch500-010',action='store_true')
    ap.add_argument('--pending-batch500-011',action='store_true')
    ap.add_argument('--pending-batch500-012',action='store_true')
    ap.add_argument('--pending-batch500-013',action='store_true')
    ap.add_argument('--pending-batch500-014',action='store_true')
    ap.add_argument('--pending-batch500-015',action='store_true')
    ap.add_argument('--pending-batch500-016',action='store_true')
    ap.add_argument('--pending-batch500-017',action='store_true')
    ap.add_argument('--pending-batch500-018',action='store_true')
    ap.add_argument('--pending-batch500-019',action='store_true')
    ap.add_argument('--pending-batch500-020',action='store_true')
    ap.add_argument('--pending-batch500-021',action='store_true')
    ap.add_argument('--pending-batch500-022',action='store_true')
    ap.add_argument('--field-b0-hints-023',action='store_true',help='development500 B0 hints; requires retained022')
    from build_arguments import expand
    expanded,argument_manifest=expand(sys.argv[1:])
    args = ap.parse_args(expanded)
    if args.field_b0_hints_023 and (not args.pending_batch500_022 or not args.keyitem_rom_translations):raise ValueError('B0 requires retained022/keyitem reader')
    if args.equipment_weapons and not args.equipment_labels:raise ValueError('equipment weapons require equipment labels')
    if args.equipment_attack_caption and not args.equipment_labels:raise ValueError('attack caption requires adopted equipment labels')
    if args.chip_name_translations and not args.chip_library:
        raise ValueError('--chip-name-translations requires --chip-library')
    if args.chip_battle_names and not args.chip_library:
        raise ValueError('--chip-battle-names requires --chip-library')
    if args.chip_secondary_name_translations and not args.chip_library:
        raise ValueError('secondary names require guarded library consumer')
    if args.chip_folder_owner_guard and not args.chip_folder:
        raise ValueError('--chip-folder-owner-guard requires --chip-folder')
    if args.chip_folder and (not args.chip_library or not args.chip_cache or not args.chip_burst_copy or args.chip_stack_renderer or args.chip_fast_copy):
        raise ValueError('--chip-folder requires --chip-library --chip-cache --chip-burst-copy and excludes stack/fast')
    if args.chip_library_late_wait and not args.chip_cache:
        raise ValueError('--chip-library-late-wait requires --chip-cache')
    if args.chip_stack_renderer and (not args.chip_burst_copy or args.chip_fast_copy):
        raise ValueError('--chip-stack-renderer requires --chip-burst-copy and excludes --chip-fast-copy')
    if args.chip_burst_copy and not args.chip_word_copy:
        raise ValueError('--chip-burst-copy requires --chip-word-copy')
    if args.chip_fast_copy and (not args.chip_word_copy or args.chip_burst_copy):
        raise ValueError('--chip-fast-copy requires --chip-word-copy and excludes --chip-burst-copy')
    if args.chip_cache and not args.chip_word_copy:
        raise ValueError("--chip-cache requires --chip-word-copy")
    if args.chip_word_copy and not args.chip_library:
        raise ValueError("--chip-word-copy requires --chip-library")
    work, output = ROOT / args.work, ROOT / args.out
    manifest_path = output.with_suffix(".json")
    if work.exists() or output.exists() or manifest_path.exists():
        raise SystemExit("refusing to overwrite build artifacts")
    config = read_json(ROOT / "project.json")
    registry_path = ROOT / "tools/specs/exe45_dialogue_archives_v1.json"
    registry = read_json(registry_path)
    if 'analysis/startup_ui_v1/selected_asset.json' in (args.translations or []) or args.pending_batch500_013:
        from startup_ui import scope as startup_scope
        registry['archives']['70904C']=startup_scope()
        from startup_ui import followup_scopes
        registry['archives'].update(followup_scopes())
    source_path = ROOT / config["source_profile"]["filename"]
    require_hash(source_path, config["source_profile"]["sha256"])
    source = source_path.read_bytes()
    from layout500_inputs_024 import load_inputs
    from layout500_product_024 import compose_primary,append_new_raw,compose_hints,finalize
    inputs024,summary024=load_inputs(source)
    from layout500_inputs_025 import load_inputs as load_inputs025
    from layout500_product_025 import compose_primary as compose_primary025,finalize as finalize025
    inputs025,summary025=load_inputs025(source)
    if not args.field_b0_hints_023:raise ValueError("024 requires full retained023 scope")
    if any(p in (args.translations or []) for p in ['analysis/first_mail_v2/6DD9AC_selected_asset.json','analysis/official_mail_v1/6DD9AC_selected_asset.json','analysis/news_mail_v1/6DD9AC_selected_asset.json']):
        from first_mail import scopes as first_mail_scopes
        mode='news' if 'analysis/news_mail_v1/6DD9AC_selected_asset.json' in (args.translations or []) else 'analysis/official_mail_v1/6DD9AC_selected_asset.json' in (args.translations or [])
        full_header='analysis/full_mail_header_v1_r2/6DD63C_selected_asset.json' in (args.translations or [])
        registry['archives'].update(first_mail_scopes(source,mode,full_header))
    if registry["source_sha256"] != sha(source):
        raise SystemExit("archive registry source mismatch")
    from mission_mail_header import ASSET as mission_asset
    if mission_asset in (args.translations or []):
        from mission_mail_header import scope as mission_scope
        registry['archives']['6DD864']=mission_scope(source)
    catalog = ROOT / config["text_catalog"]["path"]
    require_hash(catalog, config["text_catalog"]["sha256"])
    rows = parse_tpi(catalog)
    batch500=[]
    if args.pending_batch500:
        if not args.full_mail_body or not args.keyitem_rom_translations:raise ValueError('500 clone prerequisites')
        from batch500_rom import entries
        batch500=entries(source)
        for _,_,a,s,_,_ in batch500:
            if a['consumer']=='fixed-cell-big':registry['archives'][a['archive']]=s
    if args.pending_batch500_002:
        if not args.pending_batch500:raise ValueError('Batch002 needs preserved batch001')
        from batch500_002_rom import entries as entries002
        second=entries002(source)
        batch500=[x for x in batch500 if x[2]['archive']!='6E01AC']+second
        for _,_,a,s,_,_ in second:
            if s['standard_relocation']:registry['archives'][a['archive']]=s
    selected, assets = {}, []
    if args.pending_batch500_003:
        if not args.pending_batch500_002:raise ValueError('Batch003 needs preserved002')
        from batch500_003_rom import entries as entries003
        third=entries003(source);batch500+=third
        for _,_,a,s,_,_ in third:
            if s['standard_relocation']:registry['archives'][a['archive']]=s
    if args.pending_batch500_004:
        if not args.pending_batch500_003:raise ValueError('Batch004 needs preserved003')
        from batch500_004_rom import entries as entries004
        fourth=entries004(source);batch500+=fourth
        for _,_,a,s,_,_ in fourth:
            if a['archive'] in registry['archives']:raise ValueError('Batch004 overlaps prior archive scope')
            registry['archives'][a['archive']]=s
    if args.pending_batch500_005:
        if not args.pending_batch500_004:raise ValueError('Batch005 needs preserved004')
        from batch500_005_rom import entries as entries005
        fifth=entries005(source);batch500+=fifth
        for _,_,a,s,_,_ in fifth:
            if a['archive'] in registry['archives']:raise ValueError('Batch005 overlaps prior archive scope')
            registry['archives'][a['archive']]=s
    if args.pending_batch500_006:
        if not args.pending_batch500_005:raise ValueError('Batch006 needs preserved005')
        from batch500_006_rom import entries as entries006
        sixth=entries006(source);batch500+=sixth
        for _,_,a,s,_,_ in sixth:
            if a['archive'] in registry['archives']:raise ValueError('Batch006 overlaps prior archive scope')
            registry['archives'][a['archive']]=s
    from cumulative_batch500 import entries as entries007
    from cumulative_batch500_008 import entries as entries008
    from cumulative_batch500_009 import entries as entries009
    from cumulative_batch500_010 import entries as entries010
    from cumulative_batch500_011 import entries as entries011
    from cumulative_batch500_012 import entries as entries012
    from cumulative_batch500_013 import entries as entries013
    from cumulative_batch500_014 import entries as entries014
    from cumulative_batch500_015 import entries as entries015
    from cumulative_batch500_016 import entries as entries016
    from cumulative_batch500_017 import entries as entries017
    from cumulative_batch500_018 import entries as entries018
    from cumulative_batch500_019 import entries as entries019
    from cumulative_batch500_020 import entries as entries020
    from cumulative_batch500_021 import entries as entries021
    from cumulative_batch500_022 import entries as entries022
    for enabled,prerequisite,entry in [(args.pending_batch500_007,args.pending_batch500_006,entries007),(args.pending_batch500_008,args.pending_batch500_007,entries008),(args.pending_batch500_009,args.pending_batch500_008,entries009),(args.pending_batch500_010,args.pending_batch500_009,entries010),(args.pending_batch500_011,args.pending_batch500_010,entries011),(args.pending_batch500_012,args.pending_batch500_011,entries012),(args.pending_batch500_013,args.pending_batch500_012,entries013),(args.pending_batch500_014,args.pending_batch500_013,entries014),(args.pending_batch500_015,args.pending_batch500_014,entries015),(args.pending_batch500_016,args.pending_batch500_015,entries016),(args.pending_batch500_017,args.pending_batch500_016,entries017),(args.pending_batch500_018,args.pending_batch500_017,entries018),(args.pending_batch500_019,args.pending_batch500_018,entries019),(args.pending_batch500_020,args.pending_batch500_019,entries020),(args.pending_batch500_021,args.pending_batch500_020,entries021),(args.pending_batch500_022,args.pending_batch500_021,entries022)]:
        if not enabled:continue
        if not prerequisite:raise ValueError('Cumulative batch requires previous cohort')
        merged=entry(source);overlap={a['archive'] for _,_,a,_,_,_ in merged}
        # Explicit composition replaces prior writers before final planning.
        for _,_,a,s,pre,_ in merged:
            if pre['parent'] is None:
                if a['archive'] in registry['archives']:raise ValueError('New archive overlaps prior scope')
                registry['archives'][a['archive']]=s
                continue
            parent=read_json(ROOT/pre['parent']['path'])
            old_scope=selected_scope(registry['archives'][a['archive']],parent)
            if any(u not in a['units'] for u in resolve_units(parent)):raise ValueError('007 carry wording lost')
            for u in parent['units']:
                for key in ('consumer','literal_language','max_literal_rows','max_line_advance'):
                    if literal_scope(old_scope,u['id']).get(key)!=literal_scope(s,u['id']).get(key):raise ValueError('007 carry renderer contract changed')
            registry['archives'][a['archive']]=s
        batch500=[x for x in batch500 if x[2]['archive'] not in overlap]+merged
    for name in args.translations or registry["default_translations"]:
        # All selected cohorts are registered before asset processing below.
        path = ROOT / name
        asset = read_json(path)
        archive = asset["archive"]
        if (asset["policy"] != "development-draft; NON-DISTRIBUTION" or asset["source_sha256"] != sha(source)
                or asset["consumer"] not in ("normal-dialogue", "fixed-cell-big", "fixed-cell-mono") or asset["review"]["release_eligible"] is not False
                or archive not in registry["archives"] or archive in selected):
            raise SystemExit("unsupported/duplicate development scope or source profile")
        scope = selected_scope(registry["archives"][archive],asset)
        for _,_,batch_asset,_,_,_ in batch500:
            if batch_asset['archive']==archive and asset!=batch_asset:raise ValueError('500 selected input differs')
        if archive=='6DD864':
            from mission_mail_header import validate as validate_mission
            validate_mission(asset)
        if archive in ('6DD9AC','6DD0B8','6DD63C'):
            from first_mail import validate_selected
            validate_selected(asset)
        validate_numberman_return_decision(asset)
        if archive=='6368E8':
            if asset.get('scope_variant')=='save-initialize-v1':
                if not (args.calendar_presets_poc and args.mono_font_poc):raise ValueError('initialize requires retained UI providers')
                from save_initialize import validate as validate_initialize
                validate_initialize(asset);validate_calendar_menu=None
            elif asset.get('scope_variant')=='calendar-date-save-v1':
                if not (args.calendar_presets_poc and args.mono_font_poc):raise ValueError('date/save requires retained UI providers')
                from calendar_date_save import validate as validate_date_save
                validate_date_save(asset);validate_calendar_menu=None
            elif asset.get('scope_variant')=='input-remaining-v1':
                if not (args.calendar_presets_poc and args.mono_font_poc):raise ValueError('input UI requires preset/mono providers')
                from input_remaining import validate as validate_remaining
                validate_remaining(asset);validate_calendar_menu=None
            elif asset.get('scope_variant')=='input-heading-v1':
                if not (args.calendar_presets_poc and args.mono_font_poc):raise ValueError('heading requires retained preset and mono providers')
                from input_heading import validate as validate_heading
                validate_heading(asset);validate_calendar_menu=None
            elif asset.get('scope_variant')=='input-confirmation-v1':
                if not args.calendar_presets_poc:raise ValueError('confirmation requires retained preset provider')
                from input_confirmation import validate as validate_confirmation
                validate_confirmation(asset);validate_calendar_menu=None
            elif asset.get('scope_variant')=='possessions-statistics-v1':
                if not args.calendar_presets_poc:raise ValueError('statistics requires retained preset provider')
                from possessions_statistics import validate as validate_statistics
                validate_statistics(asset);validate_calendar_menu=None
            elif asset.get('scope_variant')=='frequency-names-v1':
                if not args.calendar_presets_poc:raise ValueError('frequency names require retained preset provider')
                from calendar_frequency_names import validate as validate_frequency_names
                validate_frequency_names(asset);validate_calendar_menu=None
            elif asset.get('scope_variant')=='anniversary-presets-v1':
                if not args.calendar_presets_poc:raise ValueError('anniversary presets require retained logical-cell counter')
                from calendar_anniversary_confirmation import validate as validate_anniversary_presets
                validate_anniversary_presets(asset);validate_calendar_menu=None
            elif asset.get('scope_variant')=='anniversary-labels-v1':
                if not args.calendar_presets_poc:raise ValueError('anniversary labels require retained preset counter PoC')
                from calendar_anniversary_labels import validate_parent as validate_calendar_menu
                validate_calendar_menu(asset)
                validate_calendar_menu=None
            elif asset.get('scope_variant')=='type-presets-poc-v1':
                if not args.calendar_presets_poc:raise ValueError('preset names require explicit local counter PoC')
                from calendar_presets import validate as validate_calendar_menu
            elif asset.get('scope_variant')=='type-labels-v1':
                from calendar_types_model import validate as validate_calendar_menu
            else:
                from calendar_menu_model import validate as validate_calendar_menu
            if validate_calendar_menu is not None:validate_calendar_menu(resolve_units(asset))
        if asset["consumer"] != scope["consumer"]:
            raise SystemExit("translation consumer differs from adopted scope")
        if asset['consumer']=='fixed-cell-mono' and not args.mono_font_poc:
            raise ValueError('mono translation requires explicit mono provider; big-only supply rejected')
        matching = [r for r in rows if r["offset"] == int(archive, 16)]
        if (len(matching) != 1 or matching[0]["compressed"] != scope.get("compressed", False) or matching[0]["pointers"] != scope["pointers"]
                or matching[0]["size"] != scope["source_bytes"]):
            raise SystemExit("adopted archive reference boundary changed")
        selected[archive] = (matching[0], asset, scope)
        assets.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path.read_bytes()), "archive": archive})
        if asset.get('scope_variant')=='calendar-inventory-v1':
            from gutsman_calendar_inventory import validate as validate_inventory
            cursor=validate_inventory(asset)
            assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited54 calendar units'))
            while 'parent_asset' in cursor:
                dependency=cursor['parent_asset'];kind='anniversary' if dependency['carry_units']==15 else 'calendar'
                assets.append(dict(dependency,archive=archive,scope=f'read-only inherited{dependency["carry_units"]} {kind} units'))
                cursor=read_json(ROOT/dependency['path'])
        if asset.get('scope_variant')=='calendar-schedule-delete-v1':
            from gutsman_calendar_schedule_delete import validate as validate_schedule_delete
            cursor=validate_schedule_delete(asset)
            assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited45 calendar units'))
            while 'parent_asset' in cursor:
                dependency=cursor['parent_asset'];kind='anniversary' if dependency['carry_units']==15 else 'calendar'
                assets.append(dict(dependency,archive=archive,scope=f'read-only inherited{dependency["carry_units"]} {kind} units'))
                cursor=read_json(ROOT/dependency['path'])
        if asset.get('scope_variant')=='calendar-management-v1':
            from gutsman_calendar_management import validate as validate_calendar_management
            cursor=validate_calendar_management(asset)
            assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited22 calendar units'))
            while 'parent_asset' in cursor:
                dependency=cursor['parent_asset'];kind='anniversary' if dependency['carry_units']==15 else 'calendar'
                assets.append(dict(dependency,archive=archive,scope=f'read-only inherited{dependency["carry_units"]} {kind} units'))
                cursor=read_json(ROOT/dependency['path'])
        if asset.get('scope_variant')=='calendar-navigation-v1':
            from gutsman_calendar_navigation import validate as validate_calendar_navigation
            inherited=validate_calendar_navigation(asset)
            assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited18 calendar units'))
            assets.append(dict(inherited['parent_asset'],archive=archive,scope='read-only inherited15 anniversary units'))
            cursor=read_json(ROOT/inherited['parent_asset']['path'])
            while 'parent_asset' in cursor:
                dependency=cursor['parent_asset']
                assets.append(dict(dependency,archive=archive,scope=f'read-only inherited{dependency["carry_units"]} calendar units'))
                cursor=read_json(ROOT/dependency['path'])
        if asset.get('scope_variant') in ('frequency-names-v1','possessions-statistics-v1','input-confirmation-v1','input-heading-v1','input-remaining-v1','calendar-date-save-v1','save-initialize-v1'):
            if asset['scope_variant']=='save-initialize-v1':
                from save_initialize import validate as validate_frequency_names,DELTA as INIT_DELTA
                from verify_calendar_date_save_draft import ASSET
                from input_remaining import DELTA
                for authority in (INIT_DELTA,ASSET,DELTA):assets.append(dict(path=authority,sha256=sha((ROOT/authority).read_bytes()),archive=archive,scope='authored initialization UI delta authority'))
            elif asset['scope_variant']=='calendar-date-save-v1':
                from calendar_date_save import validate as validate_frequency_names
                from verify_calendar_date_save_draft import ASSET
                from input_remaining import DELTA
                for authority in (ASSET,DELTA):assets.append(dict(path=authority,sha256=sha((ROOT/authority).read_bytes()),archive=archive,scope='authored UI delta authority'))
            elif asset['scope_variant']=='input-remaining-v1':
                from input_remaining import validate as validate_frequency_names
                from input_remaining import DELTA
                assets.append(dict(path=DELTA,sha256=sha((ROOT/DELTA).read_bytes()),archive=archive,scope='authored input UI delta21 authority'))
            elif asset['scope_variant']=='input-heading-v1':
                from input_heading import validate as validate_frequency_names
            elif asset['scope_variant']=='input-confirmation-v1':
                from input_confirmation import validate as validate_frequency_names
            elif asset['scope_variant']=='possessions-statistics-v1':
                from possessions_statistics import validate as validate_frequency_names
            else:
                from calendar_frequency_names import validate as validate_frequency_names
            cursor=validate_frequency_names(asset)
            assets.append(dict(asset['parent_asset'],archive=archive,scope=f'read-only inherited{len(cursor["units"])} preset units'))
            while 'parent_asset' in cursor:
                dependency=cursor['parent_asset'];kind='anniversary' if dependency['carry_units']==5 else 'preset'
                assets.append(dict(dependency,archive=archive,scope=f'read-only inherited{dependency["carry_units"]} {kind} units'))
                cursor=read_json(ROOT/dependency['path'])
        if asset.get('scope_variant') in ('calendar-anniversary-confirmation-v1','anniversary-presets-v1'):
            from calendar_anniversary_confirmation import validate as validate_anniversary_confirmation
            inherited=validate_anniversary_confirmation(asset)
            assets.append(dict(asset['parent_asset'],archive=archive,scope=f'read-only inherited{len(inherited["units"])} anniversary units'))
            cursor=inherited
            while 'parent_asset' in cursor:
                dependency=cursor['parent_asset'];kind='preset' if archive=='6368E8' else 'calendar'
                assets.append(dict(dependency,archive=archive,scope=f'read-only inherited{dependency["carry_units"]} {kind} units'))
                cursor=read_json(ROOT/dependency['path'])
        if archive=='665698' and asset.get('scope_variant')=='calendar-content-v1':
            from gutsman_calendar_content import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited2 calendar units'))
        if archive=='665698' and asset.get('scope_variant')=='calendar-confirmation-v1':
            from gutsman_calendar_confirmation import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited4 calendar units'))
            prior=read_json(ROOT/asset['parent_asset']['path']);assets.append(dict(prior['parent_asset'],archive=archive,scope='read-only inherited2 calendar units'))
        if archive=='665698' and asset.get('scope_variant')=='calendar-home-v1':
            from gutsman_calendar_home import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited7 calendar units'))
            prior=read_json(ROOT/asset['parent_asset']['path']);assets.append(dict(prior['parent_asset'],archive=archive,scope='read-only inherited4 calendar units'))
            base=read_json(ROOT/prior['parent_asset']['path']);assets.append(dict(base['parent_asset'],archive=archive,scope='read-only inherited2 calendar units'))
        if archive=='665698' and asset.get('scope_variant')=='calendar-register-v1':
            from gutsman_calendar_register import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited10 calendar units'))
            home=read_json(ROOT/asset['parent_asset']['path']);assets.append(dict(home['parent_asset'],archive=archive,scope='read-only inherited7 calendar units'))
            confirmation=read_json(ROOT/home['parent_asset']['path']);assets.append(dict(confirmation['parent_asset'],archive=archive,scope='read-only inherited4 calendar units'))
            content=read_json(ROOT/confirmation['parent_asset']['path']);assets.append(dict(content['parent_asset'],archive=archive,scope='read-only inherited2 calendar units'))
        if archive=='665698' and asset.get('scope_variant')=='calendar-anniversary-v1':
            from gutsman_calendar_anniversary import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited14 calendar units'))
            register=read_json(ROOT/asset['parent_asset']['path']);assets.append(dict(register['parent_asset'],archive=archive,scope='read-only inherited10 calendar units'))
            home=read_json(ROOT/register['parent_asset']['path']);assets.append(dict(home['parent_asset'],archive=archive,scope='read-only inherited7 calendar units'))
            confirmation=read_json(ROOT/home['parent_asset']['path']);assets.append(dict(confirmation['parent_asset'],archive=archive,scope='read-only inherited4 calendar units'))
            content=read_json(ROOT/confirmation['parent_asset']['path']);assets.append(dict(content['parent_asset'],archive=archive,scope='read-only inherited2 calendar units'))
        if archive=='6368E8' and asset.get('scope_variant')=='anniversary-labels-v1':
            from calendar_anniversary_labels import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited4 preset units'))
        if archive=='66A844' and asset.get('scope_variant')=='gutsman-chipquest-v1':
            from gutsman_chipquest_model import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited31 units'))
        if archive=='66651C' and asset.get('scope_variant')=='alarm-followup-v1':
            from gutsman_alarm_followup import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited3 alarm units'))
        if archive=='66651C' and asset.get('scope_variant')=='alarm-meal-v1':
            from gutsman_alarm_meal import validate_parent
            validate_parent(asset);assets.append(dict(asset['parent_asset'],archive=archive,scope='read-only inherited5 alarm units'))
            prior=read_json(ROOT/asset['parent_asset']['path']);assets.append(dict(prior['parent_asset'],archive=archive,scope='read-only inherited3 alarm units'))
    font_profile = config["development_dependencies"]["font"]
    font = ROOT / font_profile["path"]
    require_hash(font, font_profile["sha256"])
    require_hash(ROOT / font_profile["license"], font_profile["license_sha256"])
    asm = config["development_dependencies"]["thumb_assembler"]
    for field in ("python_module", "native_library", "license"):
        require_hash(ROOT / asm[field], asm[field + "_sha256"])
    glyphs = bdf_glyphs(font, {chr(0xAC00 + i) for i in range(HANGUL_COUNT)})
    needed = {ch for _, asset, _ in selected.values() for unit in resolve_units(asset)
              for ch in unit["translation"] if ch in EXTRA_CHARACTER_INDICES}
    if args.full_mail_body:
        from full_mail_body import ASSET,units
        if args.full_mail_body!=ASSET or not args.mail_rom_reader or not args.keyitem_rom_translations or selected.get('6DD9AC',(None,{}))[1].get('scope_variant')!='news-mail-v1':raise ValueError('full mail explicitly selected bounded77 prerequisites')
        full_mail_asset=read_json(ROOT/ASSET)
        if full_mail_asset['units']!=units():raise ValueError('full mail source selection')
        needed.update(ch for u in full_mail_asset['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)
    keyboard_glyphs=None
    if args.pending_batch500_022:
        if not args.pending_batch500_021 or not args.keyitem_rom_translations or not args.mail_rom_reader or not args.full_mail_body:raise ValueError('022 composed reader prerequisites')
        from hint_rom_data import input_entries as hint_entries
        for _,_,hint_asset,_,_,_,_ in hint_entries(source):
            needed.update(ch for u in hint_asset['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)
    if args.hangul_keyboard_glyphs:
        if not args.mono_font_poc:raise ValueError('keyboard glyph candidate requires both fixed-cell providers')
        needed.update(EXTRA_CHARACTER_INDICES)
    for entry024,_ in inputs024:
        asset024=read_json(ROOT/entry024['merged_asset']['path'])
        needed.update(ch for u in asset024['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)
    for entry025,_ in inputs025:
        asset025=read_json(ROOT/entry025['merged_asset']['path'])
        needed.update(ch for u in asset025['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)
    extra_chars = sorted(needed, key=EXTRA_CHARACTER_INDICES.get)
    if [EXTRA_CHARACTER_INDICES[ch] for ch in extra_chars] != list(range(HANGUL_COUNT, HANGUL_COUNT + len(extra_chars))):
        raise SystemExit("extra glyph index supply must be contiguous")
    extras = bdf_glyphs(font, needed, {ch: EXTRA_CHARACTER_METRICS[ch]["vertical_shift"] for ch in needed}) if needed else {}
    normal_extra_records=[extras[ch] for ch in extra_chars]
    if args.hangul_keyboard_glyphs:
        from hangul_editor_display import JAMO_INDICES,JAMO_BASE
        from hangul_composer_thumb import KEYS
        if HANGUL_COUNT+len(normal_extra_records)!=JAMO_BASE:raise ValueError('keyboard mapping supply gap')
        normal_jamo=bdf_glyphs(font,set(KEYS));normal_jamo_bank=b''.join(normal_jamo[ch] for ch in KEYS)
        normal_extra_records.extend(normal_jamo[ch] for ch in KEYS)
        keyboard_glyphs=dict(mapping=JAMO_INDICES,comma_index=EXTRA_CHARACTER_INDICES[','],normal_bank_sha256=sha(normal_jamo_bank),normal_jamo_bytes=len(normal_jamo_bank),input_hooks_installed=False,runtime='pending glyph selection/load/consumption',policy='development glyph supply only; NON-DISTRIBUTION')
    work.mkdir(parents=True)
    plugin = prepare_plugins(work / "plugins", needed)
    common = command(work / "plugins")
    archive_blob, products, records = bytearray(), {}, []
    for archive, (row, asset, scope) in sorted(selected.items()):
        payload, record = compile_archive(source, row, asset, scope, common, work / "plugins", work / archive)
        for _,_,batch_asset,_,pre,_ in batch500:
            if batch_asset['archive']==archive and sha(payload)!=pre['compiled_sha256']:raise ValueError('500 header preflight mismatch')
        payload,record=compose_primary(archive,payload,record,inputs024,work/'plugins')
        payload,record=compose_primary025(archive,payload,record,inputs025,work/'plugins')
        stored = payload
        if row["compressed"]:
            if scope["compression"] != "BIOS type-10 literal-only, 4-byte aligned, zero-padded":
                raise ValueError("unsupported compressed reinsertion policy")
            bounded_destinations=scope.get('source_extent_only_destinations')
            if bounded_destinations is not None:
                from keyitem_empty import DESTINATIONS
                if archive!='709408' or bounded_destinations!=DESTINATIONS or scope['max_payload_bytes']!=1291 or not record['native_storage_sharing']['no_destination_growth']:
                    raise ValueError('unregistered source-extent-only consumers')
            elif scope["decompression_destination"] + scope["max_payload_bytes"] > scope["next_scene_asset"]:
                raise ValueError("decompression cap overlaps the next scene asset")
            stored = encode_lz10(payload, limit=scope["max_payload_bytes"])
            independent, consumed = lz77_decompress(stored, 0)
            if decode_lz10(stored, limit=scope["max_payload_bytes"]) != payload or independent != payload:
                raise ValueError("compressed payload independent roundtrip failed")
            record["compression"] = {"method": scope["compression"], "stored_bytes": len(stored),
                "stored_sha256": sha(stored), "consumed_bytes": consumed, "self_roundtrip": True,
                "independent_decoder_roundtrip": True, "destination": scope.get("decompression_destination"),"source_extent_only_destinations":bounded_destinations,
                "development_size_cap": scope["max_payload_bytes"], "runtime_compatibility": "pending"}
        archive_blob.extend(b"\xFF" * (-len(archive_blob) % 4))
        offset = len(source) + len(archive_blob)
        archive_blob.extend(stored)
        products[row["offset"]] = (offset, stored, payload)
        record.update({"rom_offset": offset, "pointers": row["pointers"]})
        records.append(record)
    append_new_raw(source,archive_blob,products,records,selected,inputs024,work/'plugins')
    folder_labels=None
    if args.equipment_labels and not args.folder_labels:raise ValueError('equipment labels require folder-labels')
    if args.folder_labels:
        if not args.pet_menu_graphics or not args.chip_folder:raise ValueError('folder labels require adopted PET typography and folder path')
        path=ROOT/('translations/equipment_labels_ko.json' if args.equipment_labels else 'translations/folder_header_ko.json');asset=read_json(path)
        equipment_scope=EQUIPMENT_SCOPE
        if args.equipment_weapons:
            from equipment_weapons import merge,SCOPE as WEAPON_SCOPE
            weapon_path=ROOT/'translations/equipment_weapons_ko.json'
            asset=merge(asset,read_json(weapon_path));equipment_scope=WEAPON_SCOPE
            assets.append({'path':str(weapon_path.relative_to(ROOT)),'sha256':sha(weapon_path.read_bytes()),'archive':asset['archive'],'scope':'additional33 common equipment weapon drafts; originals and other scripts protected'})
        if args.equipment_labels:
            prior=resolve_units(read_json(ROOT/'translations/folder_header_ko.json'))
            carry=[u for u in resolve_units(asset) if u['id']=='6E2B9C:1:0']
            if len(carry)!=1 or any(carry[0][k]!=prior[0][k] for k in ['id','source','translation','state']):raise ValueError('equipment clone must preserve prior header wording')
        row=next(r for r in rows if r['offset']==0x6E2B9C)
        if row['size']!=634 or row['pointers']!=[0x3C5E8] or not row['compressed']:raise ValueError('folder header source inventory')
        native_path=validate_header_path(source)
        equipment_path=validate_equipment_labels(source) if args.equipment_labels else None
        payload,record=compile_archive(source,row,asset,equipment_scope if args.equipment_labels else HEADER_SCOPE,common,work/'plugins',work/'folder_header_clone')
        archive_blob.extend(b'\xff'*(-len(archive_blob)%4));offset=len(source)+len(archive_blob);archive_blob.extend(payload)
        record.update(rom_offset=offset,source_archive_pointers_unchanged=True,native_path=native_path,
            asset_sha256=sha(path.read_bytes()),policy='private uncompressed ROM clone, no enlarged RAM decompression')
        folder_labels={'header':record}
        if equipment_path:folder_labels['equipment']=equipment_path
        if args.equipment_weapons:folder_labels['weapons']={'new_units':33,'scripts':list(range(5,38)),'asset_sha256':sha(weapon_path.read_bytes()),'runtime':'pending exact-ROM selection and pixels'}
        assets.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes()),'archive':asset['archive'],'scope':'isolated header and common equipment fixed-text clone' if args.equipment_labels else 'isolated folder header clone only; original compressed archive and Navi RAM pools unchanged'})
    equipment_guides=None
    if args.roll_equipment_guides and not args.equipment_guides:raise ValueError('Roll guides require equipment guides')
    if args.equipment_guides:
        if not args.equipment_labels:raise ValueError('equipment guides require equipment labels')
        path=ROOT/'translations/rockman_equipment_guides_ko.json';asset=read_json(path)
        row=next(r for r in rows if r['offset']==0x6E1068)
        if row['size']!=GUIDE_SCOPE['source_bytes'] or row['pointers']!=GUIDE_SCOPE['pointers'] or not row['compressed']:raise ValueError('guide native archive inventory')
        payload,record=compile_archive(source,row,asset,GUIDE_SCOPE,common,work/'plugins',work/'equipment_guides_clone')
        archive_blob.extend(b'\xff'*(-len(archive_blob)%4));offset=len(source)+len(archive_blob);archive_blob.extend(payload)
        record.update(rom_offset=offset,asset_sha256=sha(path.read_bytes()))
        equipment_guides={'archive':record}
        assets.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes()),'archive':asset['archive'],'scope':'private Rockman guide ROM clone; original Navi RAM/pointers retained'})
        if args.roll_equipment_guides:
            path=ROOT/'translations/roll_equipment_guides_ko.json';asset=read_json(path)
            scope=dict(GUIDE_SCOPE,source_bytes=631,pointers=[0x3C5C0])
            row=next(r for r in rows if r['offset']==0x6E12DC)
            if row['size']!=scope['source_bytes'] or row['pointers']!=scope['pointers'] or not row['compressed']:raise ValueError('Roll guide inventory')
            if (asset['archive']!='6E12DC' or asset['source_sha256']!=sha(source) or asset['consumer']!='normal-dialogue'
                    or asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['review']['release_eligible'] is not False):raise ValueError('Roll guide source/consumer/policy')
            payload,record=compile_archive(source,row,asset,scope,common,work/'plugins',work/'roll_equipment_guides_clone')
            archive_blob.extend(b'\xff'*(-len(archive_blob)%4));offset=len(source)+len(archive_blob);archive_blob.extend(payload)
            record.update(rom_offset=offset,asset_sha256=sha(path.read_bytes()))
            equipment_guides['roll_archive']=record
            assets.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes()),'archive':asset['archive'],'scope':'private Navi1 guide ROM clone only; original source pool and Navi loader unchanged'})
    spec_path = ROOT / "tools/specs/exe45_dialogue_extension_v1.json"
    appended, patches, extension = construct(source, read_json(spec_path), bytes(archive_blob), glyphs,
                                             normal_extra_records)
    startup_renderer=None
    startup_welcome=None
    startup_footer=None
    if '70904C' in selected:
        from startup_ui import construct as construct_startup
        appended,new_patches,startup_renderer=construct_startup(source,appended,extension)
        patches.extend(new_patches)
        from startup_welcome_graphics import construct as construct_welcome
        welcome_path=ROOT/'translations/startup_welcome_graphics_ko.json'
        appended,welcome_patches,startup_welcome=construct_welcome(source,read_json(welcome_path),appended)
        patches.extend(welcome_patches)
        assets.append(dict(path=str(welcome_path.relative_to(ROOT)),sha256=sha(welcome_path.read_bytes()),scope='initial PET welcome bitmap'))
        from startup_footer_graphics import construct as construct_footer
        footer_path=ROOT/'translations/startup_footer_graphics_ko.json'
        footer_bytes,startup_footer=construct_footer(source,read_json(footer_path))
        patches.append((startup_footer['source_offset'],footer_bytes,'native date-input OBJ Korean button descriptions'))
        assets.append(dict(path=str(footer_path.relative_to(ROOT)),sha256=sha(footer_path.read_bytes()),scope='date-input native OBJ footer labels'))
    native_keyboard_labels=None
    if args.native_keyboard_labels:
        from native_keyboard_labels import construct as construct_keyboard_labels
        keyboard_label_path=ROOT/'translations/native_keyboard_labels_ko.json'
        label_patches,native_keyboard_labels=construct_keyboard_labels(source,read_json(keyboard_label_path))
        patches.extend(label_patches)
        assets.append(dict(path=str(keyboard_label_path.relative_to(ROOT)),sha256=sha(keyboard_label_path.read_bytes()),scope='native kana three-page command graphics only'))
    navi_card_graphics=None
    if args.navi_card_graphics:
        from navi_card_graphics import construct as construct_navi_cards
        card_path=ROOT/'translations/navi_card_graphics_ko.json'
        card_bytes,navi_card_graphics=construct_navi_cards(source,read_json(card_path))
        patches.append((navi_card_graphics['source_offset'],card_bytes,'native Navi card-name OBJ bank'))
        assets.append(dict(path=str(card_path.relative_to(ROOT)),sha256=sha(card_path.read_bytes()),scope='21 native Navi card-name graphics'))
    fixed_extension = None
    if any(scope["consumer"] in ("fixed-cell-big", "fixed-cell-mono") for _, _, scope in selected.values()):
        if args.fixedcell_visibility:
            raise ValueError("real fixed-cell translations cannot use temporary Japanese glyph replacements")
        fixed_spec_path = ROOT / "tools/specs/exe45_fixedcell_extension_v1.json"
        fixed_spec = read_json(fixed_spec_path)
        profile_path = ROOT / fixed_spec["font_profile"]
        profile = read_json(profile_path)
        for field in ("path", "license"):
            require_hash(ROOT / profile["font"][field], profile["font"]["sha256" if field == "path" else "license_sha256"])
        cells = bdf_cells(ROOT / profile["font"]["path"], {chr(0xAC00 + i) for i in range(HANGUL_COUNT)}, profile["raster"])
        mono_cells,mono_spec=None,None
        if args.mono_font_poc:
            mono_path=ROOT/'tools/specs/exe45_fixedcell_mono_v1.json'
            mono_spec=read_json(mono_path)
            mono_profile=dict(profile['raster'],**mono_spec['roles'])
            mono_cells=bdf_cells(ROOT/profile['font']['path'],set(cells),mono_profile)
        big_extras,mono_extras=[],[]
        if args.hangul_keyboard_glyphs:
            order=tuple(extra_chars)+KEYS
            big_extra=bdf_cells(ROOT/profile['font']['path'],set(order),profile['raster'])
            mono_extra=bdf_cells(ROOT/profile['font']['path'],set(order),mono_profile)
            big_extras=[big_extra[ch] for ch in order];mono_extras=[mono_extra[ch] for ch in order]
            keyboard_glyphs.update(fixed_order=list(order),big_extras_sha256=sha(b''.join(big_extras)),mono_extras_sha256=sha(b''.join(mono_extras)),fixed_extra_bytes=len(order)*64)
        appended, fixed_patches, fixed_extension = construct_fixedcell(source, fixed_spec, appended, cells,
            mono_cells=mono_cells,mono_spec=mono_spec,extra_cells=big_extras,mono_extra_cells=mono_extras)
        patches.extend(fixed_patches)
        fixed_extension.update({"spec_sha256": sha(fixed_spec_path.read_bytes()), "font_profile_sha256": sha(profile_path.read_bytes()),
                                "font": profile["font"], "raster": profile["raster"]})
        if mono_spec is not None:
            fixed_extension['mono_provider'].update(spec_sha256=sha(mono_path.read_bytes()),
                spec_path=str(mono_path.relative_to(ROOT)),raster=mono_profile,font=profile['font'])
    if args.mono_font_poc and fixed_extension is None:
        raise ValueError('--mono-font-poc requires adopted real fixed-cell translations/font')
    if args.hangul_keyboard_glyphs and fixed_extension is None:raise ValueError('keyboard fixed-cell supply missing')
    chip_extension = None
    folder_extension = None
    battle_extension = None
    if args.chip_library:
        if fixed_extension is None or "6D9EC0" not in selected or args.fixedcell_visibility:
            raise ValueError("chip-name development path requires real library headers/font")
        chip_spec_path = ROOT / "tools/specs/exe45_chip_library_v1.json"
        chip_asset_path = ROOT / (args.chip_name_translations or "translations/library_chip_names_ko.json")
        if not chip_asset_path.resolve().is_relative_to((ROOT / 'translations').resolve()):
            raise ValueError('chip-name asset must stay inside project translations')
        chip_spec, chip_asset = read_json(chip_spec_path), read_json(chip_asset_path)
        native_table_path = ROOT / config["textpet"]["plugins"] / "exe45-utf8.tbl"
        require_hash(native_table_path, config["textpet"]["plugin_sha256"][native_table_path.name])
        native_table = {int(k, 16): v for line in native_table_path.read_text(encoding="utf-8-sig").splitlines()
                        if "=" in line for k, v in [line.split("=", 1)] if len(k) == 2}
        clone, clone_record = compile_clone(source, chip_spec, chip_asset, native_table)
        secondary_clone=None;secondary_record=None
        if args.chip_secondary_name_translations:
            secondary_path=ROOT/args.chip_secondary_name_translations
            if not secondary_path.resolve().is_relative_to((ROOT/'translations').resolve()):raise ValueError('secondary asset outside translations')
            secondary_asset=read_json(secondary_path)
            secondary_spec_path=ROOT/'tools/specs/exe45_secondary_name_clone_v1.json'
            secondary_spec=read_json(secondary_spec_path)
            secondary_clone,secondary_record=compile_clone(source,secondary_spec,secondary_asset,native_table)
        appended, chip_patches, chip_extension = construct_chip_library(source, chip_spec, appended, clone,
                                                                         fixed_extension["font_offset"], args.chip_word_copy, args.chip_cache, args.chip_burst_copy, args.chip_fast_copy, args.chip_stack_renderer, args.chip_library_late_wait,secondary_clone=secondary_clone)
        if args.chip_word_copy:
            chip_extension["copy_policy"] = "experimental-inline-16-words"
            chip_extension['copy_variant'] = '6+6+4' if args.chip_burst_copy else '2x8'
            if args.chip_fast_copy:
                chip_extension['copy_policy'] = 'experimental-native-fast-bios-16-words'
                chip_extension['copy_variant'] = 'native-0800097C'
        patches.extend(chip_patches)
        chip_extension.update({"spec_sha256": sha(chip_spec_path.read_bytes()), "clone": clone_record,
                               "translated_units": len(clone_record["units"])})
        assets.append({"path": str(chip_asset_path.relative_to(ROOT)), "sha256": sha(chip_asset_path.read_bytes()),
                       "archive": chip_asset["archive"], "scope": "private library clone; source pointers unchanged"})
        if args.chip_folder:
            folder_spec_path = ROOT / 'tools/specs/exe45_chip_folder_v1.json'
            folder_spec = read_json(folder_spec_path)
            appended, folder_patches, folder_extension = construct_chip_library(source,folder_spec,appended,clone,
                fixed_extension['font_offset'],word_copy=True,cache=True,burst_copy=True,owner_guard=args.chip_folder_owner_guard,secondary_clone=secondary_clone)
            patches.extend(folder_patches)
            folder_extension.update({'spec_path':str(folder_spec_path.relative_to(ROOT)),
                'spec_sha256':sha(folder_spec_path.read_bytes()),'clone':clone_record,
                'copy_policy':'experimental-inline-16-words','copy_variant':'6+6+4',
                'translated_units_reused':len(clone_record['units']),
                'wording_source':str(chip_asset_path.relative_to(ROOT)),
                'policy':'experimental guarded folder reuse of explicitly selected unapproved library-name drafts; NON-DISTRIBUTION'})
            assets[-1]['scope']='private library and experimental folder clones; source pointers unchanged; wording counted once'
        if args.chip_battle_names:
            battle_spec_path=ROOT/'tools/specs/exe45_chip_battle_names_v1.json'
            battle_spec=read_json(battle_spec_path)
            if any(fixed_extension['raster'][k]!=v for k,v in battle_spec['roles'].items()):
                raise ValueError('battle name native palette roles do not match selected Hangul bank')
            ids={int(u['id'].split(':')[1]) for u in resolve_units(chip_asset)}
            appended,battle_patches,battle_extension=construct_battle_names(source,battle_spec,appended,chip_extension['clone_offset'],ids)
            patches.extend(battle_patches)
            battle_extension.update(spec_path=str(battle_spec_path.relative_to(ROOT)),spec_sha256=sha(battle_spec_path.read_bytes()),
                font_offset=fixed_extension['font_offset'],font=fixed_extension['font'],raster=fixed_extension['raster'],
                wording_source=str(chip_asset_path.relative_to(ROOT)),wording_sha256=sha(chip_asset_path.read_bytes()),translated_units_reused=len(ids))
            assets[-1]['scope']+='; caller-gated native8x1 battle name reuse; wording counted once'
        if secondary_record is not None:
            chip_extension['secondary_clone']=secondary_record
            chip_extension['secondary_spec_sha256']=sha(secondary_spec_path.read_bytes())
            if folder_extension is not None:folder_extension['secondary_clone']=secondary_record
            assets.append({'path':str(secondary_path.relative_to(ROOT)),'sha256':sha(secondary_path.read_bytes()),'archive':'765B18','scope':'guarded library/folder secondary clone only; source pointers and secondary battle names native'})
    visibility = None
    if args.fixedcell_visibility:
        candidate_path = ROOT / "tools/specs/exe45_fixedcell_visibility_v1.json"
        candidate = read_json(candidate_path)
        if candidate["policy"] != "functional-poc; NON-DISTRIBUTION" or candidate["source_sha256"] != sha(source):
            raise ValueError("fixed-cell visibility policy/source mismatch")
        cell = candidate["cell"]
        if (cell["width"], cell["height"], cell["bytes"]) != (8, 16, 64):
            raise ValueError("native fixed-cell representation changed")
        candidate_font = candidate["font"]
        for field in ("path", "license"):
            require_hash(ROOT / candidate_font[field], candidate_font["sha256" if field == "path" else "license_sha256"])
        mapping = candidate["temporary_reassignments"]
        cells = bdf_cells(ROOT / candidate_font["path"], {row["display"] for row in mapping}, candidate["raster"])
        replacements = []
        for row in mapping:
            offset = candidate["font_base"] + row["index"] * cell["bytes"]
            if sha(source[offset:offset + cell["bytes"]]) != row["source_glyph_sha256"]:
                raise ValueError("source visibility glyph changed")
            patches.append((offset, cells[row["display"]], "TEMPORARY fixed-cell visibility: " + row["source"] + " -> " + row["display"]))
            replacements.append({**row, "rom_offset": offset, "final_glyph_sha256": sha(cells[row["display"]])})
        visibility = {"policy": candidate["policy"], "spec_path": str(candidate_path.relative_to(ROOT)),
                      "spec_sha256": sha(candidate_path.read_bytes()), "font": candidate_font,
                      "raster": candidate["raster"], "replacements": replacements,
                      "limits": candidate["limitations"], "runtime": "pending"}
    for row, _, _ in selected.values():
        for pointer in row["pointers"]:
            if source[pointer:pointer + 4] != (0x08000000 + row["offset"]).to_bytes(4, "little"):
                raise SystemExit("source archive pointer changed")
            patches.append((pointer, (0x08000000 + products[row["offset"]][0]).to_bytes(4, "little"),
                            f"archive {row['offset']:X} relocation"))
    title_menu=None
    if args.title_menu_graphics or args.title_weekend_menu:
        from title_menu_graphics import construct as construct_title_menu
        title_menu_path=ROOT/('translations/title_menu_weekend_graphics_ko.json' if args.title_weekend_menu else 'translations/title_menu_graphics_ko.json')
        block,title_menu=construct_title_menu(source,read_json(title_menu_path))
        title_menu['asset_sha256']=sha(title_menu_path.read_bytes())
        patches.append((title_menu['source_offset'],block,'title menu same-slot Hangul graphics'))
    pet_graphics=None
    save_title=None
    if args.save_title_graphics:
        if not args.pet_menu_graphics:raise ValueError('save title requires adopted project pixel font')
        from save_title_graphics import construct as construct_save_title
        title_path=ROOT/'translations/save_title_graphics_ko.json'
        block,save_title=construct_save_title(source,read_json(title_path));save_title['asset_sha256']=sha(title_path.read_bytes())
        patches.append((save_title['source_offset'],block,'save top title Hangul typography'))
    if args.pet_menu_graphics:
        pet_asset_path=ROOT/'translations/pet_menu_graphics_ko.json'
        pet_block,pet_graphics=construct_pet_graphics(source,read_json(pet_asset_path))
        patches.append((pet_graphics['source_offset'],pet_block,'PET menu Hangul graphic labels'))
        pet_graphics['asset_sha256']=sha(pet_asset_path.read_bytes())
    if folder_labels is not None:
        if fixed_extension is None:raise ValueError('folder header requires real big font')
        title_block,title_record=construct_equipment_title(source,read_json(ROOT/'translations/pet_menu_graphics_ko.json'))
        patches.append((title_record['source_offset'],title_block,'equipment top title Hangul typography'))
        patches.append((HEADER_ROOT,(0x08000000+folder_labels['header']['rom_offset']).to_bytes(4,'little'),'isolated chip-folder header ROM clone root'))
        if args.equipment_labels:
            for root in EQUIPMENT_ROOTS:patches.append((root,(0x08000000+folder_labels['header']['rom_offset']).to_bytes(4,'little'),'shared equipment fixed-text ROM clone root'))
            patches.append((EQUIPMENT_HEADER_WIDTH,bytes([12]),'equipment title clear all12 native OBJ cells'))
        folder_labels['title']=title_record
    if equipment_guides is not None:
        appended,guide_patches,guide_hook=construct_equipment_guides(source,appended,equipment_guides['archive']['rom_offset'],equipment_guides.get('roll_archive',{}).get('rom_offset'))
        patches.extend(guide_patches);equipment_guides['selector']=guide_hook
    dialogue_chip_name=None
    if args.gutsman_dialogue_chip_name and not args.roll_dialogue_chip_name:raise ValueError('Guts name requires retained Roll selector')
    if args.roll_dialogue_chip_name:
        if 0x664E28 not in products or not args.chip_name_translations:raise ValueError('Roll dialogue name requires adopted Roll archive and chip wording input')
        from dialogue_chip_name import construct as construct_dialogue_chip_name
        at,_,payload=products[0x664E28];span=__import__('archive_scripts').script_spans(payload,255)[13]
        ar={'rom_offset':at,'script13_offset':int.from_bytes(payload[26:28],'little'),'script13_prefix_hex':span[:21].hex()}
        wording_path=ROOT/args.chip_name_translations
        guts=None
        if args.gutsman_dialogue_chip_name:
            if 0x66A844 not in products or selected['66A844'][1].get('scope_variant')!='gutsman-chipquest-v1':raise ValueError('Guts name requires adopted complete talk asset')
            from gutsman_chipquest_model import encoded_prefix
            gat,_,gp=products[0x66A844];gs=__import__('archive_scripts').script_spans(gp,255)[13];prefix=encoded_prefix()
            if not gs.startswith(prefix+bytes.fromhex('f9006801')):raise ValueError('Guts compiled printChip anchor')
            guts=0x08000000+gat+int.from_bytes(gp[26:28],'little')+len(prefix)
        appended,name_patches,dialogue_chip_name=construct_dialogue_chip_name(source,appended,ar,read_json(wording_path),guts_command=guts);patches.extend(name_patches)
        dialogue_chip_name['wording_asset_path']=str(wording_path.relative_to(ROOT));dialogue_chip_name['wording_asset_sha256']=sha(wording_path.read_bytes())
    attack_caption=None
    if args.equipment_attack_caption:
        from attack_caption import construct as caption_construct
        caption_path=ROOT/'translations/equipment_attack_caption_ko.json'
        caption_stored,_,attack_caption=caption_construct(source,read_json(caption_path))
        patches.append((attack_caption['source_offset'],caption_stored,'original-slot compressed buster attack Korean caption'))
        attack_caption['asset_sha256']=sha(caption_path.read_bytes())
        assets.append({'path':str(caption_path.relative_to(ROOT)),'sha256':sha(caption_path.read_bytes()),'scope':'single equipment caption graphic, text count unchanged'})
    calendar_frequency_graphics=None
    if args.calendar_frequency_graphics:
        from calendar_frequency_graphics import construct as frequency_construct
        frequency_path=ROOT/'translations/calendar_frequency_graphics_ko.json'
        frequency_stored,_,calendar_frequency_graphics=frequency_construct(source,read_json(frequency_path))
        patches.append((calendar_frequency_graphics['source_offset'],frequency_stored,'same-slot five calendar frequency Korean OBJ labels'))
        calendar_frequency_graphics['asset_sha256']=sha(frequency_path.read_bytes())
        assets.append({'path':str(frequency_path.relative_to(ROOT)),'sha256':sha(frequency_path.read_bytes()),'scope':'five calendar frequency graphics; text units unchanged'})
    calendar_presets=None
    if args.calendar_presets_poc:
        if '6368E8' not in selected or selected['6368E8'][1].get('scope_variant') not in ('type-presets-poc-v1','anniversary-labels-v1','anniversary-presets-v1','frequency-names-v1','possessions-statistics-v1','input-confirmation-v1','input-heading-v1','input-remaining-v1','calendar-date-save-v1','save-initialize-v1'):raise ValueError('preset PoC requires exact registered names asset or anniversary child')
        from calendar_presets import construct as construct_presets
        appended,preset_patches,calendar_presets=construct_presets(source,appended);patches.extend(preset_patches)
    keyitem_rom=None
    if args.mail_rom_reader and (not args.keyitem_rom_translations or '6DD9AC' not in selected):raise ValueError('mail ROM reader requires composed keyitem selector and selected bounded mail')
    if args.keyitem_rom_translations:
        if '709408' not in selected:raise ValueError('keyitem ROM clone requires retained bounded archive')
        from keyitem_rom_data import SCOPE as KEY_SCOPE,validate_input,install as install_keyitem
        path=ROOT/args.keyitem_rom_translations;asset=read_json(path);validate_input(source,asset)
        row=selected['709408'][0]
        payload,record=compile_archive(source,row,asset,KEY_SCOPE,common,work/'plugins',work/'keyitem_rom_clone')
        active=products[0x709408][2]
        mail_payload=products[0x6DD9AC][2] if args.mail_rom_reader else None
        mail_header=mail_payload[:16] if mail_payload is not None else None
        mail_record=None
        mission_payloads=[]
        equipment_payloads=[]
        for draft,brow,basset,bscope,pre,native in batch500:
            if basset['consumer']=='fixed-cell-big' or bscope.get('standard_relocation'):continue
            raw,r=compile_archive(source,brow,basset,bscope,common,work/'plugins',work/('batch500_'+basset['archive']))
            if sha(raw)!=pre['compiled_sha256'] or len(raw)!=pre['compiled_bytes']:raise ValueError('500 raw preflight mismatch')
            r['script_count']=pre['script_count']
            if 'equipment_navi_index' in bscope:equipment_payloads.append((raw,native,r,bscope['equipment_navi_index']))
            else:mission_payloads.append((raw,native[:16],r))
            assets.append(dict(path=draft,sha256=sha((ROOT/draft).read_bytes()),archive=basset['archive'],scope='pending500 raw-ROM clone; native RAM copy unchanged; dynamic/reward runtime review pending'))
        if args.full_mail_body:
            from full_mail_body import SCOPE as MAIL_SCOPE,NAME_RANGES
            mail_payload,mail_record=compile_archive(source,selected['6DD9AC'][0],full_mail_asset,dict(MAIL_SCOPE,full_mail_raw_rom=True),common,work/'plugins',work/'full_mail_rom_clone')
            assets.append(dict(path=args.full_mail_body,sha256=sha((ROOT/args.full_mail_body).read_bytes()),archive='6DD9AC',scope='full120 raw-ROM clone; existing77 counted once; new43 selected'))
        hint_payloads=None
        if args.pending_batch500_022:
            from hint_rom_data import compile_inputs as compile_hints,MANIFEST as HINT_MANIFEST
            hint_payloads=compile_hints(source,common,work/'plugins',work/'hint_rom_clones')
            hint_payloads=compose_hints(hint_payloads,inputs024,work/'plugins')
            assets.append(dict(path=HINT_MANIFEST,sha256=sha((ROOT/HINT_MANIFEST).read_bytes()),scope='022 guarded hint ROM clone inputs'))
        b0_payloads=None
        if args.field_b0_hints_023:
            from field_b0_rom_data import compile_inputs as compile_b0,MANIFEST as B0_MANIFEST
            b0_payloads=compile_b0(source,common,work/'plugins',work/'b0_hint_rom_clones')
            assets.append(dict(path=B0_MANIFEST,sha256=sha((ROOT/B0_MANIFEST).read_bytes()),scope='023 guarded B0 hint clone inputs'))
        appended,key_patches,keyitem_rom=install_keyitem(source,appended,payload,active[:16],record,mail_payload,mail_header,mail_record,mission_payloads,equipment_payloads,hint_payloads,b0_payloads)
        patches.extend(key_patches)
        assets.append(dict(path=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes()),archive='709408',scope='full39 raw-ROM clone; existing empty unit counted once'))
    target, allowed, writes = bytearray(source + appended), bytearray(len(source)), []
    if len(target) > 0x02000000:
        raise SystemExit("linear GBA ROM address span exceeded")
    for offset, final, writer in sorted(patches):
        if not 0 <= offset <= len(source) - len(final) or any(allowed[offset:offset + len(final)]):
            raise SystemExit("planned patch bounds or overlap violation")
        expected = source[offset:offset + len(final)]
        if target[offset:offset + len(final)] != expected:
            raise SystemExit("expected-byte mismatch")
        target[offset:offset + len(final)] = final
        allowed[offset:offset + len(final)] = b"\x01" * len(final)
        writes.append({"offset": offset, "bytes": len(final), "writer": writer,
                       "expected_hex": expected.hex(), "final_hex": final.hex()})
    if any(a != b and not allowed[i] for i, (a, b) in enumerate(zip(source, target))):
        raise SystemExit("unexplained source-extent write")
    if target[:0xC0] != source[:0xC0]:
        raise SystemExit("GBA header changed")
    preserved = 0
    for entry in rows:
        if entry["offset"] in products:
            dest, stored, payload = products[entry["offset"]]
            for pointer in entry["pointers"]:
                at = int.from_bytes(target[pointer:pointer + 4], "little") - 0x08000000
                if at != dest or target[at:at + len(stored)] != stored:
                    raise SystemExit("relocated payload reference mismatch")
            if entry["compressed"] and lz77_decompress(target, dest)[0] != payload:
                raise SystemExit("final ROM compressed payload mismatch")
        else:
            if payload_of(source, entry) != payload_of(target, entry):
                raise SystemExit("unmodified catalog payload changed")
            for pointer in entry["pointers"]:
                if source[pointer:pointer + 4] != target[pointer:pointer + 4]:
                    raise SystemExit("unmodified catalog pointer changed")
            preserved += 1
    if keyitem_rom is not None:
        from keyitem_rom_data_024 import verify_final
        keyitem_rom['final_placement_verified']=verify_final(source,target,keyitem_rom)
    if keyboard_glyphs is not None:
        normal_at=extension['normal_font_offset']+(442+JAMO_BASE)*96
        big_at=fixed_extension['font_offset']+HANGUL_COUNT*64
        mono_at=fixed_extension['mono_provider']['font_offset']+HANGUL_COUNT*64
        if sha(target[normal_at:normal_at+40*96])!=keyboard_glyphs['normal_bank_sha256'] or sha(target[big_at:big_at+len(big_extras)*64])!=keyboard_glyphs['big_extras_sha256'] or sha(target[mono_at:mono_at+len(mono_extras)*64])!=keyboard_glyphs['mono_extras_sha256']:raise ValueError('final keyboard glyph placement')
        keyboard_glyphs.update(normal_jamo_offset=normal_at,big_extra_offset=big_at,mono_extra_offset=mono_at,final_placement_verified=True)
    result = {
        "schema": 2, "policy": "development-draft; NON-DISTRIBUTION", "source_sha256": sha(source),
        "build_argument_manifest":argument_manifest,
        "output_sha256": sha(target), "output_bytes": len(target), "translation_assets": assets,
        "translated_units": sum(r["translated_units"] for r in records), "archives": records,
        "unchanged_archives": preserved, "final_diff_audited": True, "header_unchanged": True,
        "expected_writes": writes, "append_sha256": sha(appended), "append_bytes": len(appended),
        "plugin": plugin, "font": font_profile, "spec_sha256": sha(spec_path.read_bytes()),
        "archive_registry_sha256": sha(registry_path.read_bytes()), "extension": extension,
        "startup_renderer": startup_renderer,
        "startup_welcome": startup_welcome,
        "startup_footer": startup_footer,
        "native_keyboard_labels": native_keyboard_labels,
        "navi_card_graphics": navi_card_graphics,
        "extra_glyph_metrics": {ch: EXTRA_CHARACTER_METRICS[ch] for ch in extra_chars},
        "build_tools_sha256": {p.name: sha(p.read_bytes()) for p in sorted((ROOT / "tools").glob("*.py"))},
        "runtime": "pending; use a report bound to this exact output hash",
        "limits": ["runtime verification and human wording review remain per-scene requirements",
                   "fixed-cell menu labels, battle, name-entry, and graphic-text consumers unimplemented",
                   "all unselected dialogue remains Japanese; not a release candidate"],
    }
    if keyitem_rom is not None:
        result['keyitem_rom']=keyitem_rom
    if keyboard_glyphs is not None:
        result['hangul_keyboard_glyphs']=keyboard_glyphs
        result['limits'].append('Jamo glyph supply only; keyboard selection/state/display/save hooks not installed; runtime glyph reachability pending.')
    if keyitem_rom is not None:
        result['translated_units']+=keyitem_rom['archive']['translated_units']-1
        mail=keyitem_rom.get('mail_rom_reader',{})
        if mail.get('archive'):result['translated_units']+=mail['archive']['translated_units']-77
        result['translated_units']+=sum(r['translated_units'] for r in keyitem_rom.get('mission_mail_archives',[]))
        result['translated_units']+=sum(r['translated_units'] for r in keyitem_rom.get('equipment_archives',[]))
        result['translated_units']+=sum(r['translated_units'] for r in keyitem_rom.get('hint_archives',[]))
        result['translated_units']+=sum(r['translated_units'] for r in keyitem_rom.get('b0_hint_archives',[]))
        if args.field_b0_hints_023:result['field_b0_hints_023']=dict(selected_units=500,hint_archives=21,original_compressed_data_and_ram_capacity_retained=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_022:result['pending_batch500_022']=dict(selected_units=500,raw_units=136,hint_units=364,cumulative_merged_archives=3,new_archives=1,hint_archives=19,carry_consumer_contracts_preserved=True,original_hint_compressed_data_and_ram_capacity_retained=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500:result['pending_batch500']=dict(selected_units=500,rom_integrated=True,runtime='pending',dynamic_reward_review='pending; inventory caps are not reward-buffer bounds',release_eligible=False)
        if args.pending_batch500_002:result['pending_batch500_002']=dict(selected_units=500,carried_destruction_units=26,rom_integrated=True,repartition='340 mail plus160 raw dialogues; original gear153/Navi7 retained for next batch',runtime='pending',release_eligible=False)
        if args.pending_batch500_003:result['pending_batch500_003']=dict(selected_units=500,equipment_normal_units=39,star_units=6,other_raw_units=455,existing_common_aliases_not_counted=111,remaining_deferred_units=4,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_004:result['pending_batch500_004']=dict(selected_units=500,raw_normal_units=500,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_005:result['pending_batch500_005']=dict(selected_units=500,raw_normal_units=500,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_006:result['pending_batch500_006']=dict(selected_units=500,raw_normal_units=500,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_007:result['pending_batch500_007']=dict(selected_units=500,cumulative_merged_archives=13,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_008:result['pending_batch500_008']=dict(selected_units=500,cumulative_merged_archives=23,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_009:result['pending_batch500_009']=dict(selected_units=500,cumulative_merged_archives=64,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_010:result['pending_batch500_010']=dict(selected_units=500,cumulative_merged_archives=49,new_archives=20,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_011:result['pending_batch500_011']=dict(selected_units=500,cumulative_merged_archives=40,new_archives=21,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_012:result['pending_batch500_012']=dict(selected_units=268,cumulative_merged_archives=40,new_archives=8,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_013:result['pending_batch500_013']=dict(selected_units=1,cumulative_merged_archives=1,new_archives=0,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_014:result['pending_batch500_014']=dict(selected_units=10,cumulative_merged_archives=0,new_archives=3,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_015:result['pending_batch500_015']=dict(selected_units=6,cumulative_merged_archives=1,new_archives=1,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_016:result['pending_batch500_016']=dict(selected_units=500,cumulative_merged_archives=0,new_archives=24,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_017:result['pending_batch500_017']=dict(selected_units=500,cumulative_merged_archives=6,new_archives=0,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_018:result['pending_batch500_018']=dict(selected_units=500,cumulative_merged_archives=48,new_archives=30,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_019:result['pending_batch500_019']=dict(selected_units=500,cumulative_merged_archives=112,new_archives=21,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_020:result['pending_batch500_020']=dict(selected_units=500,cumulative_merged_archives=46,new_archives=6,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        if args.pending_batch500_021:result['pending_batch500_021']=dict(selected_units=500,cumulative_merged_archives=20,new_archives=0,carry_consumer_contracts_preserved=True,rom_integrated=True,runtime='pending',release_eligible=False)
        result['limits'].append('39 key-item literal drafts in guarded raw-ROM clone; one empty unit reused. Unknown callers/alternate archive native. Both consumers, quantity renderer, dynamic layout and save regression pending; NON-DISTRIBUTION')
    if calendar_frequency_graphics is not None:
        result['calendar_frequency_graphics']=calendar_frequency_graphics
        result['limits'].append('Five same-slot frequency graphics; shared four references; exact-ROM selector and other consumer verification required; '+('native names/input/storage unchanged' if calendar_presets is None else 'preset name experiment separately declared; input/persistence still pending'))
    if calendar_presets is not None:
        result['calendar_presets_poc']=calendar_presets
        result['limits'].append('Two default names and local confirmation counter PoC only; native keyboard unchanged; record/query/save/reload and other consumers pending; NON-DISTRIBUTION')
    if pet_graphics is not None:
        result['pet_menu_graphics']=pet_graphics
        result['limits'].append('Seven PET OBJ graphic labels added; exact-ROM runtime required; all other image text remains native/unverified')
    if attack_caption is not None:
        result['equipment_attack_caption']=attack_caption
        result['limits'].append('One buster attack caption graphic in original compressed slot; native decompression/residency/pixels pending; no text-unit increment')
    if dialogue_chip_name is not None:
        result['dialogue_chip_name']=dialogue_chip_name
        result['limits'].append('Only exact '+('Roll13/Guts13' if args.gutsman_dialogue_chip_name else 'Roll13')+' printChip0/104 commands in normal context use Korean name; wording counted once; other dialogue names native; ABI/lookup/copy/residency/runtime pending')
    if equipment_guides is not None:
        result['equipment_guides']=equipment_guides
        result['translated_units']+=equipment_guides['archive']['translated_units']
        if 'roll_archive' in equipment_guides:result['translated_units']+=equipment_guides['roll_archive']['translated_units']
        result['limits'].append('Source-pool-specific equipment guides60..62; exact-ROM ABI/root/pixel and other Navi fallback verification pending')
    if folder_labels is not None:
        result['folder_labels']=folder_labels
        result['translated_units']+=folder_labels['header']['translated_units']
        result['limits'].append('Equipment title and isolated script1 folder header added; exact-ROM runtime required; other equipment modes unverified')
        if args.equipment_weapons:result['limits'].append('Additional33 common equipment weapon drafts5..37; finite encoding/font/capacity checked; exact-ROM representative selection/transition/pixel QA pending; not all Navi gameplay verified')
    if save_title is not None:result['save_title_graphics']=save_title
    if title_menu is not None:result['title_menu_graphics']=title_menu
    if visibility is not None:
        result["policy"] = "functional-poc; NON-DISTRIBUTION"
        result["fixedcell_visibility"] = visibility
        result["limits"].insert(0, "NOT a translation update: four used Japanese glyph slots intentionally reassigned for visibility evidence")
    if fixed_extension is not None:
        result["fixedcell_extension"] = fixed_extension
        result["limits"][1] = "library headers implemented; chip-name tilemaps, mono descriptions, other fixed-cell labels, battle and name entry remain unimplemented"
    if chip_extension is not None:
        result["chip_library_extension"] = chip_extension
        result["translated_units"] += chip_extension["translated_units"]
        if chip_extension.get('secondary_clone') is not None:
            result['translated_units']+=len(chip_extension['secondary_clone']['units'])
        result["limits"][1] = f"{chip_extension['translated_units']} chip-name drafts on the guarded seven-row library path; other name consumers, mono descriptions, other menus, battle and name entry remain native"
    if folder_extension is not None:
        result['chip_folder_extension']=folder_extension
        result['limits'][1]=f"{chip_extension['translated_units']} chip-name drafts reused by experimental library/folder seven-row paths; other consumers, mono descriptions, battle and name entry remain native; exact folder runtime pending"
    mono_units=sum(r['translated_units'] for r in records if selected[r['archive']][2]['consumer']=='fixed-cell-mono')
    if mono_units:
        result['limits'][1]=f"{mono_units} mono description drafts with separate guarded provider; library/folder and shared description consumers require exact-ROM runtime QA; other descriptions/menus, battle and name entry not verified"
        fixed_extension['scope']='selected big library headers and explicitly registered mono description drafts; runtime approval remains consumer-specific'
    elif args.mono_font_poc:
        result['limits'].append('mono provider CPU/visibility PoC only; no mono description translation in this build')
    if battle_extension is not None:
        result['chip_battle_name_extension']=battle_extension
        result['limits'].append('Selected names additionally reused by caller166A8/native8x1 battle cards; exact-ROM runtime and other name consumers remain unverified')
    finalize025(source,target,result,inputs025,summary025,inputs024,summary024)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(target)
    manifest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built {output}\nSHA256 {sha(target)}\n{len(records)} archives; {result['translated_units']} units; {preserved} untouched archives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
