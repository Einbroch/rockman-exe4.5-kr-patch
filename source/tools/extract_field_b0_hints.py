"""Survey-only bounded B0 native hint table extraction; not product admission."""
import re,struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import parse_tpi,lz77_decompress
from textpet_korean import prepare_plugins,command
from build_development_patch import run_textpet
from tpl_literals import literals

OUT='analysis/field_b0_hints_v1'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rp=ROOT/'poc/output/pending500_022_v2.gba';require_hash(rp,'7363567b1263dac0700e2430da1046e47aa9ba65c8d9c2125b1ab9b3bd2928a1');rom=rp.read_bytes()
    proof=read('analysis/pending500_022_v2/display_runtime.json')
    if not proof['passed'] or proof['rom_sha256']!=sha(rom) or not proof['ordinary_native_hint_fallback_verified']:raise ValueError('Own022 normal B0 consumer evidence')
    if source[0x4F734:0x4F74A]!=bytes.fromhex('b1f7dafa8400084800f033f8005907499cf008fdf0bd') or source[0x4F7A6:0x4F7B6]!=bytes.fromhex('f0b557463f6c3e79803eb6008059f0bd') or rom[0x4F712:0x4F7B6]!=source[0x4F712:0x4F7B6]:raise ValueError('Native field loader/scene selector applicability')
    if struct.unpack_from('<I',source,0x54060)[0]!=0x08054238 or struct.unpack_from('<I',source,0x54064)[0]!=0x08054294 or source[0x54238:0x54294]!=rom[0x54238:0x54294]:raise ValueError('B0 23-slot table bounded by B1 reference')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);catalog=parse_tpi(ROOT/cfg['text_catalog']['path']);known={r['offset']:r for r in catalog}
    out=ROOT/OUT
    if out.exists():raise ValueError('Preserve extraction evidence')
    out.mkdir(parents=True);prepare_plugins(out/'plugins');common=command(out/'plugins');records=[];nulls=[];spans=[]
    for navi in range(23):
        slot=0x54238+navi*4;p=struct.unpack_from('<I',source,slot)[0]
        if p==0:nulls.append(navi);continue
        at=p-0x08000000
        if not 0<=at<len(source) or at&3:raise ValueError('Non-ROM/unaligned B0 source pointer')
        raw,used=lz77_decompress(source,at)
        if len(raw)<510 or int.from_bytes(raw[:2],'little')!=510 or source[at:at+used]!=rom[at:at+used]:raise ValueError('B0 native255 source/archive unchanged')
        arc=f'{at:X}';work=out/arc;work.mkdir();native=work/f'{arc}.msg';native.write_bytes(raw);tpl=work/'source.tpl';rebuilt=work/'native-rebuilt.msg'
        run_textpet(common+['Read-Text-Archives',str(native),'--format','bin','Write-Text-Archives',str(tpl),'--format','tpl'],work/'extract.log')
        run_textpet(common+['Read-Text-Archives',str(tpl),'--format','tpl','Write-Text-Archives',str(rebuilt),'--format','bin'],work/'roundtrip.log')
        if rebuilt.read_bytes()!=raw:raise ValueError('B0 native exact byte roundtrip '+arc)
        text=tpl.read_text(encoding='utf-8-sig');items=literals(text)
        if not re.search(r'^@size\s+255$',text,re.M):raise ValueError('B0 exported script denominator')
        records.append(dict(archive=arc,navi_index=navi,source_pointer=slot,source_address=p,source_bytes=len(raw),source_payload_sha256=sha(raw),compressed_bytes_consumed=used,source_compressed_sha256=sha(source[at:at+used]),source_tpl=dict(path=str(tpl.relative_to(ROOT)),sha256=sha(tpl.read_bytes())),native_roundtrip=True,exact_catalog_row=at in known,literal_units=len(items),source_characters=sum(len(u.text) for u in items),units=[dict(id=u.key,source=u.text,language=u.language,state='untranslated') for u in items]));spans.append((at,at+used));print('B0 source',arc,'Navi',navi,'units',len(items),'roundtrip PASS',flush=True)
    if nulls!=[13,14] or len(records)!=21 or any(b>c for (a,b),(c,d) in zip(sorted(spans),sorted(spans)[1:])):raise ValueError('B0 finite source table/null/storage population')
    frozen_write(out/'extraction.json',dict(schema=1,status='SURVEY_EXTRACTION_NOT_PRODUCT_ADMISSION',source_sha256=sha(source),baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(rom),scene_major=0xB0,source_root_table=0x53FA0,scene_pointer_offset=0x54060,navi_table_offset=0x54238,navi_table_slots=23,null_navi_indices=nulls,archives=records,archive_count=len(records),literal_units=sum(r['literal_units'] for r in records),uncatalogued_archives=sum(not r['exact_catalog_row'] for r in records),runtime_proof=dict(path='analysis/pending500_022_v2/display_runtime.json',sha256=sha((ROOT/'analysis/pending500_022_v2/display_runtime.json').read_bytes()),sample='Normal B0/Navi0 hint source78BF28/root0203D800 observed twice; remaining20 share the static loader/index rule, not separately runtime-tested'),rom_written=False,release_eligible=False,limits='Exhaustive only for this declared23-slot B0 table. No whole-game inventory, translation, pointer-reference completeness, Korean storage/capacity, product registration or other Navi/event runtime approval. Third-party TPI remains unchanged.'))
    print('PASS B0 bounded extraction:',len(records),'archives;',sum(r['literal_units'] for r in records),'literal units; catalog gaps',sum(not r['exact_catalog_row'] for r in records))

if __name__=='__main__':main()
