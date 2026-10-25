import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals
from draft_starman_seasonal import DRAFT

class StarSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/starman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/6A8ADC.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(48,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_voice_and_development_policy(self):
        a=read(ROOT/'translations/starman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
        self.assertIn('재작년',DRAFT[6][1]);self.assertIn('작년',DRAFT[6][3]);self.assertIn('농~담',DRAFT[2][3])
    def test_numerals_and_rows_rejected(self):
        a=read(ROOT/'translations/starman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6A8ADC']
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6A8ADC:1:2')['translation']='후지산,매,가지\n라고 하는데,'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6A8ADC:7:4')['translation']='분명,\n감동할 거야'
        t=(ROOT/'analysis/full_scope_v1/source_tpl/6A8ADC.tpl').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):replace_literals(t,bad)

if __name__=='__main__':unittest.main()
