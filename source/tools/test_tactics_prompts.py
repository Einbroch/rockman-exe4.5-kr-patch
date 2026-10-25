import unittest
from build_visibility_poc import ROOT
from build_development_patch import read_json, selected_scope
from tpl_literals import literals, replace_literals, resolve_units, skeleton


class TacticsPrompts(unittest.TestCase):
    def test_pinned_mixed_archive_scope(self):
        asset = read_json(ROOT/'translations/megaman_tactics_prompts_ko.json')
        scope = read_json(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['76C944']
        units = resolve_units(asset)
        source = (ROOT/'analysis/tpl_baseline/76C944.tpl').read_text(encoding='utf-8-sig')
        target = replace_literals(source, units, language=scope['literal_language'])
        self.assertEqual(skeleton(source), skeleton(target))
        self.assertEqual(scope['literal_scripts'], [0, 1])
        self.assertEqual(scope['script_count'], 144)
        before = {x.key:x for x in literals(source)}
        after = {x.key:x for x in literals(target)}
        selected = {u['id'] for u in units}
        for key, item in before.items():
            if key not in selected:
                self.assertEqual(item.text, after[key].text)
                self.assertEqual(item.language, after[key].language)
        for u in units:
            self.assertEqual(len(u['translation'].split('\n')), 2)
            self.assertTrue(all(len(line) <= 5 for line in u['translation'].split('\n')))
            self.assertEqual(u['state'], 'needs_review')
        self.assertFalse(asset['review']['release_eligible'])


if __name__ == '__main__':
    unittest.main()
