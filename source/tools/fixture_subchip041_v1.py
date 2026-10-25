"""041 subchip102 component in CPU memory only; no playable ROM emitted.

Existing040 image is a differential comparison fixture, never primary input.
All new target bytes come from pinned authored carry assets/source originals.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress
from archive_scripts import verify_untouched_scripts
from subchip_rom_selector041_v1 import wrap
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL

SOURCE='analysis/pending_insertion_500_041_source_v8'


def construct():
    s=read(SOURCE+'/selection.json');boundary=read(SOURCE+'/subchip_boundary_v1.json');carry=read(SOURCE+'/carry_verification_v2.json');v=read(SOURCE+'/verification_v3.json');cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);base=(ROOT/s['baseline_rom']).read_bytes();meta=read(s['baseline_rom'].replace('.gba','.json'))
    if not boundary['passed'] or boundary['baseline_sha256']!=s['baseline_sha256'] or boundary['native_consumer_contract_units']!=102 or not carry['passed'] or not v['passed']:raise ValueError('041 subchip native/source prerequisite')
    groups={r['archive']:r for r in boundary['source_consumer_records']};image=bytearray(base);guards=[];ids=set()
    def alloc(b):
        image.extend(b'\xff'*(-len(image)%4));address=0x08000000+len(image);image.extend(b);return address
    for arc,binding in sorted(groups.items()):
        r=next(r for r in carry['archives'] if r['archive']==arc);sr=next(r for r in v['archives'] if r['archive']==arc)
        for k in ('asset','compiled','target_tpl'):require_hash(ROOT/r[k]['path'],r[k]['sha256'])
        if r['inherited_ids'] or set(r['new_ids'])!=set(binding['selected_ids']):raise ValueError('041 exact selected subchip no inherited consumer')
        native=lz77_decompress(source,int(arc,16))[0];target=(ROOT/r['compiled']['path']).read_bytes();scripts=binding['selected_scripts'];count=sr['script_count']
        if sha(native)!=binding['native_sha256'] or count!=int.from_bytes(native[:2],'little')//2 or not 0<count<=32 or any(not 0<=n<count for n in scripts) or not native or len(target)>65535:raise ValueError('041 native/count/mask applicability')
        verify_untouched_scripts(native,target,count,set(scripts));asset=read(r['asset']['path'])
        if {u['id'] for u in asset['units']}!=set(r['new_ids']) or asset['source_sha256']!=sha(source):raise ValueError('041 authored exact subchip population')
        for ref in binding['references']:
            p=ref['pointer']
            if base[p:p+4]!=source[p:p+4] or int.from_bytes(source[p:p+4],'little')!=0x08000000+int(arc,16):raise ValueError('041 original table preserved')
        np=alloc(native);cp=alloc(target);mask=sum(1<<n for n in scripts);ids.update(r['new_ids']);guards.append(dict(archive=arc,native=native,target=target,native_at=np,clone=cp,scripts=count,selected_scripts=scripts,selected_ids=r['new_ids'],mask=mask,root=0x02026C00,caller_lr=0x0804F7BD,outer_lr=0x08041D8F))
    if len(guards)!=21 or len(ids)!=102:raise ValueError('041 exact subchip102/21 fixture')
    for a in guards:
        for b in guards:
            n=min(len(a['native']),len(b['native']))
            if a is not b and a['native'][:n]==b['native'][:n]:raise ValueError('041 ambiguous finite native pool prefix')
    desc=alloc(b''.join(struct.pack('<5I',g['clone'],g['native_at'],len(g['native']),g['scripts'],g['mask']) for g in guards));image.extend(b'\xff'*(-len(image)%4));address=0x08000000+len(image);previous=0x08000000+meta['keyitem_rom']['typed040']['code_offset'];code,proof=wrap(address,previous,desc,len(guards));image.extend(code)
    stub,sp=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=address|1));old=base[INSTALL:INSTALL+12]
    if len(stub)!=12 or int.from_bytes(old[8:12],'little')!=previous|1:raise ValueError('041 exact040 wrapper trampoline predecessor')
    image[INSTALL:INSTALL+12]=stub
    if image[:INSTALL]!=base[:INSTALL] or image[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('041 fixture changes outside single composed stub')
    return source,base,meta,bytes(image),guards,dict(wrapper=proof,stub=sp,code_address=address,descriptor_address=desc,previous_wrapper_address=previous,fixture_sha256=sha(image),fixture_bytes=len(image),new_stub=stub,old_stub=old)
