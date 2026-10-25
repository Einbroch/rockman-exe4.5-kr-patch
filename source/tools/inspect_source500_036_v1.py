"""Static native lookup classification for prepared036; never writes ROM."""
import struct
from prepare_source500_036_v1 import baseline,read,ROOT,OUT,ref,need,sha,require_hash,frozen_write
from verify_tpi_index import lz77_decompress


def inspect(source,rom,selection,compiled):
    for a,b in [(0x4F712,0x4F764),(0x4F764,0x4F7B6)]:need(source[a:b]==rom[a:b],'Native loader/reader changed')
    need(struct.unpack_from('<I',source,0x4F750)[0]==0x02039800,'Native NPC destination')
    need(struct.unpack_from('<I',source,0x4F78C)[0]==0x02039800,'Native cached NPC root')
    need(source[0x4F790:0x4F7A6]==bytes.fromhex('f0b557463f6c3e79803e7f79b600bf008059c059f0bd'),'Scene/sub lookup ABI')
    population=[]
    for scene in [0xA0,0xA1,0xA3]:
        top=0x53700+(scene-0x80)*4;table=struct.unpack_from('<I',source,top)[0]-0x08000000
        need(source[top:top+4]==rom[top:top+4] and source[table:table+16]==rom[table:table+16],'Scene lookup metadata preserved')
        for sub in range(4):
            slots=struct.unpack_from('<I',source,table+sub*4)[0]-0x08000000
            for slot in range(7):
                p=slots+slot*4;off=struct.unpack_from('<I',source,p)[0]-0x08000000
                payload,used=lz77_decompress(source,off)
                need(source[p:p+4]==rom[p:p+4] and source[off:off+used]==rom[off:off+used] and payload[:2]==b'\xfe\x01','Retained source population')
                population.append(dict(scene=scene,sub=sub,slot=slot,pointer=p,archive=f'{off:X}',payload=payload))
    records=[]
    for ar in compiled['archives']:
        g=next(g for g in selection['groups'] if g['archive']==ar['archive']);matches=[r for r in population if r['archive']==ar['archive']]
        need(len(matches)==1,'Unique native lookup for selected archive');r=matches[0]
        need(g['source_row']['pointers']==[r['pointer']] and sha(r['payload'])==ar['source_payload_sha256'],'Source catalog/compile lookup binding')
        for other in population:
            if other['scene']==r['scene'] and other['archive']!=r['archive']:
                n=min(len(other['payload']),len(r['payload']))
                need(other['payload'][:n]!=r['payload'][:n],'Ambiguous within-scene native identity')
        records.append(dict(archive=r['archive'],scene=r['scene'],sub=r['sub'],slot=r['slot'],pointer=r['pointer'],native_root=0x02039800,source_bytes=len(r['payload']),compiled_bytes=ar['compiled_bytes'],native_loader_retained=True,product_admitted=False))
    return records


def main():
    cfg,source,rom,m=baseline();s=read(OUT+'/selection.json');v=read(OUT+'/verification_v2.json')
    require_hash(ROOT/v['selection']['path'],v['selection']['sha256'])
    need(v['passed'] and v['units']==500,'Complete source compile prerequisite')
    records=inspect(source,rom,s,v);refusals=[]
    for at in [0x4F724,0x4F750,0x4F76E,0x4F78C,0x4F790,0x53784,0x5378C,0x539BC,0x53AFC]:
        bad=bytearray(rom);bad[at]^=1
        try:inspect(source,bytes(bad),s,v)
        except ValueError as e:refusals.append(dict(offset=at,reason=str(e)))
        else:raise ValueError('Missed native lookup corruption')
    frozen_write(ROOT/OUT/'loader_analysis_v1.json',dict(passed=True,scope='STATIC retained-source native NPC lookup only; NOT new selector installation or runtime',baseline_rom='poc/output/pending500_035_v2.gba',baseline_sha256=sha(rom),compile=ref(ROOT/OUT/'verification_v2.json'),source_population_count=84,archives=records,negative_mutations=refusals,tools=[ref(ROOT/'tools/inspect_source500_036_v1.py')],rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,limits=['All20 sources use the same native NPC root02039800, but70 units belong to sceneA1/A3 and current035 guard intentionally admitsA0 only.','Any036 selector must retain035 data/old paths, validate identity per scene and original callerLR4F773, and prove current placements/CPU/runtime/rebuild before ROM promotion.','No decompression expansion or free-RAM claim. Native source compressed bytes and pointers remain unchanged.']))
    print('PASS036 static20-source lookup,84 native population entries,9 mutation refusals; NO ROM')


if __name__=='__main__':main()
