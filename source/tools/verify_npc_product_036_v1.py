"""Independent final036 prefix, all-consumer, source/write/tail and repro audit."""
import argparse,struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_source500_036_v1 import BASE,BASE_SHA
from field_npc_rom_product_036_v1 import load_inputs,verify_final,MANIFEST
from keyitem_rom_selector import INSTALL
from verify_pending500_002_rom import clones,read_payload,at_path
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);p.add_argument('--repro');a=p.parse_args()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'))
    rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();inputs=load_inputs(source);selected={k for r,_ in inputs for k in r['new_ids']}
    for name,h in m['build_tools_sha256'].items():require_hash(ROOT/'tools'/name,h)
    if len(rom)<=len(base) or rom[:INSTALL]!=base[:INSTALL] or rom[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('036 old035 prefix preservation')
    before=list(clones(old));after=list(clones(m));oldids={u['id'] for _,r in before for u in r['layout']};newids={u['id'] for _,r in after for u in r['layout']}
    if oldids-newids or newids-oldids!=selected or len(selected)!=500 or len(after)!=len(before)+20 or m['translated_units']!=old['translated_units']+500:raise ValueError('036 actual500/20 delta')
    for path,r in before:
        cur=at_path(m,path)
        if any(cur.get(k)!=r.get(k) for k in ['archive','compiled_sha256','compiled_bytes','rom_offset','translated_units','layout','source_sha256','protected_controls_unchanged']) or read_payload(rom,cur)!=read_payload(base,r):raise ValueError('036 previous consumer altered '+str(path))
    verify_final(source,rom,m['keyitem_rom']);n=m['keyitem_rom']['npc036'];current={r['archive']:r for r in n['archives']}
    intervals=[]
    for r,payload in inputs:
        arc=r['archive'];cur=current[arc]
        if read_payload(rom,cur)!=payload or cur['layout']!=r['layout'] or cur['translated_units']!=r['translated_units'] or cur['cumulative036']['scope']!=r['scope']:raise ValueError('036 effective payload/metrics/scope')
        if verify_untouched_scripts(payload_of(source,r['source_row']),payload,255,set(r['new_scripts']))!=r['unselected_scripts']:raise ValueError('036 untouched script drift')
        owners=[x for x in m['translation_assets'] if x.get('archive')==arc and not x.get('scope','').startswith('read-only inherited')]
        if len(owners)!=1 or {k:owners[0][k] for k in ['path','sha256']}!=r['asset']:raise ValueError('036 unique new owner')
    for placement in n['placements']:
        intervals.extend([(placement['native_copy_offset'],placement['native_copy_offset']+placement['native_copy_bytes']),(placement['rom_offset'],placement['rom_offset']+placement['compiled_bytes'])])
    intervals.extend([(n['descriptor_offset'],n['descriptor_offset']+20*16),(n['code_offset'],n['code_offset']+n['code_bytes'])]);cursor=len(base)
    for lo,hi in sorted(intervals):
        if not cursor<=lo<hi<=len(rom) or lo-cursor>3 or rom[cursor:lo]!=b'\xff'*(lo-cursor):raise ValueError('036 complete append ownership/overlap/padding')
        cursor=hi
    if cursor!=len(rom):raise ValueError('036 unexplained append tail')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);primary={int(r['archive'],16):r for r in m['archives']};untouched=0
    for row in parse_tpi(ROOT/cfg['text_catalog']['path']):
        if row['offset'] in primary:
            r=primary[row['offset']]
            if row['pointers']!=r['pointers'] or any(struct.unpack_from('<I',rom,x)[0]!=0x08000000+r['rom_offset'] for x in row['pointers']) or sha(read_payload(rom,r))!=r['compiled_sha256']:raise ValueError('036 retained primary reference/payload')
        else:
            if payload_of(rom,row)!=payload_of(source,row) or any(rom[x:x+4]!=source[x:x+4] for x in row['pointers']):raise ValueError('036 unchanged source catalog drift')
            untouched+=1
    if len(primary)!=len(old['archives']) or untouched!=old['unchanged_archives'] or untouched!=m['unchanged_archives']:raise ValueError('036 source population denominator')
    covered=bytearray(len(source))
    for w in m['expected_writes']:
        off,length=w['offset'],w['bytes']
        if not 0<=off<=len(source)-length or any(covered[off:off+length]) or source[off:off+length].hex()!=w['expected_hex'] or rom[off:off+length].hex()!=w['final_hex']:raise ValueError('036 expected writes/source/overlap/final')
        covered[off:off+length]=b'\x01'*length
    if any(x!=y and not covered[i] for i,(x,y) in enumerate(zip(source,rom))) or rom[:0xC0]!=source[:0xC0] or len(rom)!=m['output_bytes'] or len(rom)-len(source)!=m['append_bytes'] or sha(rom[len(source):])!=m['append_sha256']:raise ValueError('036 complete diff/size/header/tail')
    if len([w for w in m['expected_writes'] if w['offset']==INSTALL])!=1:raise ValueError('036 single composed source writer')
    cpu=read('analysis/pending_insertion_500_036_selector_cpu_v1/cpu.json')
    if sha(rom)!=cpu['fixture_only']['sha256']:raise ValueError('036 actual ROM not byte-identical to all8423-vector CPU fixture')
    repro=False
    if a.repro:
        if (ROOT/a.repro).read_bytes()!=rom:raise ValueError('036 independent rebuild differs')
        repro=True
    deps=[MANIFEST,'tools/verify_npc_product_036_v1.py','tools/field_npc_rom_product_036_v1.py','analysis/pending_insertion_500_036_selector_cpu_v1/cpu.json','analysis/pending_insertion_500_036_selector_cpu_v1/boundaries_v1.json','analysis/pending500_035_v2/natural_cached_display_v2.json']
    frozen_write(ROOT/a.out,dict(passed=True,scope='Actual cumulative036 static artifact and CPU-fixture byte identity; NOT GBA runtime',rom_sha256=sha(rom),rom_bytes=len(rom),source_sha256=sha(source),baseline_sha256=BASE_SHA,new_units=500,total_units=m['translated_units'],new_consumers=20,preserved_consumers=len(before),primary_archives=len(primary),unchanged_source_archives=untouched,exact500_delta=True,old035_prefix_except_stub_preserved=True,old_consumer_bytes_metrics_and_owners_preserved=True,source_compression_and_references_preserved=True,complete_source_writes_and_append_ownership_verified=True,CPU8423_fixture_whole_image_byte_identical=True,independent_rebuild_byte_identical=repro,runtime_tested=False,release_eligible=False,dependencies={path:sha((ROOT/path).read_bytes()) for path in deps},limits=['035 natural evidence closes preceding035 changed-path gate only;036 A0/A1/A3 display/acquisition/timing/reentry still needs exact-ROM runtime.','Hangul composition/commit/save/redisplay and full human/game/graphics review remain incomplete.']))
    print('PASS036 actual500/total',m['translated_units'],'old',len(before),'repro',repro,'CPU image identical')


if __name__=='__main__':main()
