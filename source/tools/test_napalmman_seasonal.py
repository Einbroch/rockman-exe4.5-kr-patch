import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals
from draft_napalmman_seasonal import DRAFT

class NapalmSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/napalmman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/6C004C.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(38,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_voice_and_development_policy(self):
        a=read(ROOT/'translations/napalmman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
        self.assertIn('좋아한다고',DRAFT[8][2]);self.assertIn('108발',DRAFT[10][1]);self.assertIn('네이팜탄',DRAFT[10][1]);self.assertIn('종 대신',DRAFT[10][1])
    def test_numerals_and_rows_rejected(self):
        a=read(ROOT/'translations/napalmman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6C004C']
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6C004C:10:1')['translation']='제야의 종 대신\n109발의\n네이팜탄을'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6C004C:8:2')['translation']='정말\n좋아한다고!!'
        t=(ROOT/'analysis/full_scope_v1/source_tpl/6C004C.tpl').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):replace_literals(t,bad)

if __name__=='__main__':unittest.main()
