import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals
from draft_thunderman_seasonal import DRAFT

class ThunderSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_draft(self):
        a=read(ROOT/'translations/thunderman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/680454.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(34,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_and_draft_policy(self):
        a=read(ROOT/'translations/thunderman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
    def test_protected_numeral_and_newline_rejected(self):
        a=read(ROOT/'translations/thunderman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/680454.tpl').read_text(encoding='utf-8-sig')
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='680454:10:2')['translation']='후회 없는 하루를\n보내거라'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,dict(preserve_literal_numerals=True))
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='680454:1:0')['translation']='새해 복 많이\n받아라'
        with self.assertRaises(ValueError):replace_literals(t,bad)

if __name__=='__main__':unittest.main()
