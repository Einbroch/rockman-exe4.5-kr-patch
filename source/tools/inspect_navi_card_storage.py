"""Read-only source LZ hypotheses matched to observed native OBJ label tiles."""
import json,struct,re
from build_visibility_poc import ROOT,sha
from verify_tpi_index import lz77_decompress

def main():
    source=(ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
    folder=ROOT/'poc/runtime/native-keyboard-labels-v1-complete'
    vram=(folder/'step_023_gbaVideoRam.bin').read_bytes()
    needle=vram[0x15000:0x15080]
    results=[]
    for at in range(0x500000,0x650000,4):
        if source[at]!=0x10:continue
        n=int.from_bytes(source[at+1:at+4],'little')
        if not 128<=n<=0x20000 or n%32 not in (0,4):continue
        try:p,used=lz77_decompress(source,at)
        except (ValueError,IndexError):continue
        hit=p.find(needle)
        if hit<0:continue
        refs=[m.start() for m in re.finditer(re.escape(struct.pack('<I',0x08000000+at)),source)]
        results.append(dict(offset=at,stored_bytes=used,payload_bytes=len(p),needle_payload_offset=hit,pointers=refs,stored_sha256=sha(source[at:at+used])))
    out=ROOT/'analysis/navi_card_graphics_v1';out.mkdir(exist_ok=True)
    report=dict(source_sha256=sha(source),runtime_rom_sha256=json.loads((folder/'result.json').read_text(encoding='utf8'))['rom_sha256'],target_vram_offset=0x15000,target_bytes=128,target_sha256=sha(needle),scan_range=[0x500000,0x650000],candidates=results,scope='Read-only candidate search. No edit or reference completeness claim.')
    (out/'storage_candidates.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
