import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals
from draft_elecman_seasonal import DRAFT

class ElecSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/elecman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/6CB184.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(40,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_meaning_and_development_policy(self):
        a=read(ROOT/'translations/elecman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
        self.assertIn('아니야',DRAFT[2][3]);self.assertIn('천둥신',DRAFT[2][4]);self.assertIn('썬더맨',DRAFT[2][5]);self.assertIn('불을 끄고',DRAFT[7][1]);self.assertIn('철거',DRAFT[9][2]);self.assertIn('리세에',DRAFT[10][3]);self.assertEqual('없어',DRAFT[11][2].split('\n')[1])
    def test_numerals_and_rows_rejected(self):
        a=read(ROOT/'translations/elecman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6CB184']
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6CB184:9:2')['translation']='24일 밤이면,\n전구 장식은\n철거돼 버려!'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6CB184:2:3')['translation']='난,도깨비가\n아니야!'
        with self.assertRaises(ValueError):replace_literals((ROOT/'analysis/full_scope_v1/source_tpl/6CB184.tpl').read_text(encoding='utf-8-sig'),bad)

if __name__=='__main__':unittest.main()
