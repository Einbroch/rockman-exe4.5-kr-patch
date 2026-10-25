"""Lossless compression, graphic boundaries and fail-closed input regressions."""
import json,random,unittest
from pathlib import Path
from build_visibility_poc import ROOT
from lz10_optimal import encode
from verify_tpi_index import lz77_decompress
from startup_footer_graphics import construct as footer,OFFSET,SIZE
from startup_welcome_graphics import construct as welcome

class StartupAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
        cls.source=(ROOT/p['filename']).read_bytes()
        cls.f=json.loads((ROOT/'translations/startup_footer_graphics_ko.json').read_text(encoding='utf8'))
        cls.w=json.loads((ROOT/'translations/startup_welcome_graphics_ko.json').read_text(encoding='utf8'))
    def test_lossless_deterministic(self):
        rng=random.Random(45)
        for data in [b'a',b'a'*4097,bytes(range(256))*3,bytes(rng.randrange(256) for _ in range(520)),b'abcabcabcabc'+b'x'*80]:
            packed=encode(data,stored_limit=len(data)*2+8)
            self.assertEqual(lz77_decompress(packed,0),(data,len(packed)))
            self.assertEqual(packed,encode(data,stored_limit=len(packed)))
            with self.assertRaises(ValueError):encode(data,stored_limit=len(packed)-1)
    def test_footer_exact_and_source_guard(self):
        a,m=footer(self.source,self.f);b,_=footer(self.source,self.f)
        self.assertEqual(a,b);self.assertEqual(len(a),SIZE)
        self.assertTrue(m['protected_pixels_identical']);self.assertNotEqual(a,self.source[OFFSET:OFFSET+SIZE])
        source=bytearray(self.source);source[OFFSET]^=1
        with self.assertRaises(ValueError):footer(source,self.f)
        wrong=dict(self.f,release_eligible=True)
        with self.assertRaises(ValueError):footer(self.source,wrong)
    def test_welcome_relocation_protected_pixels(self):
        a,p,m=welcome(self.source,self.w,b'\xff'*3)
        b,q,n=welcome(self.source,self.w,b'\xff'*3)
        self.assertEqual((a,p,m),(b,q,n));self.assertEqual(len(p),2)
        self.assertTrue(m['protected_pixels_identical']);self.assertTrue(m['source_graphics_unchanged'])
        for r in m['records']:
            at=r['offset']-len(self.source)
            payload,used=lz77_decompress(a,at)
            self.assertEqual(used,r['stored_bytes']);self.assertEqual(len(payload),r['payload_bytes'])
        wrong=dict(self.w,translation_lines=['잘못된 문구'])
        with self.assertRaises(ValueError):welcome(self.source,wrong,b'')

if __name__=='__main__':unittest.main()
