import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
from draft_knightman_seasonal import DRAFT

class KnightSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/knightman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/6BA3AC.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(42,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
        from archive_scripts import script_spans
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        self.assertEqual(1,script_spans(source[0x6BA3AC:0x6BA3AC+1378],21)[1].count(bytes.fromhex('f90c0187e600f1')))
    def test_geometry_voice_and_development_policy(self):
        a=read(ROOT/'translations/knightman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id'] or u['id']=='6BA3AC:1:2':self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
        self.assertIn('그대가 준 초콜릿',DRAFT[4][1]);self.assertTrue(DRAFT[7][2].split('\n')[1].startswith(' '))
    def test_nickname_numerals_and_boundary_rejections(self):
        a=read(ROOT/'translations/knightman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6BA3AC'];validate_nickname_suffix(a['units'],'6BA3AC',scope)
        self.assertEqual(7,len(scope['nickname_suffix_profiles']))
        for p in scope['nickname_suffix_profiles']:
            bad=copy.deepcopy(a['units']);u=next(u for u in bad if u['id']==f"6BA3AC:{p['script']}:{p['literal']}");u['translation']='께서'+u['translation'][1:]
            with self.assertRaises(ValueError):validate_nickname_suffix(bad,'6BA3AC',scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6BA3AC:10:1')['translation']='올해도 끝나는군요\n후회 없는2일을\n보내십시오'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,scope)

if __name__=='__main__':unittest.main()
