import unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals,replace_literals,skeleton

class NumberManIntroTests(unittest.TestCase):
    def test_exact_scope_and_source(self):
        a=read(ROOT/'translations/numberman_intro_ko.json');s=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6872B8']
        self.assertEqual(s['pointers'],[0x38278]);self.assertEqual(s['source_bytes'],313);self.assertEqual(s['literal_scripts'],[1])
        self.assertEqual(s['literal_ids'],[u['id'] for u in a['units']]);self.assertEqual(len(a['units']),7)
        self.assertFalse(a['review']['release_eligible'])
        source=(ROOT/'analysis/tpl_baseline/6872B8.tpl').read_text(encoding='utf-8');lookup={x.key:x.text for x in literals(source)}
        self.assertTrue(all(lookup[u['id']]==u['source'] for u in a['units']))
    def test_control_and_return_dialogue_protection(self):
        a=read(ROOT/'translations/numberman_intro_ko.json');source=(ROOT/'analysis/tpl_baseline/6872B8.tpl').read_text(encoding='utf-8')
        target=replace_literals(source,a['units']);self.assertEqual(skeleton(source),skeleton(target))
        chosen={u['id'] for u in a['units']};before={x.key:x.text for x in literals(source) if x.key not in chosen};after={x.key:x.text for x in literals(target) if x.key not in chosen}
        self.assertEqual(before,after);self.assertIn('4649',after['6872B8:2:4'])

if __name__=='__main__':unittest.main()
