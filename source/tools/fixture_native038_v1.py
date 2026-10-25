"""Deterministic CPU-memory-only038 composition, never a ROM writer."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from prepare_source500_038_v5 import baseline,OUT as SOURCE
from field_native_rom_selector_038_v1 import source_population,wrap
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL

def construct():
    cfg,source,base,meta=baseline();carry=read('analysis/pending_insertion_500_038_carry_v2/verification_v1.json');tailcpu=read('analysis/pending_insertion_500_038_native_tails_v1/cpu.json');pre=read(SOURCE+'/preflight_v1.json')
    if not all(r['passed'] and not r['rom_written'] for r in (carry,tailcpu,pre)) or carry['new_units']!=500:raise ValueError('038 source/carry/native tail prerequisites')
    for r in (carry,tailcpu,pre):
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
    chosen={r['archive']:dict(source_class=r['source_class'],scene=r['source_lookup_candidates'][0]['scene'],target_sha256=r['compiled']['sha256'],script_count=r['script_count']) for r in carry['archives']}
    pool=source_population(source,chosen);image=bytearray(base);guards=[]
    def alloc(data):
        image.extend(b'\xff'*(-len(image)%4));at=len(image);image.extend(data);return at
    for r in carry['archives']:
        require_hash(ROOT/r['compiled']['path'],r['compiled']['sha256']);target=(ROOT/r['compiled']['path']).read_bytes();found=[p for p in pool if p['archive']==r['archive']]
        if len(found)!=1:raise ValueError('038 explicit source uniqueness')
        p=found[0];np=alloc(p['payload']);cp=alloc(target)
        guards.append(dict(archive=r['archive'],scene=p['scene'],root=p['root'],caller=p['caller_lr'],source_class=p['source_class'],native=p['payload'],target=target,native_at=0x08000000+np,clone=0x08000000+cp,scripts=r['script_count']))
    desc=alloc(b''.join(struct.pack('<7I',g['clone'],g['native_at'],len(g['native']),g['scene'],g['root'],g['caller'],g['scripts']) for g in guards));image.extend(b'\xff'*(-len(image)%4));at=0x08000000+len(image);previous=0x08000000+meta['keyitem_rom']['npc037']['code_offset'];code,proof=wrap(source,at,previous,0x08000000+desc,len(guards));image.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=at|1));oldstub=base[INSTALL:INSTALL+12]
    if len(stub)!=12 or len(guards)!=66:raise ValueError('038 stub/descriptor population')
    image[INSTALL:INSTALL+12]=stub
    if image[:INSTALL]!=base[:INSTALL] or image[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('038 predecessor image drift')
    return source,base,meta,bytes(image),guards,pool,dict(wrapper=proof,stub=stubproof,code_address=at,descriptor_offset=desc,previous_wrapper_address=previous,fixture_sha256=sha(bytes(image)),fixture_bytes=len(image),new_stub=stub,old_stub=oldstub)
