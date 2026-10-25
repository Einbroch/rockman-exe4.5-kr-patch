"""Source-bound redisplay destinations/widths; no adopted RAM reservation."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';path=base/'consumer_inventory.json';inv=read(path)
    require_hash(ROOT/'tools/analyze_keyboard_consumers.py',inv['tool_sha256'])
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(product,inv['current_rom_sha256']);current=product.read_bytes()
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b in [(0x38B94,0x38C10),(0x32AC6,0x32AD8)]:
        raw=rom[a:b]
        if current[a:b]!=raw:raise ValueError('redisplay code changed')
        ins=list(cs.disasm(raw,a+0x08000000))
        if sum(i.size for i in ins)!=b-a:raise ValueError('redisplay instruction extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('redisplay ISA roundtrip')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    literals={}
    for a,value in [(0x38DE4,0x0803B0D0),(0x38DE8,0x080526D0),(0x38DEC,0x02000950)]:
        if struct.unpack_from('<I',rom,a)[0]!=value or current[a:a+4]!=rom[a:a+4]:raise ValueError('redisplay source literal')
        literals[hex(a)]=hex(value)
    rows=[];all_fields=inv['metadata_rows']
    for row in all_fields:
        cap=row['native_logical_limit'];p=int(row['descriptor_pointer'],16);bound=row['descriptor_bytes']
        index=row['descriptor_index'];actual=struct.unpack_from('<II',rom,0x526D0+index*8)
        if actual!=(p,bound) or current[0x526D0+index*8:0x526D0+index*8+8]!=rom[0x526D0+index*8:0x526D0+index*8+8]:raise ValueError('descriptor identity')
        overlap=[r['descriptor_index'] for r in all_fields if p<int(r['field_end_exclusive'],16) and int(r['field_start'],16)<p+bound]
        rows.append(dict(descriptor=index,capacity=cap,records=row['count'],record_first=row['field_start'],
                         old_normalize_destination=hex(p),provider_copy_bound=bound,
                         full_Hangul_stream_bytes=4*cap+1,
                         provider_bound_deficit=4*cap+1-bound,
                         known_record_fields_overlapped=overlap,
                         first_record_body_alias=row['pointer_is_first_record_text'],
                         separate_display_storage_adopted=False))
    report=dict(id='exe45.hangul-keyboard.record-redisplay-analysis.v1',passed=True,rom_integrated=False,
                source_sha256=profile['sha256'],current_rom_sha256=inv['current_rom_sha256'],rows=rows,
                metadata_rows=len(rows),first_record_body_aliases=sum(r['first_record_body_alias'] for r in rows),
                provider_bounds_insufficient=sum(r['provider_bound_deficit']>0 for r in rows),
                packed_record_in_place_expansion_safe=False,native_code=regions,source_literals=literals,
                inventory_sha256=sha(path.read_bytes()),tools={'analyze_keyboard_record_redisplay.py':sha((ROOT/'tools/analyze_keyboard_record_redisplay.py').read_bytes())},
                confirmed=['Original reader chooses slot then passes selectedRecord+1 as source, descriptor pointer as destination to rawE5 copier08032AC6.',
                           'Raw copier recognizes E5 even inside F9FC rank or E4 payload; do not use it to move new display streams.',
                           'Descriptor copy bounds are provider consumption bounds, not proven allocation extents. Increasing them is not a RAM ownership proof.'],
                limits=['Bounded26 metadata/descriptors and explicit reader/body only; not all native or persistent save consumers.',
                        'Other10 non-first-record aliases are not automatically free/safe buffers. All writers/lifetimes and expanded stream extents need separate evidence.',
                        'New record/display helpers cannot replace original normalize ABI blindly; format selection and separate storage/provider connections remain uninstalled.'])
    (base/'record_redisplay.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS bounded redisplay destinations',len(rows),'first-record aliases',report['first_record_body_aliases'],'insufficient copy bounds',report['provider_bounds_insufficient'],flush=True)

if __name__=='__main__':main()
