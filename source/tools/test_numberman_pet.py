import unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals,replace_literals,resolve_units,skeleton

class NumberManPETTests(unittest.TestCase):
    def test_exact_scope_source_and_choices(self):
        a=read(ROOT/'translations/numberman_pet_menu_ko.json');s=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6873F4']
        self.assertEqual(s['pointers'],[0x3827C]);self.assertEqual(s['source_bytes'],1160);self.assertEqual(s['script_count'],22)
        self.assertTrue(s['complete_literal_scope']);self.assertEqual(len(s['choice_scripts']),14);self.assertFalse(a['review']['release_eligible'])
        t=(ROOT/'analysis/tpl_baseline/6873F4.tpl').read_text(encoding='utf-8');lookup={x.key:x.text for x in literals(t)};units=resolve_units(a)
        self.assertEqual(len(units),44);self.assertEqual(set(lookup),{u['id'] for u in units})
        self.assertTrue(all(lookup[u['id']]==u['source'] for u in units))
        for u in units:
            self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
            if u['source']=='はい  ':self.assertEqual(u['translation'],'예  ')
    def test_controls_and_nickname_boundary(self):
        a=read(ROOT/'translations/numberman_pet_menu_ko.json');t=(ROOT/'analysis/tpl_baseline/6873F4.tpl').read_text(encoding='utf-8')
        target=replace_literals(t,resolve_units(a));self.assertEqual(skeleton(t),skeleton(target))
        self.assertEqual(t.count('printPlayerNickname'),1);self.assertEqual(target.count('printPlayerNickname'),1)
        idle=resolve_units(a)[0];self.assertTrue(idle['translation'].endswith('\n'));self.assertEqual(idle['translation'].count('\n'),1)

if __name__=='__main__':unittest.main()
