"""022 source-bound hint clones; original compressed data and pointers retained."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from prepare_pending500_022_raw import MANIFEST
from verify_tpi_index import parse_tpi,lz77_decompress

def input_entries(source):
    m=read(MANIFEST);ref=m['source_preflight'];require_hash(ROOT/ref['path'],ref['sha256']);p=read(ref['path'])
    if m['policy']!='development-draft; NON-DISTRIBUTION' or m['release_eligible'] is not False or p['source_sha256']!=sha(source) or p['total_units']!=500:raise ValueError('Hint input policy/source')
    require_hash(ROOT/p['baseline_rom'],p['baseline_sha256']);require_hash(ROOT/p['selection']['path'],p['selection']['sha256']);require_hash(ROOT/p['individual_layout']['path'],p['individual_layout']['sha256'])
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);rows={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};layouts=read(p['individual_layout']['path'])['layouts'];result=[];seen=set()
    for b in p['archives']:
        if b['archive'] in m['raw_archives']:continue
        row=rows[b['archive']]
        if not row['compressed'] or row['size_header'] or len(row['pointers'])!=1 or row['pointers'][0] not in range(0x54180,0x541D4,4):raise ValueError('Finite hint table membership')
        index=(row['pointers'][0]-0x54180)//4
        if index in seen or struct.unpack_from('<I',source,row['pointers'][0])[0]!=0x08000000+row['offset']:raise ValueError('Hint table identity')
        seen.add(index);native=lz77_decompress(source,row['offset'])[0];require_hash(ROOT/b['draft_path'],b['draft_sha256']);a=read(b['draft_path']);require_hash(ROOT/a['source_tpl']['path'],a['source_tpl']['sha256'])
        if a['source_archive_sha256']!=sha(native) or a['source_sha256']!=sha(source) or [u['id'] for u in a['units']]!=b['selected_ids'] or any(u['state']!='needs_review' for u in a['units']):raise ValueError('Hint source/selected identities')
        for u in a['units']:
            if u['id'] in layouts:u['translation']=layouts[u['id']]
        scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_scripts=b['scripts'],literal_ids=b['selected_ids'],script_count=b['script_count'],max_literal_rows=3,max_line_advance=180,max_compiled_bytes=65535,preserve_literal_numerals=True,fullbox_capacity_profiles=b['fullbox_capacity_profiles'])
        if b['script_count']!=255 or int.from_bytes(native[:2],'little')!=510:raise ValueError('Hint table dimensions')
        result.append((b['draft_path'],row,a,scope,b,native,index))
    if len(result)!=19 or sum(len(x[2]['units']) for x in result)!=364:raise ValueError('Hint364 population')
    return result

def compile_inputs(source,common,plugins,work):
    from build_development_patch import compile_archive
    work.mkdir(parents=True)
    result=[]
    for path,row,a,scope,b,native,index in input_entries(source):
        raw,r=compile_archive(source,row,a,scope,common,plugins,work/a['archive'])
        if sha(raw)!=b['compiled_sha256'] or len(raw)!=b['compiled_bytes'] or r['layout']!=b['layout'] or r.get('fullbox_capacity_proof')!=b['fullbox_capacity_proof']:raise ValueError('Hint compiled preflight binding')
        r.update(script_count=255,navi_index=index,asset_path=path,asset_sha256=b['draft_sha256'],source_pointers=row['pointers'])
        result.append((raw,native,r,index))
    return result

def append(source,tail,payloads):
    out=bytearray(tail);table=[(0,0,0,0)]*23;records=[]
    def alloc(blob):
        out.extend(b'\xff'*(-len(out)%4));offset=len(source)+len(out);out.extend(blob);return offset
    for raw,native,record,index in payloads:
        if table[index]!=(0,0,0,0) or len(native)<510 or len(raw)>65535:raise ValueError('Hint descriptor source/bounds')
        np=alloc(native);cp=alloc(raw);table[index]=(0x08000000+cp,0x08000000+np,len(native),0)
        records.append(dict(record,rom_offset=cp,rom_sha256=sha(raw),native_copy_offset=np,native_copy_bytes=len(native),native_payload_sha256=sha(native),native_ram_archive_retained=True))
    if len(records)!=19:raise ValueError('Hint descriptor denominator')
    at=alloc(b''.join(struct.pack('<4I',*v) for v in table))
    return bytes(out),dict(descriptor_address=0x08000000+at),records

def verify_final(source,target,meta):
    inputs=input_entries(source);records=meta.get('hint_archives',[]);guard=meta.get('hint_guard')
    if len(records)!=19 or not guard or set(guard)!={'descriptor_address'}:raise ValueError('Hint final population')
    table=[(0,0,0,0)]*23;selected=set()
    for record,entry in zip(records,inputs):
        path,row,a,scope,b,native,index=entry;cp=record['rom_offset'];np=record['native_copy_offset'];raw=target[cp:cp+record['compiled_bytes']]
        if record['archive']!=a['archive'] or record['navi_index']!=index or record['asset_path']!=path or record['asset_sha256']!=b['draft_sha256'] or sha(raw)!=b['compiled_sha256'] or record['compiled_sha256']!=b['compiled_sha256'] or record['compiled_bytes']!=b['compiled_bytes'] or record['rom_sha256']!=b['compiled_sha256'] or record['layout']!=b['layout'] or record['translated_units']!=len(a['units']) or record.get('fullbox_capacity_proof')!=b['fullbox_capacity_proof']:raise ValueError('Hint final clone identity')
        if cp&3 or np&3 or not len(source)<=np<np+len(native)<=cp<cp+len(raw)<=guard['descriptor_address']-0x08000000 or record['native_ram_archive_retained'] is not True or record['source_pointers']!=row['pointers']:raise ValueError('Hint final placement/storage contract')
        if target[np:np+len(native)]!=native or record['native_copy_bytes']!=len(native) or record['native_payload_sha256']!=sha(native):raise ValueError('Hint entire native comparison copy')
        off=row['offset'];n=row['size']
        if target[off:off+n]!=source[off:off+n] or any(target[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('Original hint compressed storage/reference changed')
        table[index]=(0x08000000+cp,0x08000000+np,len(native),0);selected.update(b['selected_ids'])
    at=guard['descriptor_address']-0x08000000;expected=b''.join(struct.pack('<4I',*v) for v in table)
    if target[at:at+len(expected)]!=expected or len(selected)!=364:raise ValueError('Hint final descriptor binding')
    return selected
