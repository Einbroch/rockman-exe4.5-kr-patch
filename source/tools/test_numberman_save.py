import unittest
from report_roll_pet import ROOT,read
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope

class NumberManSaveTests(unittest.TestCase):
    def test_retained_scope_and_choices(self):
        a=read(ROOT/'translations/four_navi_save_ko.json');u=resolve_units(a)
        self.assertEqual(u[:53],resolve_units(read(ROOT/'translations/rockman_roll_gutsman_save_ko.json')))
        self.assertEqual(len(u),69);self.assertEqual({int(x['id'].split(':')[1]) for x in u[53:]},set(range(55,60)))
        scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],a)
        self.assertEqual(scope['literal_ids'],[x['id'] for x in u]);self.assertEqual(len(scope['choice_groups']),14)
        self.assertEqual(scope['standalone_choice_rows'],[{'script':26,'literals':[1,2],'prefix_pixels':24},{'script':56,'literals':[1,2],'prefix_pixels':24}])
        self.assertFalse(a['review']['release_eligible'])
    def test_source_controls_and_unselected(self):
        a=read(ROOT/'translations/four_navi_save_ko.json');u=resolve_units(a)
        scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],a)
        source=(ROOT/'analysis/tpl_baseline/6DA21C.tpl').read_text(encoding='utf-8');before={x.key:x.text for x in literals(source)}
        self.assertTrue(all(before[x['id']]==x['source'] for x in u))
        target=translate_literal_scope(source,u,scope);self.assertEqual(skeleton(source),skeleton(target))
        chosen={x['id'] for x in u};after={x.key:x.text for x in literals(target)}
        self.assertEqual({k:v for k,v in before.items() if k not in chosen},{k:v for k,v in after.items() if k not in chosen})
        for x in u[53:]:self.assertEqual(x['source'].count('\n'),x['translation'].count('\n'))

if __name__=='__main__':unittest.main()
