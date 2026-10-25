import unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals,replace_literals,skeleton

class NumberManJackInTests(unittest.TestCase):
    def test_exact_scope_source(self):
        a=read(ROOT/'translations/numberman_jackin_ko.json');s=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['687E3C']
        self.assertEqual(s['pointers'],[0x38288]);self.assertEqual(s['source_bytes'],76);self.assertEqual(s['script_count'],3)
        self.assertTrue(s['complete_literal_scope']);self.assertFalse(a['review']['release_eligible'])
        t=(ROOT/'analysis/tpl_baseline/687E3C.tpl').read_text(encoding='utf-8');ls=literals(t)
        self.assertEqual(len(ls),1);self.assertEqual(ls[0].key,a['units'][0]['id']);self.assertEqual(ls[0].text,a['units'][0]['source'])
    def test_commands_and_slogan_structure(self):
        a=read(ROOT/'translations/numberman_jackin_ko.json');t=(ROOT/'analysis/tpl_baseline/687E3C.tpl').read_text(encoding='utf-8')
        target=replace_literals(t,a['units']);self.assertEqual(skeleton(t),skeleton(target));u=a['units'][0]
        self.assertEqual(u['translation'].count('\n'),2);self.assertIn('.EXE、',u['translation']);self.assertTrue(u['translation'].endswith('!!'))
        self.assertIn('frames = 30',target);self.assertEqual(target.count('flagClear'),2);self.assertIn('type = 3',target)

if __name__=='__main__':unittest.main()
