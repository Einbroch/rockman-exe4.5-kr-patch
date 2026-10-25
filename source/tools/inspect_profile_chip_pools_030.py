"""Finite native stats chip-name pools; not Korean chip-name admission."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from archive_scripts import script_spans
from verify_tpi_index import parse_tpi

ROM='poc/output/pending500_029_v1.gba'
ROM_SHA='a089f2e0abd7fa2fc9af25549dbce6737f37487fc5a304434c5893b05dce4ff5'
OUT='analysis/pending_insertion_500_030_chip_pools_v1/census.json'
CHIPS={'printFavStandardChip1':(21,23,5),'printFavStandardChip2':(22,24,6),'printFavStandardChip3':(23,25,7),'printFavMegaChip':(24,26,8),'printFavGigaChip':(25,27,9)}

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/ROM,ROM_SHA);rom=(ROOT/ROM).read_bytes()
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows={r['offset']:r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};metrics=struct.unpack_from('<441I',source,0x5290C);records=[];fields={}
    for base,count,first in ((0x765190,256,0),(0x765B18,137,256)):
        row=rows[base];raw=source[base:base+row['size']]
        if raw!=rom[base:base+row['size']]:raise ValueError('030 shared native chip-name pool changed')
        spans=script_spans(raw,count)
        for index,blob in enumerate(spans):
            if not blob or blob[-1]!=0xE5 or any(ch>=0xE4 for ch in blob[:-1]) or len(blob)>9:raise ValueError('030 native simple bounded name population')
            offset=base+struct.unpack_from('<H',raw,2*index)[0]
            records.append(dict(chip_id=first+index,source_offset=offset,raw_hex=blob.hex(),glyphs=len(blob)-1,advance=sum(metrics[ch] for ch in blob[:-1])))
    for at in (0x3866C,0x38670):
        if source[at:at+4]!=rom[at:at+4]:raise ValueError('030 actual stats shared lookup root drift')
    for name,(row,index,category) in CHIPS.items():
        raw=source[0x3B0D0+16*row:0x3B0E0+16*row];field,size=struct.unpack_from('<II',source,0x526D0+8*index)
        hist,dest,flag=struct.unpack_from('<III',source,0x38A10+12*category)
        if raw[:3]!=bytes([1,index,8]) or size!=17 or dest+1!=field or 0x02000950+struct.unpack_from('<H',raw,14)[0]!=dest or struct.unpack_from('<H',raw,12)[0]!=flag:raise ValueError('030 stats row/descriptor/writer table')
        fields[name]=dict(row=row,index=index,category=category,history=hist,record=dest,field=field,bytes=size,flag=flag,finite_native_name_advance=max(r['advance'] for r in records))
    deps=['tools/inspect_profile_chip_pools_030.py',cfg['text_catalog']['path']]
    frozen_write(ROOT/OUT,dict(schema=1,status='FINITE_NATIVE_CHIP_POOL_ANALYSIS_NOT_PRODUCT_ADMISSION',source_sha256=sha(source),baseline_rom=ROM,baseline_sha256=sha(rom),names=records,name_count=len(records),maximum_glyphs=max(r['glyphs'] for r in records),maximum_advance=max(r['advance'] for r in records),maximum_name_bytes=max(len(bytes.fromhex(r['raw_hex'])) for r in records),fields=fields,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,product_admitted=False,limits='393 immutable native chip names and current029 stats roots only. No stats producer CPU, GBA consumer, natural battle acquisition or Korean-name serialization proof. Shared native pools deliberately stay Japanese; private Korean library/battle names do not automatically apply here.'))
    print('030 finite native chip names',len(records),'maxglyph',max(r['glyphs'] for r in records),'maxadvance',max(r['advance'] for r in records),'NO ROM written')

if __name__=='__main__':main()
