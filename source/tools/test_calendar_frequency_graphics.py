import copy,json,unittest
from calendar_frequency_graphics import ROOT,BASE,STORED,construct,decode,encode
from verify_tpi_index import lz77_decompress

class FrequencyGraphicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()
        cls.asset=json.loads((ROOT/'translations/calendar_frequency_graphics_ko.json').read_text(encoding='utf-8'))
    def test_same_slot_five_units_and_protected_header_pixels(self):
        stored,new,m=construct(self.source,self.asset);old,_=lz77_decompress(self.source,BASE)
        self.assertEqual(len(stored),STORED);self.assertEqual(len(new),len(old));self.assertEqual(new[:4],old[:4]);self.assertEqual(lz77_decompress(stored,0)[0],new)
        self.assertEqual(len(m['units']),5)
        for i in range(5):
            a=decode(old[4+i*256:4+(i+1)*256]);b=decode(new[4+i*256:4+(i+1)*256])
            self.assertEqual(encode(a),old[4+i*256:4+(i+1)*256])
            self.assertNotEqual(a,b)
            for y in [0,1,2,3,15]:self.assertEqual(a[y],b[y])
    def test_unapproved_and_wrong_boundary_fail(self):
        for key,value in [('release_eligible',True),('stored_bytes',429),('edit_rect',[0,0,32,16])]:
            a=copy.deepcopy(self.asset);a[key]=value
            with self.assertRaises(ValueError):construct(self.source,a)
    def test_wrong_wording_or_source_fail(self):
        a=copy.deepcopy(self.asset);a['units'][0]['translation']='한 번'
        with self.assertRaises(ValueError):construct(self.source,a)
        b=bytearray(self.source);b[BASE]^=1
        with self.assertRaises(ValueError):construct(bytes(b),self.asset)

if __name__=='__main__':unittest.main()
