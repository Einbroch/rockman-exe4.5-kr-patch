"""Measure candidate growth without promoting an unverified RAM capacity."""
import struct
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    pre=read('analysis/pending_insertion_500_022_preflight_v1/preflight.json')
    require_hash(ROOT/pre['baseline_rom'],pre['baseline_sha256'])
    require_hash(ROOT/pre['selection']['path'],pre['selection']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    selection=read(pre['selection']['path']);groups={g['archive']+':'+str(g['script']):g for a in selection['selected'] for g in a['groups']}
    if pre['total_units']!=500 or pre['applied_id_intersection'] or pre['source_sha256']!=sha(source):raise ValueError('Candidate scope/source')
    # Source-established third field-message loader: select scene major table,
    # index by native Navi, then decompress to the native hint RAM root.
    if source[0x4F734:0x4F74A]!=bytes.fromhex('b1f7dafa8400084800f033f8005907499cf008fdf0bd'):raise ValueError('Native hint loader')
    if source[0x4F7A6:0x4F7B6]!=bytes.fromhex('f0b557463f6c3e79803eb6008059f0bd'):raise ValueError('Native scene table selector')
    if struct.unpack_from('<I',source,0x4F75C)[0]!=0x08053FA0 or struct.unpack_from('<I',source,0x4F760)[0]!=0x0203D800:raise ValueError('Native loader literals')
    if struct.unpack_from('<I',source,0x5402C)[0]!=0x08054180:raise ValueError('Declared scene/Navi table')
    counts=Counter();result=[]
    for item in pre['archives']:
        name=item['archive'];row=rows[name];native=payload_of(source,row)
        folder=ROOT/'analysis/pending_insertion_500_022_preflight_v1'/name;path=folder/'rebuilt.msg';require_hash(path,item['compiled_sha256']);target=path.read_bytes()
        if len(native)!=item['source_bytes'] or len(target)!=item['compiled_bytes'] or not all(item[k] for k in ('source_native_roundtrip','protected_controls_unchanged','semantic_roundtrip','binary_roundtrip')):raise ValueError('Source-only proof')
        kind='raw-existing-adapter'
        if row['compressed']:
            kind='compressed-hint-RAM-growth-unverified'
            if row['size_header'] or len(row['pointers'])!=1 or row['pointers'][0] not in range(0x54180,0x541D4,4):raise ValueError('Finite compressed candidate table')
            if struct.unpack_from('<I',source,row['pointers'][0])[0]!=0x08000000+row['offset']:raise ValueError('Source pointer binding')
        counts[kind]+=item['selected_units']
        result.append(dict(archive=name,storage_kind=kind,selected_units=item['selected_units'],source_stored_bytes=row['size'],source_payload_bytes=len(native),candidate_payload_bytes=len(target),payload_growth_bytes=len(target)-len(native),source_pointers=row['pointers'],candidate_sha256=sha(target),native_hint_destination=0x0203D800 if row['compressed'] else None,hypothetical_candidate_end=0x0203D800+len(target) if row['compressed'] else None,capacity_verified=False if row['compressed'] else None))
    if sum(counts.values())!=500:raise ValueError('Distinct500 denominator')
    frozen_write(ROOT/'analysis/pending_insertion_500_022_storage_v1/storage.json',dict(schema=1,source_sha256=sha(source),baseline_rom=pre['baseline_rom'],baseline_sha256=pre['baseline_sha256'],source_preflight_sha256=sha((ROOT/'analysis/pending_insertion_500_022_preflight_v1/preflight.json').read_bytes()),selected_units=500,units_by_storage=dict(counts),archives=result,loader_static_observation=dict(entry=0x0804F712,decompress_call=0x0804F744,root_table=0x08053FA0,scene_table=0x08054180,scene_major=0xA3,destination=0x0203D800,consumer_entry=0x0804F7FC,capacity_established=False),product_admitted=False,rom_written=False,runtime_tested=False,release_eligible=False,next_action='Establish native hint RAM extent and lifetime with the field loader and consumer; alternatively investigate a source-size-preserving ROM reader. Do not infer capacity from EWRAM end or unrelated absolute literals. Only then design cumulative storage admission and build/runtime verification.'))
    print('PASS candidate growth census:',dict(counts))
    print('Compressed maximum candidate bytes:',max(r['candidate_payload_bytes'] for r in result if r['native_hint_destination']))


if __name__=='__main__':main()
