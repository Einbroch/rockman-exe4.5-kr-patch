import struct,unittest
from draft_gutsman_schedule_alarm import DRAFT,TPL_SHA,PAYLOAD_SHA
from report_roll_pet import ROOT,read,sha
from tpl_literals import literals,replace_literals,skeleton
class GutsAlarm(unittest.TestCase):
    def test_source_and_partial_scope(self):
        p=ROOT/'analysis/full_scope_v1/source_tpl/66651C.tpl';self.assertEqual(TPL_SHA,sha(p.read_bytes()));t=p.read_text(encoding='utf-8-sig');items=literals(t);a=read(ROOT/'translations/gutsman_schedule_alarm_ko.json');u=a['units'];self.assertEqual(21,len(items));self.assertEqual(3,len(u));self.assertEqual(DRAFT,{x['id']:x['translation'] for x in u});self.assertEqual({x.key:x.text for x in items if x.key in DRAFT},{x['id']:x['source'] for x in u});self.assertEqual(skeleton(t),skeleton(replace_literals(t,u)));self.assertFalse(a['review']['release_eligible']);self.assertTrue(all(x['state']=='needs_review' for x in u))
    def test_native_root_and_payload(self):
        c=read(ROOT/'project.json');b=(ROOT/c['source_profile']['filename']).read_bytes();self.assertEqual(c['source_profile']['sha256'],sha(b));self.assertEqual(PAYLOAD_SHA,sha(b[0x66651c:0x66651c+771]));self.assertEqual(0x0866651c,struct.unpack_from('<I',b,0x38124)[0]);scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['66651C'];self.assertEqual(set(DRAFT),set(scope['literal_ids']));self.assertFalse(scope['complete_literal_scope'])
    def test_page_geometry_and_newlines(self):
        for x in read(ROOT/'translations/gutsman_schedule_alarm_ko.json')['units']:
            self.assertEqual(x['source'].count('\n'),x['translation'].count('\n'))
            for line in x['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
if __name__=='__main__':unittest.main()
