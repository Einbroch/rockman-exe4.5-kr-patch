import unittest
from pathlib import Path
from report_roll_pet import ROOT,read
from tpl_literals import resolve_units,literals,replace_literals,skeleton
from build_development_patch import selected_scope

class RollSaveTests(unittest.TestCase):
    def test_retained_rockman_and_exact_roll_scope(self):
        a=read(ROOT/'translations/rockman_roll_save_ko.json');units=resolve_units(a)
        self.assertEqual(units[:16],resolve_units(read(ROOT/'translations/megaman_save_ko.json')))
        scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],a)
        self.assertEqual(scope['literal_scripts'],[0,1,2,3,4,20,21,22,23,24]);self.assertEqual(len(units),32)
        self.assertEqual({g['script'] for g in scope['choice_groups']},{0,1,2,4,20,21,22,24})
    def test_source_and_controls(self):
        source=(ROOT/'analysis/tpl_baseline/6DA21C.tpl').read_text(encoding='utf-8')
        units=resolve_units(read(ROOT/'translations/rockman_roll_save_ko.json'))
        actual={x.key:x.text for x in literals(source)}
        self.assertTrue(all(actual[u['id']]==u['source'] for u in units))
        target=replace_literals(source,units)
        self.assertEqual(skeleton(source),skeleton(target))
        chosen={u['id'] for u in units};after={x.key:x.text for x in literals(target)}
        self.assertEqual({k:v for k,v in actual.items() if k not in chosen},{k:v for k,v in after.items() if k not in chosen})

if __name__=='__main__':unittest.main()
