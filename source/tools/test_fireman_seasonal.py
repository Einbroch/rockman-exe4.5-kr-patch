import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
from draft_fireman_seasonal import DRAFT

class FireSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/fireman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/67AE2C.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(47,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_and_development_policy(self):
        a=read(ROOT/'translations/fireman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id'] or u['id']=='67AE2C:11:5':self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
    def test_nickname_boundary_rejections(self):
        a=read(ROOT/'translations/fireman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['67AE2C'];validate_nickname_suffix(a['units'],'67AE2C',scope)
        t=(ROOT/'analysis/full_scope_v1/source_tpl/67AE2C.tpl').read_text(encoding='utf-8-sig')
        for key,target in [('67AE2C:11:3','버닝!!\n'),('67AE2C:11:4','\n버닝!!'),('67AE2C:11:5','!!')]:
            bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']==key)['translation']=target
            with self.assertRaises(ValueError):
                replace_literals(t,bad);validate_nickname_suffix(bad,'67AE2C',scope)

if __name__=='__main__':unittest.main()
