import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
from draft_plantman_seasonal import DRAFT

class PlantSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/plantman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/6D0ADC.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(43,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_meaning_and_development_policy(self):
        a=read(ROOT/'translations/plantman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
        self.assertIn('다이다이',DRAFT[1][2]);self.assertIn('등자',DRAFT[1][2]);self.assertIn('대대로',DRAFT[1][3]);self.assertIn('대두',DRAFT[2][1]);self.assertIn('볶은',DRAFT[2][1]);self.assertIn('생콩',DRAFT[2][2]);self.assertIn('싹이',DRAFT[2][4]);self.assertIn('하더구나',DRAFT[6][2]);self.assertIn('나이테가 1개',DRAFT[11][1])
    def test_nickname_numerals_and_rows_rejected(self):
        a=read(ROOT/'translations/plantman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6D0ADC'];validate_nickname_suffix(a['units'],'6D0ADC',scope)
        for key in ['6D0ADC:1:0','6D0ADC:11:0']:
            bad=copy.deepcopy(a['units']);u=next(u for u in bad if u['id']==key);u['translation']='은'+u['translation'][1:]
            with self.assertRaises(ValueError):validate_nickname_suffix(bad,'6D0ADC',scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6D0ADC:11:1')['translation']='나무로 비유하면,\n나이테가 2개\n늘었구나・・・'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6D0ADC:10:2')['translation']='왠지\n애틋하구나'
        with self.assertRaises(ValueError):replace_literals((ROOT/'analysis/full_scope_v1/source_tpl/6D0ADC.tpl').read_text(encoding='utf-8-sig'),bad)

if __name__=='__main__':unittest.main()
