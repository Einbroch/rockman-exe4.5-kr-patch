"""Actual025 remainder under finite source-preserved normal/PET consumers.

Analysis only. Wording/word spaces and protected edge LF/padding are unchanged;
only existing inter-word spaces may become within-page LF. Finite026 native controls are analysis-only until product registration. Unknown
variable providers, storage adapters and renderer changes remain rejected.
"""
import re
from functools import lru_cache
from collections import defaultdict,Counter
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from nickname_capacity import advance,CPU
from survey_batch500_020_variables import applicability
from survey_batch500_017_layout import protected_edges
from survey_pet_quick_reflow_024 import replace_for_analysis
from normal_timing_capacity_025 import validate as normal_validate
from field_hint_capacity import validate as full_validate
from normal_battle_choice_capacity_026 import validate as choice_validate
from normal_vertical_choice_capacity_026 import validate as vertical_validate
from pet_nickname_capacity_025 import validate as nickname_validate
from pet_choice_capacity_026 import validate as pet_choice_validate
from pet_guard_capacity_027 import validate as guarded_validate
from pet_profile_capacity_027_v2 import validate as profile_validate
from profile_provider_bounds_027_v2 import bounds as profile_bounds
from pet_array_capacity_029 import validate as array_validate
from pet_entry_profile_capacity_030 import validate as entry_validate
from pet_chip_capacity_030 import validate as chip_validate
from pet_extended_native_capacity_031 import validate as extended_validate
from normal_player_name_capacity_031 import validate as player_validate
from event_dialogue_capacity_031 import validate as event_validate
from calendar_delete_capacity_031 import validate as calendar_validate,CALENDARS
from pet_nickname_flags_capacity_025_v2 import validate as flags_validate

SURVEY='analysis/pending_insertion_500_031_survey_v1/survey.json'
OUT='analysis/pending_insertion_500_031_calendar_layout_v2/survey.json'


def place(text,caps):
    """Finite word-boundary layouts, preserving every original word and edge."""
    if len(caps)!=3 or any(type(c) is not int or c<=0 for c in caps):raise ValueError('025 row caps')
    lines=text.split('\n')
    if len(lines)<=3 and all(advance(s)<=caps[i] for i,s in enumerate(lines)):
        return text
    if text!=text.strip() or len(lines)>3:return None
    flat=text.replace('\n',' ')
    @lru_cache(None)
    def solve(at,row,last):
        if row==last:
            tail=flat[at:]
            return (tail,) if tail and advance(tail)<=caps[row] else None
        choices=[]
        for end in range(at+1,len(flat)):
            if flat[end]!=' ':continue
            head=flat[at:end]
            if advance(head)>caps[row]:break
            if head.endswith(' '):continue
            rest=solve(end+1,row+1,last)
            if rest is not None:choices.append((head,)+rest)
        return min(choices,key=lambda xs:(max(map(advance,xs)),xs)) if choices else None
    # Keep existing row count if possible; adding LF does not add waited pages.
    for rows in range(len(lines),4):
        found=solve(0,0,rows-1)
        if found:
            value='\n'.join(found)
            if value.replace('\n',' ')!=flat:raise ValueError('025 wording changed')
            return value
    return None


def main():
    survey=read(SURVEY);require_hash(ROOT/survey['baseline_rom'],survey['baseline_sha256'])
    if survey['baseline_sha256']!='203fd306a7c9c713e3c6f4e7af3dd24d5f21eab0c000f210a061295d31083491' or survey['pinned_changed_inputs']:
        raise ValueError('025 actual025 frozen baseline')
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,survey['source_sha256']);source=sp.read_bytes();rom=(ROOT/survey['baseline_rom']).read_bytes()
    bound=applicability(source,rom,read(CPU));profile_bounds(source,rom)
    require_hash(ROOT/survey['pinned_coverage']['path'],survey['pinned_coverage']['sha256'])
    pool=defaultdict(list)
    for path,h in read(survey['pinned_coverage']['path'])['draft_asset_hashes'].items():
        require_hash(ROOT/path,h);asset=read(path)
        for u in asset['units']:pool[u['id']].append((path,h,u,asset))
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    catalog={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    tpls={};sections={};native_hashes={};good=[];bad=[];skipped=Counter()
    for group in survey['unresolved_groups']+survey['candidates']:
        if not set(group.get('reasons',[]))<={'adopted_normal_geometry','variable_insertion','different_storage_adapter','choice_layout'}:
            skipped.update(group.get('reasons',[]));continue
        arc=group['archive'];row=catalog[arc]
        hint=row['compressed'] and not row['size_header'] and len(row['pointers'])==1 and row['pointers'][0] in range(0x54180,0x541D4,4)
        if row['compressed'] and not hint or row['size_header'] or not row['pointers'] or row['pointers']==[0]:
            skipped['unsupported_storage']+=1;continue
        if arc not in native_hashes:native_hashes[arc]=sha(payload_of(source,row))
        units=[];refs=[];asset=None
        for key in group['ids']:
            choices=pool[key]
            if not choices or len({(u['source'],u['translation'],u['state']) for _,_,u,_ in choices})!=1:
                raise ValueError('025 frozen wording absent/conflicting')
            path,h,u,asset=choices[0]
            if asset['source_archive_sha256']!=native_hashes[arc]:raise ValueError('025 actual source payload')
            units.append(deepcopy(u));refs.append(dict(id=key,path=path,sha256=h))
        ref=asset['source_tpl']
        if arc not in tpls:
            require_hash(ROOT/ref['path'],ref['sha256']);tpls[arc]=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
            sections[arc]={int(m[1]):m[0] for m in re.finditer(r'^script (\d+) \w+ \{[\s\S]*?(?=^script\s|\Z)',tpls[arc],re.M)}
        original='@archive '+arc+'\n'+sections[arc][group['script']]
        quick=bool(re.search(r'^\tmsgOpenQuick\s*$',original,re.M));full_calendar=(arc in CALENDARS and group['script']==50)
        caps=(180,180,168) if full_calendar else (132,132,132) if quick else (180,180,168)
        layouts={};failure=None
        for u in units:
            value=place(u['translation'],caps)
            if value is None or not protected_edges(u['source'],value):failure='protected_same_wording_placement';break
            if value!=u['translation']:layouts[u['id']]=value
            u['translation']=value
        if failure:
            bad.append(dict(archive=arc,script=group['script'],ids=group['ids'],reason=failure));continue
        target=replace_for_analysis(original,units);errors=[];geometry=None;profile=None
        validators=[('pet-extended-native',lambda:extended_validate(original,target,[group['script']],set(group['ids']),bound)),
                    ('pet-native-nickname',lambda:nickname_validate(original,target,[group['script']],set(group['ids']),bound)),
                    ('pet-fixed-choice',lambda:pet_choice_validate(original,target,[group['script']],set(group['ids']),bound)),
                    ('pet-array-conditional',lambda:array_validate(original,target,[group['script']],set(group['ids']),bound)),
                    ('pet-direct-profile',lambda:profile_validate(original,target,[group['script']],set(group['ids']),bound)),
                    ('pet-native-chip-profile',lambda:chip_validate(original,target,[group['script']],set(group['ids']),bound)),
                    ('pet-entry-profile-conditional',lambda:entry_validate(original,target,[group['script']],set(group['ids']),bound)),
                    ('pet-entry-guards',lambda:guarded_validate(original,target,[group['script']],set(group['ids']),bound)),
                    ('pet-flags',lambda:flags_validate(original,target,[group['script']],set(group['ids']),bound))] if quick else [
                    ('normal-player-name',lambda:player_validate(original,target,[group['script']],set(group['ids']),bound,88)),
                    ('normal-horizontal-choice',lambda:choice_validate(original,target,[group['script']],set(group['ids']),bound,88)),
                    ('normal-vertical-choice',lambda:vertical_validate(original,target,[group['script']],set(group['ids']),bound,88)),
                    ('normal-pages',lambda:normal_validate(original,target,[group['script']],set(group['ids']),bound,88)),
                    ('fullbox',lambda:full_validate(original,target,[group['script']],set(group['ids']),bound,88))]
        validators.insert(0,('event-pages',lambda:event_validate(original,target,[group['script']],set(group['ids']),bound)))
        validators.insert(0,('calendar-delete-quick',lambda:calendar_validate(original,target,[group['script']],set(group['ids']),bound)))
        for name,check in validators:
            try:geometry=check();profile=name;break
            except ValueError as ex:errors.append(str(ex))
        if geometry is None:
            bad.append(dict(archive=arc,script=group['script'],ids=group['ids'],reason=' | '.join(errors)));continue
        good.append(dict(archive=arc,script=group['script'],ids=group['ids'],units=len(units),profile=profile,drafts=refs,
            source_tpl=ref,source_row=row,source_archive_sha256=native_hashes[arc],explicit_layouts=layouts,
            geometry=geometry,storage='A3-clone-merge' if hint else 'raw-known-pointer',product_admitted=False))
    states={0:[]}
    for g in sorted([g for g in good if g['profile'] in ('calendar-delete-quick','event-pages','pet-direct-profile','pet-array-conditional','pet-native-chip-profile','pet-extended-native','normal-player-name')],key=lambda g:(g['storage']!='raw-known-pointer',g['archive'],g['script'])):
        for n,chosen in list(states.items()):
            total=n+g['units']
            if total<=500 and total not in states:states[total]=chosen+[g]
    selected=states.get(500);counts=Counter()
    for g in good:counts[g['profile']]+=g['units']
    deps=[SURVEY,CPU,'tools/calendar_delete_capacity_031.py','tools/survey_calendar_layout500_031_v2.py','analysis/pending_insertion_500_031_frequency_cpu_v1/cpu.json','tools/event_dialogue_capacity_031.py','tools/survey_event_layout500_031.py','analysis/pending_insertion_500_031_event_title_bounds_v1/cpu.json','tools/pet_array_capacity_029.py','analysis/pending500_029_v1/array_cpu.json','tools/pet_entry_profile_capacity_030.py','tools/pet_chip_capacity_030.py','analysis/pending_insertion_500_030_chip_pools_v1/census.json','tools/survey_layout500_031_v1.py','tools/pet_extended_native_capacity_031.py','tools/normal_player_name_capacity_031.py','tools/pet_nickname_capacity_025.py','tools/pet_choice_capacity_026.py','tools/pet_guard_capacity_027.py','tools/pet_profile_capacity_027_v2.py','tools/profile_provider_bounds_027_v2.py','tools/normal_battle_choice_capacity_026.py','tools/normal_vertical_choice_capacity_026.py','tools/normal_timing_capacity_025.py',
          'tools/field_hint_capacity.py','tools/pet_quick_capacity.py','tools/pet_nickname_flags_capacity_025_v2.py',
          'analysis/pending_insertion_500_024_native_controls_v2/cpu.json','analysis/pending_insertion_500_026_native_controls_v1/cpu.json','analysis/pending_insertion_500_027_profile_cpu_v2/cpu.json']
    frozen_write(ROOT/OUT,dict(schema=1,status='ACTUAL030_EVENT_PROVIDERS_CONDITIONAL_ANALYSIS_NOT_ROM_ADMISSION',
        source_sha256=sha(source),baseline_rom=survey['baseline_rom'],baseline_sha256=sha(rom),
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},native_nickname_bound=bound,
        candidate_units=sum(g['units'] for g in good),candidate_groups=good,profile_units=dict(counts),
        selected500=selected,max_reachable_requested_subset=max(states),rejections=bad,
        rejection_counts=dict(Counter(g['reason'] for g in bad)),skipped_overlapping_reasons=dict(skipped),
        rom_written=False,wording_changed=False,release_eligible=False,
        limits='Frozen canonical draft wording, within existing waited pages and explicit existing consumer '
            'models only. New LF layouts require source-bound product adoption, binary roundtrip, actual025 '
            'carry/scope reconstruction, whole-ROM/repro/reader and final026 runtime verification. '
            'Not a whole-game remainder count, human approval or500 applied units.'))
    print('025 existing-model candidates',sum(g['units'] for g in good),dict(counts),'exact500',bool(selected),'max',max(states),flush=True)
    print('Top rejections',Counter(g['reason'] for g in bad).most_common(12),flush=True)


if __name__=='__main__':main()
