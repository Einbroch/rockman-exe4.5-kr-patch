import unittest,copy
from report_roll_pet import ROOT,read
from tpl_literals import resolve_units,literals,replace_literals,skeleton
from build_development_patch import selected_scope,literal_scope,translate_literal_scope

class SaveLabelTests(unittest.TestCase):
    def test_prior32_units_and_fixed_profiles(self):
        a=read(ROOT/'translations/rockman_roll_save_labels_ko.json');u=resolve_units(a)
        self.assertEqual(u[:32],resolve_units(read(ROOT/'translations/rockman_roll_save_ko.json')))
        self.assertEqual([x['translation'] for x in u[32:]],['시간','칩','컵','크레딧'])
        s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],a)
        for script in range(10,14):
            p=literal_scope(s,f'6DA21C:{script}:0');self.assertEqual(p['consumer'],'fixed-cell-big');self.assertEqual(p['max_line_advance'],48)
        self.assertEqual(literal_scope(s,'6DA21C:20:0')['consumer'],'normal-dialogue')
    def test_source_controls_numeric_units_protected(self):
        a=read(ROOT/'translations/rockman_roll_save_labels_ko.json');s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],a)
        source=(ROOT/'analysis/tpl_baseline/6DA21C.tpl').read_text(encoding='utf-8');u=resolve_units(a);before={x.key:x.text for x in literals(source)}
        self.assertTrue(all(before[x['id']]==x['source'] for x in u))
        target=translate_literal_scope(source,u,s);after={x.key:x.text for x in literals(target)}
        self.assertEqual(skeleton(source),skeleton(target));chosen={x['id'] for x in u}
        self.assertEqual({k:v for k,v in before.items() if k not in chosen},{k:v for k,v in after.items() if k not in chosen})

if __name__=='__main__':unittest.main()
