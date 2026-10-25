import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
from draft_iceman_seasonal import DRAFT

class IceSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/iceman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/6C5A88.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(34,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_meaning_and_development_policy(self):
        a=read(ROOT/'translations/iceman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
        self.assertIn('B',DRAFT[8][1]);self.assertIn('V',DRAFT[8][1]);self.assertIn('소바',DRAFT[10][3]);self.assertIn('냉중화면',DRAFT[10][3]);self.assertIn('늦게',DRAFT[5][3])
    def test_nickname_numerals_and_rows_rejected(self):
        a=read(ROOT/'translations/iceman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6C5A88'];validate_nickname_suffix(a['units'],'6C5A88',scope)
        for key in ['6C5A88:3:1','6C5A88:11:0']:
            bad=copy.deepcopy(a['units']);u=next(u for u in bad if u['id']==key);u['translation']='은'+u['translation'][1:]
            with self.assertRaises(ValueError):validate_nickname_suffix(bad,'6C5A88',scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6C5A88:8:0')['translation']='오늘은 12월25일,\n크리스마스이브예요!'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6C5A88:8:1')['translation']='B 소리 말고,V 소리예요!'
        with self.assertRaises(ValueError):replace_literals((ROOT/'analysis/full_scope_v1/source_tpl/6C5A88.tpl').read_text(encoding='utf-8-sig'),bad)

if __name__=='__main__':unittest.main()
