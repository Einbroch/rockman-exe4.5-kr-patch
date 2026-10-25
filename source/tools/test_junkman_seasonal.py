import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
from draft_junkman_seasonal import DRAFT

class JunkSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/junkman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/696DD8.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(37,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_voice_transition_and_policy(self):
        a=read(ROOT/'translations/junkman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertEqual('어때, 나 또렷하게\n말하고 있어?',next(u for u in a['units'] if u['id']=='696DD8:7:3')['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy']);self.assertIn('wordplay not reproduced',a['semantic_review'][0])
    def test_nickname_boundary_and_single_line_rejected(self):
        a=read(ROOT/'translations/junkman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['696DD8'];validate_nickname_suffix(a['units'],'696DD8',scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='696DD8:11:0')['translation']='아\n생일,\n축하해'
        with self.assertRaises(ValueError):validate_nickname_suffix(bad,'696DD8',scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='696DD8:7:1')['translation']='나, 나는\n소원 쪽지에'
        with self.assertRaises(ValueError):replace_literals((ROOT/'analysis/full_scope_v1/source_tpl/696DD8.tpl').read_text(encoding='utf-8-sig'),bad)

if __name__=='__main__':unittest.main()
