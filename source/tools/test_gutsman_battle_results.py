import struct,unittest
from draft_gutsman_battle_results import DRAFT,TPL_SHA,PAYLOAD_SHA
from report_roll_pet import ROOT,read,sha
from tpl_literals import literals,replace_literals,skeleton
class GutsBattle(unittest.TestCase):
    def test_complete_source_scope(self):
        p=ROOT/'analysis/full_scope_v1/source_tpl/66A7A8.tpl';self.assertEqual(TPL_SHA,sha(p.read_bytes()));t=p.read_text(encoding='utf-8-sig');items=literals(t);a=read(ROOT/'translations/gutsman_battle_results_ko.json');u=a['units'];self.assertEqual(3,len(items));self.assertEqual(DRAFT,{x['id']:x['translation'] for x in u});self.assertEqual({x.key:x.text for x in items},{x['id']:x['source'] for x in u});self.assertEqual(skeleton(t),skeleton(replace_literals(t,u)));self.assertFalse(a['review']['release_eligible']);self.assertTrue(all(x['state']=='needs_review' for x in u))
    def test_source_binding(self):
        c=read(ROOT/'project.json');b=(ROOT/c['source_profile']['filename']).read_bytes();self.assertEqual(c['source_profile']['sha256'],sha(b));self.assertEqual(PAYLOAD_SHA,sha(b[0x66a7a8:0x66a7a8+155]));self.assertEqual(0x0866a7a8,struct.unpack_from('<I',b,0x38130)[0]);scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['66A7A8'];self.assertTrue(scope['complete_literal_scope']);self.assertEqual([1,2,3],scope['literal_scripts'])
    def test_page_geometry_and_newlines(self):
        for x in read(ROOT/'translations/gutsman_battle_results_ko.json')['units']:
            self.assertEqual(x['source'].count('\n'),x['translation'].count('\n'));self.assertLessEqual(x['translation'].count('\n')+1,3)
            for line in x['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
if __name__=='__main__':unittest.main()
