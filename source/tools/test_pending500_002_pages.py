"""Regression checks for exact source-ID page placement, no ROM changes."""
import json
import unittest
from unittest.mock import patch
from build_visibility_poc import ROOT
from pending500_002_pages import replace,specification
from tpl_literals import literals,skeleton


class ExplicitPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.asset=json.loads((ROOT/'translations/batch500_015_mission_6DED88_draft_ko.json').read_text(encoding='utf8'))
        cls.tpl=(ROOT/cls.asset['source_tpl']['path']).read_text(encoding='utf-8-sig')

    def test_exact_wording_and_original_event_commands(self):
        target,mapping,proof=replace(self.tpl,self.asset['units'])
        self.assertEqual(proof['extra_wait_clear_pairs'],2)
        self.assertTrue(proof['native_commands_preserved_after_exact_collapse'])
        self.assertEqual(len(mapping['6DED88:49:1']),2)
        self.assertEqual(len(mapping['6DED88:55:2']),2)
        self.assertEqual(len(mapping['6DED88:41:1']),1)
        self.assertEqual(len(literals(target)),len(literals(self.tpl))+2)
        for name in ('callShadowManMissionBegin','callShadowManMissionErase','printBuffer','printItem','printCurrentNavi','checkFlag'):
            self.assertEqual(skeleton(target).count(name),skeleton(self.tpl).count(name))

    def test_word_change_rejected(self):
        spec,digest=specification()
        spec['pages']['6DED88:49:1'][0]='잘못된 문구'
        with patch('pending500_002_pages.specification',return_value=(spec,digest)):
            with self.assertRaisesRegex(ValueError,'changes words/order'):
                replace(self.tpl,self.asset['units'])

    def test_extra_page_rejected(self):
        spec,digest=specification()
        spec['pages']['6DED88:49:1'].append('추가')
        with patch('pending500_002_pages.specification',return_value=(spec,digest)):
            with self.assertRaisesRegex(ValueError,'page extent'):
                replace(self.tpl,self.asset['units'])

    def test_wrong_source_rejected(self):
        units=[dict(x) for x in self.asset['units']]
        units[0]['source']='원문 불일치'
        with self.assertRaisesRegex(ValueError,'source mismatch'):
            replace(self.tpl,units)

    def test_unrelated_archive_is_unchanged_by_page_rule(self):
        a=json.loads((ROOT/'translations/batch500_016_destruction_6E01AC_draft_ko.json').read_text(encoding='utf8'))
        tpl=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        target,mapping,proof=replace(tpl,a['units'])
        self.assertEqual(proof['extra_wait_clear_pairs'],0)
        self.assertEqual(skeleton(target),skeleton(tpl))
        self.assertTrue(all(mapping[x.key]==[x.key] for x in literals(tpl)))


if __name__=='__main__':unittest.main()
