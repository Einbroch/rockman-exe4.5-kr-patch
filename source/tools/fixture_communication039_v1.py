"""039 communication CPU-memory fixture; comparison038 is NOT product input.

No GBA file is emitted. Product integration must independently rebuild from
the immutable source and authored canonical/layout assets.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from communication_rom_selector039_v1 import source_population,wrap
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL
from prepare_repartition500 import layout_records

OUT='analysis/pending_insertion_500_039_communication_words_v1'


def construct():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/OUT/'selection.json','966a22eca30229b56984dead96e05d4c71bf0f3a8e464225432ea9ae3bdb1c08')
    require_hash(ROOT/OUT/'verification_v1.json','c838e808f881b49a936fa218c9b73ddefb09982098c426bebf95200934918576')
    s=read(OUT+'/selection.json');v=read(OUT+'/verification_v1.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);base=(ROOT/s['baseline_rom']).read_bytes();meta=read(s['baseline_rom'].replace('.gba','.json'))
    for report in (s,v):
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
    if not v['passed'] or v['units']!=500 or v['rom_written'] or v['units_with_Hangul_syllable_break_proposal']:raise ValueError('039 exact500 source prerequisite')
    oldids={u['id'] for r in layout_records(meta) for u in r['layout']};current={r['archive'] for r in layout_records(meta)}
    ids=[u['id'] for r in v['archives'] for u in r['units']]
    if len(ids)!=500 or len(set(ids))!=500 or set(ids)!=set(s['selected_ids']) or set(ids)&oldids or {r['archive'] for r in v['archives']}&current:raise ValueError('039 new500/no carry ownership')
    pool=source_population(source,{r['archive'] for r in v['archives']});indexed={p['archive']:p for p in pool};image=bytearray(base);guards=[]
    def alloc(data):
        image.extend(b'\xff'*(-len(image)%4));at=0x08000000+len(image);image.extend(data);return at
    for r in v['archives']:
        require_hash(ROOT/r['compiled']['path'],r['compiled']['sha256']);target=(ROOT/r['compiled']['path']).read_bytes();native=indexed[r['archive']]['payload']
        if sha(native)!=r['source_sha256'] or struct.unpack_from('<H',native)[0]//2!=r['script_count']:raise ValueError('039 source/script identity')
        np=alloc(native);cp=alloc(target)
        guards.append(dict(archive=r['archive'],native=native,target=target,native_at=np,clone=cp,scripts=r['script_count']))
    desc=alloc(b''.join(struct.pack('<4I',g['clone'],g['native_at'],len(g['native']),g['scripts']) for g in guards))
    image.extend(b'\xff'*(-len(image)%4));at=0x08000000+len(image);previous=0x08000000+meta['keyitem_rom']['npc038']['code_offset'];code,proof=wrap(source,at,previous,desc,len(guards));image.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=at|1));oldstub=base[INSTALL:INSTALL+12]
    if len(stub)!=12 or len(guards)!=17:raise ValueError('039 fixture population/stub')
    image[INSTALL:INSTALL+12]=stub
    if image[:INSTALL]!=base[:INSTALL] or image[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('039 comparison predecessor drift')
    return source,base,meta,bytes(image),guards,pool,dict(wrapper=proof,stub=stubproof,code_address=at,descriptor_address=desc,previous_wrapper_address=previous,fixture_sha256=sha(image),fixture_bytes=len(image),new_stub=stub,old_stub=oldstub)
