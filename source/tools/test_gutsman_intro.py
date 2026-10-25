import copy,struct,unittest
from build_visibility_poc import ROOT,require_hash
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from draft_gutsman_intro import DRAFT
from build_development_patch import validate_literal_numerals

class GutsManIntro(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/gutsman_intro_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/665EB8.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(4,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']});self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])))
        validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_and_provisional_voice(self):
        a=read(ROOT/'translations/gutsman_intro_ko.json');self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
        for u in a['units']:
            self.assertEqual('needs_review',u['state'])
            self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
        self.assertIn('처음',DRAFT[1][1]);self.assertIn('오랜만',DRAFT[2][0]);self.assertIn('다시',DRAFT[2][1])
    def test_source_binding_and_row_rejection(self):
        c=read(ROOT/'project.json');p=ROOT/c['source_profile']['filename'];require_hash(p,c['source_profile']['sha256']);b=p.read_bytes()
        self.assertEqual(0x8665EB8,struct.unpack_from('<I',b,0x38110)[0]);self.assertEqual(0x866A234,struct.unpack_from('<I',b,0x38144)[0])
        a=read(ROOT/'translations/gutsman_intro_ko.json');bad=copy.deepcopy(a['units']);bad[0]['translation']+='\n'
        with self.assertRaises(ValueError):replace_literals((ROOT/'analysis/full_scope_v1/source_tpl/665EB8.tpl').read_text(encoding='utf-8-sig'),bad)

if __name__=='__main__':unittest.main()
