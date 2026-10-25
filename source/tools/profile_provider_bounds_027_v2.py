"""Finite native direct-profile field applicability, not Hangul record support.

Bounds apply only to valid legacy records produced with the source profile
editor capacity; byte capacities alone are never treated as glyph counts.
Imported/corrupt records and array-backed producers are outside this contract.
"""
import struct
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read

FIELDS={
 'printSchool':(0,2,8,0x02000E75,17),
 'printFavFood':(6,8,8,0x02000FD7,17),
 'printDream':(8,10,8,0x0200101F,17),
 'printCrush':(9,11,8,0x02001031,17),
 'printIdol':(10,12,8,0x02001043,17),
 'printPlayerEnemy':(11,13,8,0x02001055,17),
 'printBestSubject':(13,15,4,0x0200109D,9),
 'printWorstSubject':(14,16,4,0x020010A7,9)
}

def bounds(source,rom):
    cfg=read('project.json')
    if sha(source)!=cfg['source_profile']['sha256']:raise ValueError('027 native profile revision')
    for a,n in ((0x34EFE,0x6A),(0x353B0,0x1D2),(0x3558C,0x22),(0x3B0D0,16*16),(0x526D0,28*8),(0x5290C,441*4),(0x38D9C,16),(0x355B6,64),(0x35000,50),(0x517D0,76)):
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('027 profile code/table applicability')
    widths=struct.unpack_from('<441I',source,0x5290C)
    if max(widths)!=11:raise ValueError('027 legacy metric bound')
    out={}
    for name,(row,index,cap,field,size) in FIELDS.items():
        at=0x3B0D0+row*16;record=source[at:at+16]
        if record[0]!=1 or record[1]!=index or record[2]!=cap or 0x02000950+struct.unpack_from('<H',record,14)[0]+1!=field:
            raise ValueError('027 source direct single-record profile mapping '+name)
        if struct.unpack_from('<II',source,0x526D0+index*8)!=(field,size) or size!=2*cap+1:raise ValueError('027 descriptor mapping '+name)
        out[name]=dict(profile_index=row,descriptor_index=index,logical_cap=cap,source_field=field,descriptor_bytes=size,max_advance=cap*max(widths),valid_native_editor_record_only=True,array_backed=False,suffix_appended=False)
    return out
