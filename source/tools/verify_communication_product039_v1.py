"""Actual039 cumulative image/write/consumer/repro audit; NOT GBA runtime."""
import argparse,struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from communication_rom_product039_v1 import BASE,BASE_SHA,MANIFEST,CPU,load_inputs,verify_final
from keyitem_rom_selector import INSTALL
from verify_pending500_002_rom import clones,read_payload,at_path
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);p.add_argument('--repro',required=True);a=p.parse_args()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'));rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();inputs=load_inputs(source);selected={k for r,_ in inputs for k in r['new_ids']}
    for name,h in m['build_tools_sha256'].items():require_hash(ROOT/'tools'/name,h)
    if len(rom)<=len(base) or rom[:INSTALL]!=base[:INSTALL] or rom[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('039 old038 prefix except composed stub')
    before=list(clones(old));after=list(clones(m));oldids={u['id'] for _,r in before for u in r['layout']};newids={u['id'] for _,r in after for u in r['layout']}
    if oldids-newids or newids-oldids!=selected or len(selected)!=500 or len(after)!=len(before)+17 or m['translated_units']!=old['translated_units']+500:raise ValueError('039 actual exact500/17')
    for path,r in before:
        cur=at_path(m,path)
        if any(cur.get(k)!=r.get(k) for k in ['archive','compiled_sha256','compiled_bytes','rom_offset','translated_units','layout','source_sha256','protected_controls_unchanged']) or read_payload(rom,cur)!=read_payload(base,r):raise ValueError('039 previous consumer altered '+str(path))
    if m['active_fullcarry_owners038']!=old['active_fullcarry_owners038']:raise ValueError('039 prior038 explicit ownership')
    verify_final(source,rom,m['keyitem_rom']);n=m['keyitem_rom']['communication039'];current={r['archive']:r for r in n['archives']}
    for r,payload in inputs:
        cur=current[r['archive']]
        if read_payload(rom,cur)!=payload or cur['layout']!=r['layout'] or cur['translated_units']!=r['translated_units'] or cur['cumulative039']['scope']!=r['scope'] or m['active_communication_owners039'][r['archive']]!=r['asset']:raise ValueError('039 authored target/metrics/scope/owner')
        if verify_untouched_scripts(payload_of(source,r['source_row']),payload,r['scope']['script_count'],set(r['new_scripts']))!=r['unselected_source_scripts']:raise ValueError('039 unselected source scripts')
        if len([x for x in m['translation_assets'] if x.get('archive')==r['archive'] and {k:x[k] for k in ['path','sha256']}==r['asset']])!=1:raise ValueError('039 one authored owner')
    intervals=[]
    for placement in n['placements']:intervals.extend([(placement['native_copy_offset'],placement['native_copy_offset']+placement['native_copy_bytes']),(placement['rom_offset'],placement['rom_offset']+placement['compiled_bytes'])])
    intervals.extend([(n['descriptor_offset'],n['descriptor_offset']+17*16),(n['code_offset'],n['code_offset']+n['code_bytes'])]);cursor=len(base)
    for lo,hi in sorted(intervals):
        if not cursor<=lo<hi<=len(rom) or lo-cursor>3 or rom[cursor:lo]!=b'\xff'*(lo-cursor):raise ValueError('039 complete append/padding/overlap')
        cursor=hi
    if cursor!=len(rom):raise ValueError('039 unexplained appended tail')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);primary={int(r['archive'],16):r for r in m['archives']};untouched=0
    for row in parse_tpi(ROOT/cfg['text_catalog']['path']):
        if row['offset'] in primary:
            r=primary[row['offset']]
            if row['pointers']!=r['pointers'] or any(struct.unpack_from('<I',rom,x)[0]!=0x08000000+r['rom_offset'] for x in row['pointers']) or sha(read_payload(rom,r))!=r['compiled_sha256']:raise ValueError('039 primary retained source references')
        else:
            if payload_of(rom,row)!=payload_of(source,row) or any(rom[x:x+4]!=source[x:x+4] for x in row['pointers']):raise ValueError('039 original source catalog drift')
            untouched+=1
    if len(primary)!=len(old['archives']) or untouched!=old['unchanged_archives'] or untouched!=m['unchanged_archives']:raise ValueError('039 source denominator')
    covered=bytearray(len(source))
    for w in m['expected_writes']:
        off,length=w['offset'],w['bytes']
        if not 0<=off<=len(source)-length or any(covered[off:off+length]) or source[off:off+length].hex()!=w['expected_hex'] or rom[off:off+length].hex()!=w['final_hex']:raise ValueError('039 expected source/final/overlap')
        covered[off:off+length]=b'\x01'*length
    if any(x!=y and not covered[i] for i,(x,y) in enumerate(zip(source,rom))) or rom[:0xC0]!=source[:0xC0] or len(rom)!=m['output_bytes'] or len(rom)-len(source)!=m['append_bytes'] or sha(rom[len(source):])!=m['append_sha256']:raise ValueError('039 complete diff/header/size/tail')
    if len([w for w in m['expected_writes'] if w['offset']==INSTALL])!=1:raise ValueError('039 single composed source writer')
    if sha(rom)!=read(CPU)['fixture_only']['fixture_sha256']:raise ValueError('039 CPU PREFIX fixture mismatch')
    if (ROOT/a.repro).read_bytes()!=rom:raise ValueError('039 independent reproducibility')
    deps=[MANIFEST,CPU,'tools/verify_communication_product039_v1.py','tools/communication_rom_product039_v1.py','tools/specs/primary039_v1_version.json']
    frozen_write(ROOT/a.out,dict(passed=True,scope=__doc__,rom_sha256=sha(rom),rom_bytes=len(rom),source_sha256=sha(source),baseline_sha256=BASE_SHA,new_units=500,total_units=m['translated_units'],new_consumers=17,preserved_consumers=len(before),primary_archives=len(primary),unchanged_source_archives=untouched,exact500_delta=True,old038_prefix_except_stub_preserved=True,old_consumer_bytes_metrics_and_owners_preserved=True,source_compression_and_references_preserved=True,complete_source_writes_and_append_ownership_verified=True,selector_PREFIX_CPU_fixture_whole_image_byte_identical=True,independent_rebuild_byte_identical=True,runtime_tested=False,release_eligible=False,dependencies={path:sha((ROOT/path).read_bytes()) for path in deps},limits=['039 cumulative static result only; own039 coldboot/full initialization/local communication option/hold/page/render/cancel tests still required.','Fixed-cell communication labels unchanged; multiplayer/hardware/audio/Hangul name persistence and human review incomplete.']))
    print('PASS039 actual500/total',m['translated_units'],'old',len(before),'repro identical; GBA runtime pending')


if __name__=='__main__':main()
