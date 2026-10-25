import unittest
from report_roll_pet import ROOT,read
from tpl_literals import resolve_units,literals,replace_literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope

class GutsManSaveTests(unittest.TestCase):
    def test_scope_and_retained_units(self):
        a=read(ROOT/'translations/rockman_roll_gutsman_save_ko.json');u=resolve_units(a)
        self.assertEqual(u[:37],resolve_units(read(ROOT/'translations/rockman_roll_save_surface_ko.json')))
        self.assertEqual(len(u),53)
        self.assertEqual({int(x['id'].split(':')[1]) for x in u[37:]},set(range(25,30)))
        s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],a)
        self.assertEqual(s['literal_ids'],[x['id'] for x in u]);self.assertEqual(len(s['choice_groups']),11)
        self.assertEqual(s['standalone_choice_rows'],[{'script':26,'literals':[1,2],'prefix_pixels':24}])
        self.assertFalse(a['review']['release_eligible'])
    def test_source_controls_and_unselected(self):
        source=(ROOT/'analysis/tpl_baseline/6DA21C.tpl').read_text(encoding='utf-8')
        u=resolve_units(read(ROOT/'translations/rockman_roll_gutsman_save_ko.json'));before={x.key:x.text for x in literals(source)}
        self.assertTrue(all(before[x['id']]==x['source'] for x in u))
        scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],read(ROOT/'translations/rockman_roll_gutsman_save_ko.json'))
        target=translate_literal_scope(source,u,scope);self.assertEqual(skeleton(source),skeleton(target))
        after={x.key:x.text for x in literals(target)};chosen={x['id'] for x in u}
        self.assertEqual({k:v for k,v in before.items() if k not in chosen},{k:v for k,v in after.items() if k not in chosen})
        for x in u[37:]:
            self.assertEqual(x['source'].count('\n'),x['translation'].count('\n'))
            if x['source']=='はい  ':self.assertTrue(x['translation'].endswith('  '))

if __name__=='__main__':unittest.main()
