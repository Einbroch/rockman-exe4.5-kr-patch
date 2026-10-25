import copy,json,unittest
from native_keyboard_labels import ROOT,construct,PAGES
from prepare_keyboard_page_graphics import decode

class NativeLabels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
        cls.source=(ROOT/p['filename']).read_bytes()
        cls.asset=json.loads((ROOT/'translations/native_keyboard_labels_ko.json').read_text(encoding='utf8'))
    def test_three_pages_exact_boundaries(self):
        patches,meta=construct(self.source,self.asset)
        self.assertEqual((patches,meta),construct(self.source,self.asset));self.assertEqual(len(patches),6)
        for page,(at,n,_,mp,_) in enumerate(PAGES):
            bank,mapping=patches[page*2][1],patches[page*2+1][1]
            self.assertEqual((len(bank),len(mapping)),(n,1200))
            old=decode(self.source[at:at+n],self.source[mp:mp+1200]);new=decode(bank,mapping)
            self.assertNotEqual(old,new)
            for y in range(160):
                for x in range(240):
                    if not(196<=x<224 and 56<=y<152):self.assertEqual(old[y][x],new[y][x])
    def test_fail_closed_drift_policy_wording(self):
        for key,value in [('release_eligible',True),('font_sha256','0'*64),('pages',[['한글']]*3)]:
            a=copy.deepcopy(self.asset);a[key]=value
            with self.assertRaises(ValueError):construct(self.source,a)
        s=bytearray(self.source);s[PAGES[0][0]]^=1
        with self.assertRaises(ValueError):construct(s,self.asset)
        s=bytearray(self.source);s[0x356E8+8]^=1
        with self.assertRaises(ValueError):construct(s,self.asset)

if __name__=='__main__':unittest.main()
