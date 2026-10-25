"""Fail-closed full mail selection/layout and player-name source guards."""
import copy,json,unittest
from full_mail_body import ROOT,ASSET,SCOPE,prepare,units,replace,validate
from first_mail import selected_units
from tpl_literals import literals,skeleton

class FullMailTests(unittest.TestCase):
    def setUp(self):
        self.asset=json.loads((ROOT/prepare()).read_text(encoding='utf8'))
        self.original=(ROOT/self.asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.source=(ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
        self.target=replace(self.original,self.asset['units'])
        self.layout=[dict(id=u['id'],line_advance_pixels=[sum(12 if '\uac00'<=c<='\ud7a3' or c==',' else 8 if c==' ' else 11 for c in row) for row in u['translation'].split('\n')]) for u in self.asset['units']]
    def test_exact_population_carry_and_controls(self):
        self.assertEqual(len(self.asset['units']),120)
        self.assertEqual(self.asset['units'][:77],selected_units('6DD9AC','news'))
        self.assertEqual(skeleton(self.original),skeleton(self.target))
        self.assertEqual({x.key for x in literals(self.original)},{u['id'] for u in units()})
        self.assertEqual(len(validate(self.source,self.asset,self.original,self.target,self.layout)['name_joins']),5)
    def test_changed_wording_or_scope_rejected(self):
        for field,value in [('translation','번역 변경'),('id','6DD9AC:15:0'),('state','reviewed')]:
            bad=copy.deepcopy(self.asset['units']);bad[-1][field]=value
            with self.assertRaises(ValueError):replace(self.original,bad)
    def test_changed_producer_rejected(self):
        for at in [0x39E34,0x39E68,0x35494,0x3549A,0x355D8,0x35620,0x527C8]:
            bad=bytearray(self.source);bad[at]^=1
            with self.assertRaises(ValueError):validate(bad,self.asset,self.original,self.target,self.layout)
    def test_name_and_arrow_layout_rejected(self):
        for key,row,width in [('6DD9AC:13:3',0,81),('6DD9AC:14:4',2,133)]:
            bad=copy.deepcopy(self.layout);next(x for x in bad if x['id']==key)['line_advance_pixels'][row]=width
            with self.assertRaises(ValueError):validate(self.source,self.asset,self.original,self.target,bad)

if __name__=='__main__':unittest.main()
