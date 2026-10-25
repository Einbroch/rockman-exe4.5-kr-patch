"""Exact adjacent duplicate sharing keeps the selected payload inside source extent.

Only native scripts10 and11 (identical45-byte descriptions) share storage.
The game indexes start offsets independently (0804FB74..7C), not next offsets.
TextPet's monotone span exporter treats aliases as empty, so native-resolved
script-byte equivalence is checked separately after standard TPL round trips.
"""
import struct
from build_visibility_poc import sha
from archive_scripts import script_spans

SOURCE_SHA='15bbcb0dc3e2fa083d55b00fb4180312836bef14fbd2d9f63e2d82f05760d793'
DESTINATIONS=[0x02020800,0x02031000]
READER=bytes.fromhex('4900415a4018e8626863')

def resolved(payload):
    script_spans(payload,49)
    offsets=list(struct.unpack_from('<49H',payload))
    ends=sorted(set(offsets+[len(payload)]))
    return [payload[o:next(x for x in ends if x>o)] for o in offsets]

def validate_source(rom,source):
    if len(source)!=1291 or sha(source)!=SOURCE_SHA:
        raise ValueError('keyitem immutable payload mismatch')
    if rom[0x4fb74:0x4fb7e]!=READER:
        raise ValueError('keyitem independent offset reader changed')
    for pointer in [0x34a2c,0x4c5e8]:
        if struct.unpack_from('<I',rom,pointer)[0]!=0x08709408:
            raise ValueError('keyitem source root changed')
    if (struct.unpack_from('<I',rom,0x34a30)[0],struct.unpack_from('<I',rom,0x4c5f0)[0])!=tuple(DESTINATIONS):
        raise ValueError('keyitem native destinations changed')

def compact(source,payload):
    if sha(source)!=SOURCE_SHA:raise ValueError('keyitem source mismatch')
    spans=script_spans(payload,49)
    if spans[10]!=spans[11] or len(spans[10])!=45:
        raise ValueError('keyitem exact adjacent duplicate changed')
    offsets=list(struct.unpack_from('<49H',payload));a,b=offsets[10],offsets[11]
    if b-a!=45:raise ValueError('keyitem duplicate extent')
    result=bytearray(payload[:a]+payload[b:])
    moved=[o-45 if o>=b else o for o in offsets]
    struct.pack_into('<49H',result,0,*moved)
    result=bytes(result)
    before=resolved(source);after=resolved(result);compiled=resolved(payload)
    changed=set(range(21,33))
    if any(before[i]!=after[i] for i in range(49)if i not in changed):
        raise ValueError('unselected native-resolved keyitem bytes changed')
    if any(compiled[i]!=after[i]for i in range(49)):
        raise ValueError('sharing changed compiled consumption')
    if len(result)>len(source):raise ValueError('keyitem exceeds source residency extent')
    return result,dict(method='exact adjacent duplicate10/11 shared start; native independent lookup',
        saved_bytes=45,source_extent=len(source),compiled_bytes=len(payload),final_bytes=len(result),
        duplicate_script_ids=[10,11],unchanged_native_resolved_scripts=[i for i in range(49)if i not in changed],
        existing_empty_alias_ids=sorted(changed),no_destination_growth=True,
        capacity_policy='Both unchanged destinations receive no more bytes than original1291; not maximum-allocation claim',
        destinations=DESTINATIONS)
