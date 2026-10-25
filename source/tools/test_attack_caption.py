import json,unittest
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from attack_caption import construct,decode,encode,BASE,STORED,TILES,BYTES
from verify_tpi_index import lz77_decompress

def read(p):return json.loads(p.read_text(encoding='utf-8'))

class AttackCaptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();cls.asset=read(ROOT/'translations/equipment_attack_caption_ko.json')
    def test_native_slot_and_protected_payload_pixels(self):
        stored,payload,m=construct(self.source,self.asset);old,_=lz77_decompress(self.source,BASE)
        self.assertEqual(len(stored),STORED);self.assertEqual(m['compressed_bytes'],456)
        self.assertEqual(payload[:TILES],old[:TILES]);self.assertEqual(payload[TILES+BYTES:],old[TILES+BYTES:])
        a,b=decode(old[TILES:TILES+BYTES]),decode(payload[TILES:TILES+BYTES]);self.assertEqual(encode(a),old[TILES:TILES+BYTES])
        for y in range(16):
            for x in range(96):
                if not(7<=x<67 and 4<=y<15):self.assertEqual(a[y][x],b[y][x])
        self.assertEqual(lz77_decompress(stored,0)[0],payload)
    def test_source_and_adopted_boundaries_fail_closed(self):
        for key,value in [('edit_rect',[0,0,96,16]),('translation','공격력'),('release_eligible',True),('source_offset',BASE+4)]:
            bad=deepcopy(self.asset);bad[key]=value
            with self.assertRaises(ValueError):construct(self.source,bad)
        bad=bytearray(self.source);bad[BASE]^=1
        with self.assertRaises(ValueError):construct(bytes(bad),self.asset)
    def test_integrated_native_decompression_and_all_caption_masks(self):
        from report_attack_caption_runtime import main
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible'])
        self.assertEqual(r['translated_text_units'],798);self.assertEqual(r['new_graphic_labels'],1)
        self.assertEqual(len(r['native_decompressions']),2);self.assertEqual(len(r['pages']),4)
        self.assertTrue(all(p['caption_vram_objects_pixels_match'] and p['attack_number_unchanged'] for p in r['pages']))
        mainrom=(ROOT/'poc/output/exe45_ko_development_attack_caption_v2.gba').read_bytes()
        self.assertEqual(mainrom,(ROOT/'poc/output/exe45_ko_development_attack_caption_v1.gba').read_bytes())
        self.assertEqual(mainrom,(ROOT/'poc/output/exe45_ko_development_attack_caption_v2_repro.gba').read_bytes())

if __name__=='__main__':unittest.main()
