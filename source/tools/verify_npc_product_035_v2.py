"""Actual035 all-old-consumer/prefix/source/full-write/new500/repro audit."""
import argparse,struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from inspect_remaining_035 import BASE,BASE_SHA
from field_npc_rom_product_035_v2 import load_inputs,verify_final
from keyitem_rom_selector import INSTALL
from verify_pending500_002_rom import clones,read_payload,at_path
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rom',required=True);ap.add_argument('--out',required=True);ap.add_argument('--repro');args=ap.parse_args()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);old=read(BASE.replace('.gba','.json'));base=(ROOT/BASE).read_bytes()
    rp=ROOT/args.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();inputs=load_inputs(source);selected={k for r,_ in inputs for k in r['new_ids']}
    for name,h in m['build_tools_sha256'].items():require_hash(ROOT/'tools'/name,h)
    if rom[:INSTALL]!=base[:INSTALL] or rom[INSTALL+12:len(base)]!=base[INSTALL+12:] or len(rom)<=len(base):raise ValueError('035034 whole prefix preservation outside one composed reader stub')
    before=list(clones(old));after=list(clones(m));oldids={u['id'] for _,r in before for u in r['layout']};newids={u['id'] for _,r in after for u in r['layout']}
    if oldids-newids or newids-oldids!=selected or len(selected)!=500 or len(after)!=len(before)+9 or m['translated_units']!=old['translated_units']+500:raise ValueError('035 actual500/9 delta')
    for path,r in before:
        current=at_path(m,path)
        if any(current.get(k)!=r.get(k) for k in ('archive','compiled_sha256','compiled_bytes','rom_offset','translated_units','layout','source_sha256','protected_controls_unchanged')) or read_payload(rom,current)!=read_payload(base,r):raise ValueError('035 prior compiled consumer changed '+str(path))
    verify_final(source,rom,m['keyitem_rom']);nm=m['keyitem_rom']['npc035'];current={r['archive']:r for r in nm['archives']}
    from extended_dialogue import assemble_verified
    expected_stub,stub_proof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+nm['code_offset']+1))
    if rom[INSTALL:INSTALL+12]!=expected_stub or stub_proof!=nm['stub']:raise ValueError('035 independent final stub target/ISA')
    for rec,payload in inputs:
        arc=rec['archive'];r=current[arc]
        if read_payload(rom,r)!=payload or r['layout']!=rec['layout'] or r['translated_units']!=rec['translated_units'] or r['cumulative035']['scope']!=rec['scope']:raise ValueError('035 effective NPC payload/metrics/scope')
        native=payload_of(source,rec['source_row'])
        if verify_untouched_scripts(native,payload,255,set(rec['new_scripts']))!=rec['unselected_scripts']:raise ValueError('035 unselected native script')
        owners=[x for x in m['translation_assets'] if x.get('archive')==arc and not x.get('scope','').startswith('read-only inherited')]
        if len(owners)!=1 or {k:owners[0][k] for k in ('path','sha256')}!=rec['asset']:raise ValueError('035 unique NPC input owner')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);rows=parse_tpi(ROOT/cfg['text_catalog']['path']);primary={int(r['archive'],16):r for r in m['archives']};untouched=0
    for row in rows:
        if row['offset'] in primary:
            r=primary[row['offset']]
            if row['pointers']!=r['pointers'] or any(struct.unpack_from('<I',rom,p)[0]!=0x08000000+r['rom_offset'] for p in row['pointers']) or sha(read_payload(rom,r))!=r['compiled_sha256']:raise ValueError('035 retained primary refs/payload')
        else:
            if payload_of(rom,row)!=payload_of(source,row) or any(rom[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('035 unchanged native catalog source')
            untouched+=1
    if len(primary)!=len(old['archives']) or untouched!=old['unchanged_archives'] or untouched!=m['unchanged_archives']:raise ValueError('035 primary/source population')
    coverage=bytearray(len(source))
    for w in m['expected_writes']:
        at,n=w['offset'],w['bytes']
        if not 0<=at<=len(source)-n or any(coverage[at:at+n]) or source[at:at+n].hex()!=w['expected_hex'] or rom[at:at+n].hex()!=w['final_hex']:raise ValueError('035 expected writes/source/final/overlap')
        coverage[at:at+n]=b'\x01'*n
    if any(x!=y and not coverage[i] for i,(x,y) in enumerate(zip(source,rom))) or rom[:0xC0]!=source[:0xC0] or len(rom)!=m['output_bytes'] or len(rom)-len(source)!=m['append_bytes'] or sha(rom[len(source):])!=m['append_sha256']:raise ValueError('035 complete diff/length/header/appended tail')
    if len([w for w in m['expected_writes'] if w['offset']==INSTALL])!=1:raise ValueError('035 single composed stub writer')
    repro=False
    if args.repro:
        if (ROOT/args.repro).read_bytes()!=rom:raise ValueError('035 independent rebuild differs')
        repro=True
    previous=ROOT/'poc/output/pending500_035_v1.gba'
    require_hash(previous,'41c598d4d056b76eaacab3b111cadfa4767f2dd584ae729d03cfe09b0b859bdd')
    v1=previous.read_bytes()
    changes=[i for i,(a,b) in enumerate(zip(v1,rom)) if a!=b]
    cause=read('analysis/pending500_035_v1/native_caller_cause_v1.json')
    if len(v1)!=len(rom) or changes!=cause['single_changed_file_offsets'] or len(changes)!=1 or nm['wrapper']['caller_lr']!=0x0804F773:raise ValueError('035 v2 unexplained byte change or wrong actual return guard')
    deps=['tools/verify_npc_product_035_v2.py','tools/field_npc_rom_product_035_v2.py','analysis/pending_insertion_500_035_npc_inputs_v1/manifest.json']
    frozen_write(ROOT/args.out,dict(schema=1,passed=True,rom_sha256=sha(rom),rom_bytes=len(rom),baseline_sha256=BASE_SHA,source_sha256=sha(source),new_units=500,total_units=m['translated_units'],new_npc_consumers=9,preserved_consumer_count=len(before),primary_archives=len(primary),unchanged_source_archives=untouched,
        exact_selected500_delta=True,prior034_whole_prefix_except_stub_preserved=True,all_old_compiled_bytes_metrics_and_owners_preserved=True,original_npc_compression_and_references_preserved=True,final_placed_selector_verified=True,
        expected_writes_complete_diff_header_and_tail_verified=True,independent_rebuild_byte_identical=repro,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},runtime_tested=False,release_eligible=False,
        limits='Exact cumulative artifact static audit. GBA native NPC loader/reader residency, Korean glyph/video, timing and natural route QA remain required. Full Hangul composition/commit/save/redisplay and human review remain unfinished.'))
    print('035 actual500/total',m['translated_units'],'prior',len(before),'repro',repro,'PASS')

if __name__=='__main__':main()
