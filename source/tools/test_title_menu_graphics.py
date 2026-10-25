"""Exercise source rejection, wording integrity, tile inverse and slot bounds."""
import copy
import json
import unittest
from build_visibility_poc import ROOT
from title_menu_graphics import construct, decode, encode, BASE, STORED
from verify_tpi_index import lz77_decompress


class TitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()
        cls.asset=json.loads((ROOT/'translations/title_menu_graphics_ko.json').read_text(encoding='utf-8'))

    def test_construct_and_protected_tiles(self):
        stored,record=construct(self.source,self.asset)
        self.assertEqual(len(stored),STORED)
        before,_=lz77_decompress(self.source,BASE);after,_=lz77_decompress(stored,0)
        self.assertEqual(before[:4],after[:4])
        # Third menu option and both spacers are not editable.
        for row in (0,1):
            for col in list(range(6,10))+list(range(16,26)):
                start=4+(row*26+col)*32
                self.assertEqual(before[start:start+32],after[start:start+32])

    def test_all_palette_nibbles_roundtrip(self):
        payload=bytearray(1668)
        for col in (0,10):
            rows=[[(x+y)%16 for x in range(48)] for y in range(16)]
            encode(payload,rows,col)
            self.assertEqual(decode(payload,col),rows)

    def test_weekend_preserves_prior_labels_and_spacing(self):
        asset=json.loads((ROOT/'translations/title_menu_weekend_graphics_ko.json').read_text(encoding='utf-8'))
        stored,record=construct(self.source,asset)
        old,_=construct(self.source,self.asset)
        before,_=lz77_decompress(old,0);after,_=lz77_decompress(stored,0)
        self.assertEqual(record['translated_graphic_labels'],3)
        for row in (0,1):
            start=4+row*26*32
            self.assertEqual(before[start:start+16*32],after[start:start+16*32])
        self.assertNotEqual(decode(before,16,80),decode(after,16,80))

    def test_wrong_source_rejected(self):
        wrong=bytearray(self.source);wrong[BASE]^=1
        with self.assertRaises(ValueError):construct(bytes(wrong),self.asset)

    def test_wrong_wording_rejected(self):
        asset=copy.deepcopy(self.asset);asset['units'][0]['translation']='처음'
        with self.assertRaises(ValueError):construct(self.source,asset)

    def test_overflow_profile_rejected(self):
        asset=copy.deepcopy(self.asset);asset['advance']=13
        with self.assertRaises(ValueError):construct(self.source,asset)


if __name__=='__main__':unittest.main()
