"""Bind041 source-stage closure without promoting it to ROM completion."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

SOURCE='analysis/pending_insertion_500_041_source_v8'


def main():
    selection=read(SOURCE+'/selection.json');source=read(SOURCE+'/verification_v3.json');carry=read(SOURCE+'/carry_verification_v2.json');roundtrip=read(SOURCE+'/carry_roundtrip_v2.json');inventory=read(SOURCE+'/native_contracts_v2.json')
    if selection['selected_units']!=500 or not source['passed'] or source['units']!=500 or not carry['passed'] or carry['new_units']!=500 or carry['inherited_units']!=156 or not roundtrip['passed'] or sum(inventory['family_unit_counts'].values())!=500:raise ValueError('041 bounded source-stage prerequisites')
    reports=[SOURCE+'/selection.json',SOURCE+'/verification_v3.json',SOURCE+'/carry_verification_v2.json',SOURCE+'/carry_roundtrip_v2.json',SOURCE+'/native_contracts_v2.json',SOURCE+'/native_observations_v1.json','analysis/pending_insertion_500_041_inventory_v1/authored_owners.json']
    seen={};refs=0
    def dependency(p,h):
        nonlocal refs
        p=str(p).replace('\\','/');refs+=1
        # Legacy Python dependency basenames resolve only within tools; hashes stay mandatory.
        if '/' not in p and p.endswith('.py'):p='tools/'+p
        if p in seen:
            if seen[p]!=h:raise ValueError('041 conflicting dependency identity '+p)
            return
        require_hash(ROOT/p,h);seen[p]=h
        if p.endswith('.json'):
            a=read(p)
            if isinstance(a,dict):
                for q,k in a.get('dependencies',{}).items():dependency(q,k)
    def nested(v):
        if isinstance(v,dict):
            if isinstance(v.get('path'),str) and isinstance(v.get('sha256'),str):dependency(v['path'],v['sha256'])
            for x in v.values():nested(x)
        elif isinstance(v,list):
            for x in v:nested(x)
    linked={}
    for p in reports:
        h=sha((ROOT/p).read_bytes());dependency(p,h);nested(read(p));linked[p]=h
    baseline=ROOT/selection['baseline_rom'];require_hash(baseline,selection['baseline_sha256']);cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],selection['source_sha256']);m=read(baseline.with_suffix('.json'))
    result=dict(passed=True,status='041_BOUNDED_SOURCE_STAGE_COMPLETE_NATIVE_CONSUMER_ADMISSION_PENDING',date='2026-10-23',baseline_rom=selection['baseline_rom'],baseline_sha256=selection['baseline_sha256'],baseline_integrated_IDs=m['translated_units'],new_source_units_prepared=500,new_ROM_applied_units=0,inherited_units_reproduced=156,new_archives=53,new_scripts=445,extended_glyphs_checked=source['extended_glyphs_checked'],canonical_ROM_unapplied_drafts=9424,unique_pinned_dependencies_checked=len(seen),reference_checks=refs,reports=linked,wording_changed=False,rom_written=False,distribution_packages_created=0,product_admitted=False,release_eligible=False,first_unresolved_completion_boundary='Actual loader/caller/default-origin/shared-RAM and positioned/choice consumption;491 source-reference memberships are NOT491 complete native consumer admissions. Raw9, mail alerts and secondary reader remain unresolved. Pointerless7794EC stays in canonical backlog but is replaced by source mail14 in this batch.',next='Admit only after binding all53 source lookups and preserved156 authored carries to real native consumers, then immutable-original primary/repro exactnew500 integration and own041 runtime. Never inject new-only diagnostic payloads or patch040 in place.',checker_failure_history=['Source compile_v1 binary roundtrip passed but reverse archive ID inherited filename _new_only; compile_v2 uses canonical archive filename. No prose/control or ROM change.','Owner catalog initial raw-byte slice check rejected compressed parent records; corrected via declared compression decode/storage hashes before catalog publication.'],limits=['This closes source preparation only, NOT041 ROM integration or screens.','Current playable ROM remains040/21,122; canonical unapplied remains9,424, not8,924.','Conditional layout projections do not prove native defaults, branches, clearing or natural acquisition; no human/release/hardware/audio approval.'],dependencies={'tools/verify_source500_041_handoff_v3.py':sha((ROOT/'tools/verify_source500_041_handoff_v3.py').read_bytes())})
    frozen_write(ROOT/SOURCE/'source_handoff_v3.json',result);print('PASS041 SOURCE stage500/carry156; pinned files',len(seen),'new ROM units0; consumer admission pending')


if __name__=='__main__':main()




