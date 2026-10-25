import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals
from draft_blues_seasonal import DRAFT

class BluesSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/blues_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/685C68.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(33,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_and_development_policy(self):
        a=read(ROOT/'translations/blues_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
    def test_protected_date_and_single_line_rejections(self):
        a=read(ROOT/'translations/blues_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/685C68.tpl').read_text(encoding='utf-8-sig')
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='685C68:9:1')['translation']='성탄절은 축제가\n끝난 듯한\n쓸쓸함이 있네요'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,dict(preserve_literal_numerals=True))
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='685C68:10:0')['translation']='오늘은\n섣달그믐입니다'
        with self.assertRaises(ValueError):replace_literals(t,bad)

if __name__=='__main__':unittest.main()
