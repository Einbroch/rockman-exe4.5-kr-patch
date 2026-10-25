"""040 deterministic CPU-memory-only composition. No ROM files emitted.

039 ROM is a comparison fixture, never a primary product build input.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from consumer_links040_v1 import source_population,CLASSES
from typed_rom_selector040_v1 import wrap
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL

SOURCE='analysis/pending_insertion_500_040_source_v2'
BASE='poc/output/pending500_039_v1.gba'
BASE_SHA='bfb80e29c8f72ed4595a0453ca43fa6445a94d98d6d2054158f886fde2b38430'


def construct():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();meta=read(BASE.replace('.gba','.json'))
    require_hash(ROOT/SOURCE/'selection.json','d386fed7afbd483b43b1bc5d0c7073b360fed7fd20890fa70038b029a7670bb8');require_hash(ROOT/SOURCE/'verification_v1.json','eaf2793403d87840e55474bcddb18af2c78623dfcba02af57c3bd15475e60b66');s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v1.json')
    for r in (s,v):
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
    if not v['passed'] or v['units']!=500 or v['inherited_units']!=8 or v['rom_written']:raise ValueError('040 source500/carry8 prerequisite')
    chosen={g['archive']:g['source_class'] for g in s['groups']};pool=source_population(source,chosen);image=bytearray(base);guards=[]
    def alloc(data):
        image.extend(b'\xff'*(-len(image)%4));at=0x08000000+len(image);image.extend(data);return at
    for r in v['archives']:
        require_hash(ROOT/r['compiled']['path'],r['compiled']['sha256']);target=(ROOT/r['compiled']['path']).read_bytes();p=next(p for p in pool if (p['archive'],p['source_class'])==(r['archive'],chosen[r['archive']]));native=p['payload']
        if sha(native)!=r['source_sha256'] or struct.unpack_from('<H',native)[0]//2!=r['script_count']:raise ValueError('040 native/script identity')
        np=alloc(native);cp=alloc(target);guards.append(dict(archive=r['archive'],source_class=p['source_class'],native=native,target=target,native_at=np,clone=cp,scripts=r['script_count'],**CLASSES[p['source_class']]))
    desc=alloc(b''.join(struct.pack('<7I',g['clone'],g['native_at'],len(g['native']),g['scripts'],g['root'],g['caller_lr'],g['outer_lr']) for g in guards));image.extend(b'\xff'*(-len(image)%4));at=0x08000000+len(image);previous=0x08000000+meta['keyitem_rom']['communication039']['code_offset'];code,proof=wrap(source,at,previous,desc,len(guards));image.extend(code);stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=at|1));old=base[INSTALL:INSTALL+12]
    if len(stub)!=12 or len(guards)!=10:raise ValueError('040 composed single stub/population')
    image[INSTALL:INSTALL+12]=stub
    if image[:INSTALL]!=base[:INSTALL] or image[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('040 predecessor039 prefix drift')
    return source,base,meta,bytes(image),guards,pool,dict(wrapper=proof,stub=stubproof,code_address=at,descriptor_address=desc,previous_wrapper_address=previous,fixture_sha256=sha(image),fixture_bytes=len(image),new_stub=stub,old_stub=old)
