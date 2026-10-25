"""Source table census for NEXT investigation only, not width admission.

Separate editor logical caps from scratch descriptor capacities. A table row
does not establish the cache writer, its selected record, or a terminator.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    cfg=read('project.json');p=ROOT/cfg['source_profile']['filename'];require_hash(p,cfg['source_profile']['sha256']);source=p.read_bytes();rows=[]
    for row in range(16):
        at=0x3B0D0+row*16;raw=source[at:at+16];count,index,cap,heading=raw[:4]
        if count<=1:continue
        ptr,n=struct.unpack_from('<II',source,0x526D0+index*8)
        rows.append(dict(profile_row=row,table_offset=at,raw_hex=raw.hex(),table_count=count,descriptor_index=index,logical_editor_cap_argument=cap,heading_script=heading,record_base_candidate=0x02000950+struct.unpack_from('<H',raw,14)[0],descriptor_string=ptr,descriptor_copy_bytes=n,scratch_descriptor_not_direct_saved_field=True,width_bound_adopted=False,cache_writer_and_terminator_proven=False))
    deps=['tools/inspect_profile_array_candidates_028.py','tools/profile_provider_bounds_027_v2.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_028_array_candidates_v1/source_tables.json',dict(schema=1,status='SOURCE_TABLE_CANDIDATES_NOT_ADOPTED_PROVIDER_MODEL',source_sha256=sha(source),rows=rows,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,product_admitted=False,limits='Byte2 is the existing initializer cap argument, not proof of every final cache value. Descriptor13/17 bytes never become a glyph count. Need selected-record/cache producer, all valid terminator paths, suffix/append behavior, native writer/reader CPU and GBA consumption before enabling printFriend/printHobby/printFavShow/printWish or sibling providers. Current028 still uses only adopted eight direct-field providers.'))
    print('Recorded',len(rows),'source array-table candidates; NO new provider admitted')


if __name__=='__main__':main()
