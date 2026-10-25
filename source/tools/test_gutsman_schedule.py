import copy,struct,unittest
from draft_gutsman_schedule import DRAFT,TPL_SHA,PAYLOAD_SHA
from report_roll_pet import ROOT,read,sha
from tpl_literals import literals,replace_literals,skeleton
from roll_schedule_time_model import validate
class GutsSchedule(unittest.TestCase):
    def test_complete_source_population(self):
        p=ROOT/'analysis/full_scope_v1/source_tpl/666F38.tpl';self.assertEqual(TPL_SHA,sha(p.read_bytes()));t=p.read_text(encoding='utf-8-sig');a=read(ROOT/'translations/gutsman_schedule_ko.json');u=a['units'];self.assertEqual(12,len(u));self.assertEqual(6,sum(x['source']==x['translation'] for x in u));self.assertEqual({x.key:x.text for x in literals(t)},{x['id']:x['source'] for x in u});self.assertEqual(skeleton(t),skeleton(replace_literals(t,u)))
        for x in u:
            _,s,i=x['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],x['translation']);self.assertEqual('needs_review',x['state'])
        self.assertFalse(a['review']['release_eligible'])
    def test_native_source_and_geometry(self):
        c=read(ROOT/'project.json');b=(ROOT/c['source_profile']['filename']).read_bytes();self.assertEqual(c['source_profile']['sha256'],sha(b));self.assertEqual(PAYLOAD_SHA,sha(b[0x666F38:0x666F38+265]));self.assertEqual(0x08666F38,struct.unpack_from('<I',b,0x38134)[0])
        for rows in DRAFT.values():
            for text in rows:
                for line in text.split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
    def test_clock_non_growth_rejection(self):
        t=(ROOT/'analysis/full_scope_v1/source_tpl/666F38.tpl').read_text(encoding='utf-8-sig');u=read(ROOT/'translations/gutsman_schedule_ko.json')['units'];scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['666F38'];layout=[dict(id='666F38:11:2',line_advance_pixels=[24,0])];validate(u,scope,t,replace_literals(t,u),layout);self.assertEqual(30,layout[0]['source_suffix_width'])
        with self.assertRaises(ValueError):validate(u,scope,t,replace_literals(t,u),[dict(id='666F38:11:2',line_advance_pixels=[32,0])])
        bad=copy.deepcopy(u);next(x for x in bad if x['id']=='666F38:11:0')['translation']='!'
        with self.assertRaises(ValueError):validate(bad,scope,t,replace_literals(t,bad),layout)
if __name__=='__main__':unittest.main()
