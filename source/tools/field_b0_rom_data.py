"""023 B0 source-bound clone inputs, one descriptor, original native RAM retained."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from archive_scripts import verify_untouched_scripts

MANIFEST='analysis/pending_insertion_500_023_product_preflight_v2/preflight.json'


def input_entries(source):
    p=read(MANIFEST)
    if p['source_sha256']!=sha(source) or p['total_units']!=500 or p['release_eligible'] or p['rom_written']:raise ValueError('B0 product input policy/source')
    for path,h in p['dependencies'].items():require_hash(ROOT/path,h)
    require_hash(ROOT/p['baseline_rom'],p['baseline_sha256'])
    result=[];seen=set();ids=set()
    for b in p['archives']:
        entry=b['input_asset'];require_hash(ROOT/entry['path'],entry['sha256']);a=read(entry['path']);row=b['source_catalog_row'];index=b['navi_index']
        require_hash(ROOT/a['source_tpl']['path'],a['source_tpl']['sha256'])
        if (a['policy']!='development-draft; NON-DISTRIBUTION' or a['review']['release_eligible']
                or a['source_sha256']!=sha(source) or a['archive']!=b['archive'] or index in seen
                or row['pointers']!=[0x54238+index*4] or struct.unpack_from('<I',source,row['pointers'][0])[0]!=0x08000000+row['offset']):
            raise ValueError('B0 source/Navi/catalog identity')
        seen.add(index)
        for u in a['units']:
            if u['id'] in ids or u['state']!='needs_review':raise ValueError('B0 unique needs-review identities')
            ids.add(u['id'])
            if u['id'] in b['individual_layouts']:u['translation']=b['individual_layouts'][u['id']]
        result.append((entry['path'],row,a,b['scope'],b,index))
    if seen!=set(range(23))-{13,14} or len(ids)!=500:raise ValueError('B0 finite21/500 product denominator')
    return result


def compile_inputs(source,common,plugins,work):
    from build_development_patch import compile_archive
    from compare_archive_payloads import payload_of
    work.mkdir(parents=True,exist_ok=False);result=[]
    for path,row,a,scope,b,index in input_entries(source):
        raw,r=compile_archive(source,row,a,scope,common,plugins,work/a['archive'])
        if any(r.get(k)!=b.get(k) for k in ('compiled_sha256','compiled_bytes','layout','field_hint_capacity_proof','unselected_script_bytes_preserved')):raise ValueError('B0 product compile/preflight agreement')
        native=payload_of(source,row)
        r.update(script_count=255,navi_index=index,asset_path=path,asset_sha256=b['input_asset']['sha256'],source_pointers=row['pointers'],source_compressed_bytes=row['size'])
        result.append((raw,native,r,index))
    return result


def append(source,tail,payloads):
    out=bytearray(tail);table=[(0,0,0,0)]*23;records=[]
    def alloc(data):
        out.extend(b'\xff'*(-len(out)%4));at=len(source)+len(out);out.extend(data);return at
    for raw,native,r,index in payloads:
        if table[index]!=(0,0,0,0) or int.from_bytes(native[:2],'little')!=510 or len(raw)>65535:raise ValueError('B0 descriptor bounds')
        np=alloc(native);cp=alloc(raw);table[index]=(cp+0x08000000,np+0x08000000,len(native),0)
        records.append(dict(r,rom_offset=cp,rom_sha256=sha(raw),native_copy_offset=np,native_copy_bytes=len(native),native_payload_sha256=sha(native),native_ram_archive_retained=True))
    if len(records)!=21:raise ValueError('B0 descriptor population')
    at=alloc(b''.join(struct.pack('<4I',*r) for r in table))
    return bytes(out),dict(descriptor_address=at+0x08000000),records


def verify_final(source,target,meta):
    from compare_archive_payloads import payload_of
    entries=input_entries(source);records=meta.get('b0_hint_archives',[]);guard=meta.get('b0_hint_guard')
    if len(records)!=21 or not guard or set(guard)!={'descriptor_address'}:raise ValueError('B0 final population')
    table=[(0,0,0,0)]*23;ids=set()
    for r,(path,row,a,scope,b,index) in zip(records,entries):
        cp,np=r['rom_offset'],r['native_copy_offset'];native=payload_of(source,row);raw=target[cp:cp+r['compiled_bytes']]
        if (r['archive']!=a['archive'] or r['navi_index']!=index or r['asset_path']!=path
                or r['asset_sha256']!=b['input_asset']['sha256'] or sha(raw)!=b['compiled_sha256']
                or any(r.get(k)!=b.get(k) for k in ('compiled_bytes','compiled_sha256','layout','field_hint_capacity_proof','unselected_script_bytes_preserved'))
                or r['translated_units']!=len(a['units']) or r['source_pointers']!=row['pointers']):raise ValueError('B0 final clone/consumer identity')
        if (cp&3 or np&3 or not len(source)<=np<np+len(native)<=cp<cp+len(raw)<=guard['descriptor_address']-0x08000000
                or target[np:np+len(native)]!=native or r['native_copy_bytes']!=len(native) or r['native_payload_sha256']!=sha(native)
                or r['native_ram_archive_retained'] is not True):raise ValueError('B0 final storage/native comparison extent')
        off,n=row['offset'],row['size']
        if target[off:off+n]!=source[off:off+n] or target[0x54238:0x54294]!=source[0x54238:0x54294] or target[0x4F712:0x4F7B6]!=source[0x4F712:0x4F7B6]:raise ValueError('B0 source compressed/table/loader changed')
        verify_untouched_scripts(native,raw,255,{int(u['id'].split(':')[1]) for u in a['units']})
        table[index]=(cp+0x08000000,np+0x08000000,len(native),0);ids.update(u['id'] for u in a['units'])
    at=guard['descriptor_address']-0x08000000
    if target[at:at+23*16]!=b''.join(struct.pack('<4I',*r) for r in table) or len(ids)!=500:raise ValueError('B0 final descriptor/500 IDs')
    return ids
