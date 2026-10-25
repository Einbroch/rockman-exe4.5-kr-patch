import unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals,replace_literals,resolve_units,skeleton

class NumberManTrainingTests(unittest.TestCase):
    def test_exact_scope_and_source(self):
        a=read(ROOT/'translations/numberman_training_intro_ko.json');s=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['687910']
        self.assertEqual(s['pointers'],[0x38284]);self.assertEqual(s['source_bytes'],1323);self.assertEqual(s['script_count'],65)
        self.assertEqual(s['literal_scripts'],[10,11,20,21]);self.assertFalse(a['review']['release_eligible'])
        t=(ROOT/'analysis/tpl_baseline/687910.tpl').read_text(encoding='utf-8');lookup={x.key:x.text for x in literals(t)};units=resolve_units(a)
        self.assertEqual(len(units),16);self.assertEqual(s['literal_ids'],[u['id'] for u in units])
        self.assertTrue(all(lookup[u['id']]==u['source'] for u in units))
        self.assertEqual(s['standalone_choice_rows'],[{'script':10,'literals':[4,5],'prefix_pixels':24},{'script':20,'literals':[5,6],'prefix_pixels':24}])
    def test_commands_and_results_preserved(self):
        a=read(ROOT/'translations/numberman_training_intro_ko.json');t=(ROOT/'analysis/tpl_baseline/687910.tpl').read_text(encoding='utf-8')
        units=resolve_units(a);target=replace_literals(t,units);self.assertEqual(skeleton(t),skeleton(target));chosen={u['id'] for u in units}
        self.assertEqual({x.key:x.text for x in literals(t) if x.key not in chosen},{x.key:x.text for x in literals(target) if x.key not in chosen})
        for u in units:self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
        self.assertEqual([u['translation'] for u in units if u['source']=='うん  '],['응  ','응  '])

if __name__=='__main__':unittest.main()
