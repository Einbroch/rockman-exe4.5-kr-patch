"""Independent exact500 source/parent ownership and two native lookup classes."""
import struct
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts

def main():
    out='analysis/pending_insertion_500_037_source_only_v2';s=read(out+'/selection.json');v=read(out+'/verification_v1.json');require_hash(ROOT/v['selection']['path'],v['selection']['sha256']);require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();m=read(s['baseline_rom'].replace('.gba','.json'));cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    for t in v['tools']:require_hash(ROOT/t['path'],t['sha256'])
    if not v['passed'] or v['units']!=500 or v['rom_written'] or v['product_integrated'] or s['insertion_ready']:raise ValueError('037 source-only stage applicability')
    prior={u['id'] for r in layout_records(m) for u in r['layout']};owned={r['archive'] for r in layout_records(m)};groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    ids=[];classes=Counter();scenes=Counter();records=[];punct=0
    def word(at):return struct.unpack_from('<I',source,at)[0]
    for r in v['archives']:
        arc=r['archive'];gs=groups[arc];native=payload_of(source,gs[0]['source_row']);path=ROOT/r['compiled']['path'];require_hash(path,r['compiled']['sha256']);target=path.read_bytes()
        if arc in owned or payload_of(rom,gs[0]['source_row'])!=native or sha(native)!=r['source_payload_sha256'] or len(native)!=r['native_bytes'] or len(target)!=r['compiled_bytes']:raise ValueError('037 source/current compiled ownership')
        expected_ids={k for g in gs for k in g['ids']};actual_ids={u['id'] for u in r['units']}
        if expected_ids!=actual_ids or actual_ids&prior or any(u['state']!='needs_review' for u in r['units']):raise ValueError('037 source ID/state agreement')
        kept=verify_untouched_scripts(native,target,r['script_count'],{g['script'] for g in gs})
        if kept!=r['unselected_scripts'] or not r['controls_unchanged'] or not r['roundtrip']:raise ValueError('037 selected versus native script boundaries')
        native_refs=gs[0]['source_native_lookup_candidates'];board_refs=gs[0]['source_board_lookup_candidates']
        if bool(native_refs)==bool(board_refs):raise ValueError('037 unique source lookup class')
        if native_refs:
            if len(native_refs)!=1 or r['script_count']!=255:raise ValueError('037 native NPC lookup identity')
            q=native_refs[0];top=word(0x53700+(q['scene']-0x80)*4)-0x08000000;table=word(top+q['sub']*4)-0x08000000;at=table+q['slot']*4;kind='native-NPC';root=0x02039800;reader=0x0804F764;lr=0x0804F773
        else:
            if len(board_refs)!=1:raise ValueError('037 board lookup identity')
            q=board_refs[0];table=word(0x537CC+(q['scene']-0x80)*4)-0x08000000;at=table+q['sub']*4;kind='field-board';root=0x0203C800;reader=0x0804F780;lr=0x0804F785
        if at!=q['pointer'] or word(at)!=0x08000000+int(arc,16) or len(native)!=q['native_bytes']:raise ValueError('037 independent current-source lookup')
        if any(g['source_native_lookup_candidates']!=native_refs or g['source_board_lookup_candidates']!=board_refs for g in gs):raise ValueError('037 archive source-class agreement')
        classes[kind]+=len(actual_ids);scenes[hex(q['scene'])]+=len(actual_ids);ids+=list(actual_ids)
        for u in r['units']:
            if not any(c.isalnum() for c in u['source']):punct+=1
        records.append(dict(archive=arc,units=len(actual_ids),script_count=r['script_count'],native_bytes=len(native),compiled_bytes=len(target),source_class=kind,root=root,original_reader=reader,expected_original_return_lr=lr,source_reference=q,product_admitted=False))
    if len(ids)!=len(set(ids)):raise ValueError('037 duplicate selected IDs')
    if len(ids)!=500 or set(ids)!=set(s['selected_ids']) or dict(classes)!={'field-board':137,'native-NPC':363}:raise ValueError('037 exact500/two-class denominator')
    old=read('analysis/pending_insertion_500_037_source_only_v1/selection.json');a=set(old['selected_ids']);b=set(ids)
    frozen_write(ROOT/out/'preflight_v1.json',dict(passed=True,scope='Exact500 canonical source preparation, two static native consumer classes; NOT ROM/product admission',baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],source_sha256=sha(source),units=500,scripts=len(s['groups']),archives=len(records),classes=dict(classes),source_scene_units=dict(scenes),current_ROM_glyphs_checked=v['extended_glyphs_checked'],punctuation_only_ids=punct,prose_or_label_ids=500-punct,source_and_target_roundtrips_verified=True,unselected_scripts_preserved=True,previous_ROM_ID_or_archive_overlap=False,wording_changed=False,source_only_old_cohort_replaced_ids=len(a-b),source_only_old_cohort_retained_ids=len(a&b),source_only_old_cohort_added_ids=len(b-a),archives_detail=records,rom_written=False,new_units_applied=0,product_admitted=False,runtime_tested=False,release_eligible=False,limits=['037v2 supersedes the old source-only500 selection; the old reward/tournament/A4 hint entries remain pending, not silently removed from the game scope.','NPC363 includes newA2 parameters and new source identities. Board137 uses distinct native root0203C800/caller4F780. Product registry, single-writer integration, CPU applicability, independent rebuild and exact-ROM runtime are still required.','Current ROM remains036,total19122. Canonical ROM-unapplied11424 includes these500;10924 others unselected. Not whole-game/image remainder.'],dependencies={p:sha((ROOT/p).read_bytes()) for p in [out+'/selection.json',out+'/verification_v1.json','tools/verify_source037_v2.py','tools/specs/source037_v2_version.json','tools/specs/compile037_v2_version.json']}))
    print('PASS037v2 exact500/228scripts/70archives source-only; NPC363+board137; NO ROM')

if __name__=='__main__':main()
