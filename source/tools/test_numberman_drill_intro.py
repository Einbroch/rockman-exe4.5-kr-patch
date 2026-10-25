import copy,unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals,resolve_units,skeleton
from build_development_patch import translate_literal_scope,validate_literal_numerals,validate_characters

class DrillTests(unittest.TestCase):
    def test_scope_controls_and_unselected(self):
        a=read(ROOT/'translations/numberman_drill_intro_ko.json');s=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['715064']
        self.assertEqual(s['pointers'],[0xDD394,0xDD894]);self.assertEqual(s['source_bytes'],1207);self.assertEqual(s['script_count'],16)
        self.assertFalse(a['review']['release_eligible']);u=resolve_units(a);self.assertEqual(len(u),20)
        t=(ROOT/'analysis/tpl_baseline/715064.tpl').read_text(encoding='utf-8');v=translate_literal_scope(t,u,s)
        self.assertEqual(skeleton(t),skeleton(v));selected={x['id'] for x in u}
        self.assertEqual({x.key:x.text for x in literals(t) if x.key not in selected},{x.key:x.text for x in literals(v) if x.key not in selected})
        for x in u:self.assertEqual(x['source'].count('\n'),x['translation'].count('\n'))
        validate_literal_numerals(u,s)
    def test_changed_countdown_rejected(self):
        a=read(ROOT/'translations/numberman_drill_intro_ko.json');u=resolve_units(a);u=copy.deepcopy(u)
        u[12]['translation']=u[12]['translation'].replace('40','30')
        s=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['715064']
        with self.assertRaisesRegex(ValueError,'numeral'):validate_literal_numerals(u,s)

if __name__=='__main__':unittest.main()
