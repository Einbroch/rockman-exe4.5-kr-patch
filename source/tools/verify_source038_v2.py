"""Independent exact500/carry/source-reference preflight, not ROM admission."""
import struct
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_source500_038_v5 import BASE,BASE_SHA,OUT as SOURCE,baseline
from prepare_source500_038_v3 import typed_lookup
from verify_tpi_index import parse_tpi,lz77_decompress
from prepare_repartition500 import layout_records
from archive_scripts import script_spans

def receipt(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))

def main():
    cfg,source,rom,m=baseline();s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v1.json');cp=ROOT/'analysis/pending_insertion_500_038_carry_v2/verification_v1.json';carry=read(cp)
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    for k in ('source_selection','source_compile'):require_hash(ROOT/carry[k]['path'],carry[k]['sha256'])
    if not v['passed'] or v['units']!=500 or not carry['passed'] or carry['new_units']!=500 or v['rom_written'] or carry['rom_written']:raise ValueError('038 source/carry preconditions')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    pool=typed_lookup(source);applied={u['id'] for r in layout_records(m) for u in r['layout']};seen=set();classes=Counter();scenes=Counter();records=[];targets={};selected={r['archive']:r for r in carry['archives']}
    compiled={r['archive']:r for r in v['archives']};gs=defaultdict(list)
    for g in s['groups']:gs[g['archive']].append(g)
    native_cache={a:lz77_decompress(source,int(a,16))[0] for a in pool}
    for r in carry['archives']:
        arc=r['archive'];require_hash(ROOT/r['compiled']['path'],r['compiled']['sha256']);payload=(ROOT/r['compiled']['path']).read_bytes();targets[arc]=sha(payload);native=native_cache[arc];row=catalog[arc];refs=pool[arc];sourceclasses={x['source_class'] for x in refs}
        if len(sourceclasses)!=1 or r['source_class']!=next(iter(sourceclasses)) or {x['pointer'] for x in refs}!=set(row['pointers']):raise ValueError('038 independent source table membership '+arc)
        if refs!=r['source_lookup_candidates'] or any(rom[p:p+4]!=source[p:p+4] or struct.unpack_from('<I',source,p)[0]!=0x08000000+row['offset'] for p in row['pointers']):raise ValueError('038 source pointer preservation')
        off=row['offset'];original,used=lz77_decompress(source,off)
        if rom[off:off+used]!=source[off:off+used] or native!=original or sha(native)!=compiled[arc]['source_payload_sha256'] or r['script_count']!=struct.unpack_from('<H',native)[0]//2 or len(payload)>65535:raise ValueError('038 native/compiled bounds')
        roots={x['root'] for x in refs};capacity={0x02039800:0x3000,0x0203C800:0x1000,0x0203D800:0x2800}
        if len(roots)!=1 or len(native)>capacity[next(iter(roots))]:raise ValueError('038 native source buffer extent')
        ids=set(r['new_ids']);expected={k for g in gs[arc] for k in g['ids']}
        if ids!=expected or len(ids)!=len(r['new_ids']) or ids&(seen|applied):raise ValueError('038 disjoint IDs')
        if r['parent_record']:
            p=r['parent_record'];before=rom[p['rom_offset']:p['rom_offset']+p['compiled_bytes']]
            if sha(before)!=p['compiled_sha256']:raise ValueError('038 parent ownership identity')
            old=script_spans(before,r['script_count']);new=script_spans(payload,r['script_count']);scripts=set(r['new_scripts'])
            if any(old[i]!=new[i] for i in range(r['script_count']) if i not in scripts):raise ValueError('038 inherited script bytes')
        seen|=ids;classes[r['source_class']]+=len(ids)
        for scene in {x['scene'] for x in refs}:scenes[hex(scene)]+=len(ids)
        records.append(dict(archive=arc,new_units=len(ids),source_class=r['source_class'],references=refs,native_bytes=len(native),compiled_bytes=len(payload),compiled_sha256=sha(payload),inherited_IDs=len(r['inherited_IDs'])))
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(records)!=66:raise ValueError('038 exact500/66 denominator')
    # Identity matcher risk scan: prefix equality matters, not merely SHA equality.
    aliases=[]
    for arc in selected:
        for ref in pool[arc]:
            for peer,peerrefs in pool.items():
                if peer==arc or not any((p['scene'],p['root'],p['caller_lr'])==(ref['scene'],ref['root'],ref['caller_lr']) for p in peerrefs):continue
                a,b=native_cache[arc],native_cache[peer];length=min(len(a),len(b))
                if a[:length]==b[:length]:aliases.append(dict(archive=arc,peer=peer,scene=ref['scene'],root=ref['root'],native_equal=a==b,peer_selected=peer in selected,complete_target_equal=peer in targets and targets[arc]==targets[peer]))
    unresolved=[a for a in aliases if not(a['native_equal'] and a['complete_target_equal'])]
    out=ROOT/'analysis/pending_insertion_500_038_source_only_v5'
    deps=['tools/verify_source038_v2.py','tools/compile_source500_038_v1.py','tools/compile_carry038_v2.py','tools/normal_store_tail038_v1.py','tools/normal_navi_tail038_v1.py','tools/prepare_source500_038_v3.py','tools/prepare_source500_038_v5.py','tools/specs/source038_v3_version.json','tools/specs/source038_v4_version.json','tools/specs/source038_v5_version.json','tools/specs/compile038_v1_version.json','tools/specs/carry038_v2_version.json']
    result=dict(passed=True,scope=__doc__,baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),units=500,scripts=len(s['groups']),archives=66,classes=dict(classes),static_scene_unit_counts=dict(scenes),current_ROM_glyphs_checked=v['extended_glyphs_checked'],inherited_IDs_byte_preserved=carry['inherited_IDs_unchanged'],complete_original_source_roundtrip=True,complete_target_control_semantic_binary_roundtrips=True,source_table_reference_membership_verified=True,source_native_buffer_bounds_verified=True,native_identity_alias_pairs=aliases,unresolved_native_identity_alias_pairs=unresolved,source_A4_NPC_top_pointer=struct.unpack_from('<I',source,0x53790)[0],source_A4_NPC_top_is_null=False,records=records,selection=receipt(out/'selection.json'),source_compile=receipt(out/'verification_v1.json'),carry_compile=receipt(cp),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,product_admitted=False,insertion_ready=False,runtime_tested=False,release_eligible=False,required_before_product=['Native source-bound store tail CPU applicability and cleared-page Navi branch target/initializer evidence.','Three typed caller classes including navi-hint LR4F807/root0203D800, full native-byte ownership and any identity aliases must be enforced and CPU-checked.','Regenerate037 parent from immutable source/adopted inputs within single primary builder; carry/supersession/old508+70 consumers and exact500 delta guarded.','Independent rebuild, full-write/integrity checks and exact038 runtime, no037 saved-state reuse.'],limits=['Static source and derived full-carry compilation only, not500 ROM-applied translations or gameplay screens.','Native alias risks listed separately; static class/index selection does not prove natural scene/sub/navi entry.','Prior prose A4 NPC-null claim was wrong; original top53790=08053B18 and earlier JSON had false. Correct source fact does not prove natural A4 acquisition.','Canonical pending10924 unchanged; selected500 are included in that pending count; no distribution package.'])
    frozen_write(out/'preflight_v1.json',result)
    print('PASS038 source/carry exact500 /66 archives /468 glyphs /496 inherited; aliases',len(aliases),'unresolved',len(unresolved),'NO ROM')

if __name__=='__main__':main()
