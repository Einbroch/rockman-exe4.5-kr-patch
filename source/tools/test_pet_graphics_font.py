import copy,json,unittest
from build_visibility_poc import ROOT,sha
from pet_graphics_font import construct,glyphs
from prepare_pet_graphics_v2 import decode,TILES,BASE

class PetPixelFontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
        cls.source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()

    def test_protected_pixels_and_exact_glyph(self):
        target,m=construct(self.source,self.asset)
        self.assertEqual(m['translated_graphic_labels'],7)
        self.assertTrue(m['glyphs_unscaled']);self.assertTrue(m['unchanged_roundtrip'])
        g=glyphs(self.asset);self.assertNotEqual(g['통'],g['동'])
        self.assertEqual(g['통']['bits'],[124,120,64,124,16,254,68,56])
        for left,right in TILES:
            original=decode(self.source[BASE:BASE+0x1200],left,right);actual=decode(target,left,right)
            for y in range(16):
                for x in range(64):
                    if not(1<=x<64 and 1<=y<9):self.assertEqual(actual[y][x],original[y][x])

    def test_bad_wording_spacing_and_tong_rejected(self):
        for field in ['wording','spacing','tong','source']:
            a=copy.deepcopy(self.asset)
            if field=='wording':a['units'][5]['translation']='동신'
            if field=='spacing':a['units'][3]['advance']=8
            if field=='tong':a['glyph_overrides']['통']['bits'][1]=64
            if field=='source':a['source_block_sha256']='0'*64
            with self.assertRaises(ValueError):construct(self.source,a)

if __name__=='__main__':unittest.main()
